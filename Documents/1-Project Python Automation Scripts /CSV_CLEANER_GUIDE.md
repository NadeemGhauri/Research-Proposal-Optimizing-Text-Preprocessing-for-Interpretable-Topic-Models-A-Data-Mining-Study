# CSV Data Cleaner - Quick Reference

## Configuration Guide

### Key Configuration Parameters

```python
config = {
    # Columns to check for duplicate rows
    'key_columns': ['id', 'email'],
    
    # Columns containing dates to standardize
    'date_columns': ['created_date', 'last_login', 'signup_date'],
    
    # Output date format (default: YYYY-MM-DD)
    'date_format': '%Y-%m-%d',  # or '%m/%d/%Y', '%d-%b-%Y', etc.
    
    # Columns containing email addresses
    'email_columns': ['email', 'contact_email', 'billing_email'],
    
    # Columns containing phone numbers
    'phone_columns': ['phone', 'mobile', 'work_phone'],
    
    # Text columns to remove special characters from
    'text_columns': ['name', 'address', 'company', 'title'],
    
    # Strategy for handling missing values
    # Options: 'intelligent', 'mean', 'median', 'mode', 'drop'
    'missing_value_strategy': 'intelligent',
}
```

## Common Date Format Codes

| Format Code | Example Output | Description |
|------------|---------------|-------------|
| `%Y-%m-%d` | 2023-01-15 | ISO format (default) |
| `%m/%d/%Y` | 01/15/2023 | US format |
| `%d/%m/%Y` | 15/01/2023 | European format |
| `%b %d, %Y` | Jan 15, 2023 | Month name |
| `%Y%m%d` | 20230115 | Compact format |

## Supported Input Date Formats

The script automatically recognizes and parses these formats:
- `2023-01-15` (ISO format)
- `01/15/2023` (US format)
- `15/01/2023` (European format)
- `Jan 15, 2023` (Month name)
- `January 15, 2023` (Full month)
- `2023.01.15` (Dot-separated)
- `15-Jan-2023` (Day-month-year)
- And many more variations!

## Missing Value Strategies

### `intelligent` (Recommended)
- **Numeric columns**: Fills with median value
- **Text columns**: Fills with most frequent value (mode)
- **Other columns**: Fills with 'Unknown'

### `mean`
- Fills numeric columns with mean (average)
- Text columns with mode

### `median`
- Fills numeric columns with median (middle value)
- Text columns with mode

### `mode`
- Fills all columns with most frequent value

### `drop`
- Removes rows with missing values

## Email Validation Rules

Valid email format requirements:
- Must have `@` symbol
- Must have domain extension (`.com`, `.org`, etc.)
- Can contain: letters, numbers, dots, underscores, hyphens
- Pattern: `username@domain.extension`

Examples:
- ✅ `user@example.com`
- ✅ `john.doe@company.co.uk`
- ✅ `test_user123@test-domain.org`
- ❌ `invalid-email` (no @)
- ❌ `user@domain` (no extension)
- ❌ `@domain.com` (no username)

## Phone Number Validation Rules

Valid phone number requirements:
- 10-15 digits
- Can start with `+` for country code
- Separators allowed: spaces, dashes, parentheses, dots
- These are removed during validation

Examples:
- ✅ `555-123-4567`
- ✅ `(555) 123-4567`
- ✅ `+1-555-123-4567`
- ✅ `555.123.4567`
- ✅ `5551234567`
- ❌ `123` (too short)
- ❌ `abc-def-ghij` (not numeric)

## Special Character Removal

The script removes:
- All non-alphanumeric characters (except spaces)
- Examples: `@`, `#`, `$`, `%`, `&`, `*`, `!`, `?`, etc.
- Extra whitespace is also cleaned up

Examples:
- `John@ Doe!` → `John Doe`
- `Company#123` → `Company123`
- `123  Main  St!` → `123 Main St`

## Usage Examples

### Basic Usage
```bash
python clean_csv_data.py data.csv output/
```

### With Default Sample Data
```bash
python clean_csv_data.py
```

### Programmatic Usage
```python
from clean_csv_data import CSVDataCleaner

config = {
    'key_columns': ['id'],
    'date_columns': ['date'],
    'email_columns': ['email'],
    'phone_columns': ['phone'],
    'text_columns': ['name'],
    'missing_value_strategy': 'intelligent'
}

cleaner = CSVDataCleaner('data.csv', './output', config)
cleaned_file, report = cleaner.clean()
```

## Output Files

The script generates two files:

1. **Cleaned CSV**: `cleaned_<filename>_YYYYMMDD_HHMMSS.csv`
   - Contains the cleaned and validated data
   
2. **Cleaning Report**: `cleaning_report_YYYYMMDD_HHMMSS.txt`
   - Detailed statistics about cleaning operations
   - Data quality improvement metrics

## Cleaning Report Metrics

- **Original Data**: Row and column counts
- **Duplicates Removed**: Number of duplicate rows eliminated
- **Dates Standardized**: Number of date values converted
- **Missing Values Filled**: Number of null values populated
- **Invalid Emails**: Number of invalid email addresses found
- **Invalid Phones**: Number of invalid phone numbers found
- **Special Chars Removed**: Number of values cleaned
- **Final Data**: Row and column counts after cleaning
- **Data Quality Improvement**: Overall improvement percentage

## Best Practices

1. **Always backup your original data** before running the cleaner
2. **Review the cleaning report** to understand what was changed
3. **Test with a small subset** of your data first
4. **Customize the configuration** to match your specific data structure
5. **Validate the output** to ensure cleaning meets your requirements
6. **Use key_columns wisely** - choose columns that truly identify unique records

## Common Workflows

### Workflow 1: Customer Database Cleaning
```python
config = {
    'key_columns': ['customer_id', 'email'],
    'date_columns': ['signup_date', 'last_purchase'],
    'email_columns': ['email'],
    'phone_columns': ['phone'],
    'text_columns': ['first_name', 'last_name', 'address', 'city'],
    'missing_value_strategy': 'intelligent'
}
```

### Workflow 2: Sales Data Cleaning
```python
config = {
    'key_columns': ['order_id'],
    'date_columns': ['order_date', 'ship_date', 'delivery_date'],
    'email_columns': ['customer_email'],
    'phone_columns': ['contact_phone'],
    'text_columns': ['customer_name', 'product_name'],
    'missing_value_strategy': 'drop'  # Remove incomplete orders
}
```

### Workflow 3: Survey Response Cleaning
```python
config = {
    'key_columns': ['response_id'],
    'date_columns': ['submitted_date'],
    'email_columns': ['respondent_email'],
    'phone_columns': [],  # No phone numbers
    'text_columns': ['comments', 'feedback'],
    'missing_value_strategy': 'intelligent'
}
```

## Troubleshooting

**Issue: Too many duplicates removed**
- Review your `key_columns` - they may be too restrictive
- Consider which columns truly define a unique record

**Issue: Dates not parsing correctly**
- Check if dates are in an unusual format
- The script uses fuzzy parsing but some formats may fail
- Consider pre-processing dates in a specific format

**Issue: Valid emails/phones marked as invalid**
- Check the validation rules
- Some international formats may not be recognized
- Consider customizing the validation patterns

**Issue: Important special characters removed**
- Review which columns are in `text_columns`
- Some fields (like codes) should not be cleaned
- Only add columns that truly need cleaning
