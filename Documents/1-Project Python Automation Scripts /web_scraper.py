#!/usr/bin/env python3
"""
Web Scraper - Robust web scraping with anti-detection and proxy support

Features:
- BeautifulSoup for static content parsing
- Selenium for JavaScript-rendered content
- Respects robots.txt
- Rate limiting and delays
- Table extraction to structured data
- Multi-format output (JSON, CSV, Excel)
- Proxy rotation for large-scale scraping
- Anti-detection mechanisms (user agents, headers, delays)
- Session management
- Error handling and retries

Author: Python Automation Scripts
Created: November 2025
"""

import json
import os
import random
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tenacity import retry, stop_after_attempt, wait_exponential


@dataclass
class ScraperConfig:
    """Configuration for web scraper"""
    
    # Target settings
    urls: List[str] = field(default_factory=list)
    base_url: Optional[str] = None
    
    # Scraping method
    use_selenium: bool = False  # True for JavaScript-rendered content
    selenium_wait_time: int = 10  # Max wait time for elements
    page_load_timeout: int = 30  # Page load timeout
    
    # Selectors
    css_selectors: Dict[str, str] = field(default_factory=dict)
    xpath_selectors: Dict[str, str] = field(default_factory=dict)
    table_selectors: List[str] = field(default_factory=list)
    
    # Rate limiting
    respect_robots_txt: bool = True
    min_delay: float = 1.0  # Minimum delay between requests (seconds)
    max_delay: float = 3.0  # Maximum delay between requests
    requests_per_minute: int = 30
    
    # Anti-detection
    rotate_user_agents: bool = True
    custom_headers: Dict[str, str] = field(default_factory=dict)
    session_cookies: Dict[str, str] = field(default_factory=dict)
    
    # Proxy settings
    proxies: List[str] = field(default_factory=list)  # Format: "http://user:pass@host:port"
    rotate_proxies: bool = False
    
    # Output settings
    output_folder: str = "./scraped_data"
    output_formats: List[str] = field(default_factory=lambda: ["json"])  # json, csv, excel
    base_filename: str = "scraped_data"
    
    # Advanced settings
    max_retries: int = 3
    timeout: int = 30
    verify_ssl: bool = True
    follow_redirects: bool = True
    extract_links: bool = False
    extract_images: bool = False
    
    # Headless browser
    headless: bool = True
    chrome_driver_path: Optional[str] = None


class WebScraper:
    """Robust web scraper with anti-detection and proxy support"""
    
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.session = requests.Session()
        self.ua = UserAgent() if config.rotate_user_agents else None
        self.robot_parsers: Dict[str, RobotFileParser] = {}
        self.proxy_index = 0
        self.request_count = 0
        self.last_request_time = 0
        self.driver = None
        
        # Create output folder
        Path(config.output_folder).mkdir(parents=True, exist_ok=True)
    
    def _get_user_agent(self) -> str:
        """Get random user agent for anti-detection"""
        if self.config.rotate_user_agents and self.ua:
            try:
                return self.ua.random
            except Exception:
                # Fallback user agent
                return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with anti-detection measures"""
        headers = {
            'User-Agent': self._get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Add custom headers
        headers.update(self.config.custom_headers)
        
        return headers
    
    def _get_proxy(self) -> Optional[Dict[str, str]]:
        """Get next proxy for rotation"""
        if not self.config.rotate_proxies or not self.config.proxies:
            return None
        
        proxy = self.config.proxies[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.config.proxies)
        
        return {
            'http': proxy,
            'https': proxy
        }
    
    def _check_robots_txt(self, url: str) -> bool:
        """Check if URL is allowed by robots.txt"""
        if not self.config.respect_robots_txt:
            return True
        
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        
        # Cache robot parser per domain
        if base not in self.robot_parsers:
            rp = RobotFileParser()
            robots_url = urljoin(base, '/robots.txt')
            try:
                rp.set_url(robots_url)
                rp.read()
                self.robot_parsers[base] = rp
            except Exception:
                # If robots.txt cannot be read, allow by default
                return True
        
        return self.robot_parsers[base].can_fetch(self._get_user_agent(), url)
    
    def _rate_limit(self):
        """Apply rate limiting between requests"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        # Calculate delay
        delay = random.uniform(self.config.min_delay, self.config.max_delay)
        
        # Additional delay if requests per minute exceeded
        if self.request_count >= self.config.requests_per_minute:
            time_since_first = current_time - self.last_request_time
            if time_since_first < 60:
                delay = max(delay, 60 - time_since_first)
                self.request_count = 0
        
        # Wait if needed
        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        self.last_request_time = time.time()
        self.request_count += 1
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _fetch_page(self, url: str) -> Optional[str]:
        """Fetch page content with retries"""
        # Check robots.txt
        if not self._check_robots_txt(url):
            print(f"❌ Blocked by robots.txt: {url}")
            return None
        
        # Apply rate limiting
        self._rate_limit()
        
        print(f"📥 Fetching: {url}")
        
        try:
            response = self.session.get(
                url,
                headers=self._get_headers(),
                proxies=self._get_proxy(),
                cookies=self.config.session_cookies,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl,
                allow_redirects=self.config.follow_redirects
            )
            response.raise_for_status()
            return response.text
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching {url}: {str(e)}")
            raise
    
    def _setup_selenium(self):
        """Setup Selenium WebDriver with anti-detection"""
        if self.driver:
            return
        
        chrome_options = ChromeOptions()
        
        # Headless mode
        if self.config.headless:
            chrome_options.add_argument('--headless')
        
        # Anti-detection arguments
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument(f'user-agent={self._get_user_agent()}')
        
        # Additional anti-bot detection
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Proxy support
        proxy = self._get_proxy()
        if proxy and proxy.get('http'):
            chrome_options.add_argument(f'--proxy-server={proxy["http"]}')
        
        # Create driver
        if self.config.chrome_driver_path:
            service = Service(self.config.chrome_driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            self.driver = webdriver.Chrome(options=chrome_options)
        
        # Set timeouts
        self.driver.set_page_load_timeout(self.config.page_load_timeout)
        
        # Execute script to hide webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def _fetch_page_selenium(self, url: str) -> Optional[str]:
        """Fetch page content using Selenium for JavaScript rendering"""
        # Check robots.txt
        if not self._check_robots_txt(url):
            print(f"❌ Blocked by robots.txt: {url}")
            return None
        
        # Apply rate limiting
        self._rate_limit()
        
        print(f"📥 Fetching with Selenium: {url}")
        
        try:
            self._setup_selenium()
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, self.config.selenium_wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Additional wait for dynamic content
            time.sleep(random.uniform(1, 3))
            
            return self.driver.page_source
            
        except Exception as e:
            print(f"⚠️ Error fetching with Selenium {url}: {str(e)}")
            return None
    
    def _extract_data(self, html: str, url: str) -> Dict[str, Any]:
        """Extract data from HTML using selectors"""
        soup = BeautifulSoup(html, 'lxml')
        data = {
            'url': url,
            'scraped_at': datetime.now().isoformat(),
            'extracted_data': {}
        }
        
        # Extract using CSS selectors
        for name, selector in self.config.css_selectors.items():
            elements = soup.select(selector)
            if len(elements) == 1:
                data['extracted_data'][name] = elements[0].get_text(strip=True)
            elif len(elements) > 1:
                data['extracted_data'][name] = [el.get_text(strip=True) for el in elements]
        
        # Extract tables
        if self.config.table_selectors:
            data['tables'] = []
            for selector in self.config.table_selectors:
                tables = soup.select(selector)
                for table in tables:
                    table_data = self._extract_table(table)
                    if table_data:
                        data['tables'].append(table_data)
        
        # Extract links
        if self.config.extract_links:
            links = []
            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])
                links.append({
                    'text': link.get_text(strip=True),
                    'url': full_url
                })
            data['links'] = links
        
        # Extract images
        if self.config.extract_images:
            images = []
            for img in soup.find_all('img', src=True):
                full_url = urljoin(url, img['src'])
                images.append({
                    'alt': img.get('alt', ''),
                    'url': full_url
                })
            data['images'] = images
        
        return data
    
    def _extract_table(self, table_element) -> Optional[List[Dict[str, Any]]]:
        """Extract table to list of dictionaries"""
        try:
            # Find headers
            headers = []
            header_row = table_element.find('thead')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
            else:
                # Try first row as header
                first_row = table_element.find('tr')
                if first_row:
                    headers = [th.get_text(strip=True) for th in first_row.find_all(['th', 'td'])]
            
            if not headers:
                return None
            
            # Extract rows
            rows = []
            tbody = table_element.find('tbody') or table_element
            for row in tbody.find_all('tr')[1 if not table_element.find('thead') else 0:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) == len(headers):
                    row_data = {headers[i]: cells[i].get_text(strip=True) for i in range(len(headers))}
                    rows.append(row_data)
            
            return rows if rows else None
            
        except Exception as e:
            print(f"⚠️ Error extracting table: {str(e)}")
            return None
    
    def _save_results(self, results: List[Dict[str, Any]]) -> List[str]:
        """Save results in multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = []
        
        # JSON output
        if 'json' in self.config.output_formats:
            json_file = os.path.join(
                self.config.output_folder,
                f"{self.config.base_filename}_{timestamp}.json"
            )
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            saved_files.append(json_file)
            print(f"💾 Saved JSON: {json_file}")
        
        # Flatten results for CSV/Excel
        flat_data = []
        for item in results:
            flat_item = {
                'url': item['url'],
                'scraped_at': item['scraped_at']
            }
            # Add extracted data
            if 'extracted_data' in item:
                for key, value in item['extracted_data'].items():
                    if isinstance(value, list):
                        flat_item[key] = ', '.join(str(v) for v in value)
                    else:
                        flat_item[key] = value
            flat_data.append(flat_item)
        
        if flat_data:
            df = pd.DataFrame(flat_data)
            
            # CSV output
            if 'csv' in self.config.output_formats:
                csv_file = os.path.join(
                    self.config.output_folder,
                    f"{self.config.base_filename}_{timestamp}.csv"
                )
                df.to_csv(csv_file, index=False, encoding='utf-8')
                saved_files.append(csv_file)
                print(f"💾 Saved CSV: {csv_file}")
            
            # Excel output
            if 'excel' in self.config.output_formats:
                excel_file = os.path.join(
                    self.config.output_folder,
                    f"{self.config.base_filename}_{timestamp}.xlsx"
                )
                with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Scraped Data', index=False)
                    
                    # Add tables to separate sheets if available
                    for idx, item in enumerate(results):
                        if 'tables' in item and item['tables']:
                            for table_idx, table_data in enumerate(item['tables']):
                                if table_data:
                                    sheet_name = f"Table_{idx+1}_{table_idx+1}"[:31]  # Excel limit
                                    table_df = pd.DataFrame(table_data)
                                    table_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                saved_files.append(excel_file)
                print(f"💾 Saved Excel: {excel_file}")
        
        return saved_files
    
    def scrape(self) -> List[str]:
        """Main scraping method"""
        print(f"🚀 Starting web scraper...")
        print(f"📋 URLs to scrape: {len(self.config.urls)}")
        print(f"⚙️ Using Selenium: {self.config.use_selenium}")
        print(f"🤖 Respecting robots.txt: {self.config.respect_robots_txt}")
        print(f"🔄 Rotating proxies: {self.config.rotate_proxies} ({len(self.config.proxies)} proxies)")
        print()
        
        results = []
        
        try:
            for url in self.config.urls:
                try:
                    # Fetch page
                    if self.config.use_selenium:
                        html = self._fetch_page_selenium(url)
                    else:
                        html = self._fetch_page(url)
                    
                    if html:
                        # Extract data
                        data = self._extract_data(html, url)
                        results.append(data)
                        print(f"✅ Scraped: {url}")
                    else:
                        print(f"⚠️ Skipped: {url}")
                
                except Exception as e:
                    print(f"❌ Failed to scrape {url}: {str(e)}")
                    continue
            
            # Save results
            if results:
                print(f"\n📊 Scraped {len(results)} pages successfully")
                saved_files = self._save_results(results)
                return saved_files
            else:
                print("⚠️ No data scraped")
                return []
        
        finally:
            # Cleanup
            if self.driver:
                self.driver.quit()
                self.driver = None
    
    def __del__(self):
        """Cleanup on deletion"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass


def load_config(config_path: str) -> ScraperConfig:
    """Load configuration from JSON file"""
    with open(config_path, 'r') as f:
        data = json.load(f)
    
    return ScraperConfig(**data)


def main():
    """Main entry point with example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Web Scraper - Robust web scraping tool')
    parser.add_argument('--config', type=str, help='Path to JSON configuration file')
    parser.add_argument('--url', type=str, help='Single URL to scrape')
    parser.add_argument('--urls', type=str, nargs='+', help='Multiple URLs to scrape')
    parser.add_argument('--selenium', action='store_true', help='Use Selenium for JavaScript rendering')
    parser.add_argument('--output', type=str, default='./scraped_data', help='Output folder')
    
    args = parser.parse_args()
    
    if args.config:
        # Load from config file
        config = load_config(args.config)
    else:
        # Create config from arguments
        urls = []
        if args.url:
            urls.append(args.url)
        if args.urls:
            urls.extend(args.urls)
        
        if not urls:
            print("❌ Error: Please provide --config, --url, or --urls")
            return
        
        config = ScraperConfig(
            urls=urls,
            use_selenium=args.selenium,
            output_folder=args.output,
            output_formats=['json', 'csv'],
            css_selectors={
                'title': 'h1',
                'paragraphs': 'p'
            }
        )
    
    # Run scraper
    scraper = WebScraper(config)
    output_files = scraper.scrape()
    
    if output_files:
        print(f"\n✅ Scraping complete! Files saved:")
        for file in output_files:
            print(f"   📄 {file}")
    else:
        print("\n⚠️ No data was scraped")


if __name__ == "__main__":
    main()
