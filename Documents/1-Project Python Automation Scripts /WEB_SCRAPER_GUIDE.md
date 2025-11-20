# Web Scraper - Comprehensive Guide

A robust web scraping tool with anti-detection mechanisms, proxy rotation, and support for both static and JavaScript-rendered content.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Configuration](#configuration)
6. [Scraping Methods](#scraping-methods)
7. [Anti-Detection Techniques](#anti-detection-techniques)
8. [Proxy Rotation](#proxy-rotation)
9. [Data Extraction](#data-extraction)
10. [Output Formats](#output-formats)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)
13. [Examples](#examples)

---

## Overview

The Web Scraper is a professional-grade tool designed for ethical web scraping with built-in protections and anti-detection mechanisms. It supports both static HTML parsing with BeautifulSoup and dynamic JavaScript-rendered content with Selenium.

### Key Capabilities
- **Dual scraping engines**: BeautifulSoup for static content, Selenium for JavaScript
- **Ethical scraping**: Respects robots.txt and enforces rate limiting
- **Anti-detection**: Rotating user agents, realistic headers, random delays
- **Proxy support**: Automatic proxy rotation for large-scale scraping
- **Smart extraction**: CSS/XPath selectors, table extraction, link/image discovery
- **Multi-format output**: JSON, CSV, and Excel with structured data

---

## Features

### ✅ Scraping Engines
- **BeautifulSoup**: Fast parsing for static HTML content
- **Selenium WebDriver**: Handles JavaScript-rendered pages
- **Automatic fallback**: Retry mechanisms with exponential backoff

### ✅ Ethical Scraping
- **robots.txt compliance**: Automatically checks and respects robots.txt
- **Rate limiting**: Configurable delays between requests (min/max)
- **Requests per minute**: Throttle to avoid overwhelming servers

### ✅ Anti-Detection
- **User agent rotation**: Random user agents from fake-useragent library
- **Realistic headers**: Accept, Accept-Language, DNT, Connection headers
- **Random delays**: Randomized wait times between requests
- **Session management**: Maintains cookies and session state
- **Selenium stealth**: Hides webdriver properties, uses realistic browser behavior

### ✅ Proxy Rotation
- **Multiple proxies**: Support for HTTP/HTTPS proxy lists
- **Automatic rotation**: Round-robin proxy switching
- **Authentication**: Username/password proxy auth support

### ✅ Data Extraction
- **CSS selectors**: Extract elements by CSS selectors
- **XPath selectors**: Extract elements by XPath expressions
- **Table extraction**: Automatic conversion of HTML tables to structured data
- **Link discovery**: Extract all links with text and URLs
- **Image extraction**: Discover images with alt text and URLs

### ✅ Output Options
- **JSON**: Full structured data with metadata
- **CSV**: Flattened data for analysis
- **Excel**: Multiple sheets with main data and extracted tables

---

## Installation

### Prerequisites
- Python 3.9 or higher
- Chrome/Chromium browser (for Selenium)
- ChromeDriver (for Selenium)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install ChromeDriver
**Option 1: Automatic (Selenium Manager)**
Selenium 4.15+ includes automatic driver management - no manual installation needed!

**Option 2: Manual Installation**
```bash
# macOS (with Homebrew)
brew install chromedriver

# Linux
sudo apt-get install chromium-chromedriver

# Windows - Download from:
# https://chromedriver.chromium.org/downloads
```

Verify installation:
```bash
chromedriver --version
```

---

## Quick Start

### Example 1: Simple Static Page Scraping
```python
from web_scraper import WebScraper, ScraperConfig

# Configure scraper
config = ScraperConfig(
    urls=['https://example.com'],
    css_selectors={
        'title': 'h1',
        'content': 'article p'
    },
    output_formats=['json', 'csv']
)

# Run scraper
scraper = WebScraper(config)
files = scraper.scrape()
print(f"Data saved to: {files}")
```

### Example 2: Command Line Usage
```bash
# Scrape single URL
python web_scraper.py --url https://example.com --output ./data

# Scrape multiple URLs
python web_scraper.py --urls https://site1.com https://site2.com

# Use Selenium for JavaScript content
python web_scraper.py --url https://spa-app.com --selenium

# Use config file
python web_scraper.py --config config/scraper_config.json
```

### Example 3: JavaScript-Rendered Content
```python
config = ScraperConfig(
    urls=['https://dynamic-site.com'],
    use_selenium=True,
    selenium_wait_time=10,
    css_selectors={
        'dynamic_content': '.loaded-by-js'
    }
)

scraper = WebScraper(config)
scraper.scrape()
```

---

## Configuration

### Complete Configuration Reference

```python
ScraperConfig(
    # === Target Settings ===
    urls=['https://example.com', 'https://example.com/page2'],
    base_url='https://example.com',  # Optional: base URL for relative links
    
    # === Scraping Method ===
    use_selenium=False,  # True for JavaScript-rendered content
    selenium_wait_time=10,  # Max wait time for elements (seconds)
    page_load_timeout=30,  # Page load timeout (seconds)
    
    # === Selectors ===
    css_selectors={
        'title': 'h1',
        'paragraphs': 'article p',
        'price': '.product-price'
    },
    xpath_selectors={
        'heading': '//h1[@class="main-title"]'
    },
    table_selectors=['table.data', '#results-table'],
    
    # === Rate Limiting ===
    respect_robots_txt=True,
    min_delay=1.0,  # Minimum delay between requests (seconds)
    max_delay=3.0,  # Maximum delay between requests (seconds)
    requests_per_minute=30,
    
    # === Anti-Detection ===
    rotate_user_agents=True,
    custom_headers={
        'Referer': 'https://google.com',
        'X-Custom-Header': 'value'
    },
    session_cookies={
        'session_id': 'abc123',
        'preferences': 'theme=dark'
    },
    
    # === Proxy Settings ===
    proxies=[
        'http://proxy1.com:8080',
        'http://user:pass@proxy2.com:8080',
        'https://proxy3.com:3128'
    ],
    rotate_proxies=True,
    
    # === Output Settings ===
    output_folder='./scraped_data',
    output_formats=['json', 'csv', 'excel'],
    base_filename='scraped_data',
    
    # === Advanced Settings ===
    max_retries=3,
    timeout=30,
    verify_ssl=True,
    follow_redirects=True,
    extract_links=False,
    extract_images=False,
    
    # === Selenium Settings ===
    headless=True,  # Run browser in headless mode
    chrome_driver_path=None  # Auto-detect or specify path
)
```

### Configuration File (JSON)

```json
{
  "urls": ["https://example.com"],
  "use_selenium": false,
  "css_selectors": {
    "title": "h1",
    "content": "article p"
  },
  "output_formats": ["json", "csv"],
  "min_delay": 2.0,
  "max_delay": 5.0,
  "rotate_user_agents": true
}
```

---

## Scraping Methods

### BeautifulSoup (Static Content)

**Best for:**
- Static HTML pages
- Server-side rendered content
- Fast scraping with low resource usage

**Example:**
```python
config = ScraperConfig(
    urls=['https://blog.example.com'],
    use_selenium=False,
    css_selectors={
        'title': 'h1.post-title',
        'author': '.author-name',
        'date': 'time.published',
        'content': '.post-content p'
    }
)
```

### Selenium (Dynamic Content)

**Best for:**
- Single-page applications (SPAs)
- JavaScript-rendered content
- Pages requiring user interaction
- AJAX-loaded data

**Example:**
```python
config = ScraperConfig(
    urls=['https://spa-app.com'],
    use_selenium=True,
    selenium_wait_time=10,
    headless=True,
    css_selectors={
        'loaded_content': '.dynamic-data'
    }
)
```

**When to use Selenium:**
- Content loaded via JavaScript/AJAX
- React, Vue, Angular applications
- Infinite scroll pages
- Login-protected pages

**Trade-offs:**
- ✅ Handles JavaScript
- ✅ Waits for dynamic content
- ❌ Slower (launches browser)
- ❌ Higher resource usage

---

## Anti-Detection Techniques

### 1. User Agent Rotation

Automatically rotates user agents to appear as different browsers:

```python
config = ScraperConfig(
    rotate_user_agents=True  # Uses fake-useragent library
)
```

**Examples of rotated user agents:**
- Chrome on Windows
- Firefox on macOS
- Safari on iOS
- Edge on Windows

### 2. Realistic Headers

The scraper sends realistic browser headers:

```python
headers = {
    'User-Agent': '<random>',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
```

Add custom headers:
```python
config = ScraperConfig(
    custom_headers={
        'Referer': 'https://google.com',
        'X-Requested-With': 'XMLHttpRequest'
    }
)
```

### 3. Random Delays

Randomizes delays to mimic human behavior:

```python
config = ScraperConfig(
    min_delay=1.0,  # 1 second minimum
    max_delay=3.0   # 3 seconds maximum
    # Actual delay: random.uniform(1.0, 3.0)
)
```

### 4. Rate Limiting

Prevents overwhelming target servers:

```python
config = ScraperConfig(
    requests_per_minute=30  # Max 30 requests per minute
    # If exceeded, scraper waits until minute resets
)
```

### 5. Selenium Stealth Mode

Hides automation indicators from websites:

```python
# Automatic stealth features:
# - Hides navigator.webdriver property
# - Disables automation flags
# - Uses realistic browser arguments
# - Adds random mouse movements
```

### 6. Session Management

Maintains cookies and session state:

```python
config = ScraperConfig(
    session_cookies={
        'session_id': 'abc123',
        'auth_token': 'xyz789'
    }
)
```

---

## Proxy Rotation

### Why Use Proxies?

- **Avoid IP bans**: Distribute requests across multiple IPs
- **Bypass rate limits**: Each proxy has separate rate limit
- **Geographic diversity**: Access region-specific content
- **Large-scale scraping**: Scale to thousands of requests

### Proxy Formats

```python
proxies = [
    # HTTP proxy (no auth)
    'http://proxy1.com:8080',
    
    # HTTPS proxy (no auth)
    'https://proxy2.com:3128',
    
    # HTTP proxy with authentication
    'http://username:password@proxy3.com:8080',
    
    # HTTPS proxy with authentication
    'https://user:pass@proxy4.com:3128'
]
```

### Configuration

```python
config = ScraperConfig(
    proxies=[
        'http://proxy1.com:8080',
        'http://user:pass@proxy2.com:8080',
        'http://proxy3.com:3128'
    ],
    rotate_proxies=True  # Enable rotation
)
```

### How Rotation Works

1. Scraper starts with proxy #1
2. After each request, moves to next proxy
3. When list ends, loops back to proxy #1
4. Round-robin distribution ensures even usage

### Proxy Providers

**Free Proxies (Testing Only):**
- Free Proxy List
- ProxyScrape
- PubProxy

**Paid Proxies (Production):**
- Bright Data (formerly Luminati)
- Smartproxy
- Oxylabs
- ScraperAPI
- ProxyMesh

### Testing Proxies

```python
import requests

proxy = 'http://proxy.com:8080'
try:
    response = requests.get(
        'https://httpbin.org/ip',
        proxies={'http': proxy, 'https': proxy},
        timeout=10
    )
    print(f"✅ Proxy works: {response.json()}")
except Exception as e:
    print(f"❌ Proxy failed: {e}")
```

---

## Data Extraction

### CSS Selectors

Extract elements using CSS selectors:

```python
css_selectors={
    # Single element
    'title': 'h1.main-title',
    
    # Multiple elements (returns list)
    'paragraphs': 'article p',
    
    # Nested selectors
    'product_name': '.product .title',
    'price': '.product .price span',
    
    # Attributes
    'links': 'a[href]',
    
    # ID selector
    'main_content': '#content',
    
    # Class selector
    'items': '.item-list .item'
}
```

**Common CSS Selector Patterns:**
```css
h1                  /* Tag selector */
.classname          /* Class selector */
#idname             /* ID selector */
div.container       /* Tag + class */
div > p             /* Direct child */
div p               /* Descendant */
a[href]             /* Has attribute */
a[href^="https"]    /* Starts with */
li:first-child      /* First child */
li:nth-child(2)     /* Second child */
```

### XPath Selectors

Extract elements using XPath (Selenium only):

```python
xpath_selectors={
    'heading': '//h1[@class="title"]',
    'items': '//div[@class="item"]',
    'text': '//p[contains(text(), "keyword")]'
}
```

### Table Extraction

Automatically converts HTML tables to structured data:

```python
config = ScraperConfig(
    table_selectors=[
        'table.data-table',
        '#results',
        '.pricing-table'
    ]
)
```

**Example output:**
```json
{
  "tables": [
    [
      {"Name": "Product A", "Price": "$10", "Stock": "100"},
      {"Name": "Product B", "Price": "$20", "Stock": "50"}
    ]
  ]
}
```

### Link Extraction

Extract all links from page:

```python
config = ScraperConfig(
    extract_links=True
)
```

**Output:**
```json
{
  "links": [
    {"text": "Home", "url": "https://example.com/"},
    {"text": "About", "url": "https://example.com/about"}
  ]
}
```

### Image Extraction

Extract all images from page:

```python
config = ScraperConfig(
    extract_images=True
)
```

**Output:**
```json
{
  "images": [
    {"alt": "Logo", "url": "https://example.com/logo.png"},
    {"alt": "Banner", "url": "https://example.com/banner.jpg"}
  ]
}
```

---

## Output Formats

### JSON Output

Full structured data with metadata:

```json
[
  {
    "url": "https://example.com",
    "scraped_at": "2025-11-21T10:30:00",
    "extracted_data": {
      "title": "Example Page",
      "paragraphs": ["First paragraph", "Second paragraph"]
    },
    "tables": [
      [
        {"Column1": "Value1", "Column2": "Value2"}
      ]
    ],
    "links": [...],
    "images": [...]
  }
]
```

### CSV Output

Flattened data for spreadsheet analysis:

```csv
url,scraped_at,title,paragraphs
https://example.com,2025-11-21T10:30:00,Example Page,"First, Second"
```

### Excel Output

Multiple sheets with structured data:

**Sheet 1: "Scraped Data"**
- Main extracted data with one row per URL

**Sheet 2-N: "Table_X_Y"**
- Each extracted table in separate sheet
- Preserves table structure

---

## Best Practices

### 1. Ethical Scraping

```python
# ✅ DO: Respect robots.txt
config = ScraperConfig(respect_robots_txt=True)

# ✅ DO: Use reasonable delays
config = ScraperConfig(min_delay=2.0, max_delay=5.0)

# ✅ DO: Limit request rate
config = ScraperConfig(requests_per_minute=20)

# ❌ DON'T: Overwhelm servers
config = ScraperConfig(min_delay=0.1, requests_per_minute=1000)
```

### 2. Start Small

```python
# Test with 1-2 URLs first
config = ScraperConfig(
    urls=['https://example.com'],
    output_formats=['json']
)

# Then scale up
config = ScraperConfig(
    urls=large_url_list,
    rotate_proxies=True
)
```

### 3. Handle Errors Gracefully

```python
try:
    scraper = WebScraper(config)
    files = scraper.scrape()
except Exception as e:
    print(f"Error: {e}")
    # Log error, retry later, or alert admin
```

### 4. Monitor robots.txt

Check target's robots.txt before scraping:
```
https://example.com/robots.txt
```

Look for:
```
User-agent: *
Disallow: /private/
Crawl-delay: 10
```

### 5. Use Appropriate Method

| Content Type | Method | Reason |
|--------------|--------|---------|
| Static HTML | BeautifulSoup | Faster, lower resources |
| JavaScript SPA | Selenium | Renders dynamic content |
| AJAX loaded | Selenium | Waits for data |
| Simple forms | BeautifulSoup | No JS needed |

### 6. Optimize Selectors

```python
# ✅ Specific selectors (faster)
'title': 'article h1.post-title'

# ❌ Generic selectors (slower, ambiguous)
'title': 'h1'
```

### 7. Test Selectors First

Use browser DevTools to test CSS selectors:
```javascript
// In browser console:
document.querySelectorAll('h1.title')
```

### 8. Respect Terms of Service

- Read website's Terms of Service
- Check if scraping is allowed
- Use public APIs if available
- Contact website owner if unsure

### 9. Use Proxies Responsibly

```python
# ✅ Rotate proxies for large-scale scraping
config = ScraperConfig(
    proxies=proxy_list,
    rotate_proxies=True
)

# ❌ Don't abuse free proxies
# - They're slow and unreliable
# - Often blocked by websites
# - Use paid proxies for production
```

### 10. Save Incrementally

For large scraping jobs, save data periodically:
```python
# Process in batches
batch_size = 100
for i in range(0, len(all_urls), batch_size):
    batch_urls = all_urls[i:i+batch_size]
    config = ScraperConfig(urls=batch_urls)
    scraper = WebScraper(config)
    scraper.scrape()
```

---

## Troubleshooting

### Issue 1: "Blocked by robots.txt"

**Symptom:**
```
❌ Blocked by robots.txt: https://example.com/page
```

**Solutions:**
1. Check robots.txt: `https://example.com/robots.txt`
2. Disable robots.txt check (use responsibly):
   ```python
   config = ScraperConfig(respect_robots_txt=False)
   ```
3. Use official API instead

### Issue 2: Empty Results

**Symptom:**
No data extracted from pages

**Solutions:**
1. Test selectors in browser DevTools
2. Check if content is JavaScript-rendered (use Selenium)
3. Verify page structure hasn't changed
4. Check for anti-bot protection

```python
# Enable Selenium
config = ScraperConfig(use_selenium=True)
```

### Issue 3: ChromeDriver Not Found

**Symptom:**
```
selenium.common.exceptions.WebDriverException: chromedriver not found
```

**Solutions:**
1. Install ChromeDriver:
   ```bash
   brew install chromedriver  # macOS
   ```
2. Specify path:
   ```python
   config = ScraperConfig(chrome_driver_path='/path/to/chromedriver')
   ```
3. Use Selenium Manager (automatic in Selenium 4.15+)

### Issue 4: Proxy Connection Failed

**Symptom:**
```
ProxyError: Cannot connect to proxy
```

**Solutions:**
1. Test proxy manually:
   ```bash
   curl -x http://proxy:port https://httpbin.org/ip
   ```
2. Check proxy format:
   ```python
   'http://username:password@host:port'
   ```
3. Try without proxy first
4. Use paid proxy service

### Issue 5: Rate Limited / Banned

**Symptom:**
```
HTTP 429 Too Many Requests
HTTP 403 Forbidden
```

**Solutions:**
1. Increase delays:
   ```python
   config = ScraperConfig(min_delay=5.0, max_delay=10.0)
   ```
2. Reduce request rate:
   ```python
   config = ScraperConfig(requests_per_minute=10)
   ```
3. Enable proxy rotation
4. Use different user agents

### Issue 6: SSL Certificate Error

**Symptom:**
```
SSLError: certificate verify failed
```

**Solutions:**
1. Disable SSL verification (testing only):
   ```python
   config = ScraperConfig(verify_ssl=False)
   ```
2. Update certificates:
   ```bash
   pip install --upgrade certifi
   ```

### Issue 7: Timeout Errors

**Symptom:**
```
ReadTimeout: Read timed out
```

**Solutions:**
1. Increase timeout:
   ```python
   config = ScraperConfig(timeout=60, page_load_timeout=60)
   ```
2. Check network connection
3. Use proxy with better latency

### Issue 8: JavaScript Not Loading

**Symptom:**
Content missing with Selenium

**Solutions:**
1. Increase wait time:
   ```python
   config = ScraperConfig(selenium_wait_time=20)
   ```
2. Add explicit waits in code
3. Disable headless mode for debugging:
   ```python
   config = ScraperConfig(headless=False)
   ```

---

## Examples

### Example 1: Scrape News Articles

```python
from web_scraper import WebScraper, ScraperConfig

config = ScraperConfig(
    urls=[
        'https://news-site.com/article1',
        'https://news-site.com/article2'
    ],
    css_selectors={
        'title': 'h1.article-title',
        'author': '.author-name',
        'date': 'time.published',
        'content': 'article .content p',
        'tags': '.tag-list .tag'
    },
    output_formats=['json', 'csv', 'excel'],
    min_delay=2.0,
    max_delay=4.0
)

scraper = WebScraper(config)
files = scraper.scrape()
```

### Example 2: Scrape E-commerce Product Data

```python
config = ScraperConfig(
    urls=['https://shop.com/products'],
    css_selectors={
        'product_name': '.product-title',
        'price': '.price-current',
        'rating': '.rating-stars',
        'reviews': '.review-count',
        'availability': '.stock-status'
    },
    table_selectors=['.specifications-table'],
    extract_images=True,
    output_formats=['excel'],
    min_delay=3.0,
    max_delay=6.0,
    requests_per_minute=20
)

scraper = WebScraper(config)
scraper.scrape()
```

### Example 3: Scrape JavaScript SPA

```python
config = ScraperConfig(
    urls=['https://spa-app.com/data'],
    use_selenium=True,
    selenium_wait_time=15,
    headless=True,
    css_selectors={
        'dynamic_data': '.loaded-content',
        'items': '.item-card'
    },
    output_formats=['json']
)

scraper = WebScraper(config)
scraper.scrape()
```

### Example 4: Large-Scale Scraping with Proxies

```python
# Load URLs from file
with open('urls.txt') as f:
    urls = [line.strip() for line in f]

# Load proxies
proxies = [
    'http://user:pass@proxy1.com:8080',
    'http://user:pass@proxy2.com:8080',
    'http://user:pass@proxy3.com:8080'
]

config = ScraperConfig(
    urls=urls,
    proxies=proxies,
    rotate_proxies=True,
    rotate_user_agents=True,
    min_delay=1.0,
    max_delay=2.0,
    requests_per_minute=40,
    css_selectors={
        'title': 'h1',
        'content': '.main-content'
    },
    output_formats=['json', 'csv']
)

scraper = WebScraper(config)
scraper.scrape()
```

### Example 5: Extract Tables from Wikipedia

```python
config = ScraperConfig(
    urls=['https://en.wikipedia.org/wiki/List_of_countries_by_GDP'],
    table_selectors=['table.wikitable'],
    output_formats=['excel'],
    min_delay=2.0
)

scraper = WebScraper(config)
files = scraper.scrape()
# Tables will be in separate Excel sheets
```

### Example 6: Scrape with Custom Headers & Cookies

```python
config = ScraperConfig(
    urls=['https://members-only.com/data'],
    custom_headers={
        'Referer': 'https://members-only.com/login',
        'X-API-Key': 'your-api-key'
    },
    session_cookies={
        'session_id': 'abc123def456',
        'auth_token': 'xyz789'
    },
    css_selectors={
        'member_data': '.protected-content'
    }
)

scraper = WebScraper(config)
scraper.scrape()
```

### Example 7: Extract All Links and Images

```python
config = ScraperConfig(
    urls=['https://example.com'],
    extract_links=True,
    extract_images=True,
    output_formats=['json']
)

scraper = WebScraper(config)
files = scraper.scrape()
# JSON will contain all links and images with metadata
```

### Example 8: Use Configuration File

**config/scraper_config.json:**
```json
{
  "urls": [
    "https://blog.example.com/post1",
    "https://blog.example.com/post2"
  ],
  "css_selectors": {
    "title": "h1.post-title",
    "author": ".author",
    "content": ".post-body p"
  },
  "output_formats": ["json", "csv"],
  "min_delay": 2.0,
  "max_delay": 5.0,
  "rotate_user_agents": true
}
```

**Run with config:**
```bash
python web_scraper.py --config config/scraper_config.json
```

---

## Legal and Ethical Considerations

### ⚖️ Legal Compliance

1. **Terms of Service**: Read and comply with website's ToS
2. **Copyright**: Respect intellectual property rights
3. **Privacy**: Don't scrape personal/private information
4. **CFAA**: In US, unauthorized access may violate Computer Fraud and Abuse Act

### ✅ Ethical Guidelines

1. **Respect robots.txt**: Always check and obey
2. **Rate limiting**: Don't overwhelm servers
3. **Attribution**: Credit data sources when publishing
4. **Use APIs**: Prefer official APIs over scraping
5. **Ask permission**: Contact site owner if unsure

### 🚫 What NOT to Scrape

- Login-protected content (without permission)
- Personal information (emails, phone numbers, addresses)
- Copyrighted content for commercial use
- Financial/medical records
- Any data violating privacy laws (GDPR, CCPA)

### ✅ Acceptable Use Cases

- Public data collection for research
- Price monitoring (your own products)
- SEO analysis
- Market research (public data)
- Academic research
- Personal use (non-commercial)

---

## Performance Tips

### 1. Use BeautifulSoup When Possible
```python
# 10x faster than Selenium
config = ScraperConfig(use_selenium=False)
```

### 2. Batch Processing
```python
# Process in chunks
for batch in chunks(all_urls, 100):
    config = ScraperConfig(urls=batch)
    scraper = WebScraper(config)
    scraper.scrape()
```

### 3. Concurrent Scraping
```python
from concurrent.futures import ThreadPoolExecutor

def scrape_url(url):
    config = ScraperConfig(urls=[url])
    scraper = WebScraper(config)
    return scraper.scrape()

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(scrape_url, urls)
```

### 4. Optimize Selectors
```python
# ✅ Specific
'title': 'article > h1.main-title'

# ❌ Generic (slower)
'title': 'h1'
```

### 5. Disable Unnecessary Features
```python
config = ScraperConfig(
    extract_links=False,  # If not needed
    extract_images=False,  # If not needed
    verify_ssl=False  # Only for testing
)
```

---

## Advanced Topics

### Custom Data Processing

```python
from web_scraper import WebScraper, ScraperConfig

class CustomScraper(WebScraper):
    def _extract_data(self, html, url):
        data = super()._extract_data(html, url)
        
        # Add custom processing
        if 'extracted_data' in data:
            # Clean prices
            if 'price' in data['extracted_data']:
                price = data['extracted_data']['price']
                data['extracted_data']['price_numeric'] = float(
                    price.replace('$', '').replace(',', '')
                )
        
        return data

# Use custom scraper
scraper = CustomScraper(config)
scraper.scrape()
```

### Pagination Handling

```python
def scrape_paginated_site():
    base_url = 'https://example.com/products?page={}'
    all_urls = [base_url.format(i) for i in range(1, 11)]
    
    config = ScraperConfig(
        urls=all_urls,
        css_selectors={'items': '.product-card'}
    )
    
    scraper = WebScraper(config)
    return scraper.scrape()
```

### JavaScript Execution (Selenium)

```python
from web_scraper import WebScraper, ScraperConfig

class JSScraper(WebScraper):
    def _fetch_page_selenium(self, url):
        html = super()._fetch_page_selenium(url)
        
        # Execute custom JavaScript
        if self.driver:
            # Scroll to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)
            
            # Click "Load More" button
            try:
                button = self.driver.find_element(By.CSS_SELECTOR, '.load-more')
                button.click()
                time.sleep(3)
            except:
                pass
            
            return self.driver.page_source
        
        return html
```

---

## Conclusion

This web scraper provides a robust, ethical, and feature-rich solution for web data extraction. Always scrape responsibly, respect website policies, and use official APIs when available.

For questions or issues, refer to the troubleshooting section or check the project repository.

**Happy Scraping! 🚀**
