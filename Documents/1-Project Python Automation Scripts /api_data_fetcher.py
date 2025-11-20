#!/usr/bin/env python3
"""
api_data_fetcher.py

Lightweight, configurable API data extractor with support for:
- API Key or OAuth2 (client_credentials) authentication
- Pagination strategies (page, offset/limit, next-link, cursor)
- Rate-limit handling and retries with exponential backoff
- Transform JSON responses into pandas DataFrame
- Save results to JSON, CSV and Excel
- Scheduling via simple interval or background loop
- Alerts via SMTP email on repeated failures

Usage examples:
  # Dry-run using embedded sample data
  python api_data_fetcher.py --dry-run

  # Run once using a config file
  python api_data_fetcher.py --config config/api_fetcher_config.json --once

  # Run continuously every 15 minutes
  python api_data_fetcher.py --config config/api_fetcher_config.json --interval 15

This script is designed to be configurable from a JSON file. See the README/guide for
the configuration format.
"""

from __future__ import annotations
import argparse
import time
import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Generator, Optional

import requests
import pandas as pd

try:
    from requests_oauthlib import OAuth2Session
except Exception:
    OAuth2Session = None

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Optional scheduling dependency; only used when --interval provided
try:
    import schedule
except Exception:
    schedule = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class APIFetcherConfig:
    url: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    auth_type: Optional[str] = None  # 'api_key' or 'oauth2'
    api_key: Optional[str] = None
    api_key_header: str = 'Authorization'  # header to place API key
    oauth: Dict[str, Any] = field(default_factory=dict)  # client_id, client_secret, token_url, scope
    pagination: Dict[str, Any] = field(default_factory=lambda: {'type': 'none'})
    rate_limit_sleep: float = 1.0
    max_retries: int = 5
    output_folder: str = 'output'
    save_json: bool = True
    save_csv: bool = True
    save_excel: bool = True
    email_alerts: Dict[str, Any] = field(default_factory=dict)  # smtp config


class APIDataFetcher:
    def __init__(self, config: APIFetcherConfig):
        self.config = config
        os.makedirs(self.config.output_folder, exist_ok=True)

    def _auth_headers(self) -> Dict[str, str]:
        headers = dict(self.config.headers or {})
        if self.config.auth_type == 'api_key' and self.config.api_key:
            # Support either raw header value or "Bearer <key>"
            headers[self.config.api_key_header] = self.config.api_key
        return headers

    def _get_oauth_token(self) -> Optional[str]:
        oauth_cfg = self.config.oauth or {}
        if not oauth_cfg or OAuth2Session is None:
            return None
        client_id = oauth_cfg.get('client_id')
        client_secret = oauth_cfg.get('client_secret')
        token_url = oauth_cfg.get('token_url')
        scope = oauth_cfg.get('scope')
        if not (client_id and client_secret and token_url):
            logger.warning('Incomplete OAuth2 configuration; skipping OAuth')
            return None
        try:
            # client credentials flow
            session = OAuth2Session(client=client_id, scope=scope)
            token = session.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)
            access_token = token.get('access_token')
            return access_token
        except Exception as e:
            logger.exception('OAuth token fetch failed: %s', e)
            return None

    def _prepare_headers(self) -> Dict[str, str]:
        headers = self._auth_headers()
        if self.config.auth_type == 'oauth2':
            token = self._get_oauth_token()
            if token:
                headers['Authorization'] = f'Bearer {token}'
        return headers

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10),
           retry=retry_if_exception_type((requests.exceptions.RequestException,)))
    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        headers = kwargs.pop('headers', {})
        headers.update(self._prepare_headers())
        logger.debug('Request headers: %s', headers)
        resp = requests.request(method, url, headers=headers, **kwargs)

        # Handle HTTP 429 / rate limiting
        if resp.status_code == 429:
            retry_after = resp.headers.get('Retry-After')
            wait_seconds = int(retry_after) if retry_after and retry_after.isdigit() else self.config.rate_limit_sleep
            logger.warning('Rate limited (429). Sleeping for %s seconds.', wait_seconds)
            time.sleep(wait_seconds)
            resp.raise_for_status()

        # Raise for 4xx/5xx to trigger retry logic in tenacity
        resp.raise_for_status()
        return resp

    def _paginate(self) -> Generator[Dict[str, Any], None, None]:
        """Generic pagination generator. Supports several strategies.

        Supported pagination 'type' values:
        - 'none' : single request
        - 'page' : uses 'page' param and stops when empty results
        - 'offset' : uses offset/limit
        - 'next_link' : follows a 'next' URL in response['_links'] or response['next']
        - 'cursor' : uses cursor/token returned in response
        """
        p = self.config.pagination or {'type': 'none'}
        ptype = p.get('type', 'none')
        url = self.config.url
        params = dict(self.config.params or {})

        if ptype == 'none':
            logger.info('Fetching single page: %s', url)
            resp = self._request('GET', url, params=params)
            yield resp.json()
            return

        if ptype == 'page':
            page = p.get('start_page', 1)
            page_param = p.get('page_param', 'page')
            while True:
                params[page_param] = page
                logger.info('Fetching page %s', page)
                resp = self._request('GET', url, params=params)
                data = resp.json()
                yield data
                # Stop if empty
                if not data or (isinstance(data, dict) and not data.get(p.get('data_path', 'data'))):
                    break
                page += 1
            return

        if ptype == 'offset':
            offset = p.get('start_offset', 0)
            limit = p.get('limit', 100)
            offset_param = p.get('offset_param', 'offset')
            limit_param = p.get('limit_param', 'limit')
            while True:
                params[offset_param] = offset
                params[limit_param] = limit
                logger.info('Fetching offset %s (limit %s)', offset, limit)
                resp = self._request('GET', url, params=params)
                data = resp.json()
                yield data
                # stop when fewer than limit returned
                items = data if isinstance(data, list) else data.get(p.get('data_path', 'data'), [])
                if not items or len(items) < limit:
                    break
                offset += limit
            return

        if ptype == 'next_link':
            next_url = url
            next_key = p.get('next_key', 'next')
            while next_url:
                logger.info('Fetching: %s', next_url)
                resp = self._request('GET', next_url, params=params)
                data = resp.json()
                yield data
                # attempt to find next link
                next_url = None
                if isinstance(data, dict):
                    # common locations
                    if data.get('_links') and isinstance(data['_links'], dict):
                        next_url = data['_links'].get('next')
                    next_url = next_url or data.get(next_key)
            return

        if ptype == 'cursor':
            cursor = p.get('start_cursor')
            cursor_param = p.get('cursor_param', 'cursor')
            while True:
                if cursor:
                    params[cursor_param] = cursor
                logger.info('Fetching cursor=%s', cursor)
                resp = self._request('GET', url, params=params)
                data = resp.json()
                yield data
                # extract next cursor
                cursor = None
                if isinstance(data, dict):
                    cursor = data.get(p.get('next_cursor_key', 'next_cursor'))
                if not cursor:
                    break
            return

        # Unknown pagination
        logger.warning('Unknown pagination type %s. Fetching single page.', ptype)
        resp = self._request('GET', url, params=params)
        yield resp.json()

    def _transform(self, responses: Generator[Dict[str, Any], None, None]) -> pd.DataFrame:
        """Flatten and combine JSON responses into a single DataFrame.

        Uses pandas.json_normalize; callers may post-process columns.
        """
        frames = []
        for r in responses:
            # if the response is a list, normalize each element
            if isinstance(r, list):
                df = pd.json_normalize(r)
            elif isinstance(r, dict):
                # try common 'data' key
                data = r.get('data') if 'data' in r else r
                if isinstance(data, list):
                    df = pd.json_normalize(data)
                else:
                    # single object -> single-row dataframe
                    df = pd.json_normalize(data)
            else:
                df = pd.DataFrame()
            if not df.empty:
                frames.append(df)

        if not frames:
            return pd.DataFrame()
        combined = pd.concat(frames, ignore_index=True)
        logger.info('Transformed %s rows', len(combined))
        return combined

    def _save(self, df: pd.DataFrame, base_name: str) -> Dict[str, str]:
        out = {}
        ts = time.strftime('%Y%m%d_%H%M%S')
        if df is None or df.empty:
            logger.warning('No data to save')
            return out
        if self.config.save_json:
            json_file = os.path.join(self.config.output_folder, f"{base_name}_{ts}.json")
            df.to_json(json_file, orient='records', date_format='iso')
            out['json'] = json_file
            logger.info('Saved JSON: %s', json_file)
        if self.config.save_csv:
            csv_file = os.path.join(self.config.output_folder, f"{base_name}_{ts}.csv")
            df.to_csv(csv_file, index=False)
            out['csv'] = csv_file
            logger.info('Saved CSV: %s', csv_file)
        if self.config.save_excel:
            excel_file = os.path.join(self.config.output_folder, f"{base_name}_{ts}.xlsx")
            df.to_excel(excel_file, index=False)
            out['excel'] = excel_file
            logger.info('Saved Excel: %s', excel_file)
        return out

    def _send_email_alert(self, subject: str, body: str):
        cfg = self.config.email_alerts or {}
        if not cfg.get('enabled'):
            logger.debug('Email alerts disabled in config')
            return
        import smtplib
        from email.message import EmailMessage

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = cfg.get('from')
        msg['To'] = ','.join(cfg.get('to', []))
        msg.set_content(body)

        try:
            server = cfg.get('smtp_server', 'localhost')
            port = cfg.get('smtp_port', 25)
            username = cfg.get('smtp_user')
            password = cfg.get('smtp_password')
            use_tls = cfg.get('use_tls', False)

            if use_tls:
                s = smtplib.SMTP(server, port)
                s.starttls()
            else:
                s = smtplib.SMTP(server, port)

            if username and password:
                s.login(username, password)
            s.send_message(msg)
            s.quit()
            logger.info('Alert email sent to %s', msg['To'])
        except Exception:
            logger.exception('Failed to send alert email')

    def fetch_and_save(self, base_name: str = 'api_data') -> Dict[str, str]:
        """High-level method: paginate, transform and save. Returns saved file paths."""
        try:
            responses = self._paginate()
            df = self._transform(responses)
            saved = self._save(df, base_name)
            return saved
        except Exception as e:
            logger.exception('Fetch failed: %s', e)
            self._send_email_alert('API Fetcher Failure', f'Fetch failed: {e}')
            raise


def load_config(path: Optional[str]) -> APIFetcherConfig:
    default = APIFetcherConfig()
    if not path:
        return default
    with open(path, 'r') as f:
        raw = json.load(f)
    # Map keys into dataclass
    cfg = APIFetcherConfig(
        url=raw.get('url'),
        params=raw.get('params', {}),
        headers=raw.get('headers', {}),
        auth_type=raw.get('auth_type'),
        api_key=raw.get('api_key') or os.environ.get('API_KEY'),
        api_key_header=raw.get('api_key_header', 'Authorization'),
        oauth=raw.get('oauth', {}),
        pagination=raw.get('pagination', {'type': 'none'}),
        rate_limit_sleep=raw.get('rate_limit_sleep', 1.0),
        max_retries=raw.get('max_retries', 5),
        output_folder=raw.get('output_folder', 'output'),
        save_json=raw.get('save_json', True),
        save_csv=raw.get('save_csv', True),
        save_excel=raw.get('save_excel', True),
        email_alerts=raw.get('email_alerts', {})
    )
    return cfg


SAMPLE_RESPONSE = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 35},
]


def main():
    parser = argparse.ArgumentParser(description='API Data Fetcher')
    parser.add_argument('--config', '-c', help='Path to JSON config file')
    parser.add_argument('--dry-run', action='store_true', help='Run transform/save using sample data (no API calls)')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--interval', type=int, help='Run every N minutes (background loop)')
    parser.add_argument('--base-name', default='api_data', help='Base name for saved files')
    args = parser.parse_args()

    cfg = load_config(args.config)
    fetcher = APIDataFetcher(cfg)

    def job():
        try:
            if args.dry_run or not cfg.url:
                logger.info('Dry-run: using sample data')
                responses = (SAMPLE_RESPONSE,)
                df = fetcher._transform(iter(responses))
                saved = fetcher._save(df, args.base_name)
                logger.info('Dry-run saved: %s', saved)
            else:
                saved = fetcher.fetch_and_save(args.base_name)
                logger.info('Saved: %s', saved)
        except Exception as e:
            logger.exception('Job failed: %s', e)

    if args.once:
        job()
        return

    if args.interval:
        if schedule is None:
            logger.error('`schedule` package not installed; cannot use --interval')
            return
        # schedule job every N minutes
        schedule.every(args.interval).minutes.do(job)
        logger.info('Scheduled job every %s minutes', args.interval)
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info('Stopping scheduler')
        return

    # Default: run once
    job()


if __name__ == '__main__':
    main()
