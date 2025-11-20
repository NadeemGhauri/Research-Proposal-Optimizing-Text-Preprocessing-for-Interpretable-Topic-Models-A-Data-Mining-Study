# Backup Automation - Complete Guide

A comprehensive automated backup solution with compression, versioning, integrity verification, and notification support.

---

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Backup Operations](#backup-operations)
- [Version Management](#version-management)
- [Integrity Verification](#integrity-verification)
- [Email Notifications](#email-notifications)
- [Restore from Backup](#restore-from-backup)
- [Automation & Scheduling](#automation--scheduling)
- [Use as Python Module](#use-as-python-module)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## Features

- ✅ **Compression**
  - ZIP compression with configurable levels (0-9)
  - Automatic compression ratio calculation
  - Support for large files and folders

- ✅ **Timestamping**
  - Automatic timestamp in backup filenames
  - ISO format metadata timestamps
  - Sortable backup names

- ✅ **Version Management**
  - Configurable version history (keep last N versions)
  - Automatic cleanup of old backups
  - Metadata tracking for each version

- ✅ **Integrity Verification**
  - MD5 checksum calculation
  - ZIP file validation
  - Corruption detection

- ✅ **Email Notifications**
  - Success/failure notifications
  - Detailed backup statistics
  - SMTP support (Gmail, etc.)

- ✅ **File Exclusion**
  - Pattern-based exclusion
  - Wildcard support
  - Common exclusions pre-configured

- ✅ **Metadata Tracking**
  - JSON metadata for each backup
  - File count, sizes, checksums
  - Source folder tracking

---

## Installation

**Prerequisites:**
- Python 3.7 or higher
- No additional dependencies required (uses only standard library)

**Installation:**
```bash
# No installation needed - just run the script!
python backup_automation.py
```

---

## Quick Start

### 1. Basic Backup

```python
from backup_automation import BackupAutomation

# Configure backup
config = {
    'backup_sources': ['./my_documents', './my_photos'],
    'backup_destination': './backups',
    'max_versions': 7,
}

# Create and run backup
backup_system = BackupAutomation(config)
backup_system.run_backup('my_backup')
```

### 2. Command-line Usage

Edit the `main()` function in `backup_automation.py`:

```python
config = {
    'backup_sources': [
        './data',
        './config',
    ],
    'backup_destination': './backups',
}

backup_system = BackupAutomation(config)
backup_system.run_backup('project_backup')
```

Then run:
```bash
python backup_automation.py
```

---

## Configuration

### Complete Configuration Example

```python
config = {
    # REQUIRED
    'backup_sources': [          # Folders to backup
        './documents',
        './photos',
        './config',
    ],
    
    # BACKUP SETTINGS
    'backup_destination': './backups',  # Where to store backups
    'max_versions': 7,                   # Keep last N versions
    'compression_level': 9,              # 0-9 (9 = maximum)
    
    # VERIFICATION
    'verify_integrity': True,    # Verify after backup
    
    # NOTIFICATIONS
    'send_notifications': False, # Send email notifications
    'notification_email': 'admin@example.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'smtp_user': 'sender@gmail.com',
    'smtp_password': 'app-password',
    
    # FILE FILTERING
    'exclude_patterns': [        # Files/folders to skip
        '*.tmp', '*.log', '.DS_Store',
        '__pycache__', '*.pyc', '.git',
        'node_modules', '.venv', '*.cache'
    ],
    'include_subdirs': True,     # Include subdirectories
    'follow_symlinks': False,    # Follow symbolic links
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `backup_sources` | list | `[]` | **Required**. List of folders to backup |
| `backup_destination` | str | `'./backups'` | Where to store backup files |
| `max_versions` | int | `7` | Number of backup versions to keep |
| `compression_level` | int | `9` | ZIP compression level (0-9) |
| `verify_integrity` | bool | `True` | Verify backup after creation |
| `send_notifications` | bool | `False` | Send email notifications |
| `notification_email` | str | `''` | Email to send notifications to |
| `smtp_server` | str | `'smtp.gmail.com'` | SMTP server address |
| `smtp_port` | int | `587` | SMTP port |
| `smtp_user` | str | `''` | SMTP username |
| `smtp_password` | str | `''` | SMTP password |
| `exclude_patterns` | list | See config | Patterns to exclude |
| `include_subdirs` | bool | `True` | Include subdirectories |
| `follow_symlinks` | bool | `False` | Follow symbolic links |

---

## Backup Operations

### Creating a Backup

```python
from backup_automation import BackupAutomation

config = {
    'backup_sources': ['./important_data'],
    'backup_destination': './backups',
    'max_versions': 7,
    'verify_integrity': True,
}

backup_system = BackupAutomation(config)
success = backup_system.run_backup('data_backup')

if success:
    print("Backup completed successfully!")
else:
    print("Backup failed!")
```

**Output:**
```
================================================================================
STARTING AUTOMATED BACKUP
================================================================================
Creating backup archive: data_backup_20251120_143022.zip
Scanning source: ./important_data
Found 150 file(s) to backup
Backup created: backups/data_backup_20251120_143022.zip
Original size: 45.32 MB
Compressed size: 12.87 MB
Compression ratio: 71.59%
Verifying backup integrity...
Backup verified successfully. Checksum: a1b2c3d4e5f6...
Metadata saved: backups/data_backup_20251120_143022.json
Cleaning up old backups (keeping last 7 versions)...
================================================================================
BACKUP COMPLETED SUCCESSFULLY
Backup File: data_backup_20251120_143022.zip
Files Backed Up: 150
Original Size: 45.32 MB
Compressed Size: 12.87 MB
Compression Ratio: 71.59%
Duration: 3.45 seconds
================================================================================
```

### Backup File Naming

Backups are automatically timestamped:
```
backup_name_YYYYMMDD_HHMMSS.zip
```

Examples:
```
project_backup_20251120_143022.zip
daily_backup_20251120_060000.zip
documents_20251120_235959.zip
```

---

## Version Management

The backup system automatically manages versions, keeping only the most recent N backups.

### How Version Management Works

1. After each backup, the system counts existing backup files
2. If more than `max_versions` exist, oldest ones are deleted
3. Both `.zip` and `.json` metadata files are cleaned up

### Configuration

```python
config = {
    'max_versions': 5,  # Keep last 5 backups only
}
```

### Example

```python
# Keep last 30 days of daily backups
config = {
    'backup_sources': ['./data'],
    'backup_destination': './backups/daily',
    'max_versions': 30,
}

# Or keep last 7 weekly backups
config = {
    'backup_sources': ['./data'],
    'backup_destination': './backups/weekly',
    'max_versions': 7,
}
```

### Manual Cleanup

```python
backup_system = BackupAutomation(config)
backup_system.cleanup_old_backups()
```

---

## Integrity Verification

Every backup can be automatically verified for corruption.

### What is Verified

1. **MD5 Checksum**: Calculated for the entire backup file
2. **ZIP Integrity**: ZIP file is tested for corruption
3. **Metadata**: Checksum stored in JSON metadata file

### Enable Verification

```python
config = {
    'verify_integrity': True,  # Enable verification
}
```

### Verification Process

```python
backup_system = BackupAutomation(config)
success = backup_system.run_backup('verified_backup')

# Verification happens automatically
# Check metadata for checksum
backups = backup_system.list_backups()
print(f"Checksum: {backups[0]['checksum']}")
```

### Manual Verification

```python
from pathlib import Path

backup_path = Path('./backups/my_backup_20251120_143022.zip')
is_valid, checksum = backup_system.verify_backup_integrity(backup_path)

if is_valid:
    print(f"✓ Backup is valid. Checksum: {checksum}")
else:
    print("✗ Backup is corrupted!")
```

---

## Email Notifications

Get notified when backups complete or fail.

### Setup Gmail Notifications

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**: Google Account → Security → App Passwords
3. **Configure backup system**:

```python
config = {
    'send_notifications': True,
    'notification_email': 'admin@example.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'smtp_user': 'sender@gmail.com',
    'smtp_password': 'your-app-password',  # Use app password, not regular password
}
```

### Success Notification Email

```
Subject: ✓ Backup Completed Successfully - 2025-11-20 14:30

Backup completed successfully!

Backup Details:
- Timestamp: 2025-11-20T14:30:22
- Backup File: project_backup_20251120_143022.zip
- Files Backed Up: 1,250
- Original Size: 125.45 MB
- Compressed Size: 45.32 MB
- Compression Ratio: 63.87%
- Checksum: a1b2c3d4e5f6...

Source Folders:
- ./documents
- ./photos
- ./config

Statistics:
- Files Skipped: 15
- Errors: 0
- Duration: 12.34 seconds
```

### Failure Notification Email

```
Subject: ✗ Backup Failed - 2025-11-20 14:30

Backup FAILED!

Error: Failed to create backup archive

Please check the backup system and try again.
```

### Other Email Providers

**Outlook/Hotmail:**
```python
config = {
    'smtp_server': 'smtp-mail.outlook.com',
    'smtp_port': 587,
}
```

**Yahoo:**
```python
config = {
    'smtp_server': 'smtp.mail.yahoo.com',
    'smtp_port': 587,
}
```

**Custom SMTP:**
```python
config = {
    'smtp_server': 'mail.yourdomain.com',
    'smtp_port': 465,  # or 587
}
```

---

## Restore from Backup

### List Available Backups

```python
backup_system = BackupAutomation(config)
backups = backup_system.list_backups()

for i, backup in enumerate(backups, 1):
    print(f"{i}. {backup['filename']}")
    print(f"   Created: {backup['created']}")
    print(f"   Size: {backup_system._format_size(backup['size'])}")
    print(f"   Files: {backup.get('file_count', 'N/A')}")
    print()
```

**Output:**
```
1. project_backup_20251120_143022.zip
   Created: 2025-11-20 14:30:22
   Size: 45.32 MB
   Files: 1,250

2. project_backup_20251119_143015.zip
   Created: 2025-11-19 14:30:15
   Size: 44.87 MB
   Files: 1,248
```

### Restore a Backup

```python
# Restore to original location
backup_system.restore_backup(
    'project_backup_20251120_143022.zip',
    './restored_data'
)
```

### Restore Specific Backup by Date

```python
backups = backup_system.list_backups()

# Find backup from specific date
target_date = '2025-11-15'
for backup in backups:
    if target_date in backup['filename']:
        backup_system.restore_backup(
            backup['filename'],
            './restored_data'
        )
        break
```

### Restore with User Selection

```python
backups = backup_system.list_backups()

# Display backups
for i, backup in enumerate(backups, 1):
    print(f"{i}. {backup['filename']} ({backup['created']})")

# Get user choice
choice = int(input("\nSelect backup to restore (number): ")) - 1
selected_backup = backups[choice]

# Restore
restore_path = input("Enter restore location: ")
backup_system.restore_backup(
    selected_backup['filename'],
    restore_path
)
```

---

## Automation & Scheduling

### Schedule with Cron (Linux/macOS)

Edit crontab:
```bash
crontab -e
```

Add backup schedule:
```bash
# Daily backup at 2 AM
0 2 * * * /usr/bin/python3 /path/to/backup_automation.py

# Hourly backup
0 * * * * /usr/bin/python3 /path/to/backup_automation.py

# Weekly backup (Sunday at 3 AM)
0 3 * * 0 /usr/bin/python3 /path/to/backup_automation.py

# Monthly backup (1st day at 4 AM)
0 4 1 * * /usr/bin/python3 /path/to/backup_automation.py
```

### Schedule with Windows Task Scheduler

1. Open **Task Scheduler**
2. Create **New Task**
3. **Trigger**: Set schedule (daily, weekly, etc.)
4. **Action**: Run Python script
   - Program: `C:\Python39\python.exe`
   - Arguments: `C:\path\to\backup_automation.py`

### Python Scheduler

```python
import schedule
import time
from backup_automation import BackupAutomation

config = {
    'backup_sources': ['./data'],
    'backup_destination': './backups',
    'max_versions': 7,
    'send_notifications': True,
}

def run_daily_backup():
    """Run daily backup job."""
    backup_system = BackupAutomation(config)
    backup_system.run_backup('daily_backup')

# Schedule daily backup at 2 AM
schedule.every().day.at("02:00").do(run_daily_backup)

# Or hourly
# schedule.every().hour.do(run_daily_backup)

# Or weekly
# schedule.every().monday.at("02:00").do(run_daily_backup)

print("Backup scheduler started...")
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Use as Python Module

### Basic Usage

```python
from backup_automation import BackupAutomation

config = {
    'backup_sources': ['./data'],
    'backup_destination': './backups',
}

backup_system = BackupAutomation(config)
success = backup_system.run_backup('my_backup')
```

### Advanced Usage

```python
from backup_automation import BackupAutomation
from pathlib import Path

# Custom configuration
config = {
    'backup_sources': ['./documents', './photos'],
    'backup_destination': './backups',
    'max_versions': 30,
    'compression_level': 9,
    'verify_integrity': True,
    'send_notifications': True,
    'notification_email': 'admin@example.com',
}

# Create backup system
backup_system = BackupAutomation(config)

# Create backup archive manually
backup_path = backup_system.create_backup_archive('custom_backup')

if backup_path:
    # Verify integrity
    is_valid, checksum = backup_system.verify_backup_integrity(backup_path)
    
    if is_valid:
        # Save metadata
        backup_system.save_backup_metadata(backup_path, checksum)
        
        # Cleanup old backups
        backup_system.cleanup_old_backups()
        
        print(f"✓ Backup created: {backup_path.name}")
        print(f"  Checksum: {checksum}")
    else:
        print("✗ Backup verification failed!")
else:
    print("✗ Backup creation failed!")
```

### Integration with Other Tools

```python
from backup_automation import BackupAutomation
from organize_files import FileOrganizer

# Step 1: Organize files
organizer = FileOrganizer('./downloads')
organizer.organize()

# Step 2: Backup organized files
config = {
    'backup_sources': ['./downloads/Organized'],
    'backup_destination': './backups',
    'max_versions': 7,
}

backup_system = BackupAutomation(config)
backup_system.run_backup('organized_files_backup')
```

---

## Examples

### Example 1: Daily Document Backup

```python
from backup_automation import BackupAutomation

config = {
    'backup_sources': [
        '~/Documents',
        '~/Desktop',
    ],
    'backup_destination': '~/Backups/Daily',
    'max_versions': 30,  # Keep last 30 days
    'compression_level': 9,
    'verify_integrity': True,
    'send_notifications': True,
    'notification_email': 'me@example.com',
    'exclude_patterns': [
        '*.tmp', '*.cache', '.DS_Store',
        'node_modules', '.git', '__pycache__'
    ],
}

backup_system = BackupAutomation(config)
backup_system.run_backup('daily_documents')
```

---

### Example 2: Project Source Code Backup

```python
config = {
    'backup_sources': [
        './src',
        './config',
        './tests',
    ],
    'backup_destination': './backups/project',
    'max_versions': 7,
    'exclude_patterns': [
        'node_modules', '.git', '__pycache__',
        '*.pyc', '.venv', 'dist', 'build',
        '*.log', '.DS_Store'
    ],
    'verify_integrity': True,
}

backup_system = BackupAutomation(config)
backup_system.run_backup('project_source')
```

---

### Example 3: Photo Library Backup

```python
config = {
    'backup_sources': ['~/Pictures'],
    'backup_destination': '/Volumes/External/PhotoBackups',
    'max_versions': 12,  # Keep last 12 months
    'compression_level': 6,  # Lower compression for photos
    'verify_integrity': True,
    'send_notifications': True,
    'notification_email': 'admin@example.com',
}

backup_system = BackupAutomation(config)
backup_system.run_backup('photo_library')
```

---

### Example 4: Multi-Tier Backup Strategy

```python
from backup_automation import BackupAutomation
from datetime import datetime

# Daily backups (keep 7 days)
daily_config = {
    'backup_sources': ['./data'],
    'backup_destination': './backups/daily',
    'max_versions': 7,
}

# Weekly backups (keep 4 weeks)
weekly_config = {
    'backup_sources': ['./data'],
    'backup_destination': './backups/weekly',
    'max_versions': 4,
}

# Monthly backups (keep 12 months)
monthly_config = {
    'backup_sources': ['./data'],
    'backup_destination': './backups/monthly',
    'max_versions': 12,
}

# Run daily backup
daily_backup = BackupAutomation(daily_config)
daily_backup.run_backup('daily')

# Run weekly backup (Sundays)
if datetime.now().weekday() == 6:  # Sunday
    weekly_backup = BackupAutomation(weekly_config)
    weekly_backup.run_backup('weekly')

# Run monthly backup (1st of month)
if datetime.now().day == 1:
    monthly_backup = BackupAutomation(monthly_config)
    monthly_backup.run_backup('monthly')
```

---

### Example 5: Selective Restore

```python
import zipfile
from pathlib import Path

backup_file = './backups/project_backup_20251120_143022.zip'

# Extract only specific files
with zipfile.ZipFile(backup_file, 'r') as zipf:
    # List all files
    files = zipf.namelist()
    
    # Extract only .py files
    for file in files:
        if file.endswith('.py'):
            zipf.extract(file, './restored/python_files')
    
    # Or extract specific folder
    for file in files:
        if file.startswith('config/'):
            zipf.extract(file, './restored')
```

---

## Troubleshooting

### Issue: "No backup sources specified"

**Cause:** `backup_sources` list is empty

**Solution:**
```python
config = {
    'backup_sources': ['./data', './config'],  # Add at least one source
}
```

---

### Issue: "Permission denied" when backing up

**Cause:** No read permission for source files or write permission for backup destination

**Solution:**
```bash
# Check permissions
ls -la /path/to/source

# Grant read permissions
chmod -R +r /path/to/source

# Grant write permissions to backup folder
chmod +w /path/to/backups
```

---

### Issue: Email notifications not working

**Cause:** Incorrect SMTP settings or password

**Solution:**
1. For Gmail, use **App Password** not regular password
2. Enable "Less secure app access" (if not using 2FA)
3. Check SMTP server and port settings
4. Test with basic SMTP client first

```python
import smtplib

# Test SMTP connection
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your-email@gmail.com', 'your-app-password')
    print("✓ SMTP connection successful!")
    server.quit()
except Exception as e:
    print(f"✗ SMTP error: {e}")
```

---

### Issue: Backup file corrupted

**Cause:** Interrupted backup process or disk errors

**Solution:**
1. Enable integrity verification
2. Re-run backup
3. Check disk health

```python
config = {
    'verify_integrity': True,  # Enable verification
}
```

---

### Issue: Backups taking too long

**Cause:** High compression level or large files

**Solution:**
1. Lower compression level
2. Exclude unnecessary files
3. Backup incrementally

```python
config = {
    'compression_level': 6,  # Lower from 9
    'exclude_patterns': ['*.log', '*.tmp', 'node_modules'],
}
```

---

### Issue: Running out of disk space

**Cause:** Too many backup versions or large backups

**Solution:**
1. Reduce `max_versions`
2. Increase compression level
3. Exclude large unnecessary files

```python
config = {
    'max_versions': 3,  # Keep fewer versions
    'compression_level': 9,  # Maximum compression
}
```

---

## Best Practices

### 1. Test Restore Regularly

```python
# Periodically test that backups can be restored
backup_system.restore_backup('latest_backup.zip', './test_restore')
```

### 2. Store Backups Off-Site

```python
# Backup to external drive or network location
config = {
    'backup_destination': '/Volumes/External/Backups',
    # or
    'backup_destination': '//network/share/backups',
}
```

### 3. Use 3-2-1 Rule

- **3** copies of data
- **2** different media types
- **1** copy off-site

```python
# Local backup
local_config = {'backup_destination': './backups'}

# External drive backup
external_config = {'backup_destination': '/Volumes/External/Backups'}

# Cloud backup (via sync tool)
cloud_config = {'backup_destination': '~/Dropbox/Backups'}
```

### 4. Encrypt Sensitive Backups

```python
# After backup, encrypt the zip file
import subprocess

backup_file = 'backup.zip'
subprocess.run(['gpg', '-c', backup_file])  # Creates backup.zip.gpg
```

### 5. Document Backup Strategy

Create a backup plan document:
- What is backed up
- How often
- Where stored
- Retention policy
- Restore procedure

---

## Summary

The Backup Automation system provides:

- **Reliable** compression with ZIP format
- **Automatic** version management
- **Verified** integrity with checksums
- **Flexible** configuration
- **Notification** support
- **Easy** restore process

Perfect for automated backups of documents, source code, configurations, and more!

---

## Related Tools

- **Smart File Organizer** (`organize_files.py`) - Organize before backing up
- **Excel Files Merger** (`merge_excel_files.py`) - Consolidate before backing up
- **Bulk File Renamer** (`bulk_rename.py`) - Clean filenames before backing up

---

*Last updated: November 20, 2025*
