# Bulk File Renamer - Complete Guide

A powerful and flexible tool for batch renaming files with pattern support, preview mode, and undo functionality.

---

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Renaming Operations](#renaming-operations)
  - [Sequential Numbering](#sequential-numbering)
  - [Find and Replace](#find-and-replace)
  - [Prefix and Suffix](#prefix-and-suffix)
  - [Case Changes](#case-changes)
  - [Remove Special Characters](#remove-special-characters)
- [Configuration](#configuration)
- [Advanced Usage](#advanced-usage)
- [Undo Functionality](#undo-functionality)
- [Use as Python Module](#use-as-python-module)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## Features

- ✅ **6 Renaming Operations**
  - Sequential numbering with custom patterns
  - Find and replace (with regex support)
  - Add prefix/suffix (static or dynamic)
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

- ✅ **Professional Features**
  - Detailed operation reports
  - Comprehensive logging
  - Statistics tracking
  - JSON-based undo history

---

## Installation

**Prerequisites:**
- Python 3.7 or higher
- No additional dependencies required (uses only standard library)

**Installation:**
```bash
# No installation needed - just run the script!
python bulk_rename.py /path/to/folder
```

---

## Quick Start

### 1. Preview Changes (Safe Mode)

```bash
# Preview rename operations (no actual changes)
python bulk_rename.py /path/to/folder
```

### 2. Common Use Cases

```python
from bulk_rename import BulkFileRenamer

# Remove special characters
config = {'preview_mode': True}
renamer = BulkFileRenamer('./my_files', config)
renamer.rename('remove_special', keep_chars='_-', replace_with='_')

# Add sequential numbers
renamer.rename('sequential', pattern='file_{counter}', start=1, padding=3)

# Change to lowercase
renamer.rename('case_change', case_type='lower')
```

### 3. Execute Actual Rename

```python
# Disable preview mode to actually rename files
config = {'preview_mode': False, 'create_undo_file': True}
renamer = BulkFileRenamer('./my_files', config)
renamer.rename('case_change', case_type='lower')
```

---

## Renaming Operations

### Sequential Numbering

Add sequential numbers to filenames with custom patterns.

**Parameters:**
- `pattern` (str): Naming pattern with placeholders
  - `{name}`: Original filename
  - `{counter}`: Sequential number
  - `{ext}`: File extension (without dot)
- `start` (int): Starting number (default: 1)
- `step` (int): Increment step (default: 1)
- `padding` (int): Number of digits with zero-padding (default: 3)

**Examples:**

```python
# Pattern: file_001.txt, file_002.txt, ...
renamer.rename('sequential', 
    pattern='file_{counter}',
    start=1,
    padding=3
)

# Pattern: Photo_0010.jpg, Photo_0020.jpg, ...
renamer.rename('sequential',
    pattern='Photo_{counter}',
    start=10,
    step=10,
    padding=4
)

# Pattern: document_001_backup.pdf
renamer.rename('sequential',
    pattern='document_{counter}_backup',
    start=1,
    padding=3
)

# Keep original name: report_001.txt, invoice_002.txt
renamer.rename('sequential',
    pattern='{name}_{counter}',
    start=1,
    padding=3
)
```

**Before/After Examples:**
```
report.txt           -> file_001.txt
invoice.pdf          -> file_002.pdf
data.csv             -> file_003.csv
```

---

### Find and Replace

Find and replace text in filenames with support for regex and case-insensitive matching.

**Parameters:**
- `find` (str): Text to find (or regex pattern)
- `replace` (str): Replacement text
- `use_regex` (bool): Use regular expressions (default: False)
- `case_sensitive` (bool): Case-sensitive matching (default: True)

**Examples:**

```python
# Simple replacement
renamer.rename('find_replace',
    find='2024',
    replace='2025',
    case_sensitive=True
)

# Case-insensitive replacement
renamer.rename('find_replace',
    find='backup',
    replace='archive',
    case_sensitive=False
)

# Regex: Remove numbers
renamer.rename('find_replace',
    find=r'\d+',
    replace='',
    use_regex=True
)

# Regex: Replace spaces and dashes with underscores
renamer.rename('find_replace',
    find=r'[\s-]+',
    replace='_',
    use_regex=True
)

# Regex: Extract date pattern
renamer.rename('find_replace',
    find=r'(\d{4})-(\d{2})-(\d{2})',
    replace=r'\1\2\3',
    use_regex=True
)
```

**Before/After Examples:**
```
Simple:
report_2024.txt         -> report_2025.txt
backup_2024_jan.pdf     -> backup_2025_jan.pdf

Regex:
file 123.txt            -> file.txt
data-2024-01-15.csv     -> data_20240115.csv
My Document (1).txt     -> My Document.txt
```

---

### Prefix and Suffix

Add prefix or suffix to filenames, with support for dynamic values based on file properties.

**Parameters:**
- `prefix` (str): Prefix to add (default: '')
- `suffix` (str): Suffix to add (default: '')
- `based_on` (str): Generate prefix/suffix based on file property
  - `'date'`: Use file modification date (YYYYMMDD)
  - `'size'`: Use file size category (tiny, small, medium, large)
  - `'type'`: Use file extension

**Examples:**

```python
# Static prefix
renamer.rename('prefix_suffix',
    prefix='IMG_',
    suffix=''
)

# Static suffix
renamer.rename('prefix_suffix',
    prefix='',
    suffix='_backup'
)

# Both prefix and suffix
renamer.rename('prefix_suffix',
    prefix='NEW_',
    suffix='_v2'
)

# Date-based prefix
renamer.rename('prefix_suffix',
    prefix='',
    based_on='date'
)

# Size-based suffix
renamer.rename('prefix_suffix',
    suffix='',
    based_on='size'
)

# Type-based prefix
renamer.rename('prefix_suffix',
    prefix='',
    based_on='type'
)
```

**Before/After Examples:**
```
Static:
photo.jpg               -> IMG_photo.jpg
document.pdf            -> document_backup.pdf
file.txt                -> NEW_file_v2.txt

Date-based (file modified on 2024-11-15):
report.pdf              -> 20241115_report.pdf
image.jpg               -> 20241115_image.jpg

Size-based:
tiny_file.txt (500 B)   -> tiny_file_tiny.txt
large_file.zip (50 MB)  -> large_file_large.zip

Type-based:
document.pdf            -> PDF_document.pdf
photo.jpg               -> JPG_photo.jpg
```

---

### Case Changes

Change the case of filenames to various formats.

**Parameters:**
- `case_type` (str): Type of case transformation
  - `'lower'`: lowercase
  - `'upper'`: UPPERCASE
  - `'title'`: Title Case
  - `'sentence'`: Sentence case
  - `'camel'`: camelCase
  - `'snake'`: snake_case

**Examples:**

```python
# Lowercase
renamer.rename('case_change', case_type='lower')

# Uppercase
renamer.rename('case_change', case_type='upper')

# Title Case
renamer.rename('case_change', case_type='title')

# Sentence case
renamer.rename('case_change', case_type='sentence')

# camelCase
renamer.rename('case_change', case_type='camel')

# snake_case
renamer.rename('case_change', case_type='snake')
```

**Before/After Examples:**
```
Original:                My Document File.txt

lower:                   my document file.txt
upper:                   MY DOCUMENT FILE.TXT
title:                   My Document File.txt
sentence:                My document file.txt
camel:                   myDocumentFile.txt
snake:                   my_document_file.txt
```

---

### Remove Special Characters

Remove or replace special characters from filenames, keeping only alphanumeric characters and specified exceptions.

**Parameters:**
- `keep_chars` (str): Additional characters to keep (default: '')
- `replace_with` (str): Replacement character (default: '_')

**Examples:**

```python
# Remove all special characters (replace with underscore)
renamer.rename('remove_special',
    keep_chars='',
    replace_with='_'
)

# Keep dashes and underscores
renamer.rename('remove_special',
    keep_chars='_-',
    replace_with='_'
)

# Remove special characters (replace with nothing)
renamer.rename('remove_special',
    keep_chars='',
    replace_with=''
)

# Keep dots and dashes
renamer.rename('remove_special',
    keep_chars='.-',
    replace_with='_'
)
```

**Before/After Examples:**
```
Default (replace with underscore):
My File (1).txt         -> My_File_1.txt
document#2@test.pdf     -> document_2_test.pdf
photo [vacation].jpg    -> photo_vacation.jpg

Keep dashes and underscores:
My-File_2024 (1).txt    -> My-File_2024_1.txt
test@file#2.csv         -> test_file_2.csv

Replace with nothing:
File (1) [test].txt     -> File1test.txt
photo@2024#1.jpg        -> photo20241.jpg
```

---

## Configuration

Customize the behavior with configuration options:

```python
config = {
    'preview_mode': True,           # Preview before renaming
    'recursive': False,              # Process subfolders
    'include_extensions': [],        # Only these extensions (empty = all)
    'exclude_extensions': [],        # Skip these extensions
    'include_hidden': False,         # Process hidden files
    'create_undo_file': True,        # Create undo history
}

renamer = BulkFileRenamer('./my_files', config)
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `preview_mode` | bool | `True` | Preview changes without applying them |
| `recursive` | bool | `False` | Process files in subfolders |
| `include_extensions` | list | `[]` | Only process these extensions (e.g., `['.txt', '.pdf']`) |
| `exclude_extensions` | list | `[]` | Skip these extensions (e.g., `['.tmp', '.log']`) |
| `include_hidden` | bool | `False` | Process hidden files (starting with `.`) |
| `create_undo_file` | bool | `True` | Save undo information |

### Examples

```python
# Only process images
config = {
    'include_extensions': ['.jpg', '.png', '.gif'],
    'preview_mode': False
}

# Exclude temporary files
config = {
    'exclude_extensions': ['.tmp', '.log', '.cache'],
    'preview_mode': False
}

# Process all subfolders
config = {
    'recursive': True,
    'preview_mode': True
}

# Don't create undo file (faster for large batches)
config = {
    'create_undo_file': False,
    'preview_mode': False
}
```

---

## Advanced Usage

### Chaining Operations

Apply multiple operations in sequence:

```python
config = {'preview_mode': False, 'create_undo_file': True}

# Step 1: Remove special characters
renamer1 = BulkFileRenamer('./my_files', config)
renamer1.rename('remove_special', keep_chars='_-', replace_with='_')

# Step 2: Change to lowercase
renamer2 = BulkFileRenamer('./my_files', config)
renamer2.rename('case_change', case_type='lower')

# Step 3: Add sequential numbers
renamer3 = BulkFileRenamer('./my_files', config)
renamer3.rename('sequential', pattern='{name}_{counter}', start=1, padding=3)
```

### Filtering Files

```python
# Only process PDF files
config = {
    'include_extensions': ['.pdf'],
    'preview_mode': True
}
renamer = BulkFileRenamer('./documents', config)
renamer.rename('prefix_suffix', prefix='DOC_')

# Process all files except images
config = {
    'exclude_extensions': ['.jpg', '.png', '.gif', '.bmp'],
    'preview_mode': True
}
renamer = BulkFileRenamer('./mixed_files', config)
renamer.rename('case_change', case_type='lower')
```

### Recursive Processing

```python
# Process all files in folder and subfolders
config = {
    'recursive': True,
    'preview_mode': True
}
renamer = BulkFileRenamer('./root_folder', config)
renamer.rename('remove_special', keep_chars='_-', replace_with='_')
```

---

## Undo Functionality

### How Undo Works

- Every rename operation is saved to `.rename_undo.json` in the target folder
- Undo reverses the most recent rename operation
- Can undo multiple times (LIFO - Last In, First Out)
- Undo file is automatically created unless disabled

### Using Undo

```python
from bulk_rename import BulkFileRenamer

# Execute rename with undo enabled
config = {'preview_mode': False, 'create_undo_file': True}
renamer = BulkFileRenamer('./my_files', config)
renamer.rename('case_change', case_type='lower')

# Undo the rename
renamer.undo_last_rename()
```

**Command-line undo:**

```python
# In your script:
if __name__ == "__main__":
    renamer = BulkFileRenamer('./my_files')
    renamer.undo_last_rename()
```

### Undo File Format

The `.rename_undo.json` file stores all operations:

```json
[
  {
    "timestamp": "2025-11-20T10:30:00",
    "operations": [
      {
        "old": "/path/to/OldName.txt",
        "new": "/path/to/newname.txt",
        "timestamp": "2025-11-20T10:30:00"
      }
    ]
  }
]
```

---

## Use as Python Module

### Basic Usage

```python
from bulk_rename import BulkFileRenamer

# Create renamer
config = {'preview_mode': True}
renamer = BulkFileRenamer('/path/to/folder', config)

# Execute rename
renamer.rename('sequential', pattern='file_{counter}', start=1, padding=3)
```

### Advanced Usage

```python
from bulk_rename import BulkFileRenamer
from pathlib import Path

# Custom configuration
config = {
    'preview_mode': False,
    'recursive': True,
    'include_extensions': ['.txt', '.md'],
    'create_undo_file': True
}

# Create renamer
renamer = BulkFileRenamer('./documents', config)

# Get files manually
files = renamer.get_files()
print(f"Found {len(files)} files")

# Plan operations
operations = renamer.plan_rename(files, 'find_replace', 
    find='old', replace='new', case_sensitive=False)

# Validate
valid_ops, conflicts = renamer.validate_operations(operations)
print(f"Valid: {len(valid_ops)}, Conflicts: {len(conflicts)}")

# Preview
preview = renamer.generate_preview(valid_ops, conflicts)
print(preview)

# Execute
if valid_ops:
    renamer.execute_rename(valid_ops)
    print(f"Renamed {renamer.stats['renamed_files']} files")
```

### Integration Example

```python
from bulk_rename import BulkFileRenamer
from organize_files import FileOrganizer

# Organize files first
organizer = FileOrganizer('./downloads')
organizer.organize()

# Then rename organized files
for category_folder in Path('./downloads/Organized').iterdir():
    if category_folder.is_dir():
        config = {'preview_mode': False}
        renamer = BulkFileRenamer(str(category_folder), config)
        renamer.rename('case_change', case_type='lower')
        renamer.rename('remove_special', keep_chars='_-', replace_with='_')
```

---

## Examples

### Example 1: Clean Up Downloaded Files

```python
from bulk_rename import BulkFileRenamer

config = {'preview_mode': False, 'create_undo_file': True}
renamer = BulkFileRenamer('~/Downloads', config)

# Remove special characters
renamer.rename('remove_special', keep_chars='_-', replace_with='_')

# Change to lowercase
renamer = BulkFileRenamer('~/Downloads', config)
renamer.rename('case_change', case_type='lower')
```

**Before:**
```
My File (1).txt
Document [FINAL].pdf
Photo - Vacation (2024).jpg
```

**After:**
```
my_file_1.txt
document_final.pdf
photo_vacation_2024.jpg
```

---

### Example 2: Organize Photos with Date Prefix

```python
from bulk_rename import BulkFileRenamer

config = {
    'preview_mode': False,
    'include_extensions': ['.jpg', '.png', '.jpeg'],
    'create_undo_file': True
}

renamer = BulkFileRenamer('./photos', config)

# Add date prefix based on modification date
renamer.rename('prefix_suffix', prefix='', based_on='date')

# Add sequential numbers
renamer = BulkFileRenamer('./photos', config)
renamer.rename('sequential', pattern='{name}_{counter}', start=1, padding=3)
```

**Before:**
```
IMG_1234.jpg
vacation.jpg
beach.png
```

**After:**
```
20241115_IMG_1234_001.jpg
20241116_vacation_002.jpg
20241117_beach_003.png
```

---

### Example 3: Rename Code Files to snake_case

```python
from bulk_rename import BulkFileRenamer

config = {
    'preview_mode': False,
    'include_extensions': ['.py', '.js', '.java'],
    'recursive': True,
    'create_undo_file': True
}

renamer = BulkFileRenamer('./src', config)

# Convert to snake_case
renamer.rename('case_change', case_type='snake')
```

**Before:**
```
MyComponent.js
UserService.py
DataProcessor.java
```

**After:**
```
my_component.js
user_service.py
data_processor.java
```

---

### Example 4: Version Numbering for Backups

```python
from bulk_rename import BulkFileRenamer
from datetime import datetime

# Add date and version number
today = datetime.now().strftime('%Y%m%d')

config = {'preview_mode': False, 'create_undo_file': True}
renamer = BulkFileRenamer('./backups', config)

# Add date suffix
renamer.rename('prefix_suffix', suffix=f'_{today}')

# Add version numbers
renamer = BulkFileRenamer('./backups', config)
renamer.rename('sequential', pattern='{name}_v{counter}', start=1, padding=2)
```

**Before:**
```
database.sql
config.json
users.csv
```

**After:**
```
database_20241120_v01.sql
config_20241120_v02.json
users_20241120_v03.csv
```

---

### Example 5: Remove Version Numbers and Years

```python
from bulk_rename import BulkFileRenamer

config = {'preview_mode': False, 'create_undo_file': True}
renamer = BulkFileRenamer('./documents', config)

# Remove version numbers and years with regex
renamer.rename('find_replace',
    find=r'(_v\d+|_\d{4})',
    replace='',
    use_regex=True
)
```

**Before:**
```
report_2024_v1.pdf
invoice_v2.xlsx
presentation_2024.pptx
```

**After:**
```
report.pdf
invoice.xlsx
presentation.pptx
```

---

## Troubleshooting

### Issue: "No files found to rename"

**Cause:** No files match the filtering criteria

**Solution:**
- Check that the target folder is correct
- Verify `include_extensions` and `exclude_extensions` settings
- Set `include_hidden: True` if renaming hidden files
- Check `recursive: True` if files are in subfolders

```python
# Debug: See what files are found
renamer = BulkFileRenamer('./my_files')
files = renamer.get_files()
print(f"Found {len(files)} files:")
for f in files:
    print(f"  {f}")
```

---

### Issue: "Target file already exists"

**Cause:** A file with the new name already exists

**Solution:**
- Use preview mode to see conflicts
- Rename/move existing files first
- Use a different naming pattern

```python
# Preview to see conflicts
config = {'preview_mode': True}
renamer = BulkFileRenamer('./my_files', config)
preview = renamer.rename('sequential', pattern='file_{counter}')
print(preview)  # Check CONFLICTS section
```

---

### Issue: "Multiple files rename to same name"

**Cause:** Different files would have identical names after renaming

**Solution:**
- Add sequential numbering to make names unique
- Use a more specific pattern
- Include original filename in pattern

```python
# Solution: Add sequential numbers
renamer.rename('sequential', 
    pattern='{name}_{counter}',  # Include original name
    start=1, 
    padding=3
)
```

---

### Issue: "Undo not working"

**Cause:** Undo file missing or corrupted

**Solution:**
- Ensure `create_undo_file: True` was set during rename
- Check for `.rename_undo.json` in target folder
- Verify file hasn't been manually edited

```python
# Check if undo file exists
from pathlib import Path
undo_file = Path('./my_files/.rename_undo.json')
if undo_file.exists():
    print("Undo file found")
else:
    print("No undo file - cannot undo")
```

---

### Issue: "Preview shows no changes"

**Cause:** Renaming would result in identical filenames

**Solution:**
- Check that your pattern/operation actually changes the names
- Verify case sensitivity settings
- Try a different operation

```python
# Check before/after manually
files = renamer.get_files()
operations = renamer.plan_rename(files, 'case_change', case_type='lower')
for old, new in operations[:5]:
    print(f"{old.name} -> {new.name}")
```

---

## Safety Tips

1. **Always preview first**: Use `preview_mode: True` to see changes before applying
2. **Enable undo**: Keep `create_undo_file: True` for safety
3. **Test on small batch**: Try on a few files before processing thousands
4. **Backup important files**: Make a backup before bulk renaming critical files
5. **Check conflicts**: Review the CONFLICTS section in preview
6. **Use specific patterns**: Be precise to avoid unintended renames
7. **Verify extensions**: Double-check `include_extensions` and `exclude_extensions`

---

## Tips and Best Practices

### 1. Start with Preview Mode

Always preview changes first:

```python
config = {'preview_mode': True}
renamer = BulkFileRenamer('./my_files', config)
renamer.rename('case_change', case_type='lower')

# Review the output, then execute
config['preview_mode'] = False
renamer = BulkFileRenamer('./my_files', config)
renamer.rename('case_change', case_type='lower')
```

### 2. Chain Operations for Complex Renaming

```python
# Step 1: Clean
renamer.rename('remove_special', keep_chars='_-', replace_with='_')

# Step 2: Standardize case
renamer.rename('case_change', case_type='lower')

# Step 3: Add numbers
renamer.rename('sequential', pattern='{name}_{counter}', start=1)
```

### 3. Use Regex for Powerful Replacements

```python
# Remove all numbers
renamer.rename('find_replace', find=r'\d+', replace='', use_regex=True)

# Replace multiple spaces with single underscore
renamer.rename('find_replace', find=r'\s+', replace='_', use_regex=True)

# Extract year from filename
renamer.rename('find_replace', find=r'.*(\d{4}).*', replace=r'\1', use_regex=True)
```

### 4. Test Undo on Small Batch

```python
# Rename a few files
config = {'preview_mode': False, 'include_extensions': ['.txt']}
renamer = BulkFileRenamer('./test', config)
renamer.rename('case_change', case_type='upper')

# Test undo
renamer.undo_last_rename()

# Verify files are restored
```

---

## Performance Considerations

- **Large folders (1000+ files)**: Disable undo file for faster processing
- **Recursive mode**: Be cautious with deep folder structures
- **Regex operations**: May be slower on thousands of files
- **Preview mode**: Minimal performance impact

```python
# Fast mode for large batches
config = {
    'preview_mode': False,
    'create_undo_file': False,  # Skip undo for speed
    'recursive': False
}
```

---

## Summary

The Bulk File Renamer is a versatile tool for managing filenames efficiently:

- **6 powerful renaming operations** for any scenario
- **Safe by default** with preview mode and undo
- **Flexible configuration** for precise control
- **Professional features** like conflict detection and logging
- **Easy to use** via CLI or as Python module

Start with preview mode, verify the changes, then execute with confidence!

---

## Related Tools

- **Smart File Organizer** (`organize_files.py`) - Organize files by type/date
- **CSV Data Cleaner** (`clean_csv_data.py`) - Clean and validate CSV data
- **Excel Files Merger** (`merge_excel_files.py`) - Merge multiple Excel files

---

*Last updated: November 20, 2025*
