#!/usr/bin/env python3
"""
Bulk File Renamer
Advanced file renaming with patterns, previews, and undo functionality.
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BulkFileRenamer:
    """Class to handle bulk file renaming operations."""
    
    def __init__(self, target_folder, config=None):
        """
        Initialize the Bulk File Renamer.
        
        Args:
            target_folder (str): Path to folder containing files to rename
            config (dict): Configuration options
        """
        self.target_folder = Path(target_folder)
        
        # Default configuration
        self.config = {
            'preview_mode': True,  # Preview before renaming
            'recursive': False,    # Process subfolders
            'include_extensions': [],  # Only these extensions (empty = all)
            'exclude_extensions': [],  # Skip these extensions
            'include_hidden': False,   # Process hidden files
            'create_undo_file': True,  # Create undo history
        }
        
        if config:
            self.config.update(config)
        
        # Renaming operations
        self.operations = []
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'renamed_files': 0,
            'skipped_files': 0,
            'errors': 0,
        }
        
        # Undo history
        self.undo_file = self.target_folder / '.rename_undo.json'
        
        # Validate target folder
        if not self.target_folder.exists():
            raise ValueError(f"Target folder does not exist: {self.target_folder}")
    
    def get_files(self):
        """
        Get list of files to process.
        
        Returns:
            list: List of file paths
        """
        files = []
        
        if self.config.get('recursive', False):
            pattern = '**/*'
        else:
            pattern = '*'
        
        for item in self.target_folder.glob(pattern):
            if not item.is_file():
                continue
            
            # Skip hidden files
            if not self.config.get('include_hidden', False) and item.name.startswith('.'):
                continue
            
            # Check extensions
            include_exts = self.config.get('include_extensions', [])
            exclude_exts = self.config.get('exclude_extensions', [])
            
            if include_exts and item.suffix.lower() not in include_exts:
                continue
            
            if exclude_exts and item.suffix.lower() in exclude_exts:
                continue
            
            files.append(item)
            self.stats['total_files'] += 1
        
        return sorted(files)
    
    def apply_sequential_numbering(self, files, pattern='{name}_{counter}', start=1, step=1, padding=3):
        """
        Apply sequential numbering to filenames.
        
        Args:
            files (list): List of file paths
            pattern (str): Naming pattern with placeholders
            start (int): Starting number
            step (int): Increment step
            padding (int): Number of digits (zero-padding)
            
        Returns:
            list: List of (old_path, new_path) tuples
        """
        operations = []
        counter = start
        
        for file_path in files:
            old_name = file_path.stem
            extension = file_path.suffix
            
            # Replace placeholders
            new_name = pattern.replace('{name}', old_name)
            new_name = new_name.replace('{counter}', str(counter).zfill(padding))
            new_name = new_name.replace('{ext}', extension.lstrip('.'))
            
            # Add extension
            new_path = file_path.parent / f"{new_name}{extension}"
            
            operations.append((file_path, new_path))
            counter += step
        
        return operations
    
    def apply_find_replace(self, files, find, replace, use_regex=False, case_sensitive=True):
        """
        Find and replace in filenames.
        
        Args:
            files (list): List of file paths
            find (str): Text to find (or regex pattern)
            replace (str): Replacement text
            use_regex (bool): Use regular expressions
            case_sensitive (bool): Case-sensitive matching
            
        Returns:
            list: List of (old_path, new_path) tuples
        """
        operations = []
        
        for file_path in files:
            old_name = file_path.stem
            extension = file_path.suffix
            
            if use_regex:
                # Use regex
                flags = 0 if case_sensitive else re.IGNORECASE
                new_name = re.sub(find, replace, old_name, flags=flags)
            else:
                # Simple text replacement
                if case_sensitive:
                    new_name = old_name.replace(find, replace)
                else:
                    # Case-insensitive replacement
                    pattern = re.compile(re.escape(find), re.IGNORECASE)
                    new_name = pattern.sub(replace, old_name)
            
            new_path = file_path.parent / f"{new_name}{extension}"
            operations.append((file_path, new_path))
        
        return operations
    
    def apply_prefix_suffix(self, files, prefix='', suffix='', based_on=None):
        """
        Add prefix or suffix to filenames.
        
        Args:
            files (list): List of file paths
            prefix (str): Prefix to add
            suffix (str): Suffix to add
            based_on (str): Base on file property ('date', 'size', 'type')
            
        Returns:
            list: List of (old_path, new_path) tuples
        """
        operations = []
        
        for file_path in files:
            old_name = file_path.stem
            extension = file_path.suffix
            
            # Generate prefix/suffix based on property
            computed_prefix = prefix
            computed_suffix = suffix
            
            if based_on == 'date':
                # Use modification date
                mtime = file_path.stat().st_mtime
                date_str = datetime.fromtimestamp(mtime).strftime('%Y%m%d')
                computed_prefix = f"{date_str}_{computed_prefix}" if computed_prefix else date_str
            
            elif based_on == 'size':
                # Use file size category
                size = file_path.stat().st_size
                if size < 1024:
                    size_cat = 'tiny'
                elif size < 1024 * 1024:
                    size_cat = 'small'
                elif size < 1024 * 1024 * 10:
                    size_cat = 'medium'
                else:
                    size_cat = 'large'
                computed_suffix = f"{computed_suffix}_{size_cat}" if computed_suffix else size_cat
            
            elif based_on == 'type':
                # Use file extension
                ext_name = extension.lstrip('.').upper()
                computed_prefix = f"{ext_name}_{computed_prefix}" if computed_prefix else ext_name
            
            # Construct new name
            new_name = f"{computed_prefix}{old_name}{computed_suffix}"
            new_path = file_path.parent / f"{new_name}{extension}"
            
            operations.append((file_path, new_path))
        
        return operations
    
    def apply_case_change(self, files, case_type='lower'):
        """
        Change case of filenames.
        
        Args:
            files (list): List of file paths
            case_type (str): 'lower', 'upper', 'title', 'sentence', 'camel', 'snake'
            
        Returns:
            list: List of (old_path, new_path) tuples
        """
        operations = []
        
        for file_path in files:
            old_name = file_path.stem
            extension = file_path.suffix
            
            # Apply case transformation
            if case_type == 'lower':
                new_name = old_name.lower()
            elif case_type == 'upper':
                new_name = old_name.upper()
            elif case_type == 'title':
                new_name = old_name.title()
            elif case_type == 'sentence':
                new_name = old_name.capitalize()
            elif case_type == 'camel':
                # Convert to camelCase
                words = re.split(r'[\s_-]+', old_name)
                new_name = words[0].lower() + ''.join(w.capitalize() for w in words[1:])
            elif case_type == 'snake':
                # Convert to snake_case
                new_name = re.sub(r'[\s-]+', '_', old_name).lower()
            else:
                new_name = old_name
            
            new_path = file_path.parent / f"{new_name}{extension}"
            operations.append((file_path, new_path))
        
        return operations
    
    def remove_special_characters(self, files, keep_chars='', replace_with='_'):
        """
        Remove or replace special characters.
        
        Args:
            files (list): List of file paths
            keep_chars (str): Characters to keep (in addition to alphanumeric)
            replace_with (str): Character to replace special chars with
            
        Returns:
            list: List of (old_path, new_path) tuples
        """
        operations = []
        
        for file_path in files:
            old_name = file_path.stem
            extension = file_path.suffix
            
            # Create pattern for allowed characters
            allowed_chars = re.escape(keep_chars)
            pattern = f'[^a-zA-Z0-9{allowed_chars}]'
            
            # Replace special characters
            new_name = re.sub(pattern, replace_with, old_name)
            
            # Remove consecutive replace characters
            if replace_with:
                new_name = re.sub(f'{re.escape(replace_with)}+', replace_with, new_name)
            
            # Remove leading/trailing replace characters
            new_name = new_name.strip(replace_with)
            
            new_path = file_path.parent / f"{new_name}{extension}"
            operations.append((file_path, new_path))
        
        return operations
    
    def plan_rename(self, files, operation_type, **kwargs):
        """
        Plan rename operations based on type.
        
        Args:
            files (list): List of file paths
            operation_type (str): Type of operation
            **kwargs: Operation-specific parameters
            
        Returns:
            list: List of (old_path, new_path) tuples
        """
        if operation_type == 'sequential':
            return self.apply_sequential_numbering(files, **kwargs)
        elif operation_type == 'find_replace':
            return self.apply_find_replace(files, **kwargs)
        elif operation_type == 'prefix_suffix':
            return self.apply_prefix_suffix(files, **kwargs)
        elif operation_type == 'case_change':
            return self.apply_case_change(files, **kwargs)
        elif operation_type == 'remove_special':
            return self.remove_special_characters(files, **kwargs)
        else:
            raise ValueError(f"Unknown operation type: {operation_type}")
    
    def validate_operations(self, operations):
        """
        Validate rename operations for conflicts.
        
        Args:
            operations (list): List of (old_path, new_path) tuples
            
        Returns:
            tuple: (valid_operations, conflicts)
        """
        valid_operations = []
        conflicts = []
        target_names = defaultdict(list)
        
        # Check for naming conflicts
        for old_path, new_path in operations:
            # Skip if no change
            if old_path == new_path:
                self.stats['skipped_files'] += 1
                continue
            
            # Check if target already exists (and is not in rename list)
            if new_path.exists():
                source_files = [op[0] for op in operations]
                if new_path not in source_files:
                    conflicts.append((old_path, new_path, "Target file already exists"))
                    continue
            
            # Check for duplicate target names
            target_names[str(new_path)].append(old_path)
            
            valid_operations.append((old_path, new_path))
        
        # Find duplicates
        for target, sources in target_names.items():
            if len(sources) > 1:
                for source in sources:
                    conflicts.append((source, Path(target), f"Multiple files rename to same name"))
                    # Remove from valid operations
                    valid_operations = [(o, n) for o, n in valid_operations if o != source]
        
        return valid_operations, conflicts
    
    def execute_rename(self, operations):
        """
        Execute the rename operations.
        
        Args:
            operations (list): List of (old_path, new_path) tuples
        """
        undo_data = []
        
        for old_path, new_path in operations:
            try:
                # Rename the file
                old_path.rename(new_path)
                
                # Track for undo
                undo_data.append({
                    'old': str(old_path),
                    'new': str(new_path),
                    'timestamp': datetime.now().isoformat()
                })
                
                self.stats['renamed_files'] += 1
                logger.debug(f"Renamed: {old_path.name} -> {new_path.name}")
            
            except Exception as e:
                self.stats['errors'] += 1
                logger.error(f"Error renaming {old_path.name}: {e}")
        
        # Save undo information
        if self.config.get('create_undo_file', True) and undo_data:
            self.save_undo_data(undo_data)
    
    def save_undo_data(self, undo_data):
        """
        Save undo information to file.
        
        Args:
            undo_data (list): List of rename operations
        """
        try:
            # Load existing undo data
            if self.undo_file.exists():
                with open(self.undo_file, 'r') as f:
                    existing_data = json.load(f)
            else:
                existing_data = []
            
            # Append new data
            existing_data.append({
                'timestamp': datetime.now().isoformat(),
                'operations': undo_data
            })
            
            # Save
            with open(self.undo_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
            
            logger.info(f"Undo data saved to: {self.undo_file}")
        
        except Exception as e:
            logger.error(f"Error saving undo data: {e}")
    
    def undo_last_rename(self):
        """
        Undo the last rename operation.
        
        Returns:
            bool: True if successful
        """
        if not self.undo_file.exists():
            logger.error("No undo file found")
            return False
        
        try:
            # Load undo data
            with open(self.undo_file, 'r') as f:
                undo_history = json.load(f)
            
            if not undo_history:
                logger.error("No operations to undo")
                return False
            
            # Get last operation
            last_operation = undo_history.pop()
            operations = last_operation['operations']
            
            # Reverse the operations (new -> old)
            logger.info(f"Undoing {len(operations)} rename operations...")
            
            for op in reversed(operations):
                try:
                    new_path = Path(op['new'])
                    old_path = Path(op['old'])
                    
                    if new_path.exists():
                        new_path.rename(old_path)
                        logger.debug(f"Reverted: {new_path.name} -> {old_path.name}")
                    else:
                        logger.warning(f"File not found: {new_path}")
                
                except Exception as e:
                    logger.error(f"Error reverting {op['new']}: {e}")
            
            # Update undo file
            with open(self.undo_file, 'w') as f:
                json.dump(undo_history, f, indent=2)
            
            logger.info("Undo completed successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error during undo: {e}")
            return False
    
    def generate_preview(self, operations, conflicts):
        """
        Generate a preview of rename operations.
        
        Args:
            operations (list): Valid operations
            conflicts (list): Conflicting operations
            
        Returns:
            str: Preview text
        """
        lines = [
            "=" * 80,
            "BULK FILE RENAME PREVIEW",
            "=" * 80,
            f"Target Folder: {self.target_folder}",
            f"Total Files: {self.stats['total_files']}",
            f"Files to Rename: {len(operations)}",
            f"Files Skipped: {self.stats['skipped_files']}",
            f"Conflicts: {len(conflicts)}",
            "",
        ]
        
        # Show operations
        if operations:
            lines.append("RENAME OPERATIONS:")
            for old_path, new_path in operations[:20]:  # Show first 20
                lines.append(f"  {old_path.name}")
                lines.append(f"    -> {new_path.name}")
            
            if len(operations) > 20:
                lines.append(f"  ... and {len(operations) - 20} more")
            lines.append("")
        
        # Show conflicts
        if conflicts:
            lines.append("CONFLICTS (will be skipped):")
            for old_path, new_path, reason in conflicts[:10]:
                lines.append(f"  {old_path.name} -> {new_path.name}")
                lines.append(f"    Reason: {reason}")
            
            if len(conflicts) > 10:
                lines.append(f"  ... and {len(conflicts) - 10} more")
            lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def rename(self, operation_type, **kwargs):
        """
        Execute the complete rename process.
        
        Args:
            operation_type (str): Type of renaming operation
            **kwargs: Operation-specific parameters
            
        Returns:
            str: Preview or result message
        """
        logger.info("=" * 80)
        logger.info("STARTING BULK FILE RENAME")
        logger.info("=" * 80)
        
        # Get files
        files = self.get_files()
        
        if not files:
            logger.warning("No files found to rename")
            return "No files found to rename"
        
        logger.info(f"Found {len(files)} file(s) to process")
        
        # Plan rename operations
        operations = self.plan_rename(files, operation_type, **kwargs)
        
        # Validate operations
        valid_operations, conflicts = self.validate_operations(operations)
        
        # Generate preview
        preview = self.generate_preview(valid_operations, conflicts)
        
        # Preview mode
        if self.config.get('preview_mode', True):
            logger.info("\nPREVIEW MODE: No files will be renamed")
            logger.info("Set 'preview_mode': False to execute rename\n")
            print(preview)
            return preview
        
        # Execute rename
        if valid_operations:
            logger.info(f"Renaming {len(valid_operations)} file(s)...")
            self.execute_rename(valid_operations)
        
        # Generate result
        logger.info("=" * 80)
        logger.info("RENAME COMPLETE")
        logger.info(f"Files Renamed: {self.stats['renamed_files']}")
        logger.info(f"Files Skipped: {self.stats['skipped_files']}")
        logger.info(f"Errors: {self.stats['errors']}")
        logger.info("=" * 80)
        
        return preview


def main():
    """Main execution function."""
    
    # Configuration
    config = {
        'preview_mode': True,  # Set to False to actually rename
        'recursive': False,
        'create_undo_file': True,
    }
    
    # Get target folder
    if len(sys.argv) > 1:
        target_folder = sys.argv[1]
    else:
        target_folder = "./test_files"
        logger.info(f"No folder specified, using default: {target_folder}")
    
    try:
        # Create renamer
        renamer = BulkFileRenamer(target_folder, config)
        
        # Example: Sequential numbering
        # renamer.rename('sequential', pattern='{name}_{counter}', start=1, padding=3)
        
        # Example: Find and replace
        # renamer.rename('find_replace', find='old', replace='new', case_sensitive=False)
        
        # Example: Add prefix/suffix
        # renamer.rename('prefix_suffix', prefix='IMG_', suffix='_backup')
        
        # Example: Change case
        # renamer.rename('case_change', case_type='lower')
        
        # Example: Remove special characters
        renamer.rename('remove_special', keep_chars='_-', replace_with='_')
        
        print("\n✓ Preview generated successfully!")
        print("To execute rename, set 'preview_mode': False in config")
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
