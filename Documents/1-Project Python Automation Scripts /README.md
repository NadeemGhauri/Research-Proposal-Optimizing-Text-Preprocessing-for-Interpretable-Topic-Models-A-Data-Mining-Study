# Python Data Analysis & File Management Tools

A comprehensive collection of Python scripts for automated data processing, analysis, reporting, file management, and backup automation.

---

## 📊 Data Analysis Tools

### 1. Data Validation Tool (`data_validation.py`)

Comprehensive data quality validation with 9 validation types, quality scoring, and detailed reporting.

**Features:**
- ✅ **9 Validation Types** - data types, ranges, mandatory fields, uniqueness, patterns, allowed values, string lengths, cross-field rules, business logic
- ✅ **Quality Scoring** - 0-100 score with completeness, consistency, and validity sub-scores
- ✅ **Pattern Validation** - regex-based validation for emails, phones, SKUs, etc.
- ✅ **Business Rules** - custom Python functions for complex validation logic
- ✅ **Cross-Field Validation** - validate relationships between multiple columns
- ✅ **Detailed Reports** - text and JSON formats with comprehensive error listings
- ✅ **Flexible Configuration** - JSON-based rule definitions with custom functions

**Quick Start:**
```bash
# Run with default test data
python test_validation.py

# Validate your own data
python -c "
from data_validation import DataValidator
rules = {
    'data_types': {'id': 'int', 'email': 'string', 'age': 'int'},
    'mandatory_fields': ['id', 'email'],
    'unique_fields': ['id'],
    'range_rules': {'age': (18, 100)},
    'regex_patterns': {'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'}
}
validator = DataValidator('data.csv', rules)
validator.validate()
print(f'Quality: {validator.quality_metrics[\"overall_score\"]}/100')
"
```

**Validation Types:**
1. **Data Type Validation** - int, float, string, bool, date
2. **Range Validation** - min/max values for numerical columns
3. **Mandatory Fields** - ensure required fields are not null/empty
4. **Uniqueness** - detect duplicate values in key columns
5. **Pattern Validation** - regex matching for formats (email, phone, etc.)
6. **Allowed Values** - restrict columns to predefined value sets
7. **String Lengths** - enforce min/max character lengths
8. **Cross-Field Rules** - validate relationships between columns
9. **Business Rules** - custom Python validation functions

**Example Configuration:**
```python
from data_validation import DataValidator

# Define custom business rule
def validate_senior_salary(row):
    if row.get('level') == 'senior':
        if float(row.get('salary', 0)) < 50000:
            return False, "Seniors must earn $50,000+"
    return True, None

rules = {
    'data_types': {'id': 'int', 'name': 'string', 'salary': 'float'},
    'range_rules': {'salary': (20000, 500000), 'age': (18, 100)},
    'mandatory_fields': ['id', 'name', 'email'],
    'unique_fields': ['id', 'email'],
    'regex_patterns': {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    },
    'allowed_values': {'status': ['active', 'inactive', 'pending']},
    'string_lengths': {'name': (2, 50)},
    'business_rules': [
        {'name': 'Senior Salary Check', 'function': validate_senior_salary}
    ]
}

validator = DataValidator('employees.csv', rules)
validator.validate()

print(f"Quality Score: {validator.quality_metrics['overall_score']}/100")
print(f"Total Errors: {validator.total_errors}")
print(f"Report: {validator.report_file}")
```

**Output:**
```
Quality Score: 87.5/100
  Completeness: 95.0/100
  Consistency: 92.0/100
  Validity: 85.0/100
Total Errors: 18
Report: validation_reports/validation_report_20241120_080000.txt
```

📖 **[Complete Guide](DATA_VALIDATION_GUIDE.md)** | 🧪 **[Test Suite](test_validation.py)**

---

### 2. API Data Fetcher (`api_data_fetcher.py`)

Automated REST API data extraction with authentication, pagination, rate limiting, and multi-format export.

**Features:**
- ✅ **Multiple Auth Methods** - API keys (Bearer tokens, custom headers), OAuth2 (client credentials)
- ✅ **Smart Pagination** - page-based, offset/limit, cursor-based, next-link following
- ✅ **Rate Limit Handling** - automatic retries with exponential backoff, respects Retry-After headers
- ✅ **Data Transformation** - JSON → pandas DataFrame with automatic flattening
- ✅ **Multi-Format Output** - save to JSON, CSV, and Excel simultaneously
- ✅ **Scheduling Support** - run on intervals or integrate with cron/systemd
- ✅ **Email Alerts** - get notified when API calls fail
- ✅ **Dry-Run Mode** - test configuration without making API calls

**Quick Start:**
```bash
# Dry run with sample data (no API calls)
python api_data_fetcher.py --dry-run

# Run once with config
python api_data_fetcher.py --config config/api_fetcher_example_apikey.json --once

# Schedule continuous runs every 15 minutes
python api_data_fetcher.py --config config/my_api.json --interval 15
```

**Example Config (API Key):**
```json
{
  "url": "https://api.example.com/v1/users",
  "auth_type": "api_key",
  "api_key": "Bearer YOUR_API_KEY",
  "pagination": {
    "type": "page",
    "page_param": "page",
    "start_page": 1
  },
  "output_folder": "output",
  "save_json": true,
  "save_csv": true,
  "save_excel": true
}
```

**Example Config (OAuth2):**
```json
{
  "url": "https://api.service.com/data",
  "auth_type": "oauth2",
  "oauth": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "token_url": "https://api.service.com/oauth/token",
    "scope": ["read:data"]
  },
  "pagination": {
    "type": "offset",
    "limit": 100
  }
}
```

**Pagination Strategies:**
- **None**: Single request (no pagination)
- **Page**: `?page=1`, `?page=2`, ... (stops when empty)
- **Offset/Limit**: `?offset=0&limit=100`, `?offset=100&limit=100`, ...
- **Next Link**: Follows `next` URL in response (GitHub, HAL format)
- **Cursor**: Token-based pagination (Twitter, Stripe style)

**Use as Module:**
```python
from api_data_fetcher import APIDataFetcher, APIFetcherConfig

config = APIFetcherConfig(
    url='https://api.example.com/data',
    auth_type='api_key',
    api_key='Bearer abc123',
    pagination={'type': 'page'},
    output_folder='output'
)

fetcher = APIDataFetcher(config)
saved_files = fetcher.fetch_and_save('my_data')
print(f"Saved: {saved_files}")
```

📖 **[Complete Guide](API_DATA_FETCHER_GUIDE.md)** | 🧪 **[Test Suite](test_api_fetcher.py)** | 📋 **[Example Configs](config/)**

---

### 3. Web Scraper (`web_scraper.py`)

Robust web scraping tool with anti-detection, proxy rotation, and support for both static and JavaScript-rendered content.

**Features:**
- ✅ **Dual scraping engines**
  - BeautifulSoup for fast static HTML parsing
  - Selenium for JavaScript-rendered content (SPAs, AJAX)
- ✅ **Ethical scraping**
  - Respects robots.txt automatically
  - Configurable rate limiting and delays
  - Requests per minute throttling
- ✅ **Anti-detection mechanisms**
  - Rotating user agents (fake-useragent)
  - Realistic browser headers
  - Random delays between requests
  - Selenium stealth mode (hides webdriver properties)
- ✅ **Proxy rotation**
  - Automatic round-robin proxy switching
  - HTTP/HTTPS proxy support with authentication
  - Distribute requests across multiple IPs
- ✅ **Smart data extraction**
  - CSS selector support
  - XPath selector support (Selenium)
  - Automatic table extraction to structured data
  - Link and image discovery
- ✅ **Multi-format output** - JSON, CSV, Excel with structured data

**Quick Start:**
```bash
# Scrape static content
python web_scraper.py --url https://example.com --output ./data

# Scrape JavaScript-rendered content
python web_scraper.py --url https://spa-app.com --selenium

# Use config file
python web_scraper.py --config config/scraper_basic.json
```

**Configuration Example:**
```python
from web_scraper import WebScraper, ScraperConfig

# Basic scraping
config = ScraperConfig(
    urls=['https://example.com'],
    css_selectors={
        'title': 'h1',
        'content': 'article p'
    },
    output_formats=['json', 'csv'],
    min_delay=2.0,
    max_delay=5.0
)

scraper = WebScraper(config)
files = scraper.scrape()
```

**Advanced Example with Proxies:**
```python
config = ScraperConfig(
    urls=['https://example.com/page1', 'https://example.com/page2'],
    use_selenium=True,  # For JavaScript content
    proxies=[
        'http://proxy1.com:8080',
        'http://user:pass@proxy2.com:8080'
    ],
    rotate_proxies=True,
    rotate_user_agents=True,
    table_selectors=['table.data'],
    extract_links=True,
    output_formats=['excel']
)
```

**Key Configuration Options:**
- `use_selenium`: Enable Selenium for JavaScript-rendered pages
- `respect_robots_txt`: Check and obey robots.txt (default: True)
- `min_delay`/`max_delay`: Random delay range between requests
- `proxies`: List of proxy URLs for rotation
- `css_selectors`: Dictionary of CSS selectors for data extraction
- `table_selectors`: Extract HTML tables to structured data
- `extract_links`/`extract_images`: Discover links and images

📖 **[Complete Guide](WEB_SCRAPER_GUIDE.md)** | 🧪 **[Test Suite](test_web_scraper.py)** | 📋 **[Example Configs](config/scraper_*.json)**

---

### 4. Excel Files Merger (`merge_excel_files.py`)

Merge multiple Excel files from a folder into a single master Excel file with preserved formatting and metadata.

**Features:**
- ✅ **Combine all sheets** from multiple Excel files
- ✅ **Preserve data types** and formatting
- ✅ **Add source tracking** - includes source filename, sheet name, and processing timestamp
- ✅ **Automatic sheet handling** - processes all sheets from all files
- ✅ **Error handling** - gracefully handles corrupted or problematic files
- ✅ **Timestamped output** - creates uniquely named output files
- ✅ **Professional formatting** - styled headers, auto-sized columns, frozen header row

**Quick Start:**
```bash
# Place Excel files in excel_files/ folder
python merge_excel_files.py

# Or specify custom folders
python merge_excel_files.py /path/to/input /path/to/output
```

**Use as Module:**
```python
from merge_excel_files import ExcelMerger

merger = ExcelMerger("./my_excel_files", "./results")
output_file = merger.merge(add_formatting=True)
```

---

### 5. CSV Data Cleaner (`clean_csv_data.py`)

Automated CSV data cleaning with validation, standardization, and detailed reporting.

**Features:**
- ✅ **Remove duplicates** - based on key columns
- ✅ **Standardize dates** - handles multiple input formats (MM/DD/YYYY, YYYY-MM-DD, Month DD, YYYY, etc.)
- ✅ **Fill missing values** - intelligent defaults based on data type (median for numbers, mode for text)
- ✅ **Validate emails** - checks and flags invalid email formats
- ✅ **Validate phone numbers** - standardizes and validates phone formats
- ✅ **Remove special characters** - cleans text fields while preserving alphanumerics
- ✅ **Generate cleaning report** - detailed statistics and data quality metrics

**Quick Start:**
```bash
# Use default sample data
python clean_csv_data.py

# Specify your own CSV file
python clean_csv_data.py /path/to/data.csv /path/to/output
```

**Configuration:**

Edit the `config` dictionary in `main()` function to customize cleaning behavior:

```python
config = {
    'key_columns': ['id', 'email'],              # Columns to check for duplicates
    'date_columns': ['created_date', 'last_login'],  # Date columns to standardize
    'date_format': '%Y-%m-%d',                   # Output date format
    'email_columns': ['email', 'contact_email'],  # Email columns to validate
    'phone_columns': ['phone', 'mobile'],        # Phone columns to validate
    'text_columns': ['name', 'address', 'company'],  # Text columns to clean
    'missing_value_strategy': 'intelligent',     # 'intelligent', 'mean', 'median', 'mode', 'drop'
}
```

**Use as Module:**
```python
from clean_csv_data import CSVDataCleaner

config = {
    'key_columns': ['id'],
    'date_columns': ['date'],
    'email_columns': ['email'],
    'phone_columns': ['phone'],
    'text_columns': ['name', 'address'],
}

cleaner = CSVDataCleaner('data.csv', './output', config)
cleaned_file, report = cleaner.clean()
print(report)
```

**Sample Output Report:**
```
======================================================================
CSV DATA CLEANING REPORT
======================================================================
Input File: data/sample_data.csv
Processing Date: 2025-11-19 06:39:44

ORIGINAL DATA:
  - Rows: 11
  - Columns: 12

CLEANING OPERATIONS:
  - Duplicate rows removed: 0
  - Date values standardized: 20
  - Missing values filled: 19
  - Invalid emails found: 5
  - Invalid phone numbers found: 3
  - Special characters removed: 21

FINAL DATA:
  - Rows: 11
  - Columns: 12
  - Data quality improvement: 36.36%
======================================================================
```

---

### 6. Excel Report Generator (`generate_excel_report.py`)

Automated Excel report generation with pivot tables, charts, and email delivery.

**Features:**
- ✅ **Multiple data sources** - Load from CSV, Excel, JSON files
- ✅ **Automatic pivot tables** - Create summary tables with aggregations
- ✅ **Dynamic charts** - Bar, pie, and line charts
- ✅ **Conditional formatting** - Color scales, data bars, cell highlighting
- ✅ **KPI dashboard** - Executive summary with key performance indicators
- ✅ **Auto-formatting** - Professional table styles and column widths
- ✅ **Sheet protection** - Password-protect worksheets
- ✅ **Email delivery** - Automated report distribution via SMTP

**Quick Start:**
```bash
# Use default configuration
python generate_excel_report.py

# Use custom configuration
python generate_excel_report.py /path/to/config.json
```

**Configuration Example:**
```json
{
  "report_name": "sales_report",
  "data_sources": [
    {
      "name": "Sales_Data",
      "type": "csv",
      "path": "./data/sales_data.csv"
    }
  ],
  "kpis": [
    {
      "name": "Total Revenue",
      "value": 250000,
      "target": 200000
    }
  ],
  "pivot_tables": [
    {
      "sheet_name": "Sales_By_Region",
      "source": "Sales_Data",
      "index": ["Region"],
      "values": ["Revenue"],
      "aggfunc": "sum"
    }
  ],
  "password": "SecurePass123"
}
```

**Output Includes:**
- Executive summary sheet with KPI dashboard
- Data sheets with professional formatting
- Pivot table summaries
- Visual charts
- Conditional formatting
- Password-protected sheets

See `REPORT_GENERATOR_GUIDE.md` for detailed configuration options and examples.

---

### 7. Dashboard Generator (`dashboard_generator.py`)

Create interactive HTML dashboards with Plotly charts, filters, and responsive design.

**Features:**
- ✅ **8 Chart Types** - bar, line, pie, scatter, area, heatmap, box, histogram
- ✅ **Interactive Charts** - zoom, pan, hover tooltips with Plotly.js
- ✅ **Dynamic Filters** - dropdown filters for any column with apply/reset
- ✅ **Responsive Design** - adapts to desktop, tablet, and mobile devices
- ✅ **Export Options** - save as HTML, PNG, or PDF
- ✅ **Auto-Refresh** - keep dashboards up-to-date automatically
- ✅ **Customizable Themes** - plotly, plotly_white, plotly_dark, ggplot2, seaborn
- ✅ **Data Aggregation** - sum, count, avg, min, max for grouped data

**Quick Start:**
```bash
# Generate dashboard from CSV
python dashboard_generator.py \
  --data data/sales_data.csv \
  --output ./dashboards

# Use configuration file
python dashboard_generator.py \
  --config config/dashboard_sales_real.json \
  --output ./reports
```

**Simple Configuration:**
```json
{
  "title": "Sales Dashboard",
  "data_source": "data/sales_data.csv",
  "data_source_type": "csv",
  "charts": [
    {
      "type": "bar",
      "title": "Revenue by Product",
      "data_column_x": "Product",
      "data_column_y": "Revenue",
      "aggregation": "sum"
    },
    {
      "type": "line",
      "title": "Sales Trend",
      "data_column_x": "Date",
      "data_column_y": "Revenue",
      "aggregation": "sum"
    },
    {
      "type": "pie",
      "title": "Market Share",
      "data_column_x": "Region",
      "data_column_y": "Revenue",
      "aggregation": "sum"
    }
  ],
  "filters": ["Region", "Product"],
  "theme": "plotly_white",
  "show_data_table": true,
  "enable_export": true
}
```

**Python Module Usage:**
```python
from dashboard_generator import DashboardGenerator, DashboardConfig

config = DashboardConfig(
    title="My Dashboard",
    data_source="data/sales.csv",
    charts=[
        {
            "type": "bar",
            "title": "Revenue by Region",
            "data_column_x": "Region",
            "data_column_y": "Revenue",
            "aggregation": "sum"
        }
    ],
    filters=["Region", "Product"],
    theme="plotly_dark",
    auto_refresh=True,
    refresh_interval=300  # 5 minutes
)

generator = DashboardGenerator(config)
output_path = generator.save_dashboard()
```

**Chart Types:**
1. **Bar Charts** - Compare categories, sales by product (vertical/horizontal)
2. **Line Charts** - Time series, trends over time
3. **Pie Charts** - Proportions, market share
4. **Scatter Plots** - Correlations, X vs Y relationships with color/size encoding
5. **Area Charts** - Cumulative trends, stacked areas
6. **Heatmaps** - 2D density, correlation matrices
7. **Box Plots** - Distributions, outlier detection
8. **Histograms** - Frequency distributions

**Interactive Features:**
- Hover tooltips with exact values
- Zoom and pan for detailed exploration
- Click legend to show/hide series
- Search and sort data tables
- Apply filters to update all charts
- Export dashboard or individual charts

**Configuration Options:**
- **Data Sources** - CSV, Excel, JSON files
- **Themes** - plotly, plotly_white, plotly_dark, ggplot2, seaborn
- **Color Palettes** - Custom brand colors (hex codes)
- **Layouts** - grid, single-column, two-column
- **Auto-Refresh** - Configurable intervals (seconds)
- **Export Formats** - HTML, PNG (1200x800), PDF

**Example Configs:**
- `config/dashboard_sales_real.json` - Sales performance with 5 charts
- `config/dashboard_products.json` - Product analytics with dark theme

📖 **[Complete Guide](DASHBOARD_GENERATOR_GUIDE.md)** | 🧪 **[Test Suite](test_dashboard_generator.py)** | 📋 **[Example Configs](config/)**

---

### 8. PDF Report Generator (`pdf_report_generator.py`)

Generate professional PDF reports with charts, tables, custom branding, and automatic formatting.

**Features:**
- ✅ **Multiple Data Sources** - CSV, Excel, JSON (API-ready)
- ✅ **6 Chart Types** - bar, line, pie, scatter, heatmap, box plots with Matplotlib
- ✅ **Styled Tables** - Custom headers, alternating row colors, column control
- ✅ **Professional Templates** - Cover page, table of contents, headers, footers
- ✅ **Custom Branding** - Company colors, fonts, logo, footer text
- ✅ **Auto Page Numbers** - "Page X of Y" format
- ✅ **Batch Processing** - Generate multiple reports from templates

**Quick Start:**
```bash
# Generate from configuration file
python pdf_report_generator.py \
  --config config/pdf_report_sales.json \
  --output ./reports

# Check example output
ls -lh reports/sales_report_q4_2024.pdf
```

**Simple Configuration:**
```json
{
  "title": "Monthly Sales Report",
  "subtitle": "Performance Analysis",
  "author": "Analytics Team",
  "data_sources": [
    {
      "name": "sales",
      "path": "data/sales_data.csv",
      "type": "csv"
    }
  ],
  "sections": [
    {
      "title": "Executive Summary",
      "content_type": "text",
      "content": "This report summarizes our Q4 performance..."
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
    },
    {
      "title": "Sales Data",
      "content_type": "table",
      "data_source": "sales",
      "content": {
        "title": "Top 20 Orders",
        "columns": ["Date", "Product", "Revenue", "Region"],
        "max_rows": 20
      }
    }
  ],
  "branding": {
    "primary_color": "#2c3e50",
    "company_name": "ABC Corporation",
    "report_footer": "Confidential - Internal Use Only"
  }
}
```

**Python Module Usage:**
```python
from pdf_report_generator import PDFReportGenerator, ReportConfig

config = ReportConfig(
    title="Sales Report",
    data_sources=[
        {"name": "sales", "path": "data/sales.csv", "type": "csv"}
    ],
    sections=[
        {
            "title": "Revenue Chart",
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
    branding={
        "primary_color": "#1a5490",
        "company_name": "My Company"
    }
)

generator = PDFReportGenerator(config)
output_path = generator.generate_report()
print(f"Report saved: {output_path}")
```

**Chart Types:**
1. **Bar Charts** - Compare categories, product sales, regional performance
2. **Line Charts** - Time series, trends, historical data
3. **Pie Charts** - Proportions, market share, distribution
4. **Scatter Plots** - Correlations, relationships between metrics
5. **Heatmaps** - 2D density, correlation matrices
6. **Box Plots** - Distributions, quartiles, outliers

**Document Features:**
- **Cover Page** - Title, subtitle, author, date, company logo
- **Table of Contents** - Auto-generated with clickable page links
- **Headers** - Logo and report title on every page
- **Footers** - Custom confidentiality notice
- **Page Numbers** - Automatic "Page X of Y" formatting
- **Page Breaks** - Control section positioning

**Branding Options:**
- **Colors** - Primary, secondary, accent (hex or RGB)
- **Fonts** - Title, heading, body fonts
- **Logo** - Company logo in header and cover (PNG/JPG)
- **Footer Text** - Custom confidentiality notices
- **Page Size** - Letter, A4, Legal
- **Orientation** - Portrait or Landscape

**Example Configurations:**
- `config/pdf_report_sales.json` - Q4 Sales Report with 8 sections
  - Cover page with branding
  - Table of contents
  - 4 charts (bar, pie, scatter)
  - 1 styled table (top 20 orders)
  - Custom colors and fonts
  - Result: 136KB professional PDF

**Batch Processing:**
```python
# Generate reports for multiple regions
regions = ["East", "West", "North", "South"]
for region in regions:
    config.data_sources[0]["path"] = f"data/{region.lower()}_sales.csv"
    config.output_filename = f"sales_{region.lower()}.pdf"
    generator = PDFReportGenerator(config)
    generator.generate_report()
```

📖 **[Complete Guide](PDF_REPORT_GENERATOR_GUIDE.md)** | 🧪 **[Test Suite](test_pdf_report_generator.py)** | 📋 **[Example Config](config/pdf_report_sales.json)**

---

## 📁 File Management Tools

### 9. Smart File Organizer (`organize_files.py`)

Intelligent file organization with type detection, duplicate removal, and safe preview mode.

**Features:**
- ✅ **Organize by type** - Auto-categorize files (Images, Documents, Videos, Audio, Code, etc.)
- ✅ **Organize by date** - Sort files by creation/modification date
- ✅ **Consistent naming** - Rename files with customizable patterns
- ✅ **Duplicate detection** - Find and remove duplicates using MD5 hashing
- ✅ **Auto folder creation** - Create organized folder structures automatically
- ✅ **Organization report** - Detailed statistics and operation logs
- ✅ **Safe mode** - Preview changes before executing (prevent accidents!)

**Quick Start:**
```bash
# Preview organization (Safe Mode - recommended first!)
python organize_files.py /path/to/messy/folder

# Or organize test files
python organize_files.py ./test_files
```

**Configuration Example:**
```python
config = {
    'organize_by_type': True,         # Group by category
    'organize_by_date': False,        # Group by date
    'rename_files': False,            # Apply naming pattern
    'naming_pattern': '{original_name}',
    'remove_duplicates': True,        # Remove duplicate files
    'safe_mode': True,                # Preview only (no changes)
    'min_file_size': 0,               # Minimum file size filter
    'exclude_extensions': ['.tmp'],   # Skip these extensions
}
```

**File Categories:**
- Images (`.jpg`, `.png`, `.gif`, etc.)
- Documents (`.pdf`, `.doc`, `.xlsx`, etc.)
- Videos (`.mp4`, `.avi`, `.mkv`, etc.)
- Audio (`.mp3`, `.wav`, `.flac`, etc.)
- Code (`.py`, `.js`, `.java`, etc.)
- Archives (`.zip`, `.tar`, `.rar`, etc.)
- Web (`.html`, `.css`, `.json`, etc.)
- And more...

**Output Structure:**
```
Source_Folder/
└── Organized/
    ├── Images/
    │   ├── photo1.jpg
    │   └── photo2.png
    ├── Documents/
    │   ├── report.pdf
    │   └── spreadsheet.xlsx
    ├── Videos/
    │   └── clip.mp4
    └── Code/
        └── script.py
```

**Safe Mode:**
- Always enabled by default
- Preview all operations before executing
- Review detailed report
- Set `safe_mode: False` to actually organize files

See `FILE_ORGANIZER_GUIDE.md` for advanced usage, naming patterns, and date organization.

---

### 10. Bulk File Renamer (`bulk_rename.py`)

Advanced file renaming with patterns, previews, and undo functionality for batch renaming operations.

**Features:**
- ✅ **6 Renaming Operations**
  - Sequential numbering with custom patterns
  - Find and replace (with regex support)
  - Add prefix/suffix (static or dynamic based on date/size/type)
  - Change case (lower, upper, title, sentence, camel, snake)
  - Remove special characters
- ✅ **Safety Features**
  - Preview mode (see changes before applying)
  - Conflict detection (duplicate names, existing files)
  - Undo functionality (restore original names)
  - Safe mode by default
- ✅ **Flexible Configuration**
  - File filtering by extension
  - Recursive folder processing
  - Hidden file handling
  - Customizable patterns

**Quick Start:**
```bash
# Preview rename operations (Safe Mode)
python bulk_rename.py /path/to/folder
```

**Common Use Cases:**

```python
from bulk_rename import BulkFileRenamer

# Remove special characters
config = {'preview_mode': False, 'create_undo_file': True}
renamer = BulkFileRenamer('./my_files', config)
renamer.rename('remove_special', keep_chars='_-', replace_with='_')

# Add sequential numbers
renamer.rename('sequential', pattern='file_{counter}', start=1, padding=3)

# Change to lowercase
renamer.rename('case_change', case_type='lower')

# Find and replace (with regex)
renamer.rename('find_replace', find='2024', replace='2025')

# Add date-based prefix
renamer.rename('prefix_suffix', prefix='', based_on='date')

# Undo last rename
renamer.undo_last_rename()
```

**Renaming Examples:**
```
Sequential Numbering:
report.txt              -> file_001.txt
invoice.pdf             -> file_002.pdf
data.csv                -> file_003.csv

Remove Special Characters:
My File (1).txt         -> My_File_1.txt
document#2@test.pdf     -> document_2_test.pdf

Case Changes:
MY DOCUMENT.txt         -> my_document.txt  (lowercase)
photo vacation.jpg      -> photoVacation.jpg  (camel)

Find & Replace:
report_2024.txt         -> report_2025.txt
backup_old.pdf          -> backup_new.pdf

Date-based Prefix:
photo.jpg               -> 20241120_photo.jpg
document.pdf            -> 20241120_document.pdf
```

**Safety Tips:**
- Always use preview mode first (`preview_mode: True`)
- Enable undo file creation (`create_undo_file: True`)
- Test on small batches before processing thousands of files
- Review conflicts section in preview output

See `BULK_RENAMER_GUIDE.md` for detailed configuration, all renaming patterns, regex examples, and advanced usage.

---

### 11. Backup Automation (`backup_automation.py`)

Automated backup system with compression, versioning, integrity verification, and email notifications.

**Features:**
- ✅ **Compression**
  - ZIP compression with configurable levels (0-9)
  - Automatic compression ratio calculation
  - Efficient storage of large files
- ✅ **Timestamping**
  - Automatic timestamp in backup filenames
  - ISO format metadata timestamps
  - Sortable backup organization
- ✅ **Version Management**
  - Keep last N versions (configurable)
  - Automatic cleanup of old backups
  - Metadata tracking for each version
- ✅ **Integrity Verification**
  - MD5 checksum calculation
  - ZIP file validation
  - Corruption detection
- ✅ **Email Notifications**
  - Success/failure notifications
  - Detailed backup statistics
  - SMTP support (Gmail, Outlook, etc.)
- ✅ **File Exclusion**
  - Pattern-based exclusion
  - Wildcard support
  - Skip temporary and cache files

**Quick Start:**
```bash
# Configure and run backup
python backup_automation.py
```

**Common Use Cases:**

```python
from backup_automation import BackupAutomation

# Daily document backup
config = {
    'backup_sources': ['./documents', './photos'],
    'backup_destination': './backups',
    'max_versions': 7,                  # Keep last 7 backups
    'compression_level': 9,             # Maximum compression
    'verify_integrity': True,           # Verify after backup
    'send_notifications': True,         # Email notifications
    'notification_email': 'admin@example.com',
    'exclude_patterns': [
        '*.tmp', '*.log', '.DS_Store',
        '__pycache__', '.git', 'node_modules'
    ],
}

backup_system = BackupAutomation(config)
backup_system.run_backup('daily_backup')

# List available backups
backups = backup_system.list_backups()
for backup in backups:
    print(f"{backup['filename']} - {backup['created']}")

# Restore from backup
backup_system.restore_backup(
    'daily_backup_20251120_143022.zip',
    './restored_data'
)
```

**Backup Output:**
```
================================================================================
BACKUP COMPLETED SUCCESSFULLY
Backup File: daily_backup_20251120_143022.zip
Files Backed Up: 1,250
Original Size: 125.45 MB
Compressed Size: 45.32 MB
Compression Ratio: 63.87%
Duration: 12.34 seconds
================================================================================
```

**Automation Examples:**
```python
# Schedule daily backups at 2 AM (cron)
# 0 2 * * * /usr/bin/python3 /path/to/backup_automation.py

# Multi-tier backup strategy
daily_config = {'backup_destination': './backups/daily', 'max_versions': 7}
weekly_config = {'backup_destination': './backups/weekly', 'max_versions': 4}
monthly_config = {'backup_destination': './backups/monthly', 'max_versions': 12}

# Backup with email notification
config = {
    'send_notifications': True,
    'smtp_server': 'smtp.gmail.com',
    'smtp_user': 'sender@gmail.com',
    'smtp_password': 'app-password',
}
```

**Safety Features:**
- Automatic integrity verification
- Version history management
- Email notifications on success/failure
- Metadata tracking (checksums, timestamps)
- Graceful error handling

See `BACKUP_AUTOMATION_GUIDE.md` for detailed configuration, scheduling, email setup, and restore procedures.

---

## 📋 Requirements

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

## 🚀 Installation

1. **Clone or download this project**

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Project Structure

```
Fiverr Project 1/
├── data_validation.py              # Data validation tool ⭐
├── api_data_fetcher.py             # API data fetcher tool ⭐
├── web_scraper.py                  # Web scraper tool ⭐
├── dashboard_generator.py          # Dashboard generator tool ⭐
├── pdf_report_generator.py         # PDF report generator tool ⭐ NEW
├── merge_excel_files.py            # Excel merger tool
├── clean_csv_data.py               # CSV data cleaner tool
├── generate_excel_report.py        # Excel report generator
├── organize_files.py               # Smart file organizer
├── bulk_rename.py                  # Bulk file renamer
├── backup_automation.py            # Automated backup system
├── test_validation.py              # Data validation test suite ⭐
├── test_api_fetcher.py             # API fetcher integration tests ⭐
├── test_web_scraper.py             # Web scraper integration tests ⭐
├── test_dashboard_generator.py     # Dashboard generator tests ⭐
├── test_pdf_report_generator.py    # PDF report generator tests ⭐ NEW
├── test_bulk_rename.py             # Bulk renamer test suite
├── test_backup.py                  # Backup automation test suite
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── DATA_VALIDATION_GUIDE.md        # Detailed validation guide ⭐
├── API_DATA_FETCHER_GUIDE.md       # Detailed API fetcher guide ⭐
├── WEB_SCRAPER_GUIDE.md            # Detailed web scraper guide ⭐
├── DASHBOARD_GENERATOR_GUIDE.md    # Detailed dashboard guide ⭐
├── PDF_REPORT_GENERATOR_GUIDE.md   # Detailed PDF generator guide ⭐ NEW
├── CSV_CLEANER_GUIDE.md            # Detailed CSV cleaner documentation
├── REPORT_GENERATOR_GUIDE.md       # Detailed report generator documentation
├── FILE_ORGANIZER_GUIDE.md         # Detailed file organizer documentation
├── BULK_RENAMER_GUIDE.md           # Detailed bulk renamer documentation
├── BACKUP_AUTOMATION_GUIDE.md      # Detailed backup automation documentation
├── .github/
│   └── copilot-instructions.md
├── config/                         # Configuration files
│   ├── report_config.json          # Sample Excel report configuration
│   ├── api_fetcher_example_*.json  # API fetcher configs ⭐
│   ├── scraper_*.json              # Web scraper configs ⭐
│   ├── dashboard_sales_real.json   # Sales dashboard config ⭐
│   ├── dashboard_products.json     # Product dashboard config ⭐
│   └── pdf_report_sales.json       # PDF report config ⭐ NEW
├── excel_files/                    # Input folder for Excel files
│   ├── sample1.xlsx
│   └── sample2.xlsx
├── data/                           # Input folder for CSV/JSON files
│   ├── sample_data.csv             # Sample data for cleaner
│   ├── sales_data.csv              # Sample sales data
│   ├── product_data.csv            # Sample product data
│   └── sales_sample.json           # Sample JSON data
├── test_files/                     # Test files for organizer
│   ├── (various file types)
│   └── Organized/                  # Organized output
├── rename_test/                    # Test files for bulk renamer
│   └── (various file types)
├── backups/                        # Backup output folder
│   ├── *.zip                       # Backup archives
│   └── *.json                      # Backup metadata
├── dashboards/                     # Dashboard output folder ⭐
│   └── dashboard.html              # Generated dashboards
├── validation_reports/             # Validation reports output ⭐
│   ├── validation_report_*.txt     # Text reports
│   └── validation_report_*.json    # JSON reports
├── output/                         # Output folder for merged Excel files
│   └── merged_excel_YYYYMMDD_HHMMSS.xlsx
├── cleaned_data/                   # Output folder for cleaned CSV files
│   ├── cleaned_sample_data_YYYYMMDD_HHMMSS.csv
│   └── cleaning_report_YYYYMMDD_HHMMSS.txt
└── reports/                        # Output folder for generated reports
    ├── sales_report_YYYYMMDD_HHMMSS.xlsx  # Excel reports
    └── sales_report_q4_2024.pdf           # PDF reports ⭐ NEW
```

## 🔧 Dependencies

### Core Dependencies
- `pandas>=2.0.0` - Data manipulation and analysis
- `openpyxl>=3.1.0` - Excel file handling
- `xlrd>=2.0.1` - Legacy Excel file support
- `python-dateutil>=2.8.2` - Advanced date parsing

### API & Web Scraping
- `requests>=2.31.0` - HTTP library for API calls
- `requests-oauthlib>=1.3.1` - OAuth2 authentication
- `tenacity>=8.2.2` - Retry logic with exponential backoff
- `schedule>=1.2.0` - Job scheduling
- `beautifulsoup4>=4.12.0` - HTML parsing for web scraping
- `selenium>=4.15.0` - Browser automation for JavaScript content
- `lxml>=4.9.0` - Fast XML/HTML parsing
- `fake-useragent>=1.4.0` - User agent rotation

### Visualization & Reporting
- `plotly>=5.18.0` - Interactive charts and dashboards
- `kaleido>=0.2.1` - PNG/PDF export for Plotly charts
- `jinja2>=3.1.2` - HTML templating (optional)
- `reportlab>=4.0.0` - PDF generation engine ⭐ NEW
- `pillow>=10.0.0` - Image handling for logos/charts ⭐ NEW
- `matplotlib>=3.7.0` - Chart generation for PDFs ⭐ NEW
- `seaborn>=0.12.0` - Enhanced color palettes ⭐ NEW
- `pypdf2>=3.0.0` - PDF verification (testing) ⭐ NEW

## 📝 Supported File Types

### Excel Merger:
- `.xlsx` - Excel 2007+ files
- `.xls` - Excel 97-2003 files
- `.xlsm` - Excel macro-enabled files

### CSV Cleaner:
- `.csv` - Comma-separated values files

## 🛠️ Troubleshooting

**Excel Merger Issues:**

**Issue: "No Excel files found"**
- Ensure your Excel files are in the correct input folder
- Check that files have .xlsx, .xls, or .xlsm extensions

**Issue: "Error reading file"**
- The file may be corrupted - the script will skip it and continue
- Check file permissions

**CSV Cleaner Issues:**

**Issue: "File not found"**
- Verify the CSV file path is correct
- Check file permissions

**Issue: "Invalid date format"**
- The script supports most common date formats
- Check the `date_format` configuration matches your needs

**General Issues:**

**Issue: "Module not found"**
- Run `pip install -r requirements.txt`
- Ensure you're using the correct Python environment

## 📚 Examples

### Example 1: Merge Sales Reports
```bash
python merge_excel_files.py ./sales_reports ./merged_sales
```

### Example 2: Clean Customer Database
```bash
python clean_csv_data.py ./customer_data.csv ./cleaned_customers
```

### Example 3: Generate Monthly Report
```bash
python generate_excel_report.py config/monthly_report.json
```

### Example 4: Organize Downloads Folder
```bash
python organize_files.py ~/Downloads
```

### Example 5: Batch Rename Photos
```python
from bulk_rename import BulkFileRenamer

# Clean up photo filenames
config = {'preview_mode': False, 'include_extensions': ['.jpg', '.png'], 'create_undo_file': True}
renamer = BulkFileRenamer('./vacation_photos', config)

# Remove special characters
renamer.rename('remove_special', keep_chars='_-', replace_with='_')

# Add date prefix
renamer = BulkFileRenamer('./vacation_photos', config)
renamer.rename('prefix_suffix', prefix='', based_on='date')

# Add sequential numbers
renamer = BulkFileRenamer('./vacation_photos', config)
renamer.rename('sequential', pattern='{name}_{counter}', start=1, padding=3)
```

### Example 6: Complete Workflow

```python
from merge_excel_files import ExcelMerger
from clean_csv_data import CSVDataCleaner
from generate_excel_report import ExcelReportGenerator

# 1. Merge multiple Excel files
merger = ExcelMerger("./raw_data", "./merged")
merged_file = merger.merge()

# 2. Clean the data
cleaner = CSVDataCleaner(merged_file, "./cleaned")
cleaned_file, report = cleaner.clean()

# 3. Generate report
config = {
    "data_sources": [
        {"name": "Clean_Data", "type": "csv", "path": str(cleaned_file)}
    ],
    "kpis": [
        {"name": "Total Records", "value": 1000, "target": 800}
    ]
}
generator = ExcelReportGenerator()
generator.config.update(config)
report_file = generator.generate_report()
```

### Example 7: Automated Daily Backup

```python
from backup_automation import BackupAutomation

# Configure daily backup with email notifications
config = {
    'backup_sources': [
        './documents',
        './photos',
        './important_data'
    ],
    'backup_destination': './backups/daily',
    'max_versions': 30,  # Keep last 30 days
    'compression_level': 9,
    'verify_integrity': True,
    'send_notifications': True,
    'notification_email': 'admin@example.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'smtp_user': 'sender@gmail.com',
    'smtp_password': 'app-password',
    'exclude_patterns': [
        '*.tmp', '*.log', '.DS_Store',
        '__pycache__', 'node_modules', '.git'
    ],
}

# Run backup
backup_system = BackupAutomation(config)
success = backup_system.run_backup('daily_backup')

if success:
    print("✓ Backup completed successfully!")
    
    # List all backups
    backups = backup_system.list_backups()
    print(f"\nAvailable backups: {len(backups)}")
else:
    print("✗ Backup failed!")
```

Schedule with cron for daily execution:
```bash
# Add to crontab (run daily at 2 AM)
0 2 * * * /usr/bin/python3 /path/to/backup_automation.py
```

## 📄 License

This project is provided as-is for data processing purposes.

## 👤 Author

Created for data analysis and processing automation tasks.
