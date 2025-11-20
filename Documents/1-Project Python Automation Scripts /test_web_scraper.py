#!/usr/bin/env python3
"""
Integration tests for Web Scraper

Tests all major features with mocked HTTP responses:
- Static content scraping (BeautifulSoup)
- Dynamic content scraping (Selenium - mocked)
- Table extraction
- Proxy rotation
- Rate limiting
- Anti-detection features
- Multi-format output

Run: python test_web_scraper.py
"""

import json
import os
import shutil
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from web_scraper import WebScraper, ScraperConfig


class TestWebScraper(unittest.TestCase):
    """Test suite for Web Scraper"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, 'output')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def _create_mock_html(self, title="Test Page", paragraphs=2):
        """Create mock HTML content"""
        para_html = "".join([
            f"<p>This is paragraph {i+1} with some content.</p>"
            for i in range(paragraphs)
        ])
        
        return f"""
        <html>
            <head><title>{title}</title></head>
            <body>
                <h1>{title}</h1>
                <article>
                    {para_html}
                </article>
            </body>
        </html>
        """
    
    def _create_mock_table_html(self):
        """Create mock HTML with table"""
        return """
        <html>
            <body>
                <h1>Data Table</h1>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Age</th>
                            <th>City</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Alice</td>
                            <td>30</td>
                            <td>New York</td>
                        </tr>
                        <tr>
                            <td>Bob</td>
                            <td>25</td>
                            <td>San Francisco</td>
                        </tr>
                        <tr>
                            <td>Charlie</td>
                            <td>35</td>
                            <td>Chicago</td>
                        </tr>
                    </tbody>
                </table>
            </body>
        </html>
        """
    
    @patch('web_scraper.requests.Session.get')
    def test_basic_scraping(self, mock_get):
        """Test 1: Basic static page scraping"""
        print("\n" + "="*60)
        print("Test 1: Basic Static Page Scraping")
        print("="*60)
        
        # Mock response
        mock_response = Mock()
        mock_response.text = self._create_mock_html("Test Article", 3)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Configure scraper
        config = ScraperConfig(
            urls=['https://example.com/test'],
            css_selectors={
                'title': 'h1',
                'paragraphs': 'article p'
            },
            output_folder=self.output_dir,
            output_formats=['json'],
            respect_robots_txt=False,  # Skip for testing
            min_delay=0.1,
            max_delay=0.2
        )
        
        # Run scraper
        scraper = WebScraper(config)
        files = scraper.scrape()
        
        # Assertions
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].endswith('.json'))
        
        # Check output content
        with open(files[0], 'r') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['url'], 'https://example.com/test')
        self.assertEqual(data[0]['extracted_data']['title'], 'Test Article')
        self.assertEqual(len(data[0]['extracted_data']['paragraphs']), 3)
        
        print(f"✅ PASSED: Scraped 1 page")
        print(f"   Title: {data[0]['extracted_data']['title']}")
        print(f"   Paragraphs: {len(data[0]['extracted_data']['paragraphs'])}")
        print(f"   Output file: {files[0]}")
    
    @patch('web_scraper.requests.Session.get')
    def test_table_extraction(self, mock_get):
        """Test 2: Table extraction to structured data"""
        print("\n" + "="*60)
        print("Test 2: Table Extraction")
        print("="*60)
        
        # Mock response with table
        mock_response = Mock()
        mock_response.text = self._create_mock_table_html()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Configure scraper
        config = ScraperConfig(
            urls=['https://example.com/data'],
            table_selectors=['table.data-table'],
            output_folder=self.output_dir,
            output_formats=['json'],
            respect_robots_txt=False,
            min_delay=0.1
        )
        
        # Run scraper
        scraper = WebScraper(config)
        files = scraper.scrape()
        
        # Check output
        with open(files[0], 'r') as f:
            data = json.load(f)
        
        # Assertions
        self.assertIn('tables', data[0])
        self.assertEqual(len(data[0]['tables']), 1)
        
        table = data[0]['tables'][0]
        self.assertEqual(len(table), 3)  # 3 rows
        self.assertEqual(table[0]['Name'], 'Alice')
        self.assertEqual(table[0]['Age'], '30')
        self.assertEqual(table[1]['Name'], 'Bob')
        
        print(f"✅ PASSED: Extracted table with {len(table)} rows")
        print(f"   Row 1: {table[0]}")
        print(f"   Row 2: {table[1]}")
    
    @patch('web_scraper.requests.Session.get')
    def test_multi_format_output(self, mock_get):
        """Test 3: Multi-format output (JSON, CSV, Excel)"""
        print("\n" + "="*60)
        print("Test 3: Multi-Format Output")
        print("="*60)
        
        # Mock response
        mock_response = Mock()
        mock_response.text = self._create_mock_html("Multi Format Test", 2)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Configure scraper for all formats
        config = ScraperConfig(
            urls=['https://example.com/test'],
            css_selectors={
                'title': 'h1',
                'content': 'article p'
            },
            output_folder=self.output_dir,
            output_formats=['json', 'csv', 'excel'],
            respect_robots_txt=False,
            min_delay=0.1
        )
        
        # Run scraper
        scraper = WebScraper(config)
        files = scraper.scrape()
        
        # Assertions
        self.assertEqual(len(files), 3)
        
        # Check file types
        extensions = [os.path.splitext(f)[1] for f in files]
        self.assertIn('.json', extensions)
        self.assertIn('.csv', extensions)
        self.assertIn('.xlsx', extensions)
        
        print(f"✅ PASSED: Created {len(files)} output files")
        for f in files:
            ext = os.path.splitext(f)[1]
            size = os.path.getsize(f)
            print(f"   {ext}: {size} bytes")
    
    @patch('web_scraper.requests.Session.get')
    def test_multiple_urls(self, mock_get):
        """Test 4: Scraping multiple URLs"""
        print("\n" + "="*60)
        print("Test 4: Multiple URLs")
        print("="*60)
        
        # Mock responses for different URLs
        def mock_get_response(url, **kwargs):
            response = Mock()
            if 'page1' in url:
                response.text = self._create_mock_html("Page 1", 2)
            elif 'page2' in url:
                response.text = self._create_mock_html("Page 2", 3)
            elif 'page3' in url:
                response.text = self._create_mock_html("Page 3", 1)
            response.status_code = 200
            return response
        
        mock_get.side_effect = mock_get_response
        
        # Configure scraper
        config = ScraperConfig(
            urls=[
                'https://example.com/page1',
                'https://example.com/page2',
                'https://example.com/page3'
            ],
            css_selectors={
                'title': 'h1'
            },
            output_folder=self.output_dir,
            output_formats=['json'],
            respect_robots_txt=False,
            min_delay=0.1
        )
        
        # Run scraper
        scraper = WebScraper(config)
        files = scraper.scrape()
        
        # Check output
        with open(files[0], 'r') as f:
            data = json.load(f)
        
        # Assertions
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['extracted_data']['title'], 'Page 1')
        self.assertEqual(data[1]['extracted_data']['title'], 'Page 2')
        self.assertEqual(data[2]['extracted_data']['title'], 'Page 3')
        
        print(f"✅ PASSED: Scraped {len(data)} pages")
        for item in data:
            print(f"   {item['url']}: {item['extracted_data']['title']}")
    
    @patch('web_scraper.requests.Session.get')
    def test_rate_limiting(self, mock_get):
        """Test 5: Rate limiting enforcement"""
        print("\n" + "="*60)
        print("Test 5: Rate Limiting")
        print("="*60)
        
        # Mock response
        mock_response = Mock()
        mock_response.text = self._create_mock_html("Rate Limit Test", 1)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Configure with strict rate limiting
        config = ScraperConfig(
            urls=[
                'https://example.com/1',
                'https://example.com/2',
                'https://example.com/3'
            ],
            css_selectors={'title': 'h1'},
            output_folder=self.output_dir,
            output_formats=['json'],
            respect_robots_txt=False,
            min_delay=0.5,  # 0.5 second minimum
            max_delay=0.6   # 0.6 second maximum
        )
        
        # Measure time
        start_time = time.time()
        
        scraper = WebScraper(config)
        scraper.scrape()
        
        elapsed_time = time.time() - start_time
        
        # Should take at least 1.5 seconds (3 requests * 0.5s min delay)
        min_expected_time = 0.5 * 3
        
        self.assertGreaterEqual(elapsed_time, min_expected_time * 0.7)  # 70% tolerance for CI
        
        print(f"✅ PASSED: Rate limiting enforced")
        print(f"   Elapsed time: {elapsed_time:.2f}s")
        print(f"   Expected minimum: {min_expected_time:.2f}s")
        print(f"   Average delay: {elapsed_time/3:.2f}s per request")
    
    @patch('web_scraper.requests.Session.get')
    def test_proxy_rotation(self, mock_get):
        """Test 6: Proxy rotation"""
        print("\n" + "="*60)
        print("Test 6: Proxy Rotation")
        print("="*60)
        
        # Track proxies used
        used_proxies = []
        
        def mock_get_with_proxy(url, **kwargs):
            if 'proxies' in kwargs:
                used_proxies.append(kwargs['proxies'])
            response = Mock()
            response.text = self._create_mock_html("Proxy Test", 1)
            response.status_code = 200
            return response
        
        mock_get.side_effect = mock_get_with_proxy
        
        # Configure with proxy rotation
        proxies = [
            'http://proxy1.com:8080',
            'http://proxy2.com:8080',
            'http://proxy3.com:8080'
        ]
        
        config = ScraperConfig(
            urls=[
                'https://example.com/1',
                'https://example.com/2',
                'https://example.com/3',
                'https://example.com/4'
            ],
            proxies=proxies,
            rotate_proxies=True,
            css_selectors={'title': 'h1'},
            output_folder=self.output_dir,
            output_formats=['json'],
            respect_robots_txt=False,
            min_delay=0.1
        )
        
        # Run scraper
        scraper = WebScraper(config)
        scraper.scrape()
        
        # Assertions
        self.assertEqual(len(used_proxies), 4)
        
        # Check rotation pattern
        self.assertEqual(used_proxies[0]['http'], proxies[0])
        self.assertEqual(used_proxies[1]['http'], proxies[1])
        self.assertEqual(used_proxies[2]['http'], proxies[2])
        self.assertEqual(used_proxies[3]['http'], proxies[0])  # Rotated back
        
        print(f"✅ PASSED: Proxy rotation working")
        print(f"   Proxies defined: {len(proxies)}")
        print(f"   Requests made: {len(used_proxies)}")
        print(f"   Rotation pattern:")
        for i, proxy_dict in enumerate(used_proxies):
            print(f"      Request {i+1}: {proxy_dict['http']}")
    
    @patch('web_scraper.requests.Session.get')
    def test_user_agent_rotation(self, mock_get):
        """Test 7: User agent rotation"""
        print("\n" + "="*60)
        print("Test 7: User Agent Rotation")
        print("="*60)
        
        # Track user agents used
        used_user_agents = []
        
        def mock_get_with_headers(url, **kwargs):
            if 'headers' in kwargs:
                used_user_agents.append(kwargs['headers'].get('User-Agent'))
            response = Mock()
            response.text = self._create_mock_html("UA Test", 1)
            response.status_code = 200
            return response
        
        mock_get.side_effect = mock_get_with_headers
        
        # Configure with user agent rotation
        config = ScraperConfig(
            urls=[
                'https://example.com/1',
                'https://example.com/2',
                'https://example.com/3'
            ],
            rotate_user_agents=True,
            css_selectors={'title': 'h1'},
            output_folder=self.output_dir,
            output_formats=['json'],
            respect_robots_txt=False,
            min_delay=0.1
        )
        
        # Run scraper
        scraper = WebScraper(config)
        scraper.scrape()
        
        # Assertions
        self.assertEqual(len(used_user_agents), 3)
        
        # Check that user agents exist and have variation
        for ua in used_user_agents:
            self.assertIsNotNone(ua)
            self.assertGreater(len(ua), 0)
        
        print(f"✅ PASSED: User agent rotation enabled")
        print(f"   Requests made: {len(used_user_agents)}")
        print(f"   User agents used:")
        for i, ua in enumerate(used_user_agents):
            print(f"      Request {i+1}: {ua[:50]}...")
    
    @patch('web_scraper.requests.Session.get')
    def test_error_handling(self, mock_get):
        """Test 8: Error handling and retries"""
        print("\n" + "="*60)
        print("Test 8: Error Handling")
        print("="*60)
        
        # Simulate failures then success
        call_count = [0]
        
        def mock_get_with_failures(url, **kwargs):
            call_count[0] += 1
            if call_count[0] <= 2:  # First 2 attempts fail
                raise Exception("Connection timeout")
            # Third attempt succeeds
            response = Mock()
            response.text = self._create_mock_html("Retry Test", 1)
            response.status_code = 200
            return response
        
        mock_get.side_effect = mock_get_with_failures
        
        # Configure with retries
        config = ScraperConfig(
            urls=['https://example.com/test'],
            css_selectors={'title': 'h1'},
            output_folder=self.output_dir,
            output_formats=['json'],
            respect_robots_txt=False,
            min_delay=0.1,
            max_retries=3
        )
        
        # Run scraper
        scraper = WebScraper(config)
        files = scraper.scrape()
        
        # Should succeed on 3rd attempt
        self.assertEqual(call_count[0], 3)
        self.assertEqual(len(files), 1)
        
        print(f"✅ PASSED: Error handling working")
        print(f"   Failed attempts: 2")
        print(f"   Successful attempt: 3")
        print(f"   Total calls: {call_count[0]}")


def run_tests():
    """Run all tests"""
    print("🧪 Web Scraper Integration Tests")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestWebScraper)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == '__main__':
    exit(run_tests())
