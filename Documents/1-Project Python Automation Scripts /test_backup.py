#!/usr/bin/env python3
"""
Test script for Backup Automation System.
Tests all backup features including compression, versioning, and integrity verification.
"""

import sys
import os
from pathlib import Path
import shutil
import time

# Add parent directory to path
sys.path.insert(0, '/Users/nadeemghauri/Documents/1-Project Python Automation Scripts ')

from backup_automation import BackupAutomation


def setup_test_environment():
    """Create test folders and files."""
    print("\n" + "="*80)
    print("SETTING UP TEST ENVIRONMENT")
    print("="*80)
    
    # Create test source folders
    test_source1 = Path('./backup_test/source1')
    test_source2 = Path('./backup_test/source2')
    test_backup_dir = Path('./backup_test/backups')
    
    # Clean up if exists
    if Path('./backup_test').exists():
        shutil.rmtree('./backup_test')
    
    # Create folders
    test_source1.mkdir(parents=True, exist_ok=True)
    test_source2.mkdir(parents=True, exist_ok=True)
    test_backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Create test files in source1
    (test_source1 / 'document1.txt').write_text('This is document 1')
    (test_source1 / 'document2.txt').write_text('This is document 2')
    (test_source1 / 'data.csv').write_text('col1,col2\n1,2\n3,4\n')
    
    # Create subfolder in source1
    (test_source1 / 'subfolder').mkdir(exist_ok=True)
    (test_source1 / 'subfolder' / 'nested_file.txt').write_text('Nested file content')
    
    # Create test files in source2
    (test_source2 / 'config.json').write_text('{"key": "value"}')
    (test_source2 / 'readme.md').write_text('# Test README')
    
    # Create files that should be excluded
    (test_source1 / 'temp.tmp').write_text('Temporary file')
    (test_source1 / 'debug.log').write_text('Debug log')
    (test_source1 / '.DS_Store').write_text('MacOS metadata')
    
    print("✓ Test environment created")
    print(f"  - Source 1: {test_source1} (7 files, 3 should be excluded)")
    print(f"  - Source 2: {test_source2} (2 files)")
    print(f"  - Backup destination: {test_backup_dir}")
    
    return test_source1, test_source2, test_backup_dir


def test_basic_backup(source1, source2, backup_dir):
    """Test 1: Basic backup creation."""
    print("\n" + "="*80)
    print("TEST 1: Basic Backup Creation")
    print("="*80)
    
    config = {
        'backup_sources': [str(source1), str(source2)],
        'backup_destination': str(backup_dir),
        'max_versions': 7,
        'compression_level': 9,
        'verify_integrity': True,
        'send_notifications': False,
        'exclude_patterns': ['*.tmp', '*.log', '.DS_Store'],
        'include_subdirs': True,
    }
    
    backup_system = BackupAutomation(config)
    success = backup_system.run_backup('test_backup')
    
    if success:
        print("✓ Test 1 PASSED: Backup created successfully")
        return True
    else:
        print("✗ Test 1 FAILED: Backup creation failed")
        return False


def test_compression_ratio(source1, source2, backup_dir):
    """Test 2: Verify compression is working."""
    print("\n" + "="*80)
    print("TEST 2: Compression Ratio")
    print("="*80)
    
    config = {
        'backup_sources': [str(source1), str(source2)],
        'backup_destination': str(backup_dir),
        'compression_level': 9,
        'verify_integrity': False,
        'send_notifications': False,
    }
    
    backup_system = BackupAutomation(config)
    success = backup_system.run_backup('compression_test')
    
    if success:
        compression_ratio = backup_system.metadata.get('compression_ratio', 0)
        print(f"Compression ratio: {compression_ratio}%")
        
        if compression_ratio > 0:
            print("✓ Test 2 PASSED: Compression working")
            return True
        else:
            print("✗ Test 2 FAILED: No compression achieved")
            return False
    else:
        print("✗ Test 2 FAILED: Backup creation failed")
        return False


def test_integrity_verification(source1, source2, backup_dir):
    """Test 3: Backup integrity verification."""
    print("\n" + "="*80)
    print("TEST 3: Integrity Verification")
    print("="*80)
    
    config = {
        'backup_sources': [str(source1)],
        'backup_destination': str(backup_dir),
        'verify_integrity': True,
        'send_notifications': False,
    }
    
    backup_system = BackupAutomation(config)
    success = backup_system.run_backup('integrity_test')
    
    if success:
        checksum = backup_system.metadata.get('checksum')
        
        if checksum:
            print(f"Checksum: {checksum}")
            print("✓ Test 3 PASSED: Integrity verification working")
            return True
        else:
            print("✗ Test 3 FAILED: No checksum generated")
            return False
    else:
        print("✗ Test 3 FAILED: Backup creation failed")
        return False


def test_version_management(source1, source2, backup_dir):
    """Test 4: Version history management (keep last 3 versions)."""
    print("\n" + "="*80)
    print("TEST 4: Version Management (Keep Last 3 Versions)")
    print("="*80)
    
    config = {
        'backup_sources': [str(source1)],
        'backup_destination': str(backup_dir),
        'max_versions': 3,
        'verify_integrity': False,
        'send_notifications': False,
    }
    
    # Create 5 backups
    for i in range(5):
        print(f"\nCreating backup {i+1}/5...")
        backup_system = BackupAutomation(config)
        backup_system.run_backup(f'version_test')
        time.sleep(1)  # Ensure different timestamps
    
    # Check how many backups exist
    backup_files = list(backup_dir.glob('*.zip'))
    print(f"\nBackups found: {len(backup_files)}")
    
    if len(backup_files) == 3:
        print("✓ Test 4 PASSED: Version management working (kept 3 versions)")
        return True
    else:
        print(f"✗ Test 4 FAILED: Expected 3 versions, found {len(backup_files)}")
        return False


def test_exclude_patterns(source1, source2, backup_dir):
    """Test 5: File exclusion patterns."""
    print("\n" + "="*80)
    print("TEST 5: File Exclusion Patterns")
    print("="*80)
    
    config = {
        'backup_sources': [str(source1)],
        'backup_destination': str(backup_dir),
        'exclude_patterns': ['*.tmp', '*.log', '.DS_Store'],
        'verify_integrity': False,
        'send_notifications': False,
    }
    
    backup_system = BackupAutomation(config)
    success = backup_system.run_backup('exclude_test')
    
    if success:
        files_skipped = backup_system.stats.get('files_skipped', 0)
        print(f"Files skipped: {files_skipped}")
        
        if files_skipped == 3:  # Should skip .tmp, .log, .DS_Store
            print("✓ Test 5 PASSED: Exclusion patterns working")
            return True
        else:
            print(f"✗ Test 5 FAILED: Expected 3 skipped files, got {files_skipped}")
            return False
    else:
        print("✗ Test 5 FAILED: Backup creation failed")
        return False


def test_list_backups(backup_dir):
    """Test 6: List available backups."""
    print("\n" + "="*80)
    print("TEST 6: List Available Backups")
    print("="*80)
    
    config = {
        'backup_sources': ['./data'],
        'backup_destination': str(backup_dir),
    }
    
    backup_system = BackupAutomation(config)
    backups = backup_system.list_backups()
    
    print(f"Found {len(backups)} backup(s)")
    
    for i, backup in enumerate(backups, 1):
        print(f"\n{i}. {backup['filename']}")
        print(f"   Size: {backup_system._format_size(backup['size'])}")
        if 'file_count' in backup:
            print(f"   Files: {backup['file_count']}")
        if 'checksum' in backup:
            print(f"   Checksum: {backup['checksum'][:16]}...")
    
    if len(backups) > 0:
        print("\n✓ Test 6 PASSED: List backups working")
        return True
    else:
        print("\n✗ Test 6 FAILED: No backups found")
        return False


def test_restore_backup(backup_dir):
    """Test 7: Restore from backup."""
    print("\n" + "="*80)
    print("TEST 7: Restore from Backup")
    print("="*80)
    
    config = {
        'backup_sources': ['./data'],
        'backup_destination': str(backup_dir),
    }
    
    backup_system = BackupAutomation(config)
    backups = backup_system.list_backups()
    
    if not backups:
        print("✗ Test 7 FAILED: No backups available to restore")
        return False
    
    # Restore the most recent backup
    backup_file = backups[0]['filename']
    restore_path = Path('./backup_test/restored')
    
    success = backup_system.restore_backup(backup_file, str(restore_path))
    
    if success and restore_path.exists():
        restored_files = list(restore_path.rglob('*'))
        print(f"Restored {len([f for f in restored_files if f.is_file()])} file(s)")
        print("✓ Test 7 PASSED: Restore working")
        return True
    else:
        print("✗ Test 7 FAILED: Restore failed")
        return False


def cleanup_test_environment():
    """Remove test files and folders."""
    print("\n" + "="*80)
    print("CLEANING UP TEST ENVIRONMENT")
    print("="*80)
    
    test_dir = Path('./backup_test')
    
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print("✓ Test environment cleaned up")
    else:
        print("No cleanup needed")


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("BACKUP AUTOMATION SYSTEM - TEST SUITE")
    print("="*80)
    
    # Setup
    source1, source2, backup_dir = setup_test_environment()
    
    # Run tests
    results = []
    
    results.append(("Basic Backup Creation", test_basic_backup(source1, source2, backup_dir)))
    results.append(("Compression Ratio", test_compression_ratio(source1, source2, backup_dir)))
    results.append(("Integrity Verification", test_integrity_verification(source1, source2, backup_dir)))
    results.append(("Version Management", test_version_management(source1, source2, backup_dir)))
    results.append(("Exclude Patterns", test_exclude_patterns(source1, source2, backup_dir)))
    results.append(("List Backups", test_list_backups(backup_dir)))
    results.append(("Restore Backup", test_restore_backup(backup_dir)))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*80)
    print(f"TESTS PASSED: {passed}/{total}")
    print("="*80)
    
    # Cleanup
    cleanup_response = input("\nDo you want to clean up test files? (yes/no): ")
    if cleanup_response.lower() == 'yes':
        cleanup_test_environment()
    else:
        print(f"\nTest files kept in: {Path('./backup_test').absolute()}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
