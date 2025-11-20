# Dashboard Generator - Comprehensive Guide

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Configuration](#configuration)
6. [Chart Types](#chart-types)
7. [Filters & Interactivity](#filters--interactivity)
8. [Themes & Styling](#themes--styling)
9. [Export Options](#export-options)
10. [Auto-Refresh](#auto-refresh)
11. [Responsive Design](#responsive-design)
12. [Advanced Usage](#advanced-usage)
13. [Examples](#examples)
14. [Troubleshooting](#troubleshooting)
15. [API Reference](#api-reference)

---

## Overview

The Dashboard Generator is a powerful Python tool that creates **interactive HTML dashboards** from your data using Plotly. It generates fully self-contained dashboards with dynamic charts, filters, data tables, and export capabilities - no server required!

### Key Benefits
- ✅ **No coding required** - Configure dashboards using JSON
- ✅ **Interactive charts** - Zoom, pan, hover tooltips with Plotly
- ✅ **Responsive design** - Works on desktop, tablet, and mobile
- ✅ **Self-contained** - Single HTML file with embedded charts
- ✅ **Multiple data sources** - CSV, Excel, JSON support
- ✅ **Export ready** - Save as PNG, PDF, or HTML
- ✅ **Auto-refresh** - Keep dashboards up-to-date automatically

### Use Cases
- 📊 **Business Intelligence** - Sales dashboards, KPI tracking, performance monitoring
- 📈 **Data Analysis** - Exploratory data analysis, trend visualization
- 📋 **Reporting** - Automated report generation, executive summaries
- 🎯 **Marketing Analytics** - Campaign performance, conversion funnels
- 💰 **Financial Dashboards** - Revenue tracking, budget analysis
- 🏭 **Operations** - Inventory tracking, production metrics

---

## Features

### 1. Multiple Chart Types (8 types)
- **Bar Charts** - Compare categories, sales by product
- **Line Charts** - Time series, trends over time
- **Pie Charts** - Proportions, market share
- **Scatter Plots** - Correlations, X vs Y relationships
- **Area Charts** - Cumulative trends, stacked areas
- **Heatmaps** - 2D density, correlation matrices
- **Box Plots** - Distributions, outlier detection
- **Histograms** - Frequency distributions, data ranges

### 2. Filter & Sort Capabilities
- **Dynamic Filters** - Dropdown filters for any column
- **Multi-Select** - Filter by multiple values
- **Reset Filters** - Clear all filters with one click
- **Search** - Full-text search in data tables
- **Column Sort** - Click column headers to sort

### 3. Responsive Design
- **Grid Layout** - Automatic chart arrangement
- **Mobile Friendly** - Adapts to screen size (desktop, tablet, mobile)
- **Touch Support** - Swipe and pinch gestures on mobile
- **Flexible Sizing** - Charts resize based on viewport

### 4. Export Functionality
- **HTML Export** - Save complete dashboard
- **PNG Export** - Static images of charts (1200x800)
- **PDF Export** - Print-ready documents
- **CSV Export** - Download data table as CSV

### 5. Auto-Refresh
- **Automatic Updates** - Reload data at intervals (e.g., every 5 minutes)
- **Configurable Interval** - Set refresh frequency (seconds)
- **Live Dashboards** - Keep charts up-to-date without manual refresh

### 6. Customizable Themes
- **Pre-built Themes** - plotly, plotly_white, plotly_dark, ggplot2, seaborn
- **Custom Colors** - Define your own color palette
- **Branding** - Match your company colors
- **Dark Mode** - Reduce eye strain with dark themes

### 7. Data Aggregation
- **Sum** - Total revenue, quantities
- **Count** - Number of records
- **Average** - Mean values
- **Min/Max** - Smallest/largest values
- **None** - Use raw data without aggregation

### 8. Interactive Features
- **Hover Tooltips** - Show details on hover
- **Zoom & Pan** - Explore data interactively
- **Legend Toggle** - Show/hide series by clicking legend
- **Download Charts** - Save individual charts as PNG

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
pip install pandas plotly kaleido jinja2 openpyxl
```

### Dependency Details
- **pandas** (≥2.0.0) - Data manipulation
- **plotly** (≥5.18.0) - Interactive charts
- **kaleido** (≥0.2.1) - PNG/PDF export engine
- **jinja2** (≥3.1.2) - HTML templating (optional, for advanced templates)
- **openpyxl** (≥3.1.0) - Excel file support

---

## Quick Start

### 1. Command Line Usage

**Generate dashboard from CSV:**
```bash
python dashboard_generator.py \
  --data data/sales_data.csv \
  --output ./dashboards
```

**Use a configuration file:**
```bash
python dashboard_generator.py \
  --config config/dashboard_sales.json \
  --output ./reports
```

### 2. Python Module Usage

```python
from dashboard_generator import DashboardGenerator, DashboardConfig

# Simple configuration
config = DashboardConfig(
    title="My Dashboard",
    data_source="data/sales_data.csv",
    data_source_type="csv",
    charts=[
        {
            "type": "bar",
            "title": "Sales by Product",
            "data_column_x": "Product",
            "data_column_y": "Revenue",
            "aggregation": "sum"
        }
    ],
    output_folder="./dashboards"
)

# Generate dashboard
generator = DashboardGenerator(config)
output_path = generator.save_dashboard()
print(f"Dashboard created: {output_path}")
```

### 3. Minimal Example

Create a file `simple_dashboard.json`:

```json
{
  "title": "Sales Dashboard",
  "data_source": "data/sales_data.csv",
  "data_source_type": "csv",
  "charts": [
    {
      "type": "bar",
      "title": "Revenue by Region",
      "data_column_x": "Region",
      "data_column_y": "Revenue",
      "aggregation": "sum"
    }
  ]
}
```

Generate:
```bash
python dashboard_generator.py --config simple_dashboard.json
```

---

## Configuration

### Configuration File Structure

A dashboard is configured using a JSON file with the following structure:

```json
{
  "title": "Dashboard Title",
  "description": "Optional description",
  "data_source": "path/to/data.csv",
  "data_source_type": "csv",
  "layout": "grid",
  "theme": "plotly_white",
  "charts": [ /* Chart configurations */ ],
  "filters": ["Column1", "Column2"],
  "show_data_table": true,
  "rows_per_page": 25,
  "enable_export": true,
  "export_formats": ["html", "png", "pdf"],
  "auto_refresh": false,
  "refresh_interval": 300,
  "color_palette": ["#3498db", "#2ecc71", "#e74c3c"],
  "output_folder": "./dashboards",
  "output_filename": "dashboard.html"
}
```

### Configuration Options

#### Data Settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `data_source` | string | ✅ | - | Path to data file (CSV, Excel, JSON) |
| `data_source_type` | string | ✅ | `"csv"` | Type: `csv`, `excel`, `json` |

**Example:**
```json
"data_source": "data/sales_2024.csv",
"data_source_type": "csv"
```

#### Dashboard Settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `title` | string | ❌ | `"Interactive Dashboard"` | Dashboard title |
| `description` | string | ❌ | `""` | Dashboard description |
| `layout` | string | ❌ | `"grid"` | Layout: `grid`, `single-column`, `two-column` |
| `theme` | string | ❌ | `"plotly"` | Chart theme (see Themes section) |

**Example:**
```json
"title": "Q4 2024 Sales Performance",
"description": "Regional sales analysis for Q4",
"layout": "grid",
"theme": "plotly_white"
```

#### Chart Configuration

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `charts` | array | ✅ | `[]` | List of chart configurations |

Each chart object has the following fields:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `type` | string | ✅ | `"bar"` | Chart type: `bar`, `line`, `pie`, `scatter`, `area`, `heatmap`, `box`, `histogram` |
| `title` | string | ✅ | - | Chart title |
| `data_column_x` | string | ✅* | - | X-axis column name |
| `data_column_y` | string | ✅* | - | Y-axis column name |
| `data_column_z` | string | ❌ | - | Z-axis (heatmap only) |
| `color_column` | string | ❌ | - | Column for color grouping |
| `size_column` | string | ❌ | - | Column for size (scatter only) |
| `aggregation` | string | ❌ | `"sum"` | Aggregation: `sum`, `count`, `avg`, `min`, `max`, `none` |
| `orientation` | string | ❌ | `"v"` | Bar orientation: `v` (vertical), `h` (horizontal) |
| `show_legend` | boolean | ❌ | `true` | Show/hide legend |
| `color_scheme` | string | ❌ | `"Plotly"` | Color scheme: `Plotly`, `Viridis`, `Plasma`, `Cividis`, `Blues`, `Reds`, `Greens` |
| `height` | number | ❌ | `400` | Chart height in pixels |

*Required for most chart types (see Chart Types section for details)

#### Filter Settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `filters` | array | ❌ | `[]` | Column names to create filters for |
| `default_filters` | object | ❌ | `{}` | Default filter values |

**Example:**
```json
"filters": ["Region", "Product", "Category"],
"default_filters": {
  "Region": "East",
  "Product": "Laptop"
}
```

#### Display Settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `show_data_table` | boolean | ❌ | `true` | Show data table below charts |
| `rows_per_page` | number | ❌ | `10` | Rows to display in table |
| `color_palette` | array | ❌ | Default palette | Custom colors (hex codes) |

**Example:**
```json
"show_data_table": true,
"rows_per_page": 25,
"color_palette": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"]
```

#### Export Settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `enable_export` | boolean | ❌ | `true` | Enable export functionality |
| `export_formats` | array | ❌ | `["html", "png", "pdf"]` | Export formats |

**Example:**
```json
"enable_export": true,
"export_formats": ["html", "png", "pdf"]
```

#### Auto-Refresh Settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `auto_refresh` | boolean | ❌ | `false` | Enable auto-refresh |
| `refresh_interval` | number | ❌ | `300` | Refresh interval (seconds) |

**Example:**
```json
"auto_refresh": true,
"refresh_interval": 600  // Refresh every 10 minutes
```

#### Output Settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `output_folder` | string | ❌ | `"./dashboards"` | Output directory |
| `output_filename` | string | ❌ | `"dashboard.html"` | Output filename |

**Example:**
```json
"output_folder": "./reports/2024",
"output_filename": "sales_dashboard_2024.html"
```

---

## Chart Types

### 1. Bar Chart

**Use Case:** Compare categories, show rankings

**Required Fields:**
- `data_column_x` - Category column
- `data_column_y` - Value column

**Optional Fields:**
- `aggregation` - `sum`, `count`, `avg`, `min`, `max`
- `orientation` - `v` (vertical) or `h` (horizontal)
- `color_column` - Group by color

**Example:**
```json
{
  "type": "bar",
  "title": "Revenue by Product",
  "data_column_x": "Product",
  "data_column_y": "Revenue",
  "aggregation": "sum",
  "orientation": "v",
  "color_column": "Region"
}
```

**Best Practices:**
- Use vertical bars for time series (dates on X-axis)
- Use horizontal bars for long category names
- Group by color for multi-category comparisons
- Aggregate data to avoid clutter (use `sum` or `avg`)

### 2. Line Chart

**Use Case:** Time series, trends over time

**Required Fields:**
- `data_column_x` - Time/date column
- `data_column_y` - Value column

**Optional Fields:**
- `aggregation` - `sum`, `avg`, `min`, `max`
- `color_column` - Multiple lines by category

**Example:**
```json
{
  "type": "line",
  "title": "Sales Trend Over Time",
  "data_column_x": "Date",
  "data_column_y": "Revenue",
  "aggregation": "sum",
  "color_column": "Region"
}
```

**Best Practices:**
- Ensure X-axis is sorted by date
- Use aggregation for daily/weekly/monthly rollups
- Limit to 5-7 lines for readability
- Use color_column for category comparison

### 3. Pie Chart

**Use Case:** Show proportions, market share

**Required Fields:**
- `data_column_x` - Category column (labels)
- `data_column_y` - Value column (sizes)

**Optional Fields:**
- `aggregation` - `sum`, `count`, `avg`

**Example:**
```json
{
  "type": "pie",
  "title": "Market Share by Region",
  "data_column_x": "Region",
  "data_column_y": "Revenue",
  "aggregation": "sum"
}
```

**Best Practices:**
- Limit to 5-8 slices for clarity
- Use for percentage/proportion data
- Aggregate data to sum by category
- Consider bar charts for more than 8 categories

### 4. Scatter Plot

**Use Case:** Show correlations, X vs Y relationships

**Required Fields:**
- `data_column_x` - X-axis variable
- `data_column_y` - Y-axis variable

**Optional Fields:**
- `color_column` - Group by color
- `size_column` - Point size by value
- `aggregation` - Usually `none` for scatter plots

**Example:**
```json
{
  "type": "scatter",
  "title": "Sales vs Profit Analysis",
  "data_column_x": "Sales",
  "data_column_y": "Profit",
  "color_column": "Region",
  "size_column": "Units_Sold",
  "aggregation": "none"
}
```

**Best Practices:**
- Use `aggregation: "none"` to show individual points
- Add `color_column` for segmentation
- Add `size_column` for 3-dimensional analysis
- Look for linear/non-linear relationships

### 5. Area Chart

**Use Case:** Cumulative trends, stacked areas

**Required Fields:**
- `data_column_x` - Time/category column
- `data_column_y` - Value column

**Optional Fields:**
- `aggregation` - `sum`, `avg`
- `color_column` - Stacked areas by category

**Example:**
```json
{
  "type": "area",
  "title": "Cumulative Revenue by Region",
  "data_column_x": "Date",
  "data_column_y": "Revenue",
  "aggregation": "sum",
  "color_column": "Region"
}
```

**Best Practices:**
- Use for cumulative data (running totals)
- Stack by `color_column` for part-to-whole analysis
- Sort X-axis chronologically
- Good for showing growth over time

### 6. Heatmap

**Use Case:** 2D density, correlation matrices

**Required Fields:**
- `data_column_x` - X-axis category
- `data_column_y` - Y-axis category
- `data_column_z` - Value (color intensity)

**Optional Fields:**
- `aggregation` - `sum`, `avg`, `count`
- `color_scheme` - `Viridis`, `Plasma`, `Blues`, `Reds`

**Example:**
```json
{
  "type": "heatmap",
  "title": "Sales by Region and Product",
  "data_column_x": "Product",
  "data_column_y": "Region",
  "data_column_z": "Revenue",
  "aggregation": "sum",
  "color_scheme": "Viridis"
}
```

**Best Practices:**
- Use for 2-dimensional categorical data
- Choose color schemes carefully (Viridis for general use)
- Aggregate values with `sum` or `avg`
- Good for spotting patterns in dense data

### 7. Box Plot

**Use Case:** Show distributions, identify outliers

**Required Fields:**
- `data_column_x` - Category column
- `data_column_y` - Value column

**Optional Fields:**
- `color_column` - Group boxes by category

**Example:**
```json
{
  "type": "box",
  "title": "Price Distribution by Category",
  "data_column_x": "Category",
  "data_column_y": "Price",
  "color_column": "Region"
}
```

**Best Practices:**
- Use for statistical analysis (quartiles, outliers)
- Compare distributions across categories
- Identify outliers and data quality issues
- Good for quality control and variance analysis

### 8. Histogram

**Use Case:** Frequency distributions, data ranges

**Required Fields:**
- `data_column_x` - Value column

**Optional Fields:**
- `color_column` - Overlay histograms by category

**Example:**
```json
{
  "type": "histogram",
  "title": "Age Distribution",
  "data_column_x": "Age",
  "color_column": "Department"
}
```

**Best Practices:**
- Use for understanding data distribution
- Identify normal, skewed, or bimodal distributions
- Adjust bin size for clarity (handled automatically)
- Overlay by `color_column` for comparison

---

## Filters & Interactivity

### Dynamic Filters

Filters allow users to interactively explore data by selecting specific categories.

**Configuration:**
```json
"filters": ["Region", "Product", "Category"]
```

**Generated UI:**
- Dropdown for each filter column
- "Apply Filters" button
- "Reset Filters" button

**How It Works:**
1. User selects values from dropdowns
2. Clicks "Apply Filters"
3. All charts update to show filtered data
4. Data table updates to match filters

**Example:**
```json
{
  "filters": ["Region", "Product", "Sales_Person"],
  "default_filters": {
    "Region": "East"  // Pre-select East region
  }
}
```

### Data Table Features

#### Search
- **Full-text search** across all columns
- **Real-time filtering** as you type
- **Case-insensitive** matching

#### Column Sorting
- Click column header to sort ascending
- Click again to sort descending
- Supports text, numbers, and dates

#### CSV Export
- "Export to CSV" button
- Downloads filtered/sorted data
- Preserves current view

**Configuration:**
```json
"show_data_table": true,
"rows_per_page": 25
```

### Interactive Chart Features

All charts support:
- **Hover Tooltips** - Show exact values on hover
- **Zoom** - Click and drag to zoom into area
- **Pan** - Shift+drag to pan across data
- **Legend Toggle** - Click legend items to show/hide series
- **Download** - Save individual chart as PNG (via toolbar)
- **Autoscale** - Double-click to reset zoom

---

## Themes & Styling

### Pre-built Themes

#### 1. `plotly` (Default)
- **Description:** Colorful, modern theme
- **Background:** White
- **Use Case:** General dashboards

#### 2. `plotly_white`
- **Description:** Clean, minimal theme
- **Background:** White
- **Use Case:** Professional reports, presentations

#### 3. `plotly_dark`
- **Description:** Dark background theme
- **Background:** Dark gray (#111111)
- **Use Case:** Late-night analysis, reduced eye strain

#### 4. `ggplot2`
- **Description:** Inspired by R's ggplot2
- **Background:** Light gray
- **Use Case:** Statistical analysis, academic papers

#### 5. `seaborn`
- **Description:** Inspired by Python's seaborn
- **Background:** White with subtle grid
- **Use Case:** Data science, exploratory analysis

**Usage:**
```json
"theme": "plotly_dark"
```

### Custom Color Palettes

Define your own brand colors:

```json
"color_palette": [
  "#FF6B6B",  // Red
  "#4ECDC4",  // Teal
  "#45B7D1",  // Blue
  "#FFA07A",  // Orange
  "#98D8C8",  // Mint
  "#F7B731",  // Yellow
  "#5758BB",  // Purple
  "#6F1E51"   // Maroon
]
```

**Tips:**
- Use 5-10 colors for variety
- Ensure sufficient contrast
- Test with colorblind-friendly palettes
- Use hex codes (#RRGGBB format)

### Chart-Specific Color Schemes

Some charts support color schemes:

```json
{
  "type": "heatmap",
  "color_scheme": "Viridis"
}
```

**Available Schemes:**
- `Plotly` - Default Plotly colors
- `Viridis` - Perceptually uniform (colorblind-safe)
- `Plasma` - High contrast purple-yellow
- `Cividis` - Colorblind-optimized
- `Blues`, `Reds`, `Greens` - Single-hue scales
- `RdBu`, `PiYG`, `BrBG` - Diverging scales

---

## Export Options

### HTML Export

**What It Does:** Saves the complete dashboard as a self-contained HTML file

**Features:**
- Single file (no external dependencies)
- Embedded Plotly.js library
- Interactive charts work offline
- Can be shared via email or file sharing

**Usage:**
```json
"enable_export": true,
"export_formats": ["html"]
```

**Generated Button:** "Export Dashboard"

**File Size:** ~50-200 KB (depends on data size)

### PNG Export

**What It Does:** Saves all charts as individual PNG images

**Features:**
- High resolution (1200x800 pixels)
- Static images (no interactivity)
- Good for presentations, reports
- Uses kaleido rendering engine

**Usage:**
```json
"enable_export": true,
"export_formats": ["png"]
```

**Output:** Creates `dashboard_charts/` folder with PNG files

**Requirements:** `kaleido` package must be installed

### PDF Export

**What It Does:** Saves all charts as PDF pages

**Features:**
- Vector graphics (scalable)
- Print-ready quality
- One page per chart
- Uses kaleido rendering engine

**Usage:**
```json
"enable_export": true,
"export_formats": ["pdf"]
```

**Output:** Creates `dashboard_charts/` folder with PDF files

**Requirements:** `kaleido` package must be installed

### Export Configuration

**Enable all formats:**
```json
{
  "enable_export": true,
  "export_formats": ["html", "png", "pdf"]
}
```

**Disable export:**
```json
{
  "enable_export": false
}
```

---

## Auto-Refresh

Auto-refresh keeps your dashboard up-to-date by automatically reloading data at specified intervals.

### Configuration

**Enable auto-refresh every 5 minutes:**
```json
{
  "auto_refresh": true,
  "refresh_interval": 300  // 300 seconds = 5 minutes
}
```

**Common intervals:**
```json
// 1 minute
"refresh_interval": 60

// 5 minutes
"refresh_interval": 300

// 10 minutes
"refresh_interval": 600

// 30 minutes
"refresh_interval": 1800

// 1 hour
"refresh_interval": 3600
```

### How It Works

1. Dashboard loads initial data
2. Timer starts counting down
3. When interval expires, page reloads automatically
4. Data is re-fetched from source
5. Charts update with new data
6. Timer resets

### Use Cases

**Real-time monitoring:**
```json
{
  "auto_refresh": true,
  "refresh_interval": 60  // Update every minute
}
```

**Daily reports:**
```json
{
  "auto_refresh": true,
  "refresh_interval": 3600  // Update hourly
}
```

**Live dashboards:**
- Display on TV screens or monitors
- Keep data current without manual refresh
- Good for operations centers, trading floors

### Best Practices

- **Choose appropriate intervals** - Too frequent = unnecessary load, Too rare = stale data
- **Consider data source** - File-based: 5-10 minutes, API-based: 1-2 minutes
- **Test performance** - Ensure data loads quickly
- **Inform users** - Display last update time
- **Use with static files** - Auto-refresh requires data source to update

---

## Responsive Design

### Grid Layout

**Default layout:**
```json
"layout": "grid"
```

Charts are arranged in a 2-column grid that adapts to screen size:

| Screen Size | Columns | Chart Width |
|-------------|---------|-------------|
| Desktop (>1200px) | 2 | 50% |
| Tablet (768-1200px) | 2 | 50% |
| Mobile (<768px) | 1 | 100% |

### Layout Options

#### 1. Grid Layout (Default)
```json
"layout": "grid"
```
- 2 columns on desktop/tablet
- 1 column on mobile
- Best for: Multiple charts, balanced layout

#### 2. Single Column
```json
"layout": "single-column"
```
- 1 column on all devices
- Full-width charts
- Best for: Focus on individual charts, detailed analysis

#### 3. Two Column
```json
"layout": "two-column"
```
- Always 2 columns (even on mobile)
- Best for: Side-by-side comparison, wide screens only

### Responsive Features

**Automatic:**
- Charts resize based on viewport width
- Touch gestures on mobile (pinch, zoom, swipe)
- Readable text at all sizes
- Optimized spacing and padding

**CSS Media Queries:**
The dashboard uses CSS media queries to adapt:

```css
/* Desktop */
@media (min-width: 1200px) {
  .chart-container { width: 50%; }
}

/* Tablet */
@media (min-width: 768px) and (max-width: 1199px) {
  .chart-container { width: 50%; }
}

/* Mobile */
@media (max-width: 767px) {
  .chart-container { width: 100%; }
}
```

### Mobile Optimization

**Features:**
- Simplified hover tooltips (tap instead of hover)
- Larger tap targets for filters/buttons
- Vertical scrolling for data tables
- Auto-hide legends on small screens
- Reduced padding for more content

**Best Practices:**
- Limit charts on mobile (3-5 max)
- Use vertical bar charts (easier to read)
- Keep titles concise
- Test on actual mobile devices

---

## Advanced Usage

### Use as Python Module

```python
from dashboard_generator import DashboardGenerator, DashboardConfig
from datetime import datetime

# Create configuration programmatically
config = DashboardConfig(
    title=f"Sales Report - {datetime.now().strftime('%Y-%m-%d')}",
    data_source="data/sales_today.csv",
    data_source_type="csv",
    charts=[
        {
            "type": "bar",
            "title": "Top Products",
            "data_column_x": "Product",
            "data_column_y": "Revenue",
            "aggregation": "sum",
            "orientation": "h"
        },
        {
            "type": "line",
            "title": "Hourly Trend",
            "data_column_x": "Hour",
            "data_column_y": "Revenue",
            "aggregation": "sum"
        }
    ],
    filters=["Region", "Store"],
    theme="plotly_white",
    show_data_table=True,
    rows_per_page=50,
    auto_refresh=True,
    refresh_interval=300,
    output_folder="./daily_reports",
    output_filename=f"report_{datetime.now().strftime('%Y%m%d')}.html"
)

# Generate dashboard
generator = DashboardGenerator(config)
generator.load_data()
output_path = generator.save_dashboard()

print(f"✅ Dashboard created: {output_path}")
```

### Scheduled Dashboards

**Using cron (Linux/Mac):**

Create a script `generate_daily_dashboard.sh`:
```bash
#!/bin/bash
cd /path/to/project
python dashboard_generator.py \
  --config config/daily_report.json \
  --output /var/www/html/dashboards
```

Add to crontab:
```bash
# Generate dashboard every day at 6 AM
0 6 * * * /path/to/generate_daily_dashboard.sh
```

**Using Task Scheduler (Windows):**
- Create a batch file (`.bat`) similar to above
- Open Task Scheduler
- Create Basic Task
- Set trigger (Daily, 6:00 AM)
- Set action (Start a program → your .bat file)

**Using Python schedule library:**
```python
import schedule
import time
from dashboard_generator import DashboardGenerator, load_config

def generate_dashboard():
    config = load_config('config/dashboard.json')
    generator = DashboardGenerator(config)
    generator.save_dashboard()
    print(f"Dashboard generated at {time.strftime('%Y-%m-%d %H:%M:%S')}")

# Schedule daily at 6 AM
schedule.every().day.at("06:00").do(generate_dashboard)

# Keep script running
while True:
    schedule.run_pending()
    time.sleep(60)
```

### Multiple Data Sources

**Merge data before generating:**
```python
import pandas as pd
from dashboard_generator import DashboardGenerator, DashboardConfig

# Load and merge data
sales = pd.read_csv('data/sales.csv')
products = pd.read_csv('data/products.csv')
merged = pd.merge(sales, products, on='Product_ID')

# Save merged data
merged.to_csv('data/merged_data.csv', index=False)

# Generate dashboard
config = DashboardConfig(
    data_source='data/merged_data.csv',
    # ... rest of config
)
generator = DashboardGenerator(config)
generator.save_dashboard()
```

### Custom Data Processing

```python
import pandas as pd
from dashboard_generator import DashboardGenerator, DashboardConfig

# Load and process data
df = pd.read_csv('data/raw_sales.csv')

# Data cleaning
df = df.dropna()  # Remove missing values
df['Date'] = pd.to_datetime(df['Date'])  # Parse dates
df['Revenue'] = df['Units_Sold'] * df['Unit_Price']  # Calculate revenue
df['Month'] = df['Date'].dt.to_period('M')  # Extract month

# Save processed data
df.to_csv('data/processed_sales.csv', index=False)

# Generate dashboard
config = DashboardConfig(
    data_source='data/processed_sales.csv',
    charts=[
        {
            "type": "line",
            "title": "Monthly Revenue Trend",
            "data_column_x": "Month",
            "data_column_y": "Revenue",
            "aggregation": "sum"
        }
    ]
)
generator = DashboardGenerator(config)
generator.save_dashboard()
```

---

## Examples

### Example 1: Sales Performance Dashboard

**Use Case:** Track sales by product, region, and salesperson

**Config:** `config/dashboard_sales_real.json`
```json
{
  "title": "Sales Performance Dashboard 2025",
  "data_source": "data/sales_data.csv",
  "data_source_type": "csv",
  "charts": [
    {
      "type": "bar",
      "title": "Revenue by Product",
      "data_column_x": "Product",
      "data_column_y": "Revenue",
      "aggregation": "sum",
      "orientation": "v"
    },
    {
      "type": "line",
      "title": "Sales Trend Over Time",
      "data_column_x": "Date",
      "data_column_y": "Revenue",
      "aggregation": "sum"
    },
    {
      "type": "pie",
      "title": "Market Share by Region",
      "data_column_x": "Region",
      "data_column_y": "Revenue",
      "aggregation": "sum"
    },
    {
      "type": "scatter",
      "title": "Units Sold vs Revenue",
      "data_column_x": "Units_Sold",
      "data_column_y": "Revenue",
      "color_column": "Region",
      "aggregation": "none"
    },
    {
      "type": "bar",
      "title": "Performance by Sales Person",
      "data_column_x": "Sales_Person",
      "data_column_y": "Revenue",
      "aggregation": "sum",
      "orientation": "h"
    }
  ],
  "filters": ["Region", "Product", "Sales_Person"],
  "theme": "plotly_white",
  "show_data_table": true,
  "rows_per_page": 25,
  "enable_export": true,
  "export_formats": ["html", "png", "pdf"]
}
```

**Generate:**
```bash
python dashboard_generator.py --config config/dashboard_sales_real.json
```

### Example 2: Product Analytics Dashboard

**Use Case:** Analyze product pricing, ratings, and revenue

**Config:** `config/dashboard_products.json`
```json
{
  "title": "Product Analytics Dashboard",
  "data_source": "data/product_data.csv",
  "data_source_type": "csv",
  "charts": [
    {
      "type": "histogram",
      "title": "Price Distribution",
      "data_column_x": "Price"
    },
    {
      "type": "box",
      "title": "Rating by Category",
      "data_column_x": "Category",
      "data_column_y": "Rating"
    },
    {
      "type": "area",
      "title": "Cumulative Revenue",
      "data_column_x": "Date",
      "data_column_y": "Revenue",
      "aggregation": "sum"
    }
  ],
  "filters": ["Category", "Brand"],
  "theme": "plotly_dark",
  "color_palette": [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A",
    "#98D8C8", "#F7B731", "#5758BB", "#6F1E51",
    "#C44569", "#786FA6"
  ],
  "auto_refresh": true,
  "refresh_interval": 600
}
```

**Generate:**
```bash
python dashboard_generator.py --config config/dashboard_products.json
```

### Example 3: Real-Time Monitoring Dashboard

**Use Case:** Monitor live metrics with auto-refresh

**Config:**
```json
{
  "title": "Live System Monitoring",
  "data_source": "http://api.example.com/metrics",
  "data_source_type": "api",
  "charts": [
    {
      "type": "line",
      "title": "CPU Usage (%)",
      "data_column_x": "Timestamp",
      "data_column_y": "CPU_Percent",
      "aggregation": "avg"
    },
    {
      "type": "line",
      "title": "Memory Usage (GB)",
      "data_column_x": "Timestamp",
      "data_column_y": "Memory_GB",
      "aggregation": "avg"
    },
    {
      "type": "bar",
      "title": "Active Connections",
      "data_column_x": "Server",
      "data_column_y": "Connections",
      "aggregation": "sum"
    }
  ],
  "theme": "plotly_dark",
  "auto_refresh": true,
  "refresh_interval": 60,
  "show_data_table": false
}
```

### Example 4: Executive Summary Dashboard

**Use Case:** High-level KPIs for executives

**Config:**
```json
{
  "title": "Executive Dashboard - Q4 2024",
  "description": "Key performance indicators and trends",
  "data_source": "data/kpi_data.csv",
  "data_source_type": "csv",
  "charts": [
    {
      "type": "bar",
      "title": "Revenue by Division",
      "data_column_x": "Division",
      "data_column_y": "Revenue",
      "aggregation": "sum",
      "orientation": "h"
    },
    {
      "type": "line",
      "title": "Quarterly Growth Trend",
      "data_column_x": "Quarter",
      "data_column_y": "Revenue",
      "aggregation": "sum",
      "color_column": "Division"
    },
    {
      "type": "pie",
      "title": "Cost Breakdown",
      "data_column_x": "Cost_Category",
      "data_column_y": "Amount",
      "aggregation": "sum"
    },
    {
      "type": "bar",
      "title": "Top 10 Customers",
      "data_column_x": "Customer",
      "data_column_y": "Revenue",
      "aggregation": "sum",
      "orientation": "h"
    }
  ],
  "filters": ["Division", "Region"],
  "theme": "plotly_white",
  "color_palette": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],
  "show_data_table": false,
  "enable_export": true,
  "export_formats": ["pdf"]
}
```

---

## Troubleshooting

### Common Issues

#### 1. **Dashboard is blank or charts don't load**

**Symptoms:**
- HTML file opens but no charts visible
- Console errors about Plotly

**Solutions:**
- Check internet connection (Plotly.js loads from CDN)
- Open browser console (F12) for JavaScript errors
- Verify data loaded correctly (check console logs)
- Try a different browser (Chrome, Firefox)

#### 2. **"Column not found" errors**

**Symptoms:**
```
ValueError: Value of 'x' is not the name of a column in 'data_frame'
```

**Solutions:**
- Check column names in CSV (case-sensitive)
- Verify `data_column_x` and `data_column_y` match exactly
- Print data columns: `df.columns.tolist()`
- Remove spaces from column names

**Example:**
```python
# Check columns
import pandas as pd
df = pd.read_csv('data/sales_data.csv')
print(df.columns.tolist())
# Output: ['Order_ID', 'Date', 'Region', 'Product', ...]
```

#### 3. **PNG/PDF export not working**

**Symptoms:**
- Export button does nothing
- Error about kaleido

**Solutions:**
- Install kaleido: `pip install kaleido`
- Check kaleido version: `pip show kaleido`
- Try alternative: Use browser "Print to PDF"
- Check file permissions in output folder

#### 4. **Auto-refresh not working**

**Symptoms:**
- Dashboard doesn't update automatically
- Timer doesn't start

**Solutions:**
- Verify `auto_refresh: true` in config
- Check `refresh_interval` is > 0
- Test with short interval (30 seconds)
- Update data source file manually to see if data changes

#### 5. **Charts are too small/large**

**Solutions:**
- Adjust `height` property in chart config
```json
{
  "type": "bar",
  "height": 600  // Increase height
}
```
- Change layout to `single-column` for larger charts
- Use browser zoom (Ctrl+/Ctrl-)

#### 6. **Filters not working**

**Symptoms:**
- Dropdowns don't populate
- "Apply Filters" button does nothing

**Solutions:**
- Verify filter columns exist in data
- Check for typos in column names
- Open browser console for JavaScript errors
- Ensure data loaded successfully

#### 7. **Data not aggregating correctly**

**Symptoms:**
- Bar chart shows wrong totals
- Numbers don't match source data

**Solutions:**
- Check `aggregation` setting (`sum`, `avg`, `count`)
- Verify numeric columns are actually numbers (not text)
- Remove duplicates if using `count`
- Convert string numbers to integers:
```python
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
```

#### 8. **Memory errors with large datasets**

**Symptoms:**
```
MemoryError: Unable to allocate array
```

**Solutions:**
- Reduce data size (filter date range)
- Aggregate before loading (GROUP BY in SQL)
- Use sampling: `df.sample(n=10000)`
- Increase system RAM
- Use server-side rendering (not client-side)

#### 9. **Date formatting issues**

**Symptoms:**
- Dates appear as numbers
- Line chart X-axis is scrambled

**Solutions:**
- Parse dates before generating dashboard:
```python
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')
df.to_csv('data/fixed_dates.csv', index=False)
```
- Ensure date format is consistent (YYYY-MM-DD)
- Check for invalid dates (Feb 30, etc.)

#### 10. **Dashboard file size is huge**

**Symptoms:**
- HTML file is 5+ MB
- Slow to load in browser

**Solutions:**
- Reduce data size (sample or aggregate)
- Remove unnecessary columns
- Disable data table: `"show_data_table": false`
- Use external data source instead of embedding

### Debugging Tips

**Enable verbose logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run dashboard generation
python dashboard_generator.py --config config.json
```

**Test data loading:**
```python
from dashboard_generator import DashboardGenerator, load_config

config = load_config('config/dashboard.json')
generator = DashboardGenerator(config)
df = generator.load_data()

# Check data
print(df.head())
print(df.columns.tolist())
print(df.dtypes)
```

**Validate configuration:**
```python
import json

with open('config/dashboard.json') as f:
    config = json.load(f)

# Check required fields
assert 'data_source' in config
assert 'charts' in config
assert len(config['charts']) > 0
```

---

## API Reference

### DashboardConfig

**Description:** Configuration dataclass for dashboard settings

**Fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `data_source` | str | - | Path to data file |
| `data_source_type` | str | `"csv"` | Data type: `csv`, `excel`, `json` |
| `title` | str | `"Interactive Dashboard"` | Dashboard title |
| `description` | str | `""` | Dashboard description |
| `layout` | str | `"grid"` | Layout type |
| `theme` | str | `"plotly"` | Chart theme |
| `charts` | List[Dict] | `[]` | Chart configurations |
| `filters` | List[str] | `[]` | Filter columns |
| `default_filters` | Dict | `{}` | Default filter values |
| `rows_per_page` | int | `10` | Table rows per page |
| `show_data_table` | bool | `True` | Show data table |
| `color_palette` | List[str] | Default palette | Custom colors |
| `enable_export` | bool | `True` | Enable export |
| `export_formats` | List[str] | `["html", "png", "pdf"]` | Export formats |
| `auto_refresh` | bool | `False` | Enable auto-refresh |
| `refresh_interval` | int | `300` | Refresh interval (seconds) |
| `output_folder` | str | `"./dashboards"` | Output directory |
| `output_filename` | str | `"dashboard.html"` | Output filename |

### DashboardGenerator

**Description:** Main class for generating dashboards

#### Constructor

```python
DashboardGenerator(config: DashboardConfig)
```

**Parameters:**
- `config` - DashboardConfig object

**Example:**
```python
from dashboard_generator import DashboardGenerator, DashboardConfig

config = DashboardConfig(data_source="data.csv")
generator = DashboardGenerator(config)
```

#### Methods

##### `load_data() -> pd.DataFrame`

Load data from configured source

**Returns:** pandas DataFrame

**Raises:**
- `ValueError` - If unsupported data source type
- `FileNotFoundError` - If data file not found

**Example:**
```python
df = generator.load_data()
print(f"Loaded {len(df)} rows")
```

##### `create_chart(chart_config: Dict[str, Any]) -> go.Figure`

Create a single chart

**Parameters:**
- `chart_config` - Chart configuration dictionary

**Returns:** plotly.graph_objects.Figure

**Example:**
```python
chart_config = {
    "type": "bar",
    "title": "Sales",
    "data_column_x": "Product",
    "data_column_y": "Revenue",
    "aggregation": "sum"
}
fig = generator.create_chart(chart_config)
```

##### `generate_html() -> str`

Generate complete dashboard HTML

**Returns:** HTML string

**Example:**
```python
html = generator.generate_html()
print(f"HTML length: {len(html)} bytes")
```

##### `save_dashboard() -> str`

Generate and save dashboard

**Returns:** Path to output file

**Example:**
```python
output_path = generator.save_dashboard()
print(f"Dashboard saved: {output_path}")
```

##### `export_charts_png(output_folder: str) -> List[str]`

Export charts as PNG files

**Parameters:**
- `output_folder` - Directory to save PNG files

**Returns:** List of PNG file paths

**Example:**
```python
png_files = generator.export_charts_png("./exports")
print(f"Exported {len(png_files)} charts")
```

### Utility Functions

#### `load_config(config_path: str) -> DashboardConfig`

Load configuration from JSON file

**Parameters:**
- `config_path` - Path to JSON config file

**Returns:** DashboardConfig object

**Raises:**
- `FileNotFoundError` - If config file not found
- `JSONDecodeError` - If invalid JSON

**Example:**
```python
from dashboard_generator import load_config

config = load_config('config/dashboard.json')
print(config.title)
```

---

## Best Practices

### Configuration

1. **Use meaningful titles** - Clear, descriptive chart titles
2. **Choose appropriate aggregation** - Sum for totals, avg for averages
3. **Limit chart count** - 4-8 charts per dashboard for clarity
4. **Select relevant filters** - Only include useful filter columns
5. **Set reasonable refresh intervals** - Balance freshness vs. load

### Data Preparation

1. **Clean data first** - Remove nulls, fix types before dashboard generation
2. **Parse dates** - Convert string dates to datetime
3. **Aggregate where possible** - Pre-aggregate large datasets
4. **Use consistent naming** - Avoid spaces, special characters in column names
5. **Validate data** - Check for outliers, missing values

### Performance

1. **Limit data size** - Filter to relevant date ranges
2. **Use sampling** - Sample large datasets (>100K rows)
3. **Disable unused features** - Turn off data table if not needed
4. **Optimize refresh intervals** - Longer intervals = less load
5. **Pre-process data** - Do heavy calculations before dashboard generation

### Design

1. **Choose appropriate chart types** - Bar for categories, line for trends
2. **Use consistent colors** - Define brand color palette
3. **Test on mobile** - Ensure readability on small screens
4. **Keep it simple** - Avoid chart clutter
5. **Provide context** - Add descriptions, units, labels

### Deployment

1. **Test thoroughly** - Verify all charts load correctly
2. **Check file size** - Optimize if >1 MB
3. **Use version control** - Track config changes in git
4. **Document configs** - Add comments in JSON (if supported)
5. **Monitor performance** - Track load times, errors

---

## Next Steps

### Learn More
- Read the [Plotly documentation](https://plotly.com/python/)
- Explore example dashboards in `config/` folder
- Run integration tests: `python test_dashboard_generator.py`

### Get Help
- Check [Troubleshooting](#troubleshooting) section
- Review [Examples](#examples) for common use cases
- Examine test files for code samples

### Contribute
- Report issues or bugs
- Suggest new features
- Share your dashboard configurations

---

**Last Updated:** 2024-11-21  
**Version:** 1.0.0  
**Author:** Dashboard Generator Team
