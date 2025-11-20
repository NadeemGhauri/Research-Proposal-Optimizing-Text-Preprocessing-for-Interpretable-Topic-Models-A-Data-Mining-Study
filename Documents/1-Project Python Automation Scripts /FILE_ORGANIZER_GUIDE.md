# Smart File Organizer - Complete Guide

## Overview

The Smart File Organizer is an intelligent automation tool that organizes files by type, date, detects duplicates, renames files with consistent patterns, and provides safe preview mode before making changes.

---

## 🎯 Features

- ✅ **Organize by File Type** - Automatically categorize files (Images, Documents, Videos, etc.)
- ✅ **Organize by Date** - Sort files by creation/modification date
- ✅ **Consistent Naming** - Rename files with customizable patterns
- ✅ **Duplicate Detection** - Find and remove duplicate files using MD5 hashing
- ✅ **Auto Folder Creation** - Create organized folder structures automatically
- ✅ **Organization Report** - Detailed statistics and operation logs
- ✅ **Safe Mode** - Preview changes before executing (prevent accidents)
- ✅ **Flexible Configuration** - Extensive customization options

---

## 📋 Quick Start

### 1. Basic Usage (Safe Mode - Preview Only)

```bash
# Preview organization for a folder
python organize_files.py /path/to/messy/folder

# Preview with custom target location
python organize_files.py /path/to/source /path/to/organized
```

### 2. Execute Organization (Disable Safe Mode)

Edit the `config` dictionary in the script or create your own configuration:

```python
config = {
    'safe_mode': False,  # Set to False to actually move files
    'organize_by_type': True,
    'remove_duplicates': True,
}
```

---

## 🔧 Configuration Reference

### File Organization Options

```python
config = {
    # Organization Methods
    'organize_by_type': True,        # Group files by category
    'organize_by_date': False,       # Group files by date
    'rename_files': False,           # Apply naming convention
    
    # Naming Pattern (if rename_files is True)
    'naming_pattern': '{original_name}',  # See patterns below
    
    # Duplicate Handling
    'remove_duplicates': True,       # Find and remove duplicates
    
    # Safety and Reporting
    'safe_mode': True,               # Preview only (no changes)
    'create_report': True,           # Generate organization report
    
    # File Filtering
    'min_file_size': 0,              # Minimum file size in bytes
    'exclude_extensions': [],        # Extensions to skip
    'include_hidden': False,         # Process hidden files
    
    # Date Formatting (if organize_by_date is True)
    'date_format': '%Y-%m',          # YYYY-MM (monthly folders)
}
```

---

## 📂 File Categories

The organizer automatically categorizes files into these groups:

| Category | File Extensions |
|----------|----------------|
| **Images** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`, `.ico`, `.tiff`, `.raw` |
| **Documents** | `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.csv` |
| **Videos** | `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v`, `.mpg`, `.mpeg` |
| **Audio** | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a`, `.opus` |
| **Archives** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz`, `.iso` |
| **Code** | `.py`, `.js`, `.java`, `.cpp`, `.c`, `.h`, `.cs`, `.php`, `.rb`, `.go`, `.rs`, `.swift` |
| **Web** | `.html`, `.htm`, `.css`, `.scss`, `.json`, `.xml`, `.yml`, `.yaml` |
| **Executables** | `.exe`, `.msi`, `.app`, `.deb`, `.rpm`, `.dmg`, `.pkg` |
| **Fonts** | `.ttf`, `.otf`, `.woff`, `.woff2`, `.eot` |
| **eBooks** | `.epub`, `.mobi`, `.azw`, `.azw3`, `.fb2` |
| **Other** | Any file not matching above categories |

---

## 🏷️ Naming Patterns

When `rename_files` is enabled, customize filenames with these placeholders:

### Available Placeholders

| Placeholder | Description | Example |
|------------|-------------|---------|
| `{original_name}` | Original filename (without extension) | `vacation_photo` |
| `{date}` | File modification date (YYYYMMDD) | `20240315` |
| `{counter}` | Sequential number (3 digits) | `001`, `002`, `003` |
| `{category}` | File category | `Images`, `Documents` |

### Pattern Examples

```python
# Keep original names
'naming_pattern': '{original_name}'
# Output: vacation_photo.jpg

# Add date prefix
'naming_pattern': '{date}_{original_name}'
# Output: 20240315_vacation_photo.jpg

# Numbered with category
'naming_pattern': '{category}_{counter}_{original_name}'
# Output: Images_001_vacation_photo.jpg

# Date and counter only
'naming_pattern': '{date}_{counter}'
# Output: 20240315_001.jpg
```

---

## 📅 Date Organization

Organize files into date-based folders using modification timestamps:

### Date Format Options

```python
# Monthly folders (YYYY-MM)
'date_format': '%Y-%m'
# Output: 2024-03/, 2024-04/

# Yearly folders
'date_format': '%Y'
# Output: 2024/, 2025/

# Full date
'date_format': '%Y-%m-%d'
# Output: 2024-03-15/, 2024-03-16/

# Month name
'date_format': '%Y/%B'
# Output: 2024/March/, 2024/April/

# Quarter
'date_format': '%Y-Q{quarter}'  # Requires custom logic
```

### Combined Organization

You can combine type and date organization:

```python
config = {
    'organize_by_type': True,
    'organize_by_date': True,
    'date_format': '%Y-%m',
}
```

Output structure:
```
Organized/
├── Images/
│   ├── 2024-01/
│   ├── 2024-02/
│   └── 2024-03/
├── Documents/
│   ├── 2024-01/
│   └── 2024-02/
└── Videos/
    └── 2024-03/
```

---

## 🔍 Duplicate Detection

The organizer uses MD5 hashing to identify duplicate files:

### How It Works

1. Calculates MD5 hash for each file
2. Compares hashes to find exact duplicates
3. Keeps the first occurrence
4. Optionally removes duplicates

### Configuration

```python
config = {
    'remove_duplicates': True,  # Remove duplicates
}
```

### Duplicate Report

The report shows:
- Number of duplicates found
- Which file is the original
- Space saved by removing duplicates

Example:
```
DUPLICATE FILES:
  - copy_of_document.pdf (duplicate of document_1.pdf)
  - document_backup.pdf (duplicate of document_1.pdf)

Space Saved: 2.5 MB
```

---

## 🛡️ Safe Mode

Safe Mode is a **critical safety feature** that prevents accidental file operations.

### How It Works

```python
config = {
    'safe_mode': True,  # Preview only - no files moved
}
```

**When enabled:**
- ✅ Scans all files
- ✅ Plans all operations
- ✅ Generates detailed report
- ✅ Shows what WOULD happen
- ❌ Does NOT move, rename, or delete files

**When disabled:**
- ✅ Executes all planned operations
- ✅ Actually moves and organizes files
- ✅ Removes duplicates (if enabled)

### Best Practice

**Always run in Safe Mode first:**

1. Run with `safe_mode: True`
2. Review the generated report
3. Verify the planned operations
4. Set `safe_mode: False` to execute
5. Run again to organize files

---

## 📊 Organization Report

Every run generates a detailed report:

### Report Contents

```
SMART FILE ORGANIZER REPORT
==================================================
Source Folder: /path/to/source
Target Folder: /path/to/organized
Organization Date: 2025-11-19 06:55:16

CONFIGURATION:
  - Organize by Type: True
  - Organize by Date: False
  - Rename Files: False
  - Remove Duplicates: True
  - Safe Mode: True

STATISTICS:
  - Total Files Found: 34
  - Files Organized: 32
  - Files Skipped: 0
  - Duplicates Found: 2
  - Duplicates Removed: 2
  - Space Saved: 45.2 KB
  - Errors: 0

FILES BY CATEGORY:
  - Documents: 8 files
  - Images: 6 files
  - Code: 6 files
  - Videos: 4 files
  - Audio: 4 files
  - Archives: 4 files

DUPLICATE FILES:
  - file_copy.pdf (duplicate of original.pdf)

PLANNED OPERATIONS (Safe Mode - Preview):
  - MOVE: photo.jpg -> Organized/Images/photo.jpg
  - MOVE: report.pdf -> Organized/Documents/report.pdf
  ...
```

Report is saved as: `organization_report_YYYYMMDD_HHMMSS.txt`

---

## 💡 Use Cases

### Use Case 1: Clean Up Downloads Folder

```python
config = {
    'organize_by_type': True,
    'remove_duplicates': True,
    'safe_mode': False,
    'exclude_extensions': ['.tmp', '.crdownload'],
}

organizer = SmartFileOrganizer('~/Downloads', config=config)
organizer.organize()
```

### Use Case 2: Photo Library Organization

```python
config = {
    'organize_by_type': False,      # Already know they're photos
    'organize_by_date': True,        # Organize by month
    'date_format': '%Y/%B',          # 2024/March
    'rename_files': True,
    'naming_pattern': '{date}_{counter}',
    'remove_duplicates': True,
}
```

### Use Case 3: Project File Cleanup

```python
config = {
    'organize_by_type': True,
    'rename_files': True,
    'naming_pattern': 'project_{category}_{counter}',
    'min_file_size': 1024,          # Skip files smaller than 1KB
    'exclude_extensions': ['.tmp', '.cache', '.log'],
}
```

### Use Case 4: Archive Old Files by Year

```python
config = {
    'organize_by_date': True,
    'date_format': '%Y',             # Yearly folders
    'organize_by_type': True,        # Combine with type
    'remove_duplicates': True,
}
```

---

## 🚀 Advanced Usage

### Programmatic Usage

```python
from organize_files import SmartFileOrganizer

# Custom configuration
config = {
    'organize_by_type': True,
    'organize_by_date': True,
    'date_format': '%Y-%m',
    'remove_duplicates': True,
    'safe_mode': False,
}

# Create organizer
organizer = SmartFileOrganizer(
    source_folder='/path/to/source',
    target_folder='/path/to/organized',
    config=config
)

# Run organization
report = organizer.organize()
print(report)
```

### Batch Processing

```python
import os

folders_to_organize = [
    '/Users/john/Downloads',
    '/Users/john/Desktop',
    '/Users/john/Documents/temp',
]

for folder in folders_to_organize:
    if os.path.exists(folder):
        organizer = SmartFileOrganizer(folder, config=config)
        organizer.organize()
```

### Custom Categories

Extend the file categories:

```python
# Add to SmartFileOrganizer class
FILE_CATEGORIES = {
    'Images': ['.jpg', '.png', ...],
    'Documents': ['.pdf', '.doc', ...],
    'My_Custom_Category': ['.xyz', '.abc'],  # Add custom
}
```

---

## 🐛 Troubleshooting

### Issue: "Source folder does not exist"
**Solution:** Verify the path is correct and accessible

### Issue: "Permission denied"
**Solution:** 
- Run with appropriate permissions
- Check folder ownership
- Try copying instead of moving (modify script)

### Issue: "Some files not organized"
**Solution:**
- Check file size filter (`min_file_size`)
- Verify extensions not in `exclude_extensions`
- Check if files are hidden (`include_hidden`)

### Issue: "Too many duplicates detected"
**Solution:**
- Review duplicate list in report
- Consider if files are truly identical
- MD5 hash detects byte-for-byte duplicates only

### Issue: "Files organized incorrectly"
**Solution:**
- Always use Safe Mode first
- Review the planned operations
- Adjust configuration as needed

---

## 📁 Example Folder Structure

### Before Organization
```
messy_folder/
├── photo1.jpg
├── photo2.png
├── report.pdf
├── copy_of_report.pdf (duplicate)
├── song.mp3
├── video.mp4
├── script.py
└── document.docx
```

### After Organization (Type-Based)
```
messy_folder/
└── Organized/
    ├── Images/
    │   ├── photo1.jpg
    │   └── photo2.png
    ├── Documents/
    │   ├── report.pdf
    │   └── document.docx
    ├── Audio/
    │   └── song.mp3
    ├── Videos/
    │   └── video.mp4
    └── Code/
        └── script.py
```

### After Organization (Type + Date)
```
messy_folder/
└── Organized/
    ├── Images/
    │   ├── 2024-01/
    │   │   └── photo1.jpg
    │   └── 2024-02/
    │       └── photo2.png
    ├── Documents/
    │   └── 2024-01/
    │       ├── report.pdf
    │       └── document.docx
    └── Audio/
        └── 2024-03/
            └── song.mp3
```

---

## ⚙️ Performance Tips

1. **Large Folders:** Process in batches or use file size filters
2. **Network Drives:** Copy instead of move for safety
3. **Duplicates:** Hash calculation is intensive - consider disabling for huge folders
4. **Safe Mode:** Always enabled by default - prevents mistakes

---

## 🔒 Safety Best Practices

1. **Always use Safe Mode first** - Preview before executing
2. **Backup important files** - Before organizing critical data
3. **Test on sample folder** - Verify configuration works as expected
4. **Review the report** - Check planned operations carefully
5. **Use version control** - For code projects before organizing

---

## 📚 Additional Resources

- Python `pathlib` documentation
- File hashing and duplicate detection
- Safe file operations best practices

---

## 🆘 Support

For issues or questions:
1. Run in Safe Mode and review the report
2. Check configuration settings
3. Verify file permissions
4. Review log output for specific errors
