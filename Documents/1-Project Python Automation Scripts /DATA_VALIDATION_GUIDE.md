# Data Validation Tool - Complete Guide

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Validation Types](#validation-types)
6. [Configuration Guide](#configuration-guide)
7. [Usage Examples](#usage-examples)
8. [Quality Metrics](#quality-metrics)
9. [Report Formats](#report-formats)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

---

## Overview

The Data Validation Tool is a comprehensive Python solution for automated data quality checking. It validates data against multiple rules, generates quality scores, and produces detailed reports.

### Key Capabilities
- **9 Validation Types**: Type checking, ranges, mandatory fields, uniqueness, patterns, allowed values, string lengths, cross-field rules, business logic
- **Quality Scoring**: 0-100 score with completeness, consistency, and validity sub-scores
- **Detailed Reports**: Text and JSON formats with error listings and statistics
- **Flexible Configuration**: JSON-based rule definitions with custom functions
- **Multiple Formats**: Supports CSV, Excel, and JSON data sources

---

## Features

### Data Type Validation
Ensures columns contain expected data types:
- **int**: Integer values
- **float**: Floating-point numbers
- **string**: Text data
- **bool**: Boolean values (True/False)
- **date**: Date/datetime values

### Range Validation
Checks numerical values fall within specified ranges:
- Minimum and maximum value enforcement
- Support for age, salary, price, quantity, etc.
- Configurable per-column ranges

### Mandatory Field Validation
Verifies required fields are not null or empty:
- Detects null values
- Identifies empty strings
- Ensures data completeness

### Uniqueness Validation
Enforces unique values in specified columns:
- Detects duplicate IDs
- Validates unique identifiers
- Finds redundant email addresses

### Pattern Validation
Validates data against regex patterns:
- Email format validation
- Phone number formats
- Custom regex patterns
- SKU/product code validation

### Allowed Values Validation
Restricts columns to predefined value sets:
- Status codes (active, inactive, etc.)
- Department names
- Categories and classifications
- Enum-like constraints

### String Length Validation
Enforces minimum and maximum string lengths:
- Name length constraints
- Description size limits
- Code/identifier format enforcement

### Cross-Field Validation
Validates relationships between multiple columns:
- Start date before end date
- Minimum age for certain roles
- Salary ranges based on level
- Custom multi-column rules

### Business Rule Validation
Applies custom business logic:
- Complex conditional rules
- Domain-specific validations
- Multi-step validation logic
- Custom Python functions

---

## Installation

### Prerequisites
```bash
Python 3.7+
pandas
numpy
```

### Install Dependencies
```bash
pip install pandas numpy
```

### Download Script
```bash
# Clone or download data_validation.py
python data_validation.py --help
```

---

## Quick Start

### 1. Prepare Your Data
Create a CSV file with your data:

```csv
id,name,email,age,salary,status
1,Alice,alice@example.com,25,50000,active
2,Bob,bob@example.com,30,60000,active
3,Charlie,charlie@example.com,35,75000,inactive
```

### 2. Define Validation Rules
Create a rules dictionary:

```python
rules = {
    'data_types': {
        'id': 'int',
        'name': 'string',
        'email': 'string',
        'age': 'int',
        'salary': 'float',
        'status': 'string'
    },
    'range_rules': {
        'age': (18, 100),
        'salary': (0, 1000000)
    },
    'mandatory_fields': ['id', 'name', 'email'],
    'unique_fields': ['id', 'email'],
    'regex_patterns': {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    },
    'allowed_values': {
        'status': ['active', 'inactive', 'pending']
    }
}
```

### 3. Run Validation
```python
from data_validation import DataValidator

# Create validator
validator = DataValidator('data.csv', rules)

# Run validation
validator.validate()

# View quality score
print(f"Quality Score: {validator.quality_metrics['overall_score']}/100")
```

---

## Validation Types

### 1. Data Type Validation

**Purpose**: Ensure columns contain correct data types

**Configuration**:
```python
'data_types': {
    'id': 'int',
    'price': 'float',
    'name': 'string',
    'created_at': 'date',
    'is_active': 'bool'
}
```

**Supported Types**:
- `int`: Integer values (1, 2, 3)
- `float`: Decimal numbers (1.5, 2.75)
- `string`: Text data ("hello", "world")
- `bool`: Boolean values (True, False)
- `date`: Date/datetime values ("2024-01-01", "2024-01-01 12:00:00")

**Example Errors**:
```
Row 5, Column 'age': Expected int, got string ('twenty-five')
Row 8, Column 'is_active': Expected bool, got string ('yes')
```

---

### 2. Range Validation

**Purpose**: Ensure numerical values fall within acceptable ranges

**Configuration**:
```python
'range_rules': {
    'age': (18, 100),           # Age between 18 and 100
    'salary': (0, 1000000),     # Salary 0 to 1 million
    'quantity': (1, 1000),      # Quantity 1 to 1000
    'discount': (0.0, 100.0)    # Discount 0% to 100%
}
```

**Format**: `column_name: (min_value, max_value)`

**Example Errors**:
```
Row 3, Column 'age': Value 150 outside range [18, 100]
Row 7, Column 'salary': Value -5000 outside range [0, 1000000]
```

---

### 3. Mandatory Field Validation

**Purpose**: Ensure required fields are not null or empty

**Configuration**:
```python
'mandatory_fields': ['id', 'name', 'email', 'status']
```

**Checks For**:
- Null values (None, NaN)
- Empty strings ('')
- Whitespace-only strings ('   ')

**Example Errors**:
```
Row 4, Column 'name': Mandatory field is missing
Row 9, Column 'email': Mandatory field is empty
```

---

### 4. Uniqueness Validation

**Purpose**: Ensure specified columns contain unique values

**Configuration**:
```python
'unique_fields': ['id', 'email', 'username', 'sku']
```

**Example Errors**:
```
Row 5, Column 'id': Duplicate value '1001' (also in rows: 2)
Row 8, Column 'email': Duplicate value 'john@example.com' (also in rows: 3, 5)
```

---

### 5. Pattern Validation

**Purpose**: Validate data against regex patterns

**Configuration**:
```python
'regex_patterns': {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone': r'^\d{3}-\d{3}-\d{4}$',
    'zip_code': r'^\d{5}(-\d{4})?$',
    'sku': r'^[A-Z]{2}\d{6}$'
}
```

**Common Patterns**:

**Email**:
```python
r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
```

**Phone (US)**:
```python
r'^\d{3}-\d{3}-\d{4}$'  # 123-456-7890
r'^\(\d{3}\) \d{3}-\d{4}$'  # (123) 456-7890
```

**ZIP Code**:
```python
r'^\d{5}(-\d{4})?$'  # 12345 or 12345-6789
```

**Example Errors**:
```
Row 6, Column 'email': Value 'invalid.email' does not match pattern
Row 10, Column 'phone': Value '1234567890' does not match pattern ^\d{3}-\d{3}-\d{4}$
```

---

### 6. Allowed Values Validation

**Purpose**: Restrict columns to predefined value sets

**Configuration**:
```python
'allowed_values': {
    'status': ['active', 'inactive', 'pending', 'suspended'],
    'department': ['IT', 'HR', 'Sales', 'Marketing', 'Finance'],
    'priority': ['low', 'medium', 'high', 'critical'],
    'size': ['S', 'M', 'L', 'XL', 'XXL']
}
```

**Example Errors**:
```
Row 3, Column 'status': Value 'archived' not in allowed values: ['active', 'inactive', 'pending', 'suspended']
Row 7, Column 'department': Value 'Engineering' not in allowed values: ['IT', 'HR', 'Sales', 'Marketing', 'Finance']
```

---

### 7. String Length Validation

**Purpose**: Enforce minimum and maximum string lengths

**Configuration**:
```python
'string_lengths': {
    'name': (2, 50),              # Names: 2-50 characters
    'description': (10, 500),     # Descriptions: 10-500 characters
    'sku': (8, 8),                # SKU: exactly 8 characters
    'comment': (0, 200)           # Comments: up to 200 characters
}
```

**Format**: `column_name: (min_length, max_length)`

**Example Errors**:
```
Row 2, Column 'name': Length 1 outside range [2, 50]
Row 5, Column 'description': Length 502 outside range [10, 500]
```

---

### 8. Cross-Field Validation

**Purpose**: Validate relationships between multiple columns

**Configuration**:
```python
def validate_dates(row):
    """Start date must be before end date."""
    try:
        start = pd.to_datetime(row['start_date'])
        end = pd.to_datetime(row['end_date'])
        
        if start >= end:
            return False, f"Start date ({row['start_date']}) must be before end date ({row['end_date']})"
        
        return True, None
    except:
        return True, None

'cross_field_rules': [
    {
        'name': 'Start Date Before End Date',
        'function': validate_dates
    }
]
```

**Rule Function Format**:
```python
def validation_function(row):
    """
    Args:
        row: pandas Series with row data
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    # Validation logic
    if condition_failed:
        return False, "Error message"
    return True, None
```

**Example Rules**:

**Age Eligibility**:
```python
def validate_age_eligibility(row):
    """Employees under 25 cannot be managers."""
    if row.get('age', 0) < 25 and row.get('role') == 'manager':
        return False, f"Employee age {row['age']} too young for manager role"
    return True, None
```

**Price Discount**:
```python
def validate_discount(row):
    """Discounted price must be less than original price."""
    original = float(row.get('price', 0))
    discounted = float(row.get('discounted_price', 0))
    
    if discounted >= original:
        return False, f"Discounted price ({discounted}) must be less than price ({original})"
    return True, None
```

---

### 9. Business Rule Validation

**Purpose**: Apply custom business logic

**Configuration**:
```python
def validate_senior_salary(row):
    """Senior employees must earn at least $50,000."""
    if row.get('level') == 'senior':
        salary = float(row.get('salary', 0))
        if salary < 50000:
            return False, f"Senior salary {salary} below minimum 50000"
    return True, None

'business_rules': [
    {
        'name': 'Minimum Salary for Seniors',
        'function': validate_senior_salary
    }
]
```

**Example Business Rules**:

**Approval Authority**:
```python
def validate_approval_amount(row):
    """Managers can approve up to $10,000, directors up to $100,000."""
    amount = float(row.get('amount', 0))
    role = row.get('role', '')
    
    if role == 'manager' and amount > 10000:
        return False, f"Manager cannot approve ${amount} (limit: $10,000)"
    elif role == 'director' and amount > 100000:
        return False, f"Director cannot approve ${amount} (limit: $100,000)"
    
    return True, None
```

**Age-Salary Ratio**:
```python
def validate_age_salary_ratio(row):
    """Salary should be at least $1,000 per year of age."""
    age = int(row.get('age', 0))
    salary = float(row.get('salary', 0))
    
    min_expected = age * 1000
    if salary > 0 and salary < min_expected:
        return False, f"Salary {salary} low for age {age} (expected >= {min_expected})"
    
    return True, None
```

**Vacation Days**:
```python
def validate_vacation_days(row):
    """Vacation days based on years of service."""
    years = int(row.get('years_of_service', 0))
    vacation = int(row.get('vacation_days', 0))
    
    if years < 2 and vacation > 10:
        return False, f"New employees (< 2 years) limited to 10 vacation days"
    elif years < 5 and vacation > 15:
        return False, f"Employees (< 5 years) limited to 15 vacation days"
    
    return True, None
```

---

## Configuration Guide

### Complete Configuration Example

```python
from data_validation import DataValidator
import pandas as pd

# Define cross-field validation functions
def validate_date_range(row):
    """Start date before end date."""
    try:
        start = pd.to_datetime(row['start_date'])
        end = pd.to_datetime(row['end_date'])
        if start >= end:
            return False, f"Start date must be before end date"
        return True, None
    except:
        return True, None

def validate_price_discount(row):
    """Discounted price less than original."""
    try:
        price = float(row.get('price', 0))
        discounted = float(row.get('discounted_price', 0))
        if discounted >= price:
            return False, f"Discounted price must be less than original"
        return True, None
    except:
        return True, None

# Define business rule functions
def validate_manager_salary(row):
    """Managers earn at least $60,000."""
    if row.get('role') == 'manager':
        salary = float(row.get('salary', 0))
        if salary < 60000:
            return False, f"Manager salary must be >= $60,000"
    return True, None

def validate_experience_level(row):
    """Senior level requires 5+ years experience."""
    if row.get('level') == 'senior':
        experience = int(row.get('years_experience', 0))
        if experience < 5:
            return False, f"Senior level requires 5+ years experience"
    return True, None

# Complete validation rules
rules = {
    # Data type validation
    'data_types': {
        'id': 'int',
        'name': 'string',
        'email': 'string',
        'age': 'int',
        'salary': 'float',
        'is_active': 'bool',
        'start_date': 'date',
        'end_date': 'date',
        'role': 'string',
        'level': 'string',
        'years_experience': 'int',
        'price': 'float',
        'discounted_price': 'float'
    },
    
    # Range validation
    'range_rules': {
        'age': (18, 100),
        'salary': (20000, 500000),
        'years_experience': (0, 50),
        'price': (0.01, 10000),
        'discounted_price': (0.01, 10000)
    },
    
    # Mandatory fields
    'mandatory_fields': [
        'id', 'name', 'email', 'role', 'is_active'
    ],
    
    # Unique fields
    'unique_fields': ['id', 'email'],
    
    # Regex patterns
    'regex_patterns': {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'phone': r'^\d{3}-\d{3}-\d{4}$'
    },
    
    # Allowed values
    'allowed_values': {
        'role': ['employee', 'manager', 'director', 'executive'],
        'level': ['junior', 'mid', 'senior', 'lead'],
        'department': ['IT', 'HR', 'Sales', 'Marketing', 'Finance']
    },
    
    # String lengths
    'string_lengths': {
        'name': (2, 50),
        'description': (10, 500)
    },
    
    # Cross-field rules
    'cross_field_rules': [
        {'name': 'Date Range Validation', 'function': validate_date_range},
        {'name': 'Price Discount Validation', 'function': validate_price_discount}
    ],
    
    # Business rules
    'business_rules': [
        {'name': 'Manager Salary Minimum', 'function': validate_manager_salary},
        {'name': 'Experience Level Requirement', 'function': validate_experience_level}
    ]
}

# Create validator and run
validator = DataValidator('employee_data.csv', rules)
validator.validate()

# View results
print(f"Quality Score: {validator.quality_metrics['overall_score']}/100")
print(f"Total Errors: {validator.total_errors}")
```

---

## Usage Examples

### Example 1: Basic Employee Data Validation

```python
from data_validation import DataValidator

# Simple rules for employee data
rules = {
    'data_types': {
        'employee_id': 'int',
        'name': 'string',
        'email': 'string',
        'department': 'string'
    },
    'mandatory_fields': ['employee_id', 'name', 'email'],
    'unique_fields': ['employee_id', 'email'],
    'regex_patterns': {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    },
    'allowed_values': {
        'department': ['IT', 'HR', 'Sales', 'Marketing']
    }
}

# Validate
validator = DataValidator('employees.csv', rules)
validator.validate()

# Check results
if validator.quality_metrics['overall_score'] >= 95:
    print("✓ Data quality excellent!")
else:
    print(f"⚠ Issues found: {validator.total_errors} errors")
    print(f"Check report: {validator.report_file}")
```

### Example 2: Sales Data with Business Rules

```python
from data_validation import DataValidator
import pandas as pd

# Business rule: discount cannot exceed 50%
def validate_discount_limit(row):
    try:
        price = float(row.get('price', 0))
        discounted = float(row.get('discounted_price', 0))
        discount_pct = ((price - discounted) / price) * 100
        
        if discount_pct > 50:
            return False, f"Discount {discount_pct:.1f}% exceeds 50% limit"
        return True, None
    except:
        return True, None

rules = {
    'data_types': {
        'order_id': 'int',
        'product_sku': 'string',
        'quantity': 'int',
        'price': 'float',
        'discounted_price': 'float'
    },
    'range_rules': {
        'quantity': (1, 1000),
        'price': (0.01, 10000)
    },
    'unique_fields': ['order_id'],
    'business_rules': [
        {'name': 'Discount Limit', 'function': validate_discount_limit}
    ]
}

validator = DataValidator('sales_data.csv', rules)
validator.validate()
print(f"Quality: {validator.quality_metrics['overall_score']}/100")
```

### Example 3: Product Inventory Validation

```python
from data_validation import DataValidator

rules = {
    'data_types': {
        'sku': 'string',
        'product_name': 'string',
        'quantity': 'int',
        'reorder_level': 'int',
        'price': 'float',
        'category': 'string'
    },
    'mandatory_fields': ['sku', 'product_name', 'price'],
    'unique_fields': ['sku'],
    'range_rules': {
        'quantity': (0, 10000),
        'reorder_level': (1, 1000),
        'price': (0.01, 100000)
    },
    'regex_patterns': {
        'sku': r'^[A-Z]{2}\d{6}$'  # Format: AB123456
    },
    'allowed_values': {
        'category': ['Electronics', 'Clothing', 'Food', 'Books', 'Toys']
    },
    'string_lengths': {
        'product_name': (3, 100)
    }
}

validator = DataValidator('inventory.csv', rules)
validator.validate()

# Low stock items with validation errors
if validator.total_errors > 0:
    print(f"⚠ {validator.total_errors} data quality issues found")
    print(f"Review: {validator.report_file}")
```

### Example 4: Customer Data with Complex Rules

```python
from data_validation import DataValidator
import pandas as pd

# Cross-field rule: billing address required if shipping differs
def validate_addresses(row):
    shipping = str(row.get('shipping_address', '')).strip()
    billing = str(row.get('billing_address', '')).strip()
    same_as_shipping = row.get('billing_same_as_shipping', False)
    
    if not same_as_shipping and not billing:
        return False, "Billing address required when different from shipping"
    return True, None

# Business rule: premium customers get priority
def validate_customer_tier(row):
    total_purchases = float(row.get('total_purchases', 0))
    tier = row.get('customer_tier', '')
    
    if total_purchases >= 10000 and tier != 'premium':
        return False, f"Customer with ${total_purchases} purchases should be premium tier"
    elif total_purchases < 1000 and tier == 'premium':
        return False, f"Premium tier requires $1000+ in purchases"
    return True, None

rules = {
    'data_types': {
        'customer_id': 'int',
        'name': 'string',
        'email': 'string',
        'phone': 'string',
        'total_purchases': 'float',
        'customer_tier': 'string',
        'billing_same_as_shipping': 'bool'
    },
    'mandatory_fields': ['customer_id', 'name', 'email', 'shipping_address'],
    'unique_fields': ['customer_id', 'email'],
    'regex_patterns': {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'phone': r'^\d{3}-\d{3}-\d{4}$'
    },
    'allowed_values': {
        'customer_tier': ['standard', 'gold', 'premium']
    },
    'cross_field_rules': [
        {'name': 'Billing Address Validation', 'function': validate_addresses}
    ],
    'business_rules': [
        {'name': 'Customer Tier Validation', 'function': validate_customer_tier}
    ]
}

validator = DataValidator('customers.csv', rules)
validator.validate()
print(f"Data Quality Score: {validator.quality_metrics['overall_score']}/100")
```

---

## Quality Metrics

### Quality Score Calculation

The overall quality score (0-100) is calculated from three sub-scores:

**Overall Score = (Completeness + Consistency + Validity) / 3**

### 1. Completeness Score
Measures how many mandatory fields are filled.

```
Completeness = (Total mandatory cells - Missing values) / Total mandatory cells * 100
```

**Example**:
- 4 mandatory fields × 100 rows = 400 cells
- 10 missing values
- Completeness = (400 - 10) / 400 × 100 = 97.5%

### 2. Consistency Score
Measures data type consistency and uniqueness.

```
Consistency = (Total cells - Type/Uniqueness errors) / Total cells * 100
```

**Example**:
- 1200 total cells
- 8 type errors
- 4 uniqueness errors
- Consistency = (1200 - 12) / 1200 × 100 = 99%

### 3. Validity Score
Measures compliance with all validation rules.

```
Validity = (Total rows - Validation errors) / Total rows * 100
```

**Example**:
- 100 rows
- 15 validation errors (range, pattern, business rules)
- Validity = (100 - 15) / 100 × 100 = 85%

### Quality Score Interpretation

| Score Range | Quality Level | Action Required |
|-------------|---------------|-----------------|
| 95-100 | Excellent | No action needed |
| 85-94 | Good | Minor cleanup recommended |
| 70-84 | Fair | Review and fix issues |
| 50-69 | Poor | Significant cleanup needed |
| 0-49 | Critical | Major data quality issues |

### Example Quality Metrics

```python
validator.quality_metrics = {
    'overall_score': 87.5,
    'completeness': 95.0,      # 95% mandatory fields filled
    'consistency': 92.0,       # 92% data consistent
    'validity': 85.0,          # 85% rows pass all rules
    'total_rows': 100,
    'total_errors': 18
}
```

---

## Report Formats

### Text Report Format

**Location**: `validation_reports/validation_report_YYYYMMDD_HHMMSS.txt`

**Example**:
```
================================================================================
DATA VALIDATION REPORT
================================================================================

Generated: 2024-11-20 08:00:00
Data Source: employee_data.csv
Total Rows: 100
Total Columns: 12

================================================================================
QUALITY METRICS
================================================================================

Overall Quality Score: 87.50/100

Breakdown:
  Completeness:  95.00/100
  Consistency:   92.00/100
  Validity:      85.00/100

Total Errors: 18

================================================================================
VALIDATION SUMMARY
================================================================================

✓ Data Type Errors:        3
✓ Range Errors:            5
✓ Mandatory Field Errors:  2
✓ Uniqueness Errors:       2
✓ Pattern Errors:          2
✓ Allowed Value Errors:    1
✓ String Length Errors:    1
✓ Cross-Field Errors:      1
✓ Business Rule Errors:    1

================================================================================
DETAILED ERROR REPORT
================================================================================

--- Data Type Errors ---
Row 5, Column 'age': Expected int, got string ('twenty-five')
Row 12, Column 'salary': Expected float, got string ('60k')
Row 18, Column 'is_active': Expected bool, got string ('yes')

--- Range Errors ---
Row 3, Column 'age': Value 150 outside range [18, 100]
Row 7, Column 'salary': Value -5000 outside range [0, 1000000]
Row 15, Column 'age': Value 10 outside range [18, 100]
Row 22, Column 'salary': Value 1500000 outside range [0, 1000000]
Row 28, Column 'age': Value -5 outside range [18, 100]

--- Mandatory Field Errors ---
Row 8, Column 'name': Mandatory field is missing
Row 19, Column 'email': Mandatory field is empty

--- Uniqueness Errors ---
Row 5, Column 'id': Duplicate value '1003' (also in rows: 3)
Row 10, Column 'email': Duplicate value 'john@example.com' (also in rows: 7)

--- Pattern Errors ---
Row 6, Column 'email': Value 'charlie.example.com' does not match pattern
Row 15, Column 'phone': Value '1234567890' does not match pattern ^\d{3}-\d{3}-\d{4}$

--- Allowed Value Errors ---
Row 9, Column 'status': Value 'suspended' not in allowed values: ['active', 'inactive', 'pending']

--- String Length Errors ---
Row 2, Column 'name': Length 1 outside range [2, 50]

--- Cross-Field Errors ---
Row 11: Start Date Before End Date - Start date (2020-03-01) must be before end date (2019-12-01)

--- Business Rule Errors ---
Row 14: Minimum Salary for Seniors - Senior salary 45000 below minimum 50000

================================================================================
RECOMMENDATIONS
================================================================================

1. Fix 3 data type errors - ensure correct formats
2. Review 5 range violations - check for data entry errors
3. Fill 2 mandatory fields - complete required information
4. Resolve 2 duplicate values - ensure uniqueness
5. Correct 2 pattern mismatches - validate formats
6. Update 1 invalid values - use allowed values only
7. Adjust 1 string length issues - meet length requirements
8. Review 1 cross-field issues - check related fields
9. Address 1 business rule violations - comply with business logic

Quality Score: 87.50/100 (Good - Minor cleanup recommended)

================================================================================
END OF REPORT
================================================================================
```

### JSON Report Format

**Location**: `validation_reports/validation_report_YYYYMMDD_HHMMSS.json`

**Example**:
```json
{
  "metadata": {
    "generated_at": "2024-11-20T08:00:00",
    "data_source": "employee_data.csv",
    "total_rows": 100,
    "total_columns": 12
  },
  "quality_metrics": {
    "overall_score": 87.5,
    "completeness": 95.0,
    "consistency": 92.0,
    "validity": 85.0,
    "total_errors": 18
  },
  "validation_summary": {
    "data_type_errors": 3,
    "range_errors": 5,
    "mandatory_field_errors": 2,
    "uniqueness_errors": 2,
    "pattern_errors": 2,
    "allowed_value_errors": 1,
    "string_length_errors": 1,
    "cross_field_errors": 1,
    "business_rule_errors": 1
  },
  "detailed_errors": {
    "data_type_errors": [
      {
        "row": 5,
        "column": "age",
        "value": "twenty-five",
        "expected_type": "int",
        "error": "Expected int, got string ('twenty-five')"
      }
    ],
    "range_errors": [
      {
        "row": 3,
        "column": "age",
        "value": 150,
        "min": 18,
        "max": 100,
        "error": "Value 150 outside range [18, 100]"
      }
    ],
    "mandatory_field_errors": [
      {
        "row": 8,
        "column": "name",
        "error": "Mandatory field is missing"
      }
    ],
    "uniqueness_errors": [
      {
        "row": 5,
        "column": "id",
        "value": "1003",
        "duplicate_rows": [3],
        "error": "Duplicate value '1003' (also in rows: 3)"
      }
    ]
  }
}
```

---

## Best Practices

### 1. Start Simple, Add Complexity
Begin with basic validations and gradually add more rules:

```python
# Phase 1: Basic validation
rules_v1 = {
    'data_types': {...},
    'mandatory_fields': [...]
}

# Phase 2: Add constraints
rules_v2 = {
    **rules_v1,
    'range_rules': {...},
    'unique_fields': [...]
}

# Phase 3: Add business logic
rules_v3 = {
    **rules_v2,
    'business_rules': [...]
}
```

### 2. Use Meaningful Error Messages
Make validation functions return clear, actionable errors:

```python
# Bad
return False, "Invalid"

# Good
return False, f"Salary {salary} below minimum {min_salary} for {role} role"
```

### 3. Handle Edge Cases
Add try-except blocks to validation functions:

```python
def validate_rule(row):
    try:
        # Validation logic
        if condition:
            return False, "Error message"
        return True, None
    except Exception as e:
        # Log error but don't fail validation
        return True, None  # Or return False with specific error
```

### 4. Test Validation Rules
Create test data with known issues:

```python
# Test data with intentional errors
test_data = {
    'id': [1, 2, 2],  # Duplicate
    'age': [25, 150, -5],  # Out of range
    'email': ['valid@email.com', 'invalid', None]  # Invalid format, missing
}
```

### 5. Monitor Quality Trends
Track quality scores over time:

```python
# Save quality scores
history = []
for file in data_files:
    validator = DataValidator(file, rules)
    validator.validate()
    history.append({
        'file': file,
        'score': validator.quality_metrics['overall_score'],
        'date': datetime.now()
    })

# Analyze trends
df = pd.DataFrame(history)
df.plot(x='date', y='score')
```

### 6. Use Configuration Files
Store rules in JSON for reusability:

```json
{
  "data_types": {
    "id": "int",
    "name": "string"
  },
  "mandatory_fields": ["id", "name"],
  "range_rules": {
    "age": [18, 100]
  }
}
```

```python
import json

with open('validation_rules.json', 'r') as f:
    rules = json.load(f)
    
validator = DataValidator('data.csv', rules)
```

### 7. Document Business Rules
Add docstrings to validation functions:

```python
def validate_senior_salary(row):
    """
    Validate minimum salary for senior employees.
    
    Business Rule: Senior employees must earn at least $50,000.
    
    Args:
        row: pandas Series with employee data
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if row.get('level') == 'senior':
        salary = float(row.get('salary', 0))
        if salary < 50000:
            return False, f"Senior salary {salary} below minimum 50000"
    return True, None
```

---

## Troubleshooting

### Issue: "Module not found" Error

**Problem**: `ModuleNotFoundError: No module named 'pandas'`

**Solution**:
```bash
pip install pandas numpy
```

### Issue: Date Parsing Errors

**Problem**: `ValueError: Unknown string format: '2024-13-45'`

**Solution**: Use try-except in validation functions:
```python
def validate_dates(row):
    try:
        start = pd.to_datetime(row['start_date'])
        end = pd.to_datetime(row['end_date'])
        # Validation logic
    except:
        return True, None  # Skip if dates can't be parsed
```

### Issue: Memory Error with Large Files

**Problem**: `MemoryError` when loading large CSV files

**Solution**: Process in chunks:
```python
# Instead of loading entire file
# validator = DataValidator('huge_file.csv', rules)

# Use chunking
chunk_size = 10000
for chunk in pd.read_csv('huge_file.csv', chunksize=chunk_size):
    # Validate each chunk
    validator = DataValidator(chunk, rules)
    validator.validate()
```

### Issue: Too Many Errors in Report

**Problem**: Report is too long with thousands of errors

**Solution**: Limit errors per category:
```python
# In data_validation.py, modify error reporting
MAX_ERRORS_PER_CATEGORY = 50

# Only show first 50 errors of each type
for error_type in validation_results:
    errors = validation_results[error_type][:MAX_ERRORS_PER_CATEGORY]
    # Report errors
```

### Issue: False Positives in Validation

**Problem**: Valid data flagged as errors

**Solution**: Adjust validation rules:
```python
# Too strict
'range_rules': {'age': (18, 65)}  # Excludes valid ages > 65

# Better
'range_rules': {'age': (18, 100)}  # Allows wider range
```

### Issue: Slow Validation Performance

**Problem**: Validation takes too long

**Solutions**:
1. **Optimize regex patterns** - Use simpler patterns
2. **Reduce business rules** - Combine or simplify rules
3. **Parallelize validation** - Use multiprocessing
4. **Cache results** - Store intermediate results

### Issue: Incorrect Quality Score

**Problem**: Quality score doesn't match expectations

**Solution**: Review calculation:
```python
# Check individual scores
print(f"Completeness: {validator.quality_metrics['completeness']}")
print(f"Consistency: {validator.quality_metrics['consistency']}")
print(f"Validity: {validator.quality_metrics['validity']}")

# Verify error counts
print(f"Total Errors: {validator.total_errors}")
print(f"Total Rows: {len(validator.df)}")
```

---

## Advanced Topics

### Custom Validation Functions

Create reusable validation libraries:

```python
# validation_library.py
import pandas as pd
import re

def create_email_validator(domain=None):
    """Factory function for email validation."""
    def validate_email(row):
        email = row.get('email', '')
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, str(email)):
            return False, f"Invalid email format: {email}"
        
        if domain and not email.endswith(f'@{domain}'):
            return False, f"Email must be from domain {domain}"
        
        return True, None
    return validate_email

def create_range_validator(column, min_val, max_val):
    """Factory function for range validation."""
    def validate_range(row):
        value = row.get(column, 0)
        try:
            value = float(value)
            if value < min_val or value > max_val:
                return False, f"{column} {value} outside range [{min_val}, {max_val}]"
            return True, None
        except:
            return True, None
    return validate_range

# Usage
rules = {
    'cross_field_rules': [
        {'name': 'Company Email', 'function': create_email_validator('company.com')},
        {'name': 'Age Range', 'function': create_range_validator('age', 18, 100)}
    ]
}
```

### Batch Processing Multiple Files

```python
import glob
from pathlib import Path

# Process all CSV files in a folder
data_folder = Path('./data')
results = []

for file in data_folder.glob('*.csv'):
    print(f"Validating {file.name}...")
    
    validator = DataValidator(str(file), rules)
    validator.validate()
    
    results.append({
        'file': file.name,
        'quality_score': validator.quality_metrics['overall_score'],
        'total_errors': validator.total_errors
    })

# Summary report
df_results = pd.DataFrame(results)
print(df_results.sort_values('quality_score'))
```

### Integration with Data Pipelines

```python
def validate_pipeline_data(df, rules, min_quality=90):
    """
    Validate data in a pipeline with quality threshold.
    
    Args:
        df: pandas DataFrame
        rules: validation rules
        min_quality: minimum acceptable quality score
        
    Returns:
        bool: True if data passes quality threshold
        
    Raises:
        ValueError: if quality below threshold
    """
    validator = DataValidator(df, rules)
    validator.validate()
    
    quality = validator.quality_metrics['overall_score']
    
    if quality < min_quality:
        raise ValueError(
            f"Data quality {quality:.1f} below threshold {min_quality}. "
            f"Errors: {validator.total_errors}. "
            f"Report: {validator.report_file}"
        )
    
    return True

# Pipeline usage
try:
    # Extract
    df = pd.read_csv('source_data.csv')
    
    # Validate
    validate_pipeline_data(df, rules, min_quality=95)
    
    # Transform & Load (only if validation passed)
    process_data(df)
    
except ValueError as e:
    print(f"Pipeline failed: {e}")
    # Send alert, log error, etc.
```

---

## Conclusion

The Data Validation Tool provides comprehensive data quality checking with:
- 9 types of validation rules
- Quality scoring (0-100 scale)
- Detailed error reporting
- Flexible configuration
- Custom business logic support

For questions or issues, review the test suite in `test_validation.py` for examples.

---

**Version**: 1.0  
**Last Updated**: November 2024  
**Author**: Python Automation Scripts Project
