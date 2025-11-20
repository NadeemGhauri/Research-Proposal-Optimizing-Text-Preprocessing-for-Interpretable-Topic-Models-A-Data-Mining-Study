# API Data Fetcher - Complete Guide

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Authentication](#authentication)
6. [Pagination Strategies](#pagination-strategies)
7. [Configuration Guide](#configuration-guide)
8. [Usage Examples](#usage-examples)
9. [Scheduling & Automation](#scheduling--automation)
10. [Error Handling & Alerts](#error-handling--alerts)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Overview

The API Data Fetcher is a lightweight, production-ready Python script for automating data extraction from REST APIs. It handles authentication, pagination, rate limiting, retries, and saves data in multiple formats.

### Key Capabilities
- **Multiple Auth Methods**: API keys, OAuth2 (client credentials flow)
- **Smart Pagination**: Page-based, offset/limit, cursor-based, next-link following
- **Rate Limit Handling**: Automatic retry with exponential backoff, respects Retry-After headers
- **Data Transformation**: JSON → pandas DataFrame with automatic flattening
- **Multi-Format Output**: Save to JSON, CSV, and Excel
- **Scheduling**: Run on intervals or integrate with cron/systemd
- **Email Alerts**: Get notified when API calls fail
- **Dry-Run Mode**: Test configuration without making API calls

---

## Features

### Authentication Support
- **API Key**: Bearer tokens, custom headers, query parameters
- **OAuth2**: Client credentials flow with automatic token refresh
- **Environment Variables**: Securely load credentials from environment

### Pagination Strategies
- **None**: Single request (no pagination)
- **Page-based**: Increment page number until empty
- **Offset/Limit**: Database-style pagination
- **Next Link**: Follow `next` URLs in response
- **Cursor-based**: Token-based pagination

### Rate Limiting & Retries
- Exponential backoff on failures
- Respects HTTP 429 `Retry-After` headers
- Configurable retry attempts (default: 5)
- Customizable sleep between requests

### Data Handling
- Automatic JSON flattening using `pandas.json_normalize`
- Handles nested objects and arrays
- Combines multiple pages into single DataFrame
- Timestamps on all output files

### Output Formats
- **JSON**: Records-oriented JSON (one object per row)
- **CSV**: Standard CSV with headers
- **Excel**: XLSX format with formatted columns

### Error Handling
- Comprehensive exception handling
- Detailed logging with timestamps
- Email alerts on failures
- Graceful degradation

---

## Installation

### Prerequisites
```bash
Python 3.7+
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
- `requests>=2.31.0` - HTTP library
- `requests-oauthlib>=1.3.1` - OAuth2 support
- `pandas>=2.0.0` - Data manipulation
- `openpyxl>=3.1.0` - Excel file support
- `tenacity>=8.2.2` - Retry logic
- `schedule>=1.2.0` - Job scheduling (optional)

---

## Quick Start

### 1. Dry Run (No API Calls)
Test the script with sample data:

```bash
python api_data_fetcher.py --dry-run
```

**Output:**
```
2025-11-21 01:35:52 - INFO - Dry-run: using sample data
2025-11-21 01:35:52 - INFO - Transformed 2 rows
2025-11-21 01:35:52 - INFO - Saved JSON: output/api_data_20251121_013552.json
2025-11-21 01:35:52 - INFO - Saved CSV: output/api_data_20251121_013552.csv
2025-11-21 01:35:52 - INFO - Saved Excel: output/api_data_20251121_013552.xlsx
```

### 2. Run Once with Config
```bash
python api_data_fetcher.py --config config/api_fetcher_example_apikey.json --once
```

### 3. Schedule Continuous Runs
```bash
# Run every 15 minutes
python api_data_fetcher.py --config config/my_api.json --interval 15
```

---

## Authentication

### API Key Authentication

**Configuration:**
```json
{
  "url": "https://api.example.com/data",
  "auth_type": "api_key",
  "api_key": "Bearer YOUR_API_KEY_HERE",
  "api_key_header": "Authorization"
}
```

**Common Formats:**

**Bearer Token:**
```json
{
  "auth_type": "api_key",
  "api_key": "Bearer sk-1234567890abcdef",
  "api_key_header": "Authorization"
}
```

**Custom Header:**
```json
{
  "auth_type": "api_key",
  "api_key": "abc123xyz789",
  "api_key_header": "X-API-Key"
}
```

**Environment Variable:**
```json
{
  "auth_type": "api_key",
  "api_key": null
}
```
```bash
export API_KEY="Bearer your-token-here"
python api_data_fetcher.py --config config.json
```

---

### OAuth2 Authentication (Client Credentials)

**Configuration:**
```json
{
  "url": "https://api.example.com/data",
  "auth_type": "oauth2",
  "oauth": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "token_url": "https://api.example.com/oauth/token",
    "scope": ["read:data", "read:reports"]
  }
}
```

**How It Works:**
1. Script requests access token from `token_url`
2. Includes `client_id` and `client_secret` in token request
3. Adds `Authorization: Bearer <token>` to all API requests
4. Token is fetched once per script run

**Example APIs using OAuth2:**
- GitHub API
- Salesforce API
- Google APIs
- Microsoft Graph API
- Auth0

---

## Pagination Strategies

### 1. No Pagination (Single Request)

**Use Case**: Small datasets, single-page responses

**Configuration:**
```json
{
  "pagination": {
    "type": "none"
  }
}
```

---

### 2. Page-Based Pagination

**Use Case**: APIs that use `?page=1`, `?page=2`, etc.

**Configuration:**
```json
{
  "pagination": {
    "type": "page",
    "page_param": "page",
    "start_page": 1,
    "data_path": "users"
  }
}
```

**How It Works:**
1. Start at `start_page` (default: 1)
2. Increment page number on each request
3. Stop when response is empty or `data_path` returns no results

**Example Request Flow:**
```
GET /api/users?page=1
GET /api/users?page=2
GET /api/users?page=3
... (stops when empty)
```

**Example Response:**
```json
{
  "users": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "page": 1,
  "total_pages": 5
}
```

---

### 3. Offset/Limit Pagination

**Use Case**: Database-style pagination with offset and limit

**Configuration:**
```json
{
  "pagination": {
    "type": "offset",
    "offset_param": "offset",
    "limit_param": "limit",
    "limit": 100,
    "start_offset": 0,
    "data_path": "items"
  }
}
```

**How It Works:**
1. Start at `start_offset` (default: 0)
2. Request `limit` records per page
3. Increment offset by `limit` on each request
4. Stop when fewer than `limit` results returned

**Example Request Flow:**
```
GET /api/items?offset=0&limit=100   (returns 100 items)
GET /api/items?offset=100&limit=100 (returns 100 items)
GET /api/items?offset=200&limit=100 (returns 50 items - STOP)
```

**Example Response:**
```json
{
  "items": [...],
  "offset": 0,
  "limit": 100,
  "total": 250
}
```

---

### 4. Next Link Pagination

**Use Case**: APIs that provide a `next` URL in the response

**Configuration:**
```json
{
  "pagination": {
    "type": "next_link",
    "next_key": "next"
  }
}
```

**How It Works:**
1. Make initial request
2. Look for `next` URL in response
3. Follow `next` URL until it's null/missing
4. Supports HAL-style `_links.next` and simple `next` key

**Example Response (HAL format):**
```json
{
  "data": [...],
  "_links": {
    "next": "https://api.example.com/data?cursor=abc123"
  }
}
```

**Example Response (Simple format):**
```json
{
  "results": [...],
  "next": "https://api.example.com/data?page=2"
}
```

**GitHub Example:**
```json
{
  "pagination": {
    "type": "next_link",
    "next_key": "next"
  }
}
```

---

### 5. Cursor-Based Pagination

**Use Case**: Token/cursor-based pagination (Twitter, Stripe, etc.)

**Configuration:**
```json
{
  "pagination": {
    "type": "cursor",
    "cursor_param": "cursor",
    "start_cursor": null,
    "next_cursor_key": "next_cursor"
  }
}
```

**How It Works:**
1. Start without cursor (or with `start_cursor`)
2. Extract `next_cursor` from response
3. Use cursor in next request
4. Stop when `next_cursor` is null

**Example Request Flow:**
```
GET /api/data
GET /api/data?cursor=eyJpZCI6MTAwfQ
GET /api/data?cursor=eyJpZCI6MjAwfQ
... (stops when next_cursor is null)
```

**Example Response:**
```json
{
  "data": [...],
  "next_cursor": "eyJpZCI6MTAwfQ",
  "has_more": true
}
```

---

## Configuration Guide

### Complete Configuration Example

```json
{
  "url": "https://api.example.com/v1/data",
  "params": {
    "filter": "active",
    "include": "details"
  },
  "headers": {
    "Accept": "application/json",
    "User-Agent": "DataFetcher/1.0"
  },
  "auth_type": "api_key",
  "api_key": "Bearer YOUR_API_KEY",
  "api_key_header": "Authorization",
  "pagination": {
    "type": "offset",
    "offset_param": "offset",
    "limit_param": "limit",
    "limit": 100,
    "start_offset": 0,
    "data_path": "results"
  },
  "rate_limit_sleep": 1.0,
  "max_retries": 5,
  "output_folder": "output/api_data",
  "save_json": true,
  "save_csv": true,
  "save_excel": true,
  "email_alerts": {
    "enabled": true,
    "from": "alerts@company.com",
    "to": ["admin@company.com", "dev@company.com"],
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "alerts@company.com",
    "smtp_password": "app-password",
    "use_tls": true
  }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `url` | string | required | API endpoint URL |
| `params` | object | `{}` | Query parameters |
| `headers` | object | `{}` | HTTP headers |
| `auth_type` | string | `null` | `"api_key"` or `"oauth2"` |
| `api_key` | string | `null` | API key (supports env var) |
| `api_key_header` | string | `"Authorization"` | Header name for API key |
| `oauth` | object | `{}` | OAuth2 configuration |
| `pagination` | object | `{"type": "none"}` | Pagination settings |
| `rate_limit_sleep` | float | `1.0` | Seconds between requests |
| `max_retries` | int | `5` | Max retry attempts |
| `output_folder` | string | `"output"` | Output directory |
| `save_json` | bool | `true` | Save JSON file |
| `save_csv` | bool | `true` | Save CSV file |
| `save_excel` | bool | `true` | Save Excel file |
| `email_alerts` | object | `{}` | Email alert settings |

---

## Usage Examples

### Example 1: GitHub Commits API

**Config (`config/github_commits.json`):**
```json
{
  "url": "https://api.github.com/repos/octocat/Hello-World/commits",
  "params": {
    "per_page": 30
  },
  "headers": {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
  },
  "auth_type": "api_key",
  "api_key": "Bearer ghp_YOUR_TOKEN",
  "api_key_header": "Authorization",
  "pagination": {
    "type": "next_link"
  },
  "output_folder": "output/github",
  "save_csv": true,
  "save_excel": true
}
```

**Run:**
```bash
python api_data_fetcher.py --config config/github_commits.json --once
```

---

### Example 2: Paginated User API

**Config (`config/users_api.json`):**
```json
{
  "url": "https://api.company.com/users",
  "auth_type": "api_key",
  "api_key": "Bearer abc123",
  "pagination": {
    "type": "page",
    "page_param": "page",
    "data_path": "users"
  },
  "rate_limit_sleep": 0.5,
  "output_folder": "output/users"
}
```

**Run:**
```bash
python api_data_fetcher.py --config config/users_api.json --once
```

---

### Example 3: OAuth2 with Offset Pagination

**Config (`config/oauth_api.json`):**
```json
{
  "url": "https://api.service.com/v2/transactions",
  "auth_type": "oauth2",
  "oauth": {
    "client_id": "client_abc123",
    "client_secret": "secret_xyz789",
    "token_url": "https://api.service.com/oauth/token",
    "scope": ["read:transactions"]
  },
  "pagination": {
    "type": "offset",
    "limit": 200,
    "data_path": "transactions"
  },
  "output_folder": "output/transactions",
  "save_json": true,
  "save_csv": true
}
```

**Run:**
```bash
python api_data_fetcher.py --config config/oauth_api.json --once
```

---

### Example 4: Scheduled Data Sync

**Run every 30 minutes:**
```bash
python api_data_fetcher.py --config config/my_api.json --interval 30
```

**Output:**
```
2025-11-21 08:00:00 - INFO - Scheduled job every 30 minutes
2025-11-21 08:00:00 - INFO - Fetching...
2025-11-21 08:00:05 - INFO - Saved: output/api_data_20251121_080005.csv
2025-11-21 08:30:00 - INFO - Fetching...
2025-11-21 08:30:04 - INFO - Saved: output/api_data_20251121_083004.csv
```

Stop with `Ctrl+C`

---

## Scheduling & Automation

### Option 1: Built-in Scheduler (Simple)

**Run continuously with interval:**
```bash
python api_data_fetcher.py --config config/my_api.json --interval 15
```

**Pros:**
- Simple, no external dependencies
- Works on all platforms
- Good for development/testing

**Cons:**
- Process must stay running
- No log rotation
- No error recovery

---

### Option 2: Cron (Linux/macOS)

**Every hour:**
```bash
crontab -e
```

Add:
```cron
0 * * * * cd /path/to/project && /path/to/.venv/bin/python api_data_fetcher.py --config config/my_api.json --once >> logs/fetcher.log 2>&1
```

**Every 15 minutes:**
```cron
*/15 * * * * cd /path/to/project && /path/to/.venv/bin/python api_data_fetcher.py --config config/my_api.json --once >> logs/fetcher.log 2>&1
```

**Daily at 2 AM:**
```cron
0 2 * * * cd /path/to/project && /path/to/.venv/bin/python api_data_fetcher.py --config config/my_api.json --once >> logs/fetcher.log 2>&1
```

---

### Option 3: Systemd Service (Linux)

**Create service file (`/etc/systemd/system/api-fetcher.service`):**
```ini
[Unit]
Description=API Data Fetcher
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/project
ExecStart=/path/to/.venv/bin/python api_data_fetcher.py --config config/my_api.json --interval 30
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable api-fetcher
sudo systemctl start api-fetcher
sudo systemctl status api-fetcher
```

**View logs:**
```bash
journalctl -u api-fetcher -f
```

---

### Option 4: Task Scheduler (Windows)

**Create task:**
```powershell
$action = New-ScheduledTaskAction -Execute "C:\path\to\python.exe" -Argument "C:\path\to\api_data_fetcher.py --config config\my_api.json --once"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 15)
Register-ScheduledTask -TaskName "APIDataFetcher" -Action $action -Trigger $trigger
```

---

## Error Handling & Alerts

### Automatic Retries

The script automatically retries on failures:

**Retry Scenarios:**
- Network errors (connection timeout, DNS failure)
- HTTP 5xx errors (500, 502, 503, 504)
- HTTP 429 (rate limit) - respects `Retry-After` header

**Retry Strategy:**
- Exponential backoff: 1s, 2s, 4s, 8s, 16s
- Max attempts: 3 (configurable via `max_retries`)
- Uses `tenacity` library for robust retry logic

**Example Log:**
```
2025-11-21 10:00:00 - WARNING - Rate limited (429). Sleeping for 60 seconds.
2025-11-21 10:01:00 - INFO - Retrying request... (attempt 1/3)
```

---

### Email Alerts

Get notified when API fetches fail:

**Configuration:**
```json
{
  "email_alerts": {
    "enabled": true,
    "from": "api-monitor@company.com",
    "to": ["admin@company.com", "dev-team@company.com"],
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "api-monitor@company.com",
    "smtp_password": "app-password",
    "use_tls": true
  }
}
```

**Gmail Setup:**
1. Enable 2-factor authentication
2. Generate app password: https://myaccount.google.com/apppasswords
3. Use app password (not regular password)

**Example Alert Email:**
```
Subject: API Fetcher Failure

Fetch failed: HTTPError 403 Forbidden

Traceback:
...
```

---

### Logging

**Log Levels:**
- `INFO`: Normal operation (requests, saves)
- `WARNING`: Rate limits, retries
- `ERROR`: Failed requests, exceptions

**Example Log Output:**
```
2025-11-21 10:00:00,123 - INFO - Fetching page 1
2025-11-21 10:00:01,456 - INFO - Fetching page 2
2025-11-21 10:00:02,789 - WARNING - Rate limited (429). Sleeping for 5 seconds.
2025-11-21 10:00:08,012 - INFO - Transformed 250 rows
2025-11-21 10:00:08,345 - INFO - Saved CSV: output/api_data_20251121_100008.csv
```

**Redirect to File:**
```bash
python api_data_fetcher.py --config config.json --once > logs/fetcher.log 2>&1
```

---

## Best Practices

### 1. Use Environment Variables for Secrets

**Don't:**
```json
{
  "api_key": "Bearer sk-1234567890abcdef"
}
```

**Do:**
```json
{
  "api_key": null
}
```

```bash
export API_KEY="Bearer sk-1234567890abcdef"
python api_data_fetcher.py --config config.json
```

---

### 2. Start with Dry Run

Always test configuration without making API calls:

```bash
python api_data_fetcher.py --config config/my_api.json --dry-run
```

---

### 3. Use Appropriate Rate Limiting

**Conservative (default):**
```json
{
  "rate_limit_sleep": 1.0
}
```

**Aggressive (if API allows):**
```json
{
  "rate_limit_sleep": 0.1
}
```

**Check API documentation** for rate limits and adjust accordingly.

---

### 4. Monitor Output File Sizes

Large datasets can create huge files:

```bash
# Check file sizes
ls -lh output/

# Limit data with query params
{
  "params": {
    "limit": 1000,
    "date_from": "2024-01-01"
  }
}
```

---

### 5. Version Your Config Files

Keep configs in version control:

```
config/
├── api_fetcher_production.json
├── api_fetcher_staging.json
└── api_fetcher_development.json
```

---

### 6. Test Pagination Logic

Use small limits to verify pagination:

```json
{
  "pagination": {
    "type": "offset",
    "limit": 10
  }
}
```

Then check logs to see multiple requests.

---

### 7. Handle API Changes

APIs can change response formats. Monitor errors:

```bash
# Check recent runs
tail -f logs/fetcher.log

# Verify data
head -n 5 output/api_data_latest.csv
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tenacity'"

**Solution:**
```bash
pip install -r requirements.txt
```

Or:
```bash
pip install requests requests-oauthlib tenacity schedule pandas openpyxl
```

---

### Issue: OAuth Token Fetch Fails

**Problem:**
```
OAuth token fetch failed: invalid_client
```

**Solutions:**
1. Verify `client_id` and `client_secret`
2. Check `token_url` is correct
3. Ensure `scope` is allowed
4. Test OAuth flow manually:

```bash
curl -X POST https://api.example.com/oauth/token \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

---

### Issue: Rate Limited (429)

**Problem:**
```
WARNING - Rate limited (429). Sleeping for 60 seconds.
```

**Solutions:**
1. Increase `rate_limit_sleep`:
   ```json
   {
     "rate_limit_sleep": 2.0
   }
   ```

2. Reduce pagination `limit`:
   ```json
   {
     "pagination": {
       "limit": 50
     }
   }
   ```

3. Check API rate limit documentation

---

### Issue: Empty Output Files

**Problem:** Files created but contain no data

**Possible Causes:**

1. **Wrong `data_path`**:
   ```json
   {
     "pagination": {
       "data_path": "results"
     }
   }
   ```
   
   Check API response structure. Might be `"data"`, `"items"`, etc.

2. **No results from API**:
   - Check `params` filters
   - Verify API credentials
   - Test API endpoint manually

3. **Pagination stops early**:
   - Review pagination logic
   - Check logs for error messages

---

### Issue: SSL Certificate Errors

**Problem:**
```
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**Solutions:**

1. **Update certificates** (recommended):
   ```bash
   pip install --upgrade certifi
   ```

2. **Use specific CA bundle**:
   ```json
   {
     "headers": {
       "verify": "/path/to/ca-bundle.crt"
     }
   }
   ```

3. **Disable verification** (not recommended for production):
   Modify `_request()` method to add `verify=False`

---

### Issue: Memory Error with Large Datasets

**Problem:**
```
MemoryError: Unable to allocate array
```

**Solutions:**

1. **Reduce pagination limit**:
   ```json
   {
     "pagination": {
       "limit": 50
     }
   }
   ```

2. **Process in batches** - run multiple times with date filters:
   ```json
   {
     "params": {
       "date_from": "2024-01-01",
       "date_to": "2024-01-31"
     }
   }
   ```

3. **Save only needed formats**:
   ```json
   {
     "save_json": false,
     "save_excel": false,
     "save_csv": true
   }
   ```

---

### Issue: Script Hangs/Freezes

**Possible Causes:**

1. **Slow API response** - add timeout:
   ```python
   # Modify _request() to add timeout
   resp = requests.request(method, url, timeout=30, **kwargs)
   ```

2. **Infinite pagination** - check pagination logic:
   - Verify stop condition
   - Add max page limit

3. **Network issue** - check connectivity:
   ```bash
   curl -I https://api.example.com
   ```

---

## Advanced Topics

### Custom Data Transformation

Modify `_transform()` method to customize DataFrame creation:

```python
def _transform(self, responses):
    frames = []
    for r in responses:
        # Custom logic here
        df = pd.json_normalize(r['custom_path'])
        
        # Add computed columns
        df['fetch_date'] = pd.Timestamp.now()
        df['source'] = 'MyAPI'
        
        frames.append(df)
    
    combined = pd.concat(frames, ignore_index=True)
    
    # Post-processing
    combined['price'] = combined['price'].astype(float)
    combined['date'] = pd.to_datetime(combined['date'])
    
    return combined
```

---

### Using as a Module

```python
from api_data_fetcher import APIDataFetcher, APIFetcherConfig

config = APIFetcherConfig(
    url='https://api.example.com/data',
    auth_type='api_key',
    api_key='Bearer abc123',
    pagination={'type': 'page'},
    output_folder='my_output'
)

fetcher = APIDataFetcher(config)
saved_files = fetcher.fetch_and_save('my_data')

print(f"Saved: {saved_files}")
```

---

### Parallel Requests (Experimental)

For multiple independent endpoints:

```python
import concurrent.futures

configs = [
    APIFetcherConfig(url='https://api.example.com/users', ...),
    APIFetcherConfig(url='https://api.example.com/orders', ...),
    APIFetcherConfig(url='https://api.example.com/products', ...)
]

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(APIDataFetcher(cfg).fetch_and_save, f'data_{i}')
        for i, cfg in enumerate(configs)
    ]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]
```

---

## API-Specific Examples

### GitHub API

```json
{
  "url": "https://api.github.com/repos/owner/repo/issues",
  "headers": {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
  },
  "auth_type": "api_key",
  "api_key": "Bearer ghp_YOUR_TOKEN",
  "pagination": {
    "type": "page",
    "page_param": "page",
    "data_path": null
  }
}
```

### Stripe API

```json
{
  "url": "https://api.stripe.com/v1/customers",
  "auth_type": "api_key",
  "api_key": "Bearer sk_test_YOUR_KEY",
  "pagination": {
    "type": "cursor",
    "cursor_param": "starting_after",
    "next_cursor_key": "has_more"
  }
}
```

### Twitter API v2

```json
{
  "url": "https://api.twitter.com/2/tweets/search/recent",
  "auth_type": "api_key",
  "api_key": "Bearer YOUR_BEARER_TOKEN",
  "pagination": {
    "type": "cursor",
    "cursor_param": "next_token",
    "next_cursor_key": "next_token"
  }
}
```

---

## Conclusion

The API Data Fetcher provides a robust, configurable solution for automated API data extraction. Key features:

- **Flexible Authentication**: API keys, OAuth2
- **Smart Pagination**: Handles all common patterns
- **Production-Ready**: Retries, rate limiting, error handling
- **Multiple Outputs**: JSON, CSV, Excel
- **Easy Scheduling**: Built-in intervals, cron, systemd

For questions or issues, check the troubleshooting section or review example configs in `config/`.

---

**Version**: 1.0  
**Last Updated**: November 2024  
**Author**: Python Automation Scripts Project
