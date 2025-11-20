#!/usr/bin/env python3
"""
Test script for Bulk File Renamer.
Tests all renaming features.
"""

import sys
sys.path.insert(0, '/Users/nadeemghauri/Documents/Fiverr Project 1')

from bulk_rename import BulkFileRenamer

def test_special_character_removal():
    """Test 1: Remove special characters"""
    print("\n" + "="*80)
    print("TEST 1: Remove Special Characters")
    print("="*80)
    
    config = {'preview_mode': True, 'create_undo_file': False}
    renamer = BulkFileRenamer('rename_test', config)
    renamer.rename('remove_special', keep_chars='_-', replace_with='_')

def test_sequential_numbering():
    """Test 2: Sequential numbering"""
    print("\n" + "="*80)
    print("TEST 2: Sequential Numbering")
    print("="*80)
    
    config = {'preview_mode': True, 'create_undo_file': False}
    renamer = BulkFileRenamer('rename_test', config)
    renamer.rename('sequential', pattern='file_{counter}', start=1, padding=3)

def test_case_change():
    """Test 3: Change case to lowercase"""
    print("\n" + "="*80)
    print("TEST 3: Change Case to Lowercase")
    print("="*80)
    
    config = {'preview_mode': True, 'create_undo_file': False}
    renamer = BulkFileRenamer('rename_test', config)
    renamer.rename('case_change', case_type='lower')

def test_find_replace():
    """Test 4: Find and replace"""
    print("\n" + "="*80)
    print("TEST 4: Find and Replace")
    print("="*80)
    
    config = {'preview_mode': True, 'create_undo_file': False}
    renamer = BulkFileRenamer('rename_test', config)
    renamer.rename('find_replace', find='2024', replace='2025', case_sensitive=True)

def test_prefix_suffix():
    """Test 5: Add prefix and suffix"""
    print("\n" + "="*80)
    print("TEST 5: Add Prefix and Suffix")
    print("="*80)
    
    config = {'preview_mode': True, 'create_undo_file': False}
    renamer = BulkFileRenamer('rename_test', config)
    renamer.rename('prefix_suffix', prefix='NEW_', suffix='_v2')

def test_prefix_based_on_date():
    """Test 6: Add prefix based on file date"""
    print("\n" + "="*80)
    print("TEST 6: Add Prefix Based on File Date")
    print("="*80)
    
    config = {'preview_mode': True, 'create_undo_file': False}
    renamer = BulkFileRenamer('rename_test', config)
    renamer.rename('prefix_suffix', prefix='', based_on='date')

def test_actual_rename():
    """Test 7: Actually rename files (with undo)"""
    print("\n" + "="*80)
    print("TEST 7: Actual Rename (Lowercase + Remove Special Chars)")
    print("="*80)
    
    config = {'preview_mode': False, 'create_undo_file': True}
    renamer = BulkFileRenamer('rename_test', config)
    
    # First, remove special characters
    files = renamer.get_files()
    operations = renamer.plan_rename(files, 'remove_special', keep_chars='_-.', replace_with='_')
    valid_ops, conflicts = renamer.validate_operations(operations)
    
    if valid_ops:
        renamer.execute_rename(valid_ops)
        print(f"\n✓ Renamed {renamer.stats['renamed_files']} files")
    
    # Then, change to lowercase
    config2 = {'preview_mode': False, 'create_undo_file': True}
    renamer2 = BulkFileRenamer('rename_test', config2)
    renamer2.rename('case_change', case_type='lower')

def test_undo():
    """Test 8: Undo last rename"""
    print("\n" + "="*80)
    print("TEST 8: Undo Last Rename")
    print("="*80)
    
    renamer = BulkFileRenamer('rename_test', {})
    success = renamer.undo_last_rename()
    
    if success:
        print("✓ Undo successful!")
    else:
        print("✗ Undo failed")

if __name__ == "__main__":
    # Run all tests
    test_special_character_removal()
    test_sequential_numbering()
    test_case_change()
    test_find_replace()
    test_prefix_suffix()
    test_prefix_based_on_date()
    
    # Ask before actual rename
    print("\n" + "="*80)
    print("The above were preview tests. Do you want to test actual renaming?")
    print("This will rename files but create an undo file.")
    print("="*80)
    response = input("Continue with actual rename test? (yes/no): ")
    
    if response.lower() == 'yes':
        test_actual_rename()
        
        # Ask for undo
        print("\n" + "="*80)
        response2 = input("Do you want to undo the rename? (yes/no): ")
        if response2.lower() == 'yes':
            test_undo()
            # Undo again to restore original
            test_undo()
    
    print("\n✓ All tests completed!")
