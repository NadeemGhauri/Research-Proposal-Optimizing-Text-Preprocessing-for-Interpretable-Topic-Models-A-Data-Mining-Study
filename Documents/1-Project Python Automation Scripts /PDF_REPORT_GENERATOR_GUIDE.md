# PDF Report Generator - Comprehensive Guide

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Configuration](#configuration)
6. [Branding & Styling](#branding--styling)
7. [Charts & Visualizations](#charts--visualizations)
8. [Tables & Data](#tables--data)
9. [Document Structure](#document-structure)
10. [Batch Processing](#batch-processing)
11. [Examples](#examples)
12. [Troubleshooting](#troubleshooting)
13. [API Reference](#api-reference)

---

## Overview

The PDF Report Generator is a professional Python tool that creates publication-ready PDF reports with charts, tables, and custom branding. It uses ReportLab for PDF generation and Matplotlib for visualizations.

### Key Benefits
- ✅ **Professional Output** - Publication-quality PDFs with custom branding
- ✅ **Multi-Source Data** - Load from CSV, Excel, JSON, or APIs
- ✅ **Rich Visualizations** - 6 chart types with Matplotlib/Seaborn
- ✅ **Automatic TOC** - Generated table of contents with page links
- ✅ **Custom Templates** - Full control over colors, fonts, logos
- ✅ **Batch Processing** - Generate multiple reports automatically

### Use Cases
- 📊 **Business Reports** - Sales reports, financial statements, KPI dashboards
- 📈 **Analytics Reports** - Data analysis, trend reports, performance reviews
- 📋 **Executive Summaries** - Board presentations, investor reports
- 🎯 **Marketing Reports** - Campaign performance, ROI analysis
- 💼 **Client Deliverables** - Professional reports with your branding

---

## Features

### 1. Multiple Data Sources
- **CSV Files** - Standard comma-separated values
- **Excel Files** - .xlsx and .xls formats
- **JSON Files** - Structured JSON data
- **APIs** - (Extension ready)

### 2. Charts & Visualizations (6 Types)
- **Bar Charts** - Compare categories, sales by product
- **Line Charts** - Time series, trends over time
- **Pie Charts** - Proportions, market share
- **Scatter Plots** - Correlations, relationships
- **Heatmaps** - 2D density, correlation matrices
- **Box Plots** - Distributions, outliers

### 3. Professional Templates
- **Cover Page** - Title, subtitle, author, date, logo
- **Table of Contents** - Auto-generated with page links
- **Headers** - Logo, report title on every page
- **Footers** - Custom text, page numbers ("Page X of Y")
- **Page Numbers** - Automatic numbering (skip cover page)

### 4. Custom Branding
- **Colors** - Primary, secondary, accent colors (hex or RGB)
- **Fonts** - Custom fonts for title, headings, body
- **Logo** - Company logo in header and cover
- **Footer Text** - Custom confidentiality notices

### 5. Tables with Styling
- **Column Selection** - Choose specific columns to display
- **Row Limiting** - Show top N rows
- **Alternating Colors** - Striped rows for readability
- **Custom Headers** - Colored header backgrounds
- **Auto-sizing** - Automatic or fixed column widths

### 6. Batch Processing
- **Multiple Reports** - Generate many reports at once
- **Template Reuse** - Single config, multiple data sources
- **Automated Workflows** - Schedule with cron/Task Scheduler

---

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install reportlab pillow matplotlib seaborn pandas openpyxl
```

### Dependency Details
- **reportlab** (≥4.0.0) - PDF generation engine
- **pillow** (≥10.0.0) - Image handling for logos/charts
- **matplotlib** (≥3.7.0) - Chart generation
- **seaborn** (≥0.12.0) - Enhanced color palettes
- **pandas** (≥2.0.0) - Data manipulation
- **openpyxl** (≥3.1.0) - Excel file support

---

## Quick Start

### 1. Command Line Usage

**Generate report from config:**
```bash
python pdf_report_generator.py --config config/pdf_report_sales.json
```

**Specify output folder:**
```bash
python pdf_report_generator.py \
  --config config/report.json \
  --output ./custom_reports
```

### 2. Python Module Usage

```python
from pdf_report_generator import PDFReportGenerator, ReportConfig

# Create configuration
config = ReportConfig(
    title="Monthly Sales Report",
    data_sources=[
        {"name": "sales", "path": "data/sales.csv", "type": "csv"}
    ],
    sections=[
        {
            "title": "Revenue Analysis",
            "content_type": "chart",
            "data_source": "sales",
            "content": {
                "chart_type": "bar",
                "title": "Revenue by Product",
                "data_column_x": "Product",
                "data_column_y": "Revenue",
                "aggregation": "sum"
            }
        }
    ],
    output_folder="./reports",
    output_filename="monthly_sales.pdf"
)

# Generate report
generator = PDFReportGenerator(config)
output_path = generator.generate_report()
print(f"Report saved: {output_path}")
```

### 3. Minimal Example

**Create `simple_report.json`:**
```json
{
  "title": "Simple Sales Report",
  "data_sources": [
    {"name": "sales", "path": "data/sales_data.csv", "type": "csv"}
  ],
  "sections": [
    {
      "title": "Executive Summary",
      "content_type": "text",
      "content": "This report summarizes our sales performance for Q4 2024."
    },
    {
      "title": "Sales by Product",
      "content_type": "chart",
      "data_source": "sales",
      "content": {
        "chart_type": "bar",
        "title": "Total Revenue by Product",
        "data_column_x": "Product",
        "data_column_y": "Revenue",
        "aggregation": "sum"
      }
    }
  ]
}
```

**Generate:**
```bash
python pdf_report_generator.py --config simple_report.json
```

---

## Configuration

### Configuration File Structure

```json
{
  "title": "Report Title",
  "subtitle": "Report Subtitle",
  "author": "Author Name",
  "subject": "Report Subject",
  "date": "November 21, 2024",
  
  "data_sources": [ /* Data source configs */ ],
  "sections": [ /* Section configs */ ],
  "branding": { /* Branding config */ },
  
  "page_size": "letter",
  "orientation": "portrait",
  
  "include_cover_page": true,
  "include_toc": true,
  "include_header": true,
  "include_footer": true,
  "include_page_numbers": true,
  
  "output_folder": "./reports",
  "output_filename": "report.pdf"
}
```

### Report Metadata

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `title` | string | ✅ | - | Report title |
| `subtitle` | string | ❌ | `""` | Subtitle (cover page) |
| `author` | string | ❌ | `""` | Author name |
| `subject` | string | ❌ | `""` | PDF subject metadata |
| `date` | string | ❌ | Today's date | Report date |

### Page Settings

| Field | Type | Default | Options | Description |
|-------|------|---------|---------|-------------|
| `page_size` | string | `"letter"` | `letter`, `a4`, `legal` | Page size |
| `orientation` | string | `"portrait"` | `portrait`, `landscape` | Page orientation |

### Document Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `include_cover_page` | boolean | `true` | Generate cover page |
| `include_toc` | boolean | `true` | Generate table of contents |
| `include_header` | boolean | `true` | Show header on pages |
| `include_footer` | boolean | `true` | Show footer on pages |
| `include_page_numbers` | boolean | `true` | Show page numbers |
| `toc_title` | string | `"Table of Contents"` | TOC heading |
| `cover_subtitle` | string | `""` | Additional cover text |
| `cover_image` | string | `null` | Path to cover image |

### Data Sources Configuration

**Format:**
```json
"data_sources": [
  {
    "name": "sales",
    "path": "data/sales_data.csv",
    "type": "csv"
  },
  {
    "name": "products",
    "path": "data/products.xlsx",
    "type": "excel"
  }
]
```

**Fields:**
- `name` - Identifier for this data source
- `path` - File path (relative or absolute)
- `type` - Data type: `csv`, `excel`, `json`

### Sections Configuration

Each section has:
- `title` - Section heading
- `content_type` - Type: `text`, `chart`, `table`
- `content` - Content configuration (depends on type)
- `data_source` - Data source name (for charts/tables)
- `page_break_before` - Insert page break before section
- `page_break_after` - Insert page break after section

**Example:**
```json
"sections": [
  {
    "title": "Introduction",
    "content_type": "text",
    "content": "This report provides an overview..."
  },
  {
    "title": "Sales Analysis",
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
]
```

---

## Branding & Styling

### Branding Configuration

```json
"branding": {
  "primary_color": "#2c3e50",
  "secondary_color": "#3498db",
  "accent_color": "#e74c3c",
  "text_color": "#34495e",
  
  "logo_path": "assets/logo.png",
  "logo_width": 144,
  "logo_height": 36,
  
  "title_font": "Helvetica-Bold",
  "heading_font": "Helvetica-Bold",
  "body_font": "Helvetica",
  
  "title_size": 28,
  "heading1_size": 20,
  "heading2_size": 16,
  "heading3_size": 12,
  "body_size": 11,
  
  "company_name": "ABC Corporation",
  "report_footer": "Confidential - Internal Use Only"
}
```

### Color Configuration

**Hex Colors:**
```json
"primary_color": "#1f77b4"
```

**RGB Tuples:**
```json
"primary_color": [31, 119, 180]
```

### Font Options

**Available Fonts:**
- `Helvetica` - Sans-serif, clean
- `Helvetica-Bold` - Bold sans-serif
- `Times-Roman` - Serif, classic
- `Times-Bold` - Bold serif
- `Courier` - Monospace

### Logo Configuration

**Logo Settings:**
- `logo_path` - Path to logo image (PNG, JPG)
- `logo_width` - Width in points (72 points = 1 inch)
- `logo_height` - Height in points
- Logo appears in: Header (small) and Cover Page (large)

**Example:**
```json
"logo_path": "assets/company_logo.png",
"logo_width": 144,  // 2 inches
"logo_height": 36   // 0.5 inches
```

---

## Charts & Visualizations

### Chart Configuration

```json
{
  "chart_type": "bar",
  "title": "Chart Title",
  "data_column_x": "Category",
  "data_column_y": "Value",
  "data_columns": ["Series1", "Series2"],
  "aggregation": "sum",
  "width": 432,
  "height": 288,
  "color_scheme": "Set2",
  "show_legend": true,
  "show_grid": true,
  "xlabel": "X-axis Label",
  "ylabel": "Y-axis Label"
}
```

### Chart Types

#### 1. Bar Chart

**Use Case:** Compare categories

**Configuration:**
```json
{
  "chart_type": "bar",
  "title": "Revenue by Product",
  "data_column_x": "Product",
  "data_column_y": "Revenue",
  "aggregation": "sum",
  "width": 432,
  "height": 288,
  "color_scheme": "Set2",
  "show_grid": true,
  "ylabel": "Revenue ($)"
}
```

**Aggregation Options:**
- `sum` - Total values
- `count` - Count records
- `avg` - Average values
- `min` - Minimum value
- `max` - Maximum value
- `none` - No aggregation

#### 2. Line Chart

**Use Case:** Time series, trends

**Configuration:**
```json
{
  "chart_type": "line",
  "title": "Sales Trend Over Time",
  "data_column_x": "Date",
  "data_column_y": "Revenue",
  "aggregation": "sum",
  "show_grid": true
}
```

**Multi-Series:**
```json
{
  "chart_type": "line",
  "title": "Revenue by Region",
  "data_column_x": "Date",
  "data_columns": ["East", "West", "North", "South"],
  "show_legend": true
}
```

#### 3. Pie Chart

**Use Case:** Proportions, market share

**Configuration:**
```json
{
  "chart_type": "pie",
  "title": "Market Share by Region",
  "data_column_x": "Region",
  "data_column_y": "Revenue",
  "aggregation": "sum",
  "color_scheme": "Set3"
}
```

#### 4. Scatter Plot

**Use Case:** Correlations, relationships

**Configuration:**
```json
{
  "chart_type": "scatter",
  "title": "Revenue vs Units Sold",
  "data_column_x": "Units_Sold",
  "data_column_y": "Revenue",
  "aggregation": "none",
  "show_grid": true,
  "xlabel": "Units Sold",
  "ylabel": "Revenue ($)"
}
```

#### 5. Heatmap

**Use Case:** 2D density, correlation

**Configuration:**
```json
{
  "chart_type": "heatmap",
  "title": "Sales by Region and Product",
  "data_column_x": "Product",
  "data_column_y": "Region",
  "data_column_z": "Revenue",
  "aggregation": "sum",
  "color_scheme": "YlOrRd"
}
```

#### 6. Box Plot

**Use Case:** Distributions, outliers

**Configuration:**
```json
{
  "chart_type": "box",
  "title": "Price Distribution by Category",
  "data_column_x": "Category",
  "data_column_y": "Price",
  "data_columns": ["Electronics", "Furniture", "Clothing"]
}
```

### Color Schemes

**Matplotlib/Seaborn Palettes:**
- `Set1`, `Set2`, `Set3` - Categorical colors
- `viridis`, `plasma`, `inferno` - Perceptually uniform
- `YlOrRd`, `YlGnBu`, `RdYlGn` - Sequential/diverging
- `deep`, `muted`, `pastel` - Seaborn palettes

---

## Tables & Data

### Table Configuration

```json
{
  "title": "Table Title",
  "columns": ["Col1", "Col2", "Col3"],
  "max_rows": 20,
  "show_index": false,
  "alternate_row_colors": true,
  "header_bg_color": "#2c3e50",
  "header_text_color": "#FFFFFF",
  "col_widths": [2.0, 1.5, 1.5]
}
```

### Table Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `title` | string | - | Table heading |
| `columns` | array | All columns | Columns to display |
| `max_rows` | number | All rows | Limit number of rows |
| `show_index` | boolean | `false` | Show DataFrame index |
| `alternate_row_colors` | boolean | `true` | Striped rows |
| `header_bg_color` | string | Primary color | Header background |
| `header_text_color` | string | White | Header text color |
| `col_widths` | array | Auto | Column widths (inches) |

### Example: Top 10 Table

```json
{
  "title": "Section Title",
  "content_type": "table",
  "data_source": "sales",
  "content": {
    "title": "Top 10 Products by Revenue",
    "columns": ["Product", "Region", "Revenue", "Units_Sold"],
    "max_rows": 10,
    "alternate_row_colors": true,
    "header_bg_color": "#34495e"
  }
}
```

### Example: Full Data Table

```json
{
  "content_type": "table",
  "data_source": "sales",
  "content": {
    "title": "Complete Sales Data",
    "show_index": true,
    "col_widths": [0.5, 2.0, 1.5, 1.5, 1.5, 1.0]
  }
}
```

---

## Document Structure

### Cover Page

**Automatically includes:**
- Company logo (if provided)
- Cover image (if provided)
- Report title (large, centered)
- Subtitle (if provided)
- Cover subtitle (if provided)
- Prepared by (author name)
- Date
- Company name

**Customization:**
```json
{
  "title": "Annual Sales Report 2024",
  "subtitle": "Comprehensive Performance Analysis",
  "author": "Analytics Team",
  "cover_subtitle": "Fiscal Year 2024 - Global Operations",
  "cover_image": "assets/cover_graphic.png",
  "branding": {
    "logo_path": "assets/logo.png",
    "company_name": "ABC Corporation"
  }
}
```

### Table of Contents

**Features:**
- Auto-generated from section titles
- Clickable page links
- Two-level hierarchy (H1, H2)
- Page numbers aligned right

**Configuration:**
```json
{
  "include_toc": true,
  "toc_title": "Table of Contents"
}
```

### Headers

**Includes:**
- Company logo (left, small)
- Report title (right)
- Horizontal line separator
- Skipped on cover page

**Customization:**
```json
{
  "include_header": true,
  "branding": {
    "logo_path": "assets/logo.png"
  }
}
```

### Footers

**Includes:**
- Custom footer text (left)
- Page numbers (right, "Page X of Y")
- Horizontal line separator
- Skipped on cover page

**Customization:**
```json
{
  "include_footer": true,
  "include_page_numbers": true,
  "branding": {
    "report_footer": "Confidential - Q4 2024 Report"
  }
}
```

### Page Breaks

**Insert page breaks:**
```json
{
  "title": "New Section",
  "page_break_before": true,
  "page_break_after": false,
  "content_type": "text",
  "content": "This section starts on a new page."
}
```

---

## Batch Processing

### Batch Mode Concept

Generate multiple reports from the same template with different data sources.

### Configuration

```json
{
  "title": "Regional Sales Report - {region}",
  "batch_mode": true,
  "batch_data_sources": [
    "data/sales_east.csv",
    "data/sales_west.csv",
    "data/sales_north.csv",
    "data/sales_south.csv"
  ],
  "sections": [ /* Same sections for all reports */ ]
}
```

### Python Script for Batch Processing

```python
from pdf_report_generator import PDFReportGenerator, ReportConfig
import os

# Define regions
regions = ["East", "West", "North", "South"]

for region in regions:
    config = ReportConfig(
        title=f"{region} Region Sales Report",
        data_sources=[
            {
                "name": "sales",
                "path": f"data/sales_{region.lower()}.csv",
                "type": "csv"
            }
        ],
        sections=[
            {
                "title": "Overview",
                "content_type": "text",
                "content": f"This report covers {region} region performance."
            },
            {
                "title": "Revenue Analysis",
                "content_type": "chart",
                "data_source": "sales",
                "content": {
                    "chart_type": "bar",
                    "title": "Revenue by Product",
                    "data_column_x": "Product",
                    "data_column_y": "Revenue",
                    "aggregation": "sum"
                }
            }
        ],
        output_folder="./reports",
        output_filename=f"sales_report_{region.lower()}.pdf"
    )
    
    generator = PDFReportGenerator(config)
    output_path = generator.generate_report()
    print(f"✅ Generated: {output_path}")
```

### Scheduled Batch Processing

**Using cron (Linux/Mac):**
```bash
# Daily at 8 AM
0 8 * * * cd /path/to/project && python batch_reports.py
```

**Using Task Scheduler (Windows):**
- Create batch script: `batch_reports.bat`
- Schedule task in Task Scheduler
- Set trigger (daily, weekly, etc.)

---

## Examples

### Example 1: Sales Report

**Full configuration:** `config/pdf_report_sales.json`

**Features:**
- Cover page with branding
- Table of contents
- 8 sections (text, charts, table)
- Custom colors and fonts
- Headers and footers

**Generate:**
```bash
python pdf_report_generator.py --config config/pdf_report_sales.json
```

**Result:** 136KB professional PDF with 4 charts, 1 table, professional styling

### Example 2: Financial Report

```json
{
  "title": "Quarterly Financial Report",
  "subtitle": "Q4 2024",
  "author": "Finance Department",
  "data_sources": [
    {"name": "financials", "path": "data/financials.csv", "type": "csv"}
  ],
  "branding": {
    "primary_color": "#1a5490",
    "company_name": "Finance Corp",
    "report_footer": "Confidential Financial Information"
  },
  "sections": [
    {
      "title": "Revenue Breakdown",
      "content_type": "chart",
      "data_source": "financials",
      "content": {
        "chart_type": "pie",
        "title": "Revenue by Division",
        "data_column_x": "Division",
        "data_column_y": "Revenue",
        "aggregation": "sum"
      }
    },
    {
      "title": "Expense Trends",
      "content_type": "chart",
      "data_source": "financials",
      "content": {
        "chart_type": "line",
        "title": "Monthly Expenses",
        "data_column_x": "Month",
        "data_column_y": "Expenses",
        "aggregation": "sum"
      }
    }
  ]
}
```

### Example 3: Product Catalog

```json
{
  "title": "Product Catalog 2024",
  "include_toc": true,
  "data_sources": [
    {"name": "products", "path": "data/products.xlsx", "type": "excel"}
  ],
  "sections": [
    {
      "title": "Product Inventory",
      "content_type": "table",
      "data_source": "products",
      "content": {
        "title": "Complete Product List",
        "columns": ["SKU", "Name", "Category", "Price", "Stock"],
        "alternate_row_colors": true
      }
    },
    {
      "title": "Price Distribution",
      "content_type": "chart",
      "data_source": "products",
      "content": {
        "chart_type": "box",
        "title": "Price by Category",
        "data_column_x": "Category",
        "data_column_y": "Price"
      }
    }
  ]
}
```

---

## Troubleshooting

### Common Issues

#### 1. "Data source not found"

**Problem:** Cannot load data file

**Solutions:**
- Check file path is correct (relative or absolute)
- Verify file exists: `ls data/sales_data.csv`
- Check file permissions
- Use absolute path: `/full/path/to/data.csv`

#### 2. "Error creating chart"

**Problem:** Chart generation fails

**Solutions:**
- Verify column names match data (case-sensitive)
- Check aggregation is appropriate for data type
- Ensure numeric columns for numeric charts
- Print data columns:
```python
import pandas as pd
df = pd.read_csv('data.csv')
print(df.columns.tolist())
```

#### 3. Logo not appearing

**Problem:** Logo missing in header/cover

**Solutions:**
- Check `logo_path` is correct
- Verify image file exists
- Use PNG or JPG format
- Check file permissions
- Try absolute path

#### 4. PDF file size too large

**Problem:** Generated PDF is very large

**Solutions:**
- Reduce chart sizes (width/height)
- Limit table rows (`max_rows`)
- Optimize logo image (compress, resize)
- Use fewer sections/charts

#### 5. Text encoding errors

**Problem:** Special characters not displaying

**Solutions:**
- Use UTF-8 encoding for data files
- Avoid special characters in config JSON
- Use HTML entities: `&amp;`, `&lt;`, `&gt;`

#### 6. Charts look distorted

**Problem:** Charts appear stretched or squished

**Solutions:**
- Adjust `width` and `height` proportionally
- Standard ratio: width=432, height=288 (3:2)
- For square charts: width=360, height=360
- Test different sizes

#### 7. Page breaks in wrong places

**Problem:** Content split across pages awkwardly

**Solutions:**
- Use `page_break_before: true` for sections
- Reduce table row count
- Split large sections
- Use `KeepTogether` (already implemented for tables)

---

## API Reference

### ReportConfig

**Description:** Configuration dataclass for PDF reports

**Fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `data_sources` | List[Dict] | `[]` | Data source configurations |
| `title` | str | `"Professional Report"` | Report title |
| `subtitle` | str | `""` | Report subtitle |
| `author` | str | `""` | Author name |
| `subject` | str | `""` | PDF subject metadata |
| `date` | str | Today | Report date |
| `page_size` | str | `"letter"` | Page size |
| `orientation` | str | `"portrait"` | Page orientation |
| `sections` | List[Dict] | `[]` | Report sections |
| `branding` | Dict | `None` | Branding configuration |
| `include_toc` | bool | `True` | Include TOC |
| `toc_title` | str | `"Table of Contents"` | TOC heading |
| `include_cover_page` | bool | `True` | Include cover |
| `cover_subtitle` | str | `""` | Cover subtitle |
| `cover_image` | str | `None` | Cover image path |
| `include_header` | bool | `True` | Include header |
| `include_footer` | bool | `True` | Include footer |
| `include_page_numbers` | bool | `True` | Include page numbers |
| `output_folder` | str | `"./reports"` | Output directory |
| `output_filename` | str | `"report.pdf"` | Output filename |
| `batch_mode` | bool | `False` | Batch processing |
| `batch_data_sources` | List[str] | `[]` | Batch data paths |

### PDFReportGenerator

**Description:** Main class for PDF report generation

#### Constructor

```python
PDFReportGenerator(config: ReportConfig)
```

**Parameters:**
- `config` - ReportConfig object

**Example:**
```python
from pdf_report_generator import PDFReportGenerator, ReportConfig

config = ReportConfig(title="My Report")
generator = PDFReportGenerator(config)
```

#### Methods

##### `load_data() -> None`

Load all configured data sources

**Example:**
```python
generator.load_data()
print(f"Loaded {len(generator.data)} data sources")
```

##### `create_cover_page() -> None`

Create report cover page with logo and metadata

**Called automatically by:** `generate_report()`

##### `create_toc() -> None`

Create table of contents with section links

**Called automatically by:** `generate_report()`

##### `create_chart(chart_config, data) -> Optional[Image]`

Create chart and return as reportlab Image

**Parameters:**
- `chart_config` - ChartConfig object
- `data` - pandas DataFrame

**Returns:** reportlab Image flowable or None

**Example:**
```python
from pdf_report_generator import ChartConfig

chart_config = ChartConfig(
    chart_type="bar",
    title="Sales Chart",
    data_column_x="Product",
    data_column_y="Revenue",
    aggregation="sum"
)

img = generator.create_chart(chart_config, df)
```

##### `create_table(table_config, data) -> Optional[KeepTogether]`

Create styled table

**Parameters:**
- `table_config` - TableConfig object
- `data` - pandas DataFrame

**Returns:** reportlab KeepTogether flowable or None

##### `generate_report() -> str`

Generate complete PDF report

**Returns:** Output file path

**Example:**
```python
output_path = generator.generate_report()
print(f"Report saved: {output_path}")
```

### Utility Functions

#### `load_config(config_path: str) -> ReportConfig`

Load configuration from JSON file

**Parameters:**
- `config_path` - Path to JSON config file

**Returns:** ReportConfig object

**Example:**
```python
from pdf_report_generator import load_config

config = load_config('config/report.json')
print(config.title)
```

---

## Best Practices

### Configuration

1. **Use descriptive titles** - Clear section headings
2. **Organize logically** - Introduction → Analysis → Conclusion
3. **Limit sections** - 5-10 sections for clarity
4. **Break up text** - Use charts and tables to visualize
5. **Consistent branding** - Use company colors throughout

### Data Preparation

1. **Clean data first** - Remove nulls, fix types
2. **Aggregate appropriately** - Sum for totals, avg for rates
3. **Sort data** - Order by relevance (e.g., top 10)
4. **Format dates** - Use consistent date format
5. **Round numbers** - Use reasonable precision

### Chart Design

1. **Choose appropriate type** - Bar for categories, line for trends
2. **Use descriptive labels** - Clear axis labels and titles
3. **Limit data points** - Avoid overcrowded charts
4. **Color wisely** - Use color schemes that work in print
5. **Test in grayscale** - Ensure readability in B&W

### Table Design

1. **Select relevant columns** - Don't show everything
2. **Limit rows** - Use `max_rows` for large datasets
3. **Use alternating colors** - Improves readability
4. **Format numbers** - Currency, percentages, decimals
5. **Sort meaningfully** - Descending by key metric

### Performance

1. **Optimize images** - Compress logos and cover images
2. **Limit chart sizes** - Balance quality and file size
3. **Reduce table rows** - Show top N, link to full data
4. **Reuse configurations** - Template for multiple reports
5. **Batch efficiently** - Process multiple reports at once

---

## Next Steps

### Learn More
- Read ReportLab documentation: https://www.reportlab.com/docs/
- Explore Matplotlib gallery: https://matplotlib.org/stable/gallery/
- Review example configs in `config/` folder

### Get Help
- Check [Troubleshooting](#troubleshooting) section
- Review [Examples](#examples) for common use cases
- Examine test files for code samples

---

**Last Updated:** 2024-11-21  
**Version:** 1.0.0  
**Author:** PDF Report Generator Team
