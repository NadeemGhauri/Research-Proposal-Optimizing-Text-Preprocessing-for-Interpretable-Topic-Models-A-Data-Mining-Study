# Excel Report Generator - Complete Guide

## Overview

The Excel Report Generator is an advanced automation tool that creates professional Excel reports from multiple data sources with pivot tables, charts, conditional formatting, KPIs, and optional email delivery.

---

## 🎯 Features

- ✅ **Multiple Data Sources** - Load from CSV, Excel, JSON files
- ✅ **Automatic Pivot Tables** - Create summary tables with aggregations
- ✅ **Dynamic Charts** - Bar charts, pie charts, line charts
- ✅ **Conditional Formatting** - Color scales, data bars, cell highlighting
- ✅ **KPI Dashboard** - Executive summary with key metrics
- ✅ **Auto-formatting** - Professional table styles and column widths
- ✅ **Sheet Protection** - Password-protect worksheets
- ✅ **Email Delivery** - Automated report distribution

---

## 📋 Quick Start

### 1. Basic Usage

```bash
# Use default configuration
python generate_excel_report.py

# Use custom configuration
python generate_excel_report.py /path/to/config.json
```

### 2. Configuration File

Create a JSON configuration file to customize your report:

```json
{
  "output_folder": "./reports",
  "report_name": "monthly_report",
  "data_sources": [
    {
      "name": "Sales_Data",
      "type": "csv",
      "path": "./data/sales.csv"
    }
  ],
  "kpis": [
    {
      "name": "Total Revenue",
      "value": 250000,
      "target": 200000
    }
  ],
  "password": "SecurePass123",
  "email": {
    "enabled": false
  }
}
```

---

## 🔧 Configuration Reference

### Data Sources

Load data from multiple file formats:

```json
"data_sources": [
  {
    "name": "Sales_Data",
    "type": "csv",
    "path": "./data/sales.csv"
  },
  {
    "name": "Customer_Data",
    "type": "excel",
    "path": "./data/customers.xlsx",
    "sheet_name": "Sheet1"
  },
  {
    "name": "Product_Data",
    "type": "json",
    "path": "./data/products.json"
  }
]
```

**Supported Types:**
- `csv` - Comma-separated values
- `excel` - Excel files (.xlsx, .xls)
- `json` - JSON files

### KPIs (Key Performance Indicators)

Define metrics for the summary dashboard:

```json
"kpis": [
  {
    "name": "Total Revenue",
    "value": 250000,
    "target": 200000
  },
  {
    "name": "Total Orders",
    "value": 450,
    "target": 500
  },
  {
    "name": "Customer Satisfaction",
    "value": 4.5,
    "target": 4.0
  }
]
```

**Status Indicators:**
- ✓ On Target (≥100% of target) - Green
- ⚠ Warning (80-99% of target) - Yellow
- ✗ Below Target (<80% of target) - Red

### Pivot Tables

Create automatic pivot table summaries:

```json
"pivot_tables": [
  {
    "sheet_name": "Sales_By_Region",
    "source": "Sales_Data",
    "index": ["Region"],
    "values": ["Revenue", "Units_Sold"],
    "aggfunc": "sum"
  },
  {
    "sheet_name": "Sales_By_Product",
    "source": "Sales_Data",
    "index": ["Product", "Category"],
    "columns": "Region",
    "values": ["Revenue"],
    "aggfunc": "mean"
  }
]
```

**Parameters:**
- `sheet_name` - Name of the pivot table sheet
- `source` - Source data name (from data_sources)
- `index` - Row grouping columns
- `columns` - Column grouping (optional)
- `values` - Columns to aggregate
- `aggfunc` - Aggregation function: `sum`, `mean`, `count`, `min`, `max`

### Charts

Add visual charts to worksheets:

```json
"charts": [
  {
    "sheet_name": "Sales_By_Region",
    "type": "bar",
    "title": "Revenue by Region",
    "data_range": "A1:B10",
    "position": "E2"
  },
  {
    "sheet_name": "Sales_By_Product",
    "type": "pie",
    "title": "Product Distribution",
    "data_range": "A1:B7",
    "position": "E2"
  }
]
```

**Chart Types:**
- `bar` - Bar chart (vertical bars)
- `pie` - Pie chart
- `line` - Line chart

**Parameters:**
- `sheet_name` - Sheet to add chart to
- `type` - Chart type
- `title` - Chart title
- `data_range` - Excel range (e.g., "A1:B10")
- `position` - Top-left cell position (e.g., "E2")

### Conditional Formatting

Apply visual formatting rules:

```json
"conditional_formatting": [
  {
    "sheet_name": "Sales_Data",
    "type": "color_scale",
    "range": "E2:E100"
  },
  {
    "sheet_name": "Sales_Data",
    "type": "highlight_cells",
    "range": "F2:F100",
    "operator": "greaterThan",
    "threshold": 1000,
    "color": "00FF00"
  }
]
```

**Formatting Types:**

1. **Color Scale** - Three-color gradient (Red → Yellow → Green)
   ```json
   {
     "type": "color_scale",
     "range": "E2:E100"
   }
   ```

2. **Data Bars** - Visual bars in cells
   ```json
   {
     "type": "data_bars",
     "range": "E2:E100"
   }
   ```

3. **Highlight Cells** - Conditional cell highlighting
   ```json
   {
     "type": "highlight_cells",
     "range": "F2:F100",
     "operator": "greaterThan",
     "threshold": 1000,
     "color": "00FF00"
   }
   ```

**Operators:** `greaterThan`, `lessThan`, `equal`, `between`

### Sheet Protection

Protect sheets with a password:

```json
"password": "SecurePassword123"
```

All sheets will be protected with this password. Users will need the password to edit the sheets.

### Email Configuration

Automatically send reports via email:

```json
"email": {
  "enabled": true,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@gmail.com",
  "sender_password": "your-app-password",
  "recipients": [
    "recipient1@example.com",
    "recipient2@example.com"
  ],
  "subject": "Monthly Sales Report",
  "body": "Please find the attached monthly sales report.\n\nBest regards,\nAutomated Reporting System"
}
```

**Gmail Setup:**
1. Enable 2-Factor Authentication in Gmail
2. Generate an App Password (Google Account → Security → App Passwords)
3. Use the app password in `sender_password`

**Parameters:**
- `enabled` - Set to `true` to send emails
- `smtp_server` - SMTP server address
- `smtp_port` - SMTP port (587 for TLS, 465 for SSL)
- `sender_email` - Your email address
- `sender_password` - Email password or app password
- `recipients` - List of recipient emails
- `subject` - Email subject line
- `body` - Email message body

---

## 📊 Report Structure

Generated reports include:

### 1. Summary Sheet (First Sheet)
- Executive summary with report date
- KPI dashboard with status indicators
- Visual status colors (Green/Yellow/Red)

### 2. Data Sheets
- All source data with professional table formatting
- Frozen header rows
- Auto-sized columns
- Color-coded headers

### 3. Pivot Table Sheets
- Aggregated summaries
- Multiple grouping levels
- Clean, readable format

### 4. Charts (Embedded in Sheets)
- Visual data representations
- Professional styling
- Positioned for easy viewing

---

## 💡 Use Cases

### Use Case 1: Monthly Sales Report

```json
{
  "report_name": "monthly_sales_report",
  "data_sources": [
    {"name": "Sales", "type": "csv", "path": "./data/sales.csv"}
  ],
  "kpis": [
    {"name": "Total Revenue", "value": 500000, "target": 450000},
    {"name": "Total Orders", "value": 1250, "target": 1000}
  ],
  "pivot_tables": [
    {
      "sheet_name": "By_Region",
      "source": "Sales",
      "index": ["Region"],
      "values": ["Revenue"],
      "aggfunc": "sum"
    }
  ]
}
```

### Use Case 2: Inventory Report

```json
{
  "report_name": "inventory_report",
  "data_sources": [
    {"name": "Inventory", "type": "excel", "path": "./data/inventory.xlsx"}
  ],
  "conditional_formatting": [
    {
      "sheet_name": "Inventory",
      "type": "highlight_cells",
      "range": "E2:E1000",
      "operator": "lessThan",
      "threshold": 10,
      "color": "FF0000"
    }
  ]
}
```

### Use Case 3: Multi-Source Analytics

```json
{
  "report_name": "analytics_dashboard",
  "data_sources": [
    {"name": "Sales", "type": "csv", "path": "./data/sales.csv"},
    {"name": "Customers", "type": "excel", "path": "./data/customers.xlsx"},
    {"name": "Products", "type": "json", "path": "./data/products.json"}
  ],
  "kpis": [
    {"name": "Total Customers", "value": 5000, "target": 4500},
    {"name": "Active Products", "value": 250, "target": 200}
  ],
  "email": {
    "enabled": true,
    "recipients": ["manager@company.com", "team@company.com"]
  }
}
```

---

## 🔒 Security Best Practices

1. **Passwords**
   - Use strong passwords for sheet protection
   - Store passwords securely
   - Change passwords regularly

2. **Email Credentials**
   - Use app-specific passwords (not account password)
   - Store credentials in environment variables
   - Never commit credentials to version control

3. **Configuration Files**
   - Add `config/*.json` to `.gitignore`
   - Use separate configs for different environments
   - Keep sensitive data in environment variables

---

## 🐛 Troubleshooting

### Issue: "Data source not found"
**Solution:** Check that file paths in config are correct and files exist

### Issue: "Email sending failed"
**Solution:** 
- Verify SMTP settings
- For Gmail, ensure 2FA is enabled and use App Password
- Check firewall/network settings

### Issue: "Pivot table creation failed"
**Solution:**
- Verify column names exist in source data
- Check that source data name matches data_sources name
- Ensure values columns are numeric for sum/mean operations

### Issue: "Chart not appearing"
**Solution:**
- Verify data_range matches actual data in sheet
- Check that sheet_name exists
- Ensure position cell is valid (e.g., "E2")

### Issue: "Conditional formatting not applied"
**Solution:**
- Verify range format (e.g., "E2:E100")
- Check that sheet_name exists
- Ensure columns have appropriate data types

---

## 📁 Example Project Structure

```
project/
├── generate_excel_report.py
├── config/
│   ├── report_config.json
│   ├── sales_report.json
│   └── inventory_report.json
├── data/
│   ├── sales.csv
│   ├── customers.xlsx
│   └── products.json
└── reports/
    └── (generated reports appear here)
```

---

## 🚀 Advanced Tips

### Tip 1: Dynamic KPI Values

Calculate KPI values from your data before generating the report:

```python
import pandas as pd
from generate_excel_report import ExcelReportGenerator

# Load data
df = pd.read_csv('data/sales.csv')

# Calculate KPIs
total_revenue = df['Revenue'].sum()
total_orders = len(df)

# Update config
config = {
    "kpis": [
        {"name": "Total Revenue", "value": total_revenue, "target": 200000},
        {"name": "Total Orders", "value": total_orders, "target": 500}
    ]
}

# Generate report
generator = ExcelReportGenerator()
generator.config.update(config)
generator.generate_report()
```

### Tip 2: Scheduled Reports

Use cron (Linux/Mac) or Task Scheduler (Windows) to run reports automatically:

```bash
# Cron example - Run every Monday at 9 AM
0 9 * * 1 cd /path/to/project && /path/to/python generate_excel_report.py
```

### Tip 3: Multiple Configurations

Maintain separate configs for different report types:

```bash
python generate_excel_report.py config/daily_report.json
python generate_excel_report.py config/weekly_report.json
python generate_excel_report.py config/monthly_report.json
```

---

## 📚 Additional Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [OpenPyXL Documentation](https://openpyxl.readthedocs.io/)
- [Gmail App Passwords Guide](https://support.google.com/accounts/answer/185833)

---

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review sample configurations
3. Verify data format and structure
4. Check log output for specific error messages
