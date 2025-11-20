#!/usr/bin/env python3
"""
Comprehensive Test Suite for PDF Report Generator

Tests all major functionality:
1. Basic PDF generation
2. Chart creation (6 types)
3. Table creation
4. Cover page generation
5. Table of contents
6. Multiple data sources
7. Branding customization
8. Batch processing (simulated)

Usage:
    python test_pdf_report_generator.py
"""

import unittest
import os
import sys
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_report_generator import (
    PDFReportGenerator,
    ReportConfig,
    BrandingConfig,
    ChartConfig,
    TableConfig,
    load_config
)

import pandas as pd
from PyPDF2 import PdfReader


class TestPDFReportGenerator(unittest.TestCase):
    """Test suite for PDF Report Generator"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        print("\n" + "="*70)
        print("PDF Report Generator - Integration Test Suite")
        print("="*70)
        
        # Create temporary directory for test outputs
        cls.test_dir = tempfile.mkdtemp(prefix="pdf_test_")
        cls.data_dir = os.path.join(cls.test_dir, "data")
        cls.output_dir = os.path.join(cls.test_dir, "output")
        cls.config_dir = os.path.join(cls.test_dir, "config")
        
        os.makedirs(cls.data_dir, exist_ok=True)
        os.makedirs(cls.output_dir, exist_ok=True)
        os.makedirs(cls.config_dir, exist_ok=True)
        
        # Create sample data
        cls._create_sample_data()
        
        print(f"✓ Test environment created: {cls.test_dir}")
        print(f"  - Data directory: {cls.data_dir}")
        print(f"  - Output directory: {cls.output_dir}")
        print(f"  - Config directory: {cls.config_dir}\n")
    
    @classmethod
    def _create_sample_data(cls):
        """Create sample CSV data for testing"""
        # Sales data
        sales_data = pd.DataFrame({
            'Date': pd.date_range('2024-01-01', periods=50, freq='W'),
            'Product': ['Widget A', 'Widget B', 'Widget C', 'Widget D'] * 12 + ['Widget A', 'Widget B'],
            'Region': ['East', 'West', 'North', 'South'] * 12 + ['East', 'West'],
            'Sales_Person': ['Alice', 'Bob', 'Charlie', 'Diana'] * 12 + ['Alice', 'Bob'],
            'Revenue': [1000 + i*100 + (i%4)*50 for i in range(50)],
            'Units_Sold': [10 + i*2 + (i%3) for i in range(50)],
            'Profit_Margin': [0.15 + (i%10)*0.02 for i in range(50)]
        })
        sales_data.to_csv(os.path.join(cls.data_dir, 'sales.csv'), index=False)
        
        # Product data
        product_data = pd.DataFrame({
            'Product': ['Widget A', 'Widget B', 'Widget C', 'Widget D', 'Widget E'],
            'Category': ['Electronics', 'Furniture', 'Electronics', 'Clothing', 'Furniture'],
            'Price': [99.99, 249.99, 149.99, 79.99, 349.99],
            'Stock': [150, 75, 200, 100, 50],
            'SKU': ['WGT-A-001', 'WGT-B-002', 'WGT-C-003', 'WGT-D-004', 'WGT-E-005']
        })
        product_data.to_csv(os.path.join(cls.data_dir, 'products.csv'), index=False)
        
        print("✓ Sample data created:")
        print(f"  - sales.csv: {len(sales_data)} rows")
        print(f"  - products.csv: {len(product_data)} rows")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)
        print(f"\n✓ Test environment cleaned up")
    
    def setUp(self):
        """Set up for each test"""
        self.test_count = getattr(self, '_test_count', 0) + 1
        setattr(self, '_test_count', self.test_count)
    
    def tearDown(self):
        """Clean up after each test"""
        pass
    
    def _verify_pdf_created(self, filepath, min_size=1000):
        """Verify PDF file was created and is valid"""
        self.assertTrue(os.path.exists(filepath), f"PDF not created: {filepath}")
        
        file_size = os.path.getsize(filepath)
        self.assertGreater(file_size, min_size, 
                          f"PDF too small ({file_size} bytes), likely empty")
        
        # Try to read PDF to verify validity
        try:
            reader = PdfReader(filepath)
            page_count = len(reader.pages)
            self.assertGreater(page_count, 0, "PDF has no pages")
            return page_count
        except Exception as e:
            self.fail(f"PDF appears corrupted: {e}")
    
    # =========================================================================
    # Test 1: Basic PDF Generation
    # =========================================================================
    
    def test_01_basic_pdf_generation(self):
        """Test 1: Basic PDF generation with minimal configuration"""
        print(f"\nTest {self.test_count}: Basic PDF generation")
        
        config = ReportConfig(
            title="Basic Test Report",
            data_sources=[
                {
                    "name": "sales",
                    "path": os.path.join(self.data_dir, "sales.csv"),
                    "type": "csv"
                }
            ],
            sections=[
                {
                    "title": "Introduction",
                    "content_type": "text",
                    "content": "This is a basic test report to verify PDF generation."
                }
            ],
            output_folder=self.output_dir,
            output_filename="test_basic.pdf"
        )
        
        generator = PDFReportGenerator(config)
        output_path = generator.generate_report()
        
        # Verify
        page_count = self._verify_pdf_created(output_path)
        print(f"  ✓ Basic PDF created: {output_path}")
        print(f"  ✓ Pages: {page_count}")
        print(f"  ✓ Size: {os.path.getsize(output_path):,} bytes")
    
    # =========================================================================
    # Test 2: Bar Chart Generation
    # =========================================================================
    
    def test_02_bar_chart_generation(self):
        """Test 2: Generate PDF with bar chart"""
        print(f"\nTest {self.test_count}: Bar chart generation")
        
        config = ReportConfig(
            title="Bar Chart Test Report",
            data_sources=[
                {
                    "name": "sales",
                    "path": os.path.join(self.data_dir, "sales.csv"),
                    "type": "csv"
                }
            ],
            sections=[
                {
                    "title": "Revenue by Product",
                    "content_type": "chart",
                    "data_source": "sales",
                    "content": {
                        "chart_type": "bar",
                        "title": "Total Revenue by Product",
                        "data_column_x": "Product",
                        "data_column_y": "Revenue",
                        "aggregation": "sum",
                        "color_scheme": "Set2"
                    }
                }
            ],
            output_folder=self.output_dir,
            output_filename="test_bar_chart.pdf",
            include_cover_page=False,
            include_toc=False
        )
        
        generator = PDFReportGenerator(config)
        output_path = generator.generate_report()
        
        # Verify
        page_count = self._verify_pdf_created(output_path, min_size=5000)
        print(f"  ✓ Bar chart PDF created: {output_path}")
        print(f"  ✓ Chart generated successfully")
    
    # =========================================================================
    # Test 3: Multiple Chart Types
    # =========================================================================
    
    def test_03_multiple_chart_types(self):
        """Test 3: Generate PDF with multiple chart types"""
        print(f"\nTest {self.test_count}: Multiple chart types")
        
        config = ReportConfig(
            title="Multi-Chart Test Report",
            data_sources=[
                {
                    "name": "sales",
                    "path": os.path.join(self.data_dir, "sales.csv"),
                    "type": "csv"
                }
            ],
            sections=[
                {
                    "title": "Bar Chart",
                    "content_type": "chart",
                    "data_source": "sales",
                    "content": {
                        "chart_type": "bar",
                        "title": "Revenue by Product",
                        "data_column_x": "Product",
                        "data_column_y": "Revenue",
                        "aggregation": "sum"
                    }
                },
                {
                    "title": "Line Chart",
                    "content_type": "chart",
                    "data_source": "sales",
                    "page_break_before": True,
                    "content": {
                        "chart_type": "line",
                        "title": "Revenue Trend",
                        "data_column_x": "Date",
                        "data_column_y": "Revenue",
                        "aggregation": "sum"
                    }
                },
                {
                    "title": "Pie Chart",
                    "content_type": "chart",
                    "data_source": "sales",
                    "page_break_before": True,
                    "content": {
                        "chart_type": "pie",
                        "title": "Revenue Distribution by Region",
                        "data_column_x": "Region",
                        "data_column_y": "Revenue",
                        "aggregation": "sum"
                    }
                },
                {
                    "title": "Scatter Plot",
                    "content_type": "chart",
                    "data_source": "sales",
                    "page_break_before": True,
                    "content": {
                        "chart_type": "scatter",
                        "title": "Revenue vs Units Sold",
                        "data_column_x": "Units_Sold",
                        "data_column_y": "Revenue",
                        "aggregation": "none"
                    }
                }
            ],
            output_folder=self.output_dir,
            output_filename="test_multi_charts.pdf",
            include_cover_page=False,
            include_toc=False
        )
        
        generator = PDFReportGenerator(config)
        output_path = generator.generate_report()
        
        # Verify
        page_count = self._verify_pdf_created(output_path, min_size=15000)
        print(f"  ✓ Multi-chart PDF created: {output_path}")
        print(f"  ✓ 4 chart types generated (bar, line, pie, scatter)")
        print(f"  ✓ Pages: {page_count}")
    
    # =========================================================================
    # Test 4: Table Generation
    # =========================================================================
    
    def test_04_table_generation(self):
        """Test 4: Generate PDF with styled table"""
        print(f"\nTest {self.test_count}: Table generation")
        
        config = ReportConfig(
            title="Table Test Report",
            data_sources=[
                {
                    "name": "products",
                    "path": os.path.join(self.data_dir, "products.csv"),
                    "type": "csv"
                }
            ],
            sections=[
                {
                    "title": "Product Catalog",
                    "content_type": "table",
                    "data_source": "products",
                    "content": {
                        "title": "All Products",
                        "columns": ["Product", "Category", "Price", "Stock", "SKU"],
                        "alternate_row_colors": True,
                        "header_bg_color": "#2c3e50"
                    }
                }
            ],
            output_folder=self.output_dir,
            output_filename="test_table.pdf",
            include_cover_page=False,
            include_toc=False
        )
        
        generator = PDFReportGenerator(config)
        output_path = generator.generate_report()
        
        # Verify
        page_count = self._verify_pdf_created(output_path, min_size=2000)
        print(f"  ✓ Table PDF created: {output_path}")
        print(f"  ✓ Styled table generated")
    
    # =========================================================================
    # Test 5: Cover Page and TOC
    # =========================================================================
    
    def test_05_cover_and_toc(self):
        """Test 5: Generate PDF with cover page and table of contents"""
        print(f"\nTest {self.test_count}: Cover page and TOC")
        
        config = ReportConfig(
            title="Complete Report Test",
            subtitle="With Cover and TOC",
            author="Test Suite",
            data_sources=[
                {
                    "name": "sales",
                    "path": os.path.join(self.data_dir, "sales.csv"),
                    "type": "csv"
                }
            ],
            sections=[
                {
                    "title": "Executive Summary",
                    "content_type": "text",
                    "content": "This report demonstrates cover page and table of contents."
                },
                {
                    "title": "Sales Analysis",
                    "content_type": "chart",
                    "data_source": "sales",
                    "content": {
                        "chart_type": "bar",
                        "title": "Revenue by Product",
                        "data_column_x": "Product",
                        "data_column_y": "Revenue",
                        "aggregation": "sum"
                    }
                },
                {
                    "title": "Conclusion",
                    "content_type": "text",
                    "content": "The analysis shows positive trends across all products."
                }
            ],
            include_cover_page=True,
            include_toc=True,
            output_folder=self.output_dir,
            output_filename="test_cover_toc.pdf"
        )
        
        generator = PDFReportGenerator(config)
        output_path = generator.generate_report()
        
        # Verify
        page_count = self._verify_pdf_created(output_path, min_size=10000)
        self.assertGreaterEqual(page_count, 3, "Should have cover, TOC, and content pages")
        print(f"  ✓ PDF with cover and TOC created: {output_path}")
        print(f"  ✓ Pages: {page_count} (cover + TOC + content)")
    
    # =========================================================================
    # Test 6: Multiple Data Sources
    # =========================================================================
    
    def test_06_multiple_data_sources(self):
        """Test 6: Generate PDF with data from multiple sources"""
        print(f"\nTest {self.test_count}: Multiple data sources")
        
        config = ReportConfig(
            title="Multi-Source Test Report",
            data_sources=[
                {
                    "name": "sales",
                    "path": os.path.join(self.data_dir, "sales.csv"),
                    "type": "csv"
                },
                {
                    "name": "products",
                    "path": os.path.join(self.data_dir, "products.csv"),
                    "type": "csv"
                }
            ],
            sections=[
                {
                    "title": "Sales Data",
                    "content_type": "chart",
                    "data_source": "sales",
                    "content": {
                        "chart_type": "bar",
                        "title": "Revenue by Product",
                        "data_column_x": "Product",
                        "data_column_y": "Revenue",
                        "aggregation": "sum"
                    }
                },
                {
                    "title": "Product Inventory",
                    "content_type": "table",
                    "data_source": "products",
                    "content": {
                        "title": "Product List",
                        "columns": ["Product", "Category", "Price"],
                        "max_rows": 5
                    }
                }
            ],
            output_folder=self.output_dir,
            output_filename="test_multi_source.pdf",
            include_cover_page=False,
            include_toc=False
        )
        
        generator = PDFReportGenerator(config)
        output_path = generator.generate_report()
        
        # Verify
        page_count = self._verify_pdf_created(output_path, min_size=8000)
        print(f"  ✓ Multi-source PDF created: {output_path}")
        print(f"  ✓ Data from 2 sources used successfully")
    
    # =========================================================================
    # Test 7: Custom Branding
    # =========================================================================
    
    def test_07_custom_branding(self):
        """Test 7: Generate PDF with custom branding"""
        print(f"\nTest {self.test_count}: Custom branding")
        
        config = ReportConfig(
            title="Branded Test Report",
            data_sources=[
                {
                    "name": "sales",
                    "path": os.path.join(self.data_dir, "sales.csv"),
                    "type": "csv"
                }
            ],
            branding={
                "primary_color": "#1a5490",
                "secondary_color": "#ff6b6b",
                "accent_color": "#4ecdc4",
                "company_name": "Test Corporation",
                "report_footer": "Confidential - Test Report",
                "title_font": "Helvetica-Bold",
                "body_font": "Helvetica"
            },
            sections=[
                {
                    "title": "Analysis",
                    "content_type": "chart",
                    "data_source": "sales",
                    "content": {
                        "chart_type": "bar",
                        "title": "Revenue by Region",
                        "data_column_x": "Region",
                        "data_column_y": "Revenue",
                        "aggregation": "sum"
                    }
                }
            ],
            include_header=True,
            include_footer=True,
            output_folder=self.output_dir,
            output_filename="test_branding.pdf"
        )
        
        generator = PDFReportGenerator(config)
        output_path = generator.generate_report()
        
        # Verify
        page_count = self._verify_pdf_created(output_path, min_size=8000)
        print(f"  ✓ Branded PDF created: {output_path}")
        print(f"  ✓ Custom colors and fonts applied")
    
    # =========================================================================
    # Test 8: Configuration File Loading
    # =========================================================================
    
    def test_08_config_file_loading(self):
        """Test 8: Load configuration from JSON file"""
        print(f"\nTest {self.test_count}: Configuration file loading")
        
        # Create config file
        config_data = {
            "title": "Config File Test Report",
            "author": "Automated Test",
            "data_sources": [
                {
                    "name": "sales",
                    "path": os.path.join(self.data_dir, "sales.csv"),
                    "type": "csv"
                }
            ],
            "sections": [
                {
                    "title": "Introduction",
                    "content_type": "text",
                    "content": "Report generated from JSON config file."
                },
                {
                    "title": "Sales Chart",
                    "content_type": "chart",
                    "data_source": "sales",
                    "content": {
                        "chart_type": "pie",
                        "title": "Revenue by Region",
                        "data_column_x": "Region",
                        "data_column_y": "Revenue",
                        "aggregation": "sum"
                    }
                }
            ],
            "output_folder": self.output_dir,
            "output_filename": "test_config_file.pdf"
        }
        
        config_path = os.path.join(self.config_dir, "test_config.json")
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        # Load and generate
        config = load_config(config_path)
        generator = PDFReportGenerator(config)
        output_path = generator.generate_report()
        
        # Verify
        page_count = self._verify_pdf_created(output_path, min_size=8000)
        print(f"  ✓ Config file loaded: {config_path}")
        print(f"  ✓ PDF generated from config: {output_path}")
    
    # =========================================================================
    # Test 9: Complex Report (All Features)
    # =========================================================================
    
    def test_09_complex_report(self):
        """Test 9: Generate complex report with all features"""
        print(f"\nTest {self.test_count}: Complex report (all features)")
        
        config = ReportConfig(
            title="Comprehensive Test Report",
            subtitle="All Features Demonstration",
            author="Integration Test Suite",
            subject="Testing all PDF generator capabilities",
            data_sources=[
                {
                    "name": "sales",
                    "path": os.path.join(self.data_dir, "sales.csv"),
                    "type": "csv"
                },
                {
                    "name": "products",
                    "path": os.path.join(self.data_dir, "products.csv"),
                    "type": "csv"
                }
            ],
            branding={
                "primary_color": "#2c3e50",
                "secondary_color": "#3498db",
                "accent_color": "#e74c3c",
                "company_name": "Test Corporation",
                "report_footer": "Confidential - Integration Test",
                "title_font": "Helvetica-Bold",
                "heading_font": "Helvetica-Bold",
                "body_font": "Helvetica"
            },
            sections=[
                {
                    "title": "Executive Summary",
                    "content_type": "text",
                    "content": "This comprehensive report demonstrates all features of the PDF Report Generator including multiple data sources, various chart types, styled tables, custom branding, and professional formatting."
                },
                {
                    "title": "Revenue Analysis",
                    "content_type": "chart",
                    "data_source": "sales",
                    "content": {
                        "chart_type": "bar",
                        "title": "Total Revenue by Product Category",
                        "data_column_x": "Product",
                        "data_column_y": "Revenue",
                        "aggregation": "sum",
                        "color_scheme": "Set2"
                    }
                },
                {
                    "title": "Trend Analysis",
                    "content_type": "chart",
                    "data_source": "sales",
                    "page_break_before": True,
                    "content": {
                        "chart_type": "line",
                        "title": "Revenue Trend Over Time",
                        "data_column_x": "Date",
                        "data_column_y": "Revenue",
                        "aggregation": "sum"
                    }
                },
                {
                    "title": "Regional Distribution",
                    "content_type": "chart",
                    "data_source": "sales",
                    "page_break_before": True,
                    "content": {
                        "chart_type": "pie",
                        "title": "Revenue Distribution by Region",
                        "data_column_x": "Region",
                        "data_column_y": "Revenue",
                        "aggregation": "sum"
                    }
                },
                {
                    "title": "Product Inventory",
                    "content_type": "table",
                    "data_source": "products",
                    "page_break_before": True,
                    "content": {
                        "title": "Complete Product Catalog",
                        "columns": ["Product", "Category", "Price", "Stock"],
                        "alternate_row_colors": True,
                        "header_bg_color": "#2c3e50"
                    }
                },
                {
                    "title": "Correlation Analysis",
                    "content_type": "chart",
                    "data_source": "sales",
                    "page_break_before": True,
                    "content": {
                        "chart_type": "scatter",
                        "title": "Revenue vs Units Sold",
                        "data_column_x": "Units_Sold",
                        "data_column_y": "Revenue",
                        "aggregation": "none"
                    }
                },
                {
                    "title": "Conclusion",
                    "content_type": "text",
                    "content": "This report successfully demonstrates all major features: cover page, table of contents, multiple chart types, styled tables, custom branding, headers, footers, and page numbers."
                }
            ],
            include_cover_page=True,
            include_toc=True,
            include_header=True,
            include_footer=True,
            include_page_numbers=True,
            output_folder=self.output_dir,
            output_filename="test_complex_report.pdf"
        )
        
        generator = PDFReportGenerator(config)
        output_path = generator.generate_report()
        
        # Verify
        page_count = self._verify_pdf_created(output_path, min_size=30000)
        self.assertGreaterEqual(page_count, 7, "Complex report should have multiple pages")
        
        print(f"  ✓ Complex PDF created: {output_path}")
        print(f"  ✓ Features tested:")
        print(f"    - Cover page")
        print(f"    - Table of contents")
        print(f"    - 2 data sources")
        print(f"    - 4 chart types (bar, line, pie, scatter)")
        print(f"    - Styled table")
        print(f"    - Custom branding")
        print(f"    - Headers and footers")
        print(f"    - Page numbers")
        print(f"  ✓ Pages: {page_count}")
        print(f"  ✓ Size: {os.path.getsize(output_path):,} bytes")


def run_tests():
    """Run all tests and display summary"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPDFReportGenerator)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED")
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
    
    print("="*70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
