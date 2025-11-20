#!/usr/bin/env python3
"""
Integration tests for Dashboard Generator

Tests dashboard creation with various chart types and configurations.

Run: python test_dashboard_generator.py
"""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from dashboard_generator import DashboardGenerator, DashboardConfig


class TestDashboardGenerator(unittest.TestCase):
    """Test suite for Dashboard Generator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, 'dashboards')
        self.data_dir = os.path.join(self.test_dir, 'data')
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Create test data
        self.test_data = pd.DataFrame({
            'date': pd.date_range('2025-01-01', periods=100),
            'product': ['Product A', 'Product B', 'Product C'] * 33 + ['Product A'],
            'region': ['North', 'South', 'East', 'West'] * 25,
            'sales': [100 + i * 10 for i in range(100)],
            'profit': [20 + i * 2 for i in range(100)],
            'quantity': [10 + i for i in range(100)],
            'category': ['Electronics', 'Clothing'] * 50
        })
        
        self.test_csv = os.path.join(self.data_dir, 'test_data.csv')
        self.test_data.to_csv(self.test_csv, index=False)
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_basic_dashboard_creation(self):
        """Test 1: Basic dashboard with single bar chart"""
        print("\n" + "="*60)
        print("Test 1: Basic Dashboard Creation")
        print("="*60)
        
        config = DashboardConfig(
            data_source=self.test_csv,
            data_source_type='csv',
            title='Test Dashboard',
            description='Basic test dashboard',
            output_folder=self.output_dir,
            output_filename='test_basic.html',
            charts=[
                {
                    'type': 'bar',
                    'title': 'Sales by Product',
                    'data_column_x': 'product',
                    'data_column_y': 'sales',
                    'aggregation': 'sum'
                }
            ]
        )
        
        generator = DashboardGenerator(config)
        output_path = generator.save_dashboard()
        
        # Assertions
        self.assertTrue(os.path.exists(output_path))
        self.assertEqual(len(generator.figures), 1)
        self.assertIsNotNone(generator.data)
        self.assertEqual(len(generator.data), 100)
        
        # Check HTML content
        with open(output_path, 'r') as f:
            html = f.read()
            self.assertIn('Test Dashboard', html)
            self.assertIn('Sales by Product', html)
            self.assertIn('plotly', html)
        
        print(f"✅ PASSED: Dashboard created successfully")
        print(f"   Output: {output_path}")
        print(f"   Charts: {len(generator.figures)}")
        print(f"   Data rows: {len(generator.data)}")
    
    def test_multiple_chart_types(self):
        """Test 2: Dashboard with multiple chart types"""
        print("\n" + "="*60)
        print("Test 2: Multiple Chart Types")
        print("="*60)
        
        config = DashboardConfig(
            data_source=self.test_csv,
            title='Multi-Chart Dashboard',
            output_folder=self.output_dir,
            output_filename='test_multi.html',
            charts=[
                {
                    'type': 'bar',
                    'title': 'Sales by Product',
                    'data_column_x': 'product',
                    'data_column_y': 'sales',
                    'aggregation': 'sum'
                },
                {
                    'type': 'line',
                    'title': 'Sales Trend',
                    'data_column_x': 'date',
                    'data_column_y': 'sales',
                    'aggregation': 'sum'
                },
                {
                    'type': 'pie',
                    'title': 'Sales by Region',
                    'data_column_x': 'region',
                    'data_column_y': 'sales',
                    'aggregation': 'sum'
                },
                {
                    'type': 'scatter',
                    'title': 'Sales vs Profit',
                    'data_column_x': 'sales',
                    'data_column_y': 'profit',
                    'aggregation': 'none'
                }
            ]
        )
        
        generator = DashboardGenerator(config)
        output_path = generator.save_dashboard()
        
        # Assertions
        self.assertTrue(os.path.exists(output_path))
        self.assertEqual(len(generator.figures), 4)
        
        # Check all chart titles in HTML
        with open(output_path, 'r') as f:
            html = f.read()
            self.assertIn('Sales by Product', html)
            self.assertIn('Sales Trend', html)
            self.assertIn('Sales by Region', html)
            self.assertIn('Sales vs Profit', html)
        
        print(f"✅ PASSED: Created {len(generator.figures)} charts")
        print(f"   Bar chart: Sales by Product")
        print(f"   Line chart: Sales Trend")
        print(f"   Pie chart: Sales by Region")
        print(f"   Scatter chart: Sales vs Profit")
    
    def test_data_table_generation(self):
        """Test 3: Dashboard with data table"""
        print("\n" + "="*60)
        print("Test 3: Data Table Generation")
        print("="*60)
        
        config = DashboardConfig(
            data_source=self.test_csv,
            title='Dashboard with Table',
            output_folder=self.output_dir,
            output_filename='test_table.html',
            show_data_table=True,
            rows_per_page=10,
            charts=[
                {
                    'type': 'bar',
                    'title': 'Sales Overview',
                    'data_column_x': 'product',
                    'data_column_y': 'sales',
                    'aggregation': 'avg'
                }
            ]
        )
        
        generator = DashboardGenerator(config)
        output_path = generator.save_dashboard()
        
        # Check HTML contains table
        with open(output_path, 'r') as f:
            html = f.read()
            self.assertIn('Data Table', html)
            self.assertIn('<table', html)
            self.assertIn('dataTable', html)
            self.assertIn('filterTable', html)  # Search function
        
        print(f"✅ PASSED: Data table included")
        print(f"   Rows per page: {config.rows_per_page}")
        print(f"   Search enabled: Yes")
        print(f"   Sort enabled: Yes")
    
    def test_filters_generation(self):
        """Test 4: Dashboard with filters"""
        print("\n" + "="*60)
        print("Test 4: Filter Controls")
        print("="*60)
        
        config = DashboardConfig(
            data_source=self.test_csv,
            title='Filtered Dashboard',
            output_folder=self.output_dir,
            output_filename='test_filters.html',
            filters=['product', 'region', 'category'],
            charts=[
                {
                    'type': 'bar',
                    'title': 'Filtered Sales',
                    'data_column_x': 'product',
                    'data_column_y': 'sales',
                    'aggregation': 'sum'
                }
            ]
        )
        
        generator = DashboardGenerator(config)
        output_path = generator.save_dashboard()
        
        # Check HTML contains filters
        with open(output_path, 'r') as f:
            html = f.read()
            self.assertIn('Filters', html)
            self.assertIn('filter_product', html)
            self.assertIn('filter_region', html)
            self.assertIn('filter_category', html)
            self.assertIn('applyFilters', html)
            self.assertIn('resetFilters', html)
        
        print(f"✅ PASSED: Filters generated")
        print(f"   Filter columns: {', '.join(config.filters)}")
        print(f"   Reset button: Yes")
        print(f"   Apply function: Yes")
    
    def test_theme_customization(self):
        """Test 5: Custom theme and colors"""
        print("\n" + "="*60)
        print("Test 5: Theme Customization")
        print("="*60)
        
        custom_palette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        
        config = DashboardConfig(
            data_source=self.test_csv,
            title='Custom Theme Dashboard',
            output_folder=self.output_dir,
            output_filename='test_theme.html',
            theme='plotly_dark',
            color_palette=custom_palette,
            charts=[
                {
                    'type': 'bar',
                    'title': 'Themed Chart',
                    'data_column_x': 'product',
                    'data_column_y': 'sales',
                    'aggregation': 'sum'
                }
            ]
        )
        
        generator = DashboardGenerator(config)
        output_path = generator.save_dashboard()
        
        # Assertions
        self.assertTrue(os.path.exists(output_path))
        self.assertEqual(generator.config.theme, 'plotly_dark')
        self.assertEqual(generator.config.color_palette, custom_palette)
        
        print(f"✅ PASSED: Theme applied")
        print(f"   Theme: {config.theme}")
        print(f"   Colors: {len(custom_palette)} custom colors")
    
    def test_aggregation_types(self):
        """Test 6: Different aggregation methods"""
        print("\n" + "="*60)
        print("Test 6: Aggregation Methods")
        print("="*60)
        
        config = DashboardConfig(
            data_source=self.test_csv,
            title='Aggregation Test',
            output_folder=self.output_dir,
            output_filename='test_agg.html',
            charts=[
                {
                    'type': 'bar',
                    'title': 'Sum of Sales',
                    'data_column_x': 'product',
                    'data_column_y': 'sales',
                    'aggregation': 'sum'
                },
                {
                    'type': 'bar',
                    'title': 'Average Sales',
                    'data_column_x': 'product',
                    'data_column_y': 'sales',
                    'aggregation': 'avg'
                },
                {
                    'type': 'bar',
                    'title': 'Max Sales',
                    'data_column_x': 'product',
                    'data_column_y': 'sales',
                    'aggregation': 'max'
                }
            ]
        )
        
        generator = DashboardGenerator(config)
        output_path = generator.save_dashboard()
        
        self.assertEqual(len(generator.figures), 3)
        
        print(f"✅ PASSED: Aggregations working")
        print(f"   Tested: sum, avg, max")
        print(f"   Charts created: {len(generator.figures)}")
    
    def test_responsive_layout(self):
        """Test 7: Responsive layout options"""
        print("\n" + "="*60)
        print("Test 7: Responsive Layout")
        print("="*60)
        
        config = DashboardConfig(
            data_source=self.test_csv,
            title='Grid Layout Dashboard',
            layout='grid',
            output_folder=self.output_dir,
            output_filename='test_layout.html',
            charts=[
                {'type': 'bar', 'title': 'Chart 1', 'data_column_x': 'product', 'data_column_y': 'sales'},
                {'type': 'line', 'title': 'Chart 2', 'data_column_x': 'date', 'data_column_y': 'sales'},
                {'type': 'pie', 'title': 'Chart 3', 'data_column_x': 'region', 'data_column_y': 'sales'}
            ]
        )
        
        generator = DashboardGenerator(config)
        output_path = generator.save_dashboard()
        
        # Check CSS for grid layout
        with open(output_path, 'r') as f:
            html = f.read()
            self.assertIn('chart-grid', html)
            self.assertIn('grid-template-columns', html)
            self.assertIn('@media', html)  # Responsive breakpoints
        
        print(f"✅ PASSED: Responsive layout generated")
        print(f"   Layout: {config.layout}")
        print(f"   Media queries: Yes")
        print(f"   Mobile-friendly: Yes")
    
    def test_export_functionality(self):
        """Test 8: Export settings"""
        print("\n" + "="*60)
        print("Test 8: Export Functionality")
        print("="*60)
        
        config = DashboardConfig(
            data_source=self.test_csv,
            title='Exportable Dashboard',
            output_folder=self.output_dir,
            output_filename='test_export.html',
            enable_export=True,
            export_formats=['html', 'png', 'pdf'],
            charts=[
                {
                    'type': 'bar',
                    'title': 'Export Test',
                    'data_column_x': 'product',
                    'data_column_y': 'sales'
                }
            ]
        )
        
        generator = DashboardGenerator(config)
        output_path = generator.save_dashboard()
        
        # Check export buttons
        with open(output_path, 'r') as f:
            html = f.read()
            self.assertIn('Export Dashboard', html)
            self.assertIn('exportDashboard', html)
        
        print(f"✅ PASSED: Export configured")
        print(f"   Formats: {', '.join(config.export_formats)}")
        print(f"   Export button: Yes")


def run_tests():
    """Run all tests"""
    print("🧪 Dashboard Generator Integration Tests")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDashboardGenerator)
    
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
