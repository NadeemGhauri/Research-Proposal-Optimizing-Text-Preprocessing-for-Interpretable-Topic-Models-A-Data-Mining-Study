#!/usr/bin/env python3
"""
Automated Backup System
Comprehensive backup solution with compression, versioning, and integrity verification.
"""

import os
import sys
import shutil
import zipfile
import hashlib
import json
import smtplib
from pathlib import Path
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BackupAutomation:
    """Class to handle automated backup operations."""
    
    def __init__(self, config=None):
        """
        Initialize the Backup Automation system.
        
        Args:
            config (dict): Configuration options
        """
        # Default configuration
        self.config = {
            'backup_sources': [],          # List of folders to backup
            'backup_destination': './backups',  # Where to store backups
            'max_versions': 7,             # Keep last N versions
            'compression_level': 9,        # 0-9 (9 = maximum compression)
            'verify_integrity': True,      # Verify backups after creation
            'send_notifications': False,   # Send email notifications
            'notification_email': '',      # Email to send notifications to
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_user': '',
            'smtp_password': '',
            'exclude_patterns': [          # Patterns to exclude
                '*.tmp', '*.log', '.DS_Store', '__pycache__', 
                '*.pyc', '.git', 'node_modules', '.venv'
            ],
            'include_subdirs': True,       # Include subdirectories
            'follow_symlinks': False,      # Follow symbolic links
        }
        
        if config:
            self.config.update(config)
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'total_size': 0,
            'compressed_size': 0,
            'backup_duration': 0,
            'files_skipped': 0,
            'errors': 0,
        }
        
        # Backup metadata
        self.metadata = {
            'timestamp': None,
            'source_folders': [],
            'file_count': 0,
            'original_size': 0,
            'compressed_size': 0,
            'checksum': None,
            'compression_ratio': 0,
        }
        
        # Create backup destination
        self.backup_dir = Path(self.config['backup_destination'])
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def should_exclude(self, file_path):
        """
        Check if file should be excluded based on patterns.
        
        Args:
            file_path (Path): Path to check
            
        Returns:
            bool: True if should be excluded
        """
        file_str = str(file_path)
        file_name = file_path.name
        
        for pattern in self.config.get('exclude_patterns', []):
            # Simple wildcard matching
            if pattern.startswith('*'):
                if file_name.endswith(pattern[1:]):
                    return True
            elif pattern.endswith('*'):
                if file_name.startswith(pattern[:-1]):
                    return True
            else:
                if pattern in file_str or file_name == pattern:
                    return True
        
        return False
    
    def get_files_to_backup(self, source_folder):
        """
        Get list of files to backup from source folder.
        
        Args:
            source_folder (Path): Source folder path
            
        Returns:
            list: List of file paths
        """
        files = []
        source_folder = Path(source_folder)
        
        if not source_folder.exists():
            logger.warning(f"Source folder does not exist: {source_folder}")
            return files
        
        if source_folder.is_file():
            # Single file
            if not self.should_exclude(source_folder):
                files.append(source_folder)
            return files
        
        # Directory
        if self.config.get('include_subdirs', True):
            pattern = '**/*'
        else:
            pattern = '*'
        
        for item in source_folder.glob(pattern):
            # Skip if should exclude
            if self.should_exclude(item):
                self.stats['files_skipped'] += 1
                continue
            
            # Skip directories
            if item.is_dir():
                continue
            
            # Handle symlinks
            if item.is_symlink() and not self.config.get('follow_symlinks', False):
                logger.debug(f"Skipping symlink: {item}")
                continue
            
            files.append(item)
            self.stats['total_files'] += 1
            self.stats['total_size'] += item.stat().st_size
        
        return files
    
    def create_backup_archive(self, backup_name):
        """
        Create compressed backup archive.
        
        Args:
            backup_name (str): Name for the backup file
            
        Returns:
            Path: Path to created backup file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{backup_name}_{timestamp}.zip"
        backup_path = self.backup_dir / backup_filename
        
        logger.info(f"Creating backup archive: {backup_filename}")
        
        # Get all files from all source folders
        all_files = []
        source_folders = self.config.get('backup_sources', [])
        
        if not source_folders:
            logger.error("No backup sources specified")
            return None
        
        for source in source_folders:
            source_path = Path(source)
            logger.info(f"Scanning source: {source_path}")
            files = self.get_files_to_backup(source_path)
            all_files.extend(files)
            self.metadata['source_folders'].append(str(source_path))
        
        if not all_files:
            logger.warning("No files found to backup")
            return None
        
        logger.info(f"Found {len(all_files)} file(s) to backup")
        
        # Create zip archive
        try:
            compression = zipfile.ZIP_DEFLATED
            compress_level = self.config.get('compression_level', 9)
            
            with zipfile.ZipFile(backup_path, 'w', compression, compresslevel=compress_level) as zipf:
                for file_path in all_files:
                    try:
                        # Calculate relative path for archive
                        # Try to find the source folder this file belongs to
                        arcname = None
                        for source in source_folders:
                            source_path = Path(source)
                            try:
                                arcname = file_path.relative_to(source_path.parent)
                                break
                            except ValueError:
                                continue
                        
                        if arcname is None:
                            arcname = file_path.name
                        
                        zipf.write(file_path, arcname)
                        logger.debug(f"Added to archive: {arcname}")
                    
                    except Exception as e:
                        logger.error(f"Error adding {file_path} to archive: {e}")
                        self.stats['errors'] += 1
            
            # Update metadata
            self.metadata['file_count'] = len(all_files)
            self.metadata['original_size'] = self.stats['total_size']
            self.metadata['compressed_size'] = backup_path.stat().st_size
            self.stats['compressed_size'] = self.metadata['compressed_size']
            
            if self.metadata['original_size'] > 0:
                ratio = (1 - self.metadata['compressed_size'] / self.metadata['original_size']) * 100
                self.metadata['compression_ratio'] = round(ratio, 2)
            
            logger.info(f"Backup created: {backup_path}")
            logger.info(f"Original size: {self._format_size(self.metadata['original_size'])}")
            logger.info(f"Compressed size: {self._format_size(self.metadata['compressed_size'])}")
            logger.info(f"Compression ratio: {self.metadata['compression_ratio']}%")
            
            return backup_path
        
        except Exception as e:
            logger.error(f"Error creating backup archive: {e}")
            self.stats['errors'] += 1
            return None
    
    def verify_backup_integrity(self, backup_path):
        """
        Verify backup file integrity using checksum.
        
        Args:
            backup_path (Path): Path to backup file
            
        Returns:
            tuple: (is_valid, checksum)
        """
        logger.info("Verifying backup integrity...")
        
        try:
            # Calculate MD5 checksum
            md5_hash = hashlib.md5()
            
            with open(backup_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    md5_hash.update(chunk)
            
            checksum = md5_hash.hexdigest()
            
            # Verify zip file can be opened
            try:
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    # Test the archive
                    bad_file = zipf.testzip()
                    if bad_file:
                        logger.error(f"Corrupted file in archive: {bad_file}")
                        return False, checksum
            except zipfile.BadZipFile:
                logger.error("Backup archive is corrupted")
                return False, checksum
            
            logger.info(f"Backup verified successfully. Checksum: {checksum}")
            return True, checksum
        
        except Exception as e:
            logger.error(f"Error verifying backup: {e}")
            return False, None
    
    def save_backup_metadata(self, backup_path, checksum):
        """
        Save backup metadata to JSON file.
        
        Args:
            backup_path (Path): Path to backup file
            checksum (str): Backup file checksum
        """
        metadata_path = backup_path.with_suffix('.json')
        
        self.metadata['timestamp'] = datetime.now().isoformat()
        self.metadata['checksum'] = checksum
        self.metadata['backup_file'] = backup_path.name
        
        try:
            with open(metadata_path, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            
            logger.info(f"Metadata saved: {metadata_path}")
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
    
    def cleanup_old_backups(self):
        """
        Remove old backup versions, keeping only the latest N versions.
        """
        max_versions = self.config.get('max_versions', 7)
        logger.info(f"Cleaning up old backups (keeping last {max_versions} versions)...")
        
        # Get all backup files
        backup_files = sorted(
            self.backup_dir.glob('*.zip'),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        if len(backup_files) <= max_versions:
            logger.info(f"No cleanup needed. Found {len(backup_files)} backup(s).")
            return
        
        # Remove old backups
        files_to_remove = backup_files[max_versions:]
        
        for old_backup in files_to_remove:
            try:
                # Remove backup file
                old_backup.unlink()
                logger.info(f"Removed old backup: {old_backup.name}")
                
                # Remove associated metadata file
                metadata_file = old_backup.with_suffix('.json')
                if metadata_file.exists():
                    metadata_file.unlink()
                    logger.debug(f"Removed metadata: {metadata_file.name}")
            
            except Exception as e:
                logger.error(f"Error removing {old_backup.name}: {e}")
        
        logger.info(f"Cleanup complete. Removed {len(files_to_remove)} old backup(s).")
    
    def send_notification(self, success, backup_path=None, error_msg=None):
        """
        Send email notification about backup status.
        
        Args:
            success (bool): Whether backup was successful
            backup_path (Path): Path to backup file
            error_msg (str): Error message if failed
        """
        if not self.config.get('send_notifications', False):
            return
        
        email = self.config.get('notification_email')
        if not email:
            logger.warning("No notification email configured")
            return
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config.get('smtp_user', '')
            msg['To'] = email
            
            if success:
                msg['Subject'] = f"✓ Backup Completed Successfully - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                
                body = f"""
Backup completed successfully!

Backup Details:
- Timestamp: {self.metadata.get('timestamp', 'N/A')}
- Backup File: {backup_path.name if backup_path else 'N/A'}
- Files Backed Up: {self.metadata.get('file_count', 0)}
- Original Size: {self._format_size(self.metadata.get('original_size', 0))}
- Compressed Size: {self._format_size(self.metadata.get('compressed_size', 0))}
- Compression Ratio: {self.metadata.get('compression_ratio', 0)}%
- Checksum: {self.metadata.get('checksum', 'N/A')}

Source Folders:
{chr(10).join(f"- {folder}" for folder in self.metadata.get('source_folders', []))}

Statistics:
- Files Skipped: {self.stats['files_skipped']}
- Errors: {self.stats['errors']}
- Duration: {self.stats.get('backup_duration', 0):.2f} seconds

---
Automated Backup System
"""
            else:
                msg['Subject'] = f"✗ Backup Failed - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                
                body = f"""
Backup FAILED!

Error: {error_msg or 'Unknown error'}

Please check the backup system and try again.

---
Automated Backup System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(
                self.config.get('smtp_server', 'smtp.gmail.com'),
                self.config.get('smtp_port', 587)
            )
            server.starttls()
            server.login(
                self.config.get('smtp_user', ''),
                self.config.get('smtp_password', '')
            )
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Notification sent to {email}")
        
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
    
    def run_backup(self, backup_name='backup'):
        """
        Execute the complete backup process.
        
        Args:
            backup_name (str): Base name for backup file
            
        Returns:
            bool: True if backup was successful
        """
        start_time = datetime.now()
        
        logger.info("=" * 80)
        logger.info("STARTING AUTOMATED BACKUP")
        logger.info("=" * 80)
        
        try:
            # Create backup archive
            backup_path = self.create_backup_archive(backup_name)
            
            if not backup_path:
                logger.error("Failed to create backup archive")
                self.send_notification(False, error_msg="Failed to create backup archive")
                return False
            
            # Verify backup integrity
            if self.config.get('verify_integrity', True):
                is_valid, checksum = self.verify_backup_integrity(backup_path)
                
                if not is_valid:
                    logger.error("Backup verification failed!")
                    self.send_notification(False, backup_path, "Backup verification failed")
                    return False
                
                # Save metadata
                self.save_backup_metadata(backup_path, checksum)
            
            # Cleanup old backups
            self.cleanup_old_backups()
            
            # Calculate duration
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            self.stats['backup_duration'] = duration
            
            # Send success notification
            self.send_notification(True, backup_path)
            
            # Print summary
            logger.info("=" * 80)
            logger.info("BACKUP COMPLETED SUCCESSFULLY")
            logger.info(f"Backup File: {backup_path.name}")
            logger.info(f"Files Backed Up: {self.metadata['file_count']}")
            logger.info(f"Original Size: {self._format_size(self.metadata['original_size'])}")
            logger.info(f"Compressed Size: {self._format_size(self.metadata['compressed_size'])}")
            logger.info(f"Compression Ratio: {self.metadata['compression_ratio']}%")
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info("=" * 80)
            
            return True
        
        except Exception as e:
            logger.error(f"Fatal error during backup: {e}")
            self.send_notification(False, error_msg=str(e))
            return False
    
    def list_backups(self):
        """
        List all available backups with metadata.
        
        Returns:
            list: List of backup information dicts
        """
        backups = []
        
        for backup_file in sorted(self.backup_dir.glob('*.zip'), key=lambda p: p.stat().st_mtime, reverse=True):
            metadata_file = backup_file.with_suffix('.json')
            
            backup_info = {
                'filename': backup_file.name,
                'size': backup_file.stat().st_size,
                'created': datetime.fromtimestamp(backup_file.stat().st_mtime),
            }
            
            # Load metadata if available
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                        backup_info.update(metadata)
                except Exception as e:
                    logger.error(f"Error reading metadata for {backup_file.name}: {e}")
            
            backups.append(backup_info)
        
        return backups
    
    def restore_backup(self, backup_file, restore_path):
        """
        Restore files from a backup archive.
        
        Args:
            backup_file (str): Name of backup file to restore
            restore_path (str): Path where to restore files
            
        Returns:
            bool: True if restore was successful
        """
        backup_path = self.backup_dir / backup_file
        
        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_file}")
            return False
        
        restore_path = Path(restore_path)
        restore_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Restoring backup: {backup_file}")
        logger.info(f"Restore location: {restore_path}")
        
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(restore_path)
            
            logger.info("Restore completed successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False
    
    def _format_size(self, size_bytes):
        """
        Format bytes to human-readable size.
        
        Args:
            size_bytes (int): Size in bytes
            
        Returns:
            str: Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"


def main():
    """Main execution function."""
    
    # Example configuration
    config = {
        'backup_sources': [
            './data',           # Backup the data folder
            './config',         # Backup the config folder
        ],
        'backup_destination': './backups',
        'max_versions': 7,
        'compression_level': 9,
        'verify_integrity': True,
        'send_notifications': False,  # Set to True to enable email notifications
        'notification_email': 'your-email@example.com',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'smtp_user': 'your-email@example.com',
        'smtp_password': 'your-app-password',  # Use app-specific password
        'exclude_patterns': [
            '*.tmp', '*.log', '.DS_Store', '__pycache__',
            '*.pyc', '.git', 'node_modules', '.venv', '*.cache'
        ],
        'include_subdirs': True,
        'follow_symlinks': False,
    }
    
    try:
        # Create backup system
        backup_system = BackupAutomation(config)
        
        # Run backup
        success = backup_system.run_backup(backup_name='project_backup')
        
        if success:
            print("\n✓ Backup completed successfully!")
            
            # List all backups
            print("\n" + "=" * 80)
            print("AVAILABLE BACKUPS:")
            print("=" * 80)
            
            backups = backup_system.list_backups()
            for i, backup in enumerate(backups, 1):
                print(f"\n{i}. {backup['filename']}")
                print(f"   Size: {backup_system._format_size(backup['size'])}")
                print(f"   Created: {backup['created']}")
                if 'file_count' in backup:
                    print(f"   Files: {backup['file_count']}")
                if 'checksum' in backup:
                    print(f"   Checksum: {backup['checksum']}")
        else:
            print("\n✗ Backup failed! Check logs for details.")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
