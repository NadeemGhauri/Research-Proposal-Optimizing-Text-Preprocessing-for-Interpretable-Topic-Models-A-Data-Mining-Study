#!/usr/bin/env python3
"""
Smart File Organizer
Intelligent file organization with type detection, duplicate removal, and safe mode.
"""

import os
import sys
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import mimetypes
import json
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SmartFileOrganizer:
    """Class to handle intelligent file organization operations."""
    
    # File type categories
    FILE_CATEGORIES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff', '.raw'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'],
        'Code': ['.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs', '.swift'],
        'Web': ['.html', '.htm', '.css', '.scss', '.sass', '.less', '.json', '.xml', '.yml', '.yaml'],
        'Executables': ['.exe', '.msi', '.app', '.deb', '.rpm', '.dmg', '.pkg'],
        'Fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot'],
        'eBooks': ['.epub', '.mobi', '.azw', '.azw3', '.fb2'],
    }
    
    def __init__(self, source_folder, target_folder=None, config=None):
        """
        Initialize the Smart File Organizer.
        
        Args:
            source_folder (str): Path to folder to organize
            target_folder (str): Path to organized output folder (defaults to source_folder)
            config (dict): Configuration options
        """
        self.source_folder = Path(source_folder)
        self.target_folder = Path(target_folder) if target_folder else self.source_folder / 'Organized'
        
        # Default configuration
        self.config = {
            'organize_by_type': True,
            'organize_by_date': False,
            'rename_files': False,
            'naming_pattern': '{original_name}',  # or '{date}_{counter}_{original_name}'
            'remove_duplicates': True,
            'safe_mode': True,  # Preview before moving
            'create_report': True,
            'date_format': '%Y-%m',  # YYYY-MM for monthly folders
            'min_file_size': 0,  # Minimum file size in bytes (0 = all files)
            'exclude_extensions': [],  # Extensions to skip
            'include_hidden': False,  # Include hidden files
        }
        
        if config:
            self.config.update(config)
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'organized_files': 0,
            'skipped_files': 0,
            'duplicates_found': 0,
            'duplicates_removed': 0,
            'errors': 0,
            'categories': defaultdict(int),
            'space_saved': 0,
        }
        
        # Duplicate tracking
        self.file_hashes = {}
        self.duplicate_files = []
        
        # Operations log for safe mode
        self.operations = []
        
        # Validate source folder
        if not self.source_folder.exists():
            raise ValueError(f"Source folder does not exist: {self.source_folder}")
    
    def get_file_hash(self, file_path):
        """
        Calculate MD5 hash of a file for duplicate detection.
        
        Args:
            file_path (Path): Path to file
            
        Returns:
            str: MD5 hash of file
        """
        hasher = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                # Read in chunks for large files
                for chunk in iter(lambda: f.read(4096), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return None
    
    def get_file_category(self, file_path):
        """
        Determine the category of a file based on its extension.
        
        Args:
            file_path (Path): Path to file
            
        Returns:
            str: Category name or 'Other'
        """
        extension = file_path.suffix.lower()
        
        for category, extensions in self.FILE_CATEGORIES.items():
            if extension in extensions:
                return category
        
        return 'Other'
    
    def get_date_folder(self, file_path):
        """
        Get the date-based folder name for a file.
        
        Args:
            file_path (Path): Path to file
            
        Returns:
            str: Date folder name (e.g., '2024-01' or '2024/January')
        """
        try:
            # Get modification time
            mtime = file_path.stat().st_mtime
            date_obj = datetime.fromtimestamp(mtime)
            
            # Format based on config
            date_format = self.config.get('date_format', '%Y-%m')
            return date_obj.strftime(date_format)
        
        except Exception as e:
            logger.error(f"Error getting date for {file_path}: {e}")
            return 'Unknown_Date'
    
    def generate_new_filename(self, file_path, counter=1):
        """
        Generate a new filename based on naming pattern.
        
        Args:
            file_path (Path): Original file path
            counter (int): Counter for duplicate names
            
        Returns:
            str: New filename
        """
        pattern = self.config.get('naming_pattern', '{original_name}')
        
        # Get file info
        original_name = file_path.stem
        extension = file_path.suffix
        
        # Get date
        try:
            mtime = file_path.stat().st_mtime
            date_obj = datetime.fromtimestamp(mtime)
            date_str = date_obj.strftime('%Y%m%d')
        except:
            date_str = 'unknown'
        
        # Replace placeholders
        new_name = pattern.replace('{original_name}', original_name)
        new_name = new_name.replace('{date}', date_str)
        new_name = new_name.replace('{counter}', str(counter).zfill(3))
        new_name = new_name.replace('{category}', self.get_file_category(file_path))
        
        return f"{new_name}{extension}"
    
    def get_target_path(self, file_path, counter=1):
        """
        Determine the target path for a file.
        
        Args:
            file_path (Path): Original file path
            counter (int): Counter for naming
            
        Returns:
            Path: Target path for the file
        """
        target_path = self.target_folder
        
        # Organize by type
        if self.config.get('organize_by_type', True):
            category = self.get_file_category(file_path)
            target_path = target_path / category
            self.stats['categories'][category] += 1
        
        # Organize by date
        if self.config.get('organize_by_date', False):
            date_folder = self.get_date_folder(file_path)
            target_path = target_path / date_folder
        
        # Generate filename
        if self.config.get('rename_files', False):
            filename = self.generate_new_filename(file_path, counter)
        else:
            filename = file_path.name
        
        return target_path / filename
    
    def is_duplicate(self, file_path):
        """
        Check if a file is a duplicate.
        
        Args:
            file_path (Path): Path to file
            
        Returns:
            tuple: (is_duplicate, original_file_path)
        """
        if not self.config.get('remove_duplicates', True):
            return False, None
        
        file_hash = self.get_file_hash(file_path)
        
        if file_hash is None:
            return False, None
        
        if file_hash in self.file_hashes:
            self.stats['duplicates_found'] += 1
            return True, self.file_hashes[file_hash]
        
        self.file_hashes[file_hash] = file_path
        return False, None
    
    def should_process_file(self, file_path):
        """
        Determine if a file should be processed.
        
        Args:
            file_path (Path): Path to file
            
        Returns:
            bool: True if file should be processed
        """
        # Skip if not a file
        if not file_path.is_file():
            return False
        
        # Skip hidden files if configured
        if not self.config.get('include_hidden', False) and file_path.name.startswith('.'):
            return False
        
        # Skip excluded extensions
        if file_path.suffix.lower() in self.config.get('exclude_extensions', []):
            return False
        
        # Skip files below minimum size
        try:
            if file_path.stat().st_size < self.config.get('min_file_size', 0):
                return False
        except:
            return False
        
        return True
    
    def scan_files(self):
        """
        Scan source folder and collect files to organize.
        
        Returns:
            list: List of file paths to process
        """
        logger.info(f"Scanning folder: {self.source_folder}")
        files_to_process = []
        
        for item in self.source_folder.rglob('*'):
            if self.should_process_file(item):
                files_to_process.append(item)
                self.stats['total_files'] += 1
        
        logger.info(f"Found {len(files_to_process)} files to process")
        return files_to_process
    
    def plan_operations(self, files):
        """
        Plan all file operations without executing them.
        
        Args:
            files (list): List of file paths
            
        Returns:
            list: List of operations (dict with action, source, target, reason)
        """
        logger.info("Planning operations...")
        operations = []
        file_counters = defaultdict(int)
        
        for file_path in files:
            # Check for duplicates
            is_dup, original_file = self.is_duplicate(file_path)
            
            if is_dup:
                operations.append({
                    'action': 'skip_duplicate',
                    'source': str(file_path),
                    'target': None,
                    'reason': f'Duplicate of {original_file}',
                    'size': file_path.stat().st_size
                })
                self.duplicate_files.append((file_path, original_file))
                continue
            
            # Determine target path
            target_path = self.get_target_path(file_path, file_counters[file_path.name])
            
            # Handle name conflicts
            while target_path.exists() and target_path != file_path:
                file_counters[file_path.name] += 1
                target_path = self.get_target_path(file_path, file_counters[file_path.name])
            
            # Skip if source and target are the same
            if target_path == file_path:
                operations.append({
                    'action': 'skip_same',
                    'source': str(file_path),
                    'target': str(target_path),
                    'reason': 'Already in correct location',
                    'size': file_path.stat().st_size
                })
                self.stats['skipped_files'] += 1
                continue
            
            operations.append({
                'action': 'move',
                'source': str(file_path),
                'target': str(target_path),
                'reason': 'Organize file',
                'size': file_path.stat().st_size
            })
        
        self.operations = operations
        logger.info(f"Planned {len(operations)} operations")
        return operations
    
    def execute_operations(self):
        """Execute the planned operations."""
        logger.info("Executing operations...")
        
        for operation in self.operations:
            try:
                if operation['action'] == 'move':
                    source = Path(operation['source'])
                    target = Path(operation['target'])
                    
                    # Create target directory
                    target.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Move file
                    shutil.move(str(source), str(target))
                    self.stats['organized_files'] += 1
                    logger.debug(f"Moved: {source.name} -> {target}")
                
                elif operation['action'] == 'skip_duplicate':
                    # Optionally remove duplicate
                    if self.config.get('remove_duplicates', True):
                        source = Path(operation['source'])
                        file_size = operation['size']
                        source.unlink()
                        self.stats['duplicates_removed'] += 1
                        self.stats['space_saved'] += file_size
                        logger.debug(f"Removed duplicate: {source.name}")
                
                elif operation['action'] == 'skip_same':
                    # Do nothing
                    pass
            
            except Exception as e:
                self.stats['errors'] += 1
                logger.error(f"Error processing {operation['source']}: {e}")
    
    def generate_report(self):
        """
        Generate a detailed organization report.
        
        Returns:
            str: Report text
        """
        report_lines = [
            "=" * 80,
            "SMART FILE ORGANIZER REPORT",
            "=" * 80,
            f"Source Folder: {self.source_folder}",
            f"Target Folder: {self.target_folder}",
            f"Organization Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "CONFIGURATION:",
            f"  - Organize by Type: {self.config['organize_by_type']}",
            f"  - Organize by Date: {self.config['organize_by_date']}",
            f"  - Rename Files: {self.config['rename_files']}",
            f"  - Remove Duplicates: {self.config['remove_duplicates']}",
            f"  - Safe Mode: {self.config['safe_mode']}",
            "",
            "STATISTICS:",
            f"  - Total Files Found: {self.stats['total_files']:,}",
            f"  - Files Organized: {self.stats['organized_files']:,}",
            f"  - Files Skipped: {self.stats['skipped_files']:,}",
            f"  - Duplicates Found: {self.stats['duplicates_found']:,}",
            f"  - Duplicates Removed: {self.stats['duplicates_removed']:,}",
            f"  - Space Saved: {self._format_size(self.stats['space_saved'])}",
            f"  - Errors: {self.stats['errors']:,}",
            "",
        ]
        
        # Category breakdown
        if self.stats['categories']:
            report_lines.append("FILES BY CATEGORY:")
            for category, count in sorted(self.stats['categories'].items(), key=lambda x: x[1], reverse=True):
                report_lines.append(f"  - {category}: {count:,} files")
            report_lines.append("")
        
        # Duplicates list
        if self.duplicate_files and len(self.duplicate_files) <= 20:
            report_lines.append("DUPLICATE FILES:")
            for dup, original in self.duplicate_files[:20]:
                report_lines.append(f"  - {dup.name} (duplicate of {original.name})")
            if len(self.duplicate_files) > 20:
                report_lines.append(f"  ... and {len(self.duplicate_files) - 20} more")
            report_lines.append("")
        
        # Operations preview (if safe mode)
        if self.config['safe_mode'] and self.operations:
            report_lines.append("PLANNED OPERATIONS (Safe Mode - Preview):")
            move_ops = [op for op in self.operations if op['action'] == 'move']
            for op in move_ops[:10]:
                report_lines.append(f"  - MOVE: {Path(op['source']).name} -> {op['target']}")
            if len(move_ops) > 10:
                report_lines.append(f"  ... and {len(move_ops) - 10} more operations")
            report_lines.append("")
        
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def _format_size(self, size_bytes):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def save_report(self, report_text):
        """Save report to file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.target_folder.parent / f"organization_report_{timestamp}.txt"
        
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write(report_text)
        
        logger.info(f"Report saved to: {report_path}")
        return report_path
    
    def organize(self):
        """
        Execute the complete file organization process.
        
        Returns:
            str: Report text
        """
        logger.info("=" * 80)
        logger.info("STARTING SMART FILE ORGANIZATION")
        logger.info("=" * 80)
        
        # Scan files
        files = self.scan_files()
        
        if not files:
            logger.warning("No files found to organize")
            return None
        
        # Plan operations
        self.plan_operations(files)
        
        # Generate report
        report = self.generate_report()
        
        # Safe mode - preview only
        if self.config['safe_mode']:
            logger.info("\n" + "=" * 80)
            logger.info("SAFE MODE: Preview only - No files will be moved")
            logger.info("Set 'safe_mode': false in config to execute operations")
            logger.info("=" * 80)
            print("\n" + report)
            
            # Save report
            if self.config['create_report']:
                self.save_report(report)
            
            return report
        
        # Execute operations
        self.execute_operations()
        
        # Regenerate report with execution results
        report = self.generate_report()
        
        # Save report
        if self.config['create_report']:
            self.save_report(report)
        
        logger.info("=" * 80)
        logger.info("FILE ORGANIZATION COMPLETE")
        logger.info("=" * 80)
        
        return report


def main():
    """Main execution function."""
    
    # Example configuration
    config = {
        'organize_by_type': True,
        'organize_by_date': False,
        'rename_files': False,
        'naming_pattern': '{original_name}',
        'remove_duplicates': True,
        'safe_mode': True,  # Set to False to actually move files
        'create_report': True,
        'date_format': '%Y-%m',
        'min_file_size': 0,
        'exclude_extensions': ['.tmp', '.cache'],
        'include_hidden': False,
    }
    
    # Get source folder from command line or use default
    if len(sys.argv) > 1:
        source_folder = sys.argv[1]
    else:
        source_folder = "./test_files"
        logger.info(f"No source folder specified, using default: {source_folder}")
    
    # Get target folder from command line or use default
    if len(sys.argv) > 2:
        target_folder = sys.argv[2]
    else:
        target_folder = None  # Will create 'Organized' subfolder
    
    try:
        # Create organizer
        organizer = SmartFileOrganizer(source_folder, target_folder, config)
        
        # Run organization
        report = organizer.organize()
        
        if report:
            print("\n✓ Organization complete! Check the report above.")
        else:
            print("\n✗ No files to organize.")
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
