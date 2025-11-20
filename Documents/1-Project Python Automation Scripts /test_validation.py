#!/usr/bin/env python3
"""
Test script for Data Validation Tool.
Tests all validation features including type checking, ranges, mandatory fields,
cross-field rules, and business logic.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import shutil

# Add parent directory to path
sys.path.insert(0, '/Users/nadeemghauri/Documents/1-Project Python Automation Scripts ')

from data_validation import DataValidator


def setup_test_environment():
    """Create test data with various validation issues."""
    print("\n" + "="*80)
    print("SETTING UP TEST ENVIRONMENT")
    print("="*80)
    
    # Create test data folder
    test_folder = Path('./validation_test')
    test_folder.mkdir(exist_ok=True)
    
    # Create test CSV with validation issues
    test_data = {
        'id': [1, 2, 3, 3, 5, 6, 7, 8, 9, 10],  # Duplicate ID: 3
        'name': ['Alice', 'Bob', '', 'David', 'Eve', 'F', 'George Washington Adams III', 
                 'Hannah', 'Ian', None],  # Empty and null names, one too short, one too long
        'email': ['alice@example.com', 'bob@example.com', 'charlie.example.com',  # Invalid email
                 'david@example.com', 'eve@example.com', 'frank@example.com',
                 'george@example.com', None, 'ian@example.com', 'jack@example.com'],  # Null email
        'age': [25, 30, 150, 35, 10, 28, 45, 50, -5, 32],  # Out of range: 150, 10, -5
        'salary': [50000, 60000, 75000, 80000, 45000, 55000, 90000, 
                  -10000, 65000, 1500000],  # Negative and too high
        'status': ['active', 'inactive', 'suspended', 'active', 'pending',  # Invalid: suspended
                  'active', 'inactive', 'active', 'active', 'active'],
        'department': ['IT', 'HR', 'IT', 'Sales', 'Marketing', 
                      'Finance', 'IT', 'Sales', 'HR', 'IT'],  # Invalid: Finance
        'phone': ['123-456-7890', '234-567-8901', '345-678-9012', '456-789-0123',
                 '567-890-1234', '1234567890', '789-012-3456', '890-123-4567',  # Invalid format
                 '901-234-5678', '012-345-6789'],
        'start_date': ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01',
                      '2020-06-01', '2020-07-01', '2020-08-01', '2020-09-01', '2020-10-01'],
        'end_date': ['2021-01-01', '2021-02-01', '2019-12-01', '2021-04-01', '2021-05-01',  # Before start
                    '2021-06-01', '2021-07-01', '2021-08-01', '2021-09-01', '2021-10-01'],
        'level': ['junior', 'senior', 'junior', 'senior', 'junior',
                 'senior', 'senior', 'senior', 'junior', 'senior'],
        'is_active': [True, True, True, False, True, True, 'yes', True, True, False],  # Invalid: 'yes'
    }
    
    df = pd.DataFrame(test_data)
    test_file = test_folder / 'test_data.csv'
    df.to_csv(test_file, index=False)
    
    print(f"✓ Test data created: {test_file}")
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {len(df.columns)}")
    print(f"  Intentional issues: ~20 validation errors")
    
    return test_file, test_folder


def define_validation_rules():
    """Define comprehensive validation rules for testing."""
    
    # Cross-field validation: start_date < end_date
    def validate_dates(row):
        try:
            if 'start_date' in row and 'end_date' in row:
                start = pd.to_datetime(row['start_date'])
                end = pd.to_datetime(row['end_date'])
                if start >= end:
                    return False, f"Start date ({row['start_date']}) must be before end date ({row['end_date']})"
            return True, None
        except:
            return True, None
    
    # Business rule: seniors must have salary >= 50000
    def validate_senior_salary(row):
        try:
            if row.get('level') == 'senior':
                salary = float(row.get('salary', 0))
                if salary < 50000:
                    return False, f"Senior employees must have salary >= 50000 (got {salary})"
            return True, None
        except:
            return True, None
    
    # Business rule: age-appropriate salary
    def validate_age_salary_ratio(row):
        try:
            age = int(row.get('age', 0))
            salary = float(row.get('salary', 0))
            
            # Minimum salary should be at least $1000 per year of age
            min_expected = age * 1000
            if salary > 0 and salary < min_expected:
                return False, f"Salary {salary} seems low for age {age} (expected at least {min_expected})"
            return True, None
        except:
            return True, None
    
    rules = {
        # Data type validation
        'data_types': {
            'id': 'int',
            'name': 'string',
            'email': 'string',
            'age': 'int',
            'salary': 'float',
            'status': 'string',
            'department': 'string',
            'phone': 'string',
            'start_date': 'date',
            'end_date': 'date',
            'level': 'string',
            'is_active': 'bool',
        },
        
        # Range validation
        'range_rules': {
            'age': (18, 100),
            'salary': (0, 1000000),
        },
        
        # Mandatory fields
        'mandatory_fields': ['id', 'name', 'email', 'status'],
        
        # Unique fields
        'unique_fields': ['id', 'email'],
        
        # Regex patterns
        'regex_patterns': {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\d{3}-\d{3}-\d{4}$',
        },
        
        # Allowed values
        'allowed_values': {
            'status': ['active', 'inactive', 'pending'],
            'department': ['IT', 'HR', 'Sales', 'Marketing'],
            'level': ['junior', 'senior'],
        },
        
        # String lengths
        'string_lengths': {
            'name': (2, 30),
        },
        
        # Cross-field validation
        'cross_field_rules': [
            {
                'name': 'Start Date Before End Date',
                'function': validate_dates
            },
        ],
        
        # Business rules
        'business_rules': [
            {
                'name': 'Minimum Salary for Seniors',
                'function': validate_senior_salary
            },
            {
                'name': 'Age-Salary Ratio Check',
                'function': validate_age_salary_ratio
            },
        ],
    }
    
    return rules


def test_data_type_validation():
    """Test 1: Data type validation."""
    print("\n" + "="*80)
    print("TEST 1: Data Type Validation")
    print("="*80)
    
    test_file, _ = setup_test_environment()
    rules = define_validation_rules()
    
    validator = DataValidator(str(test_file), rules)
    validator.load_data()
    validator.validate_data_types()
    
    type_errors = len(validator.validation_results.get('data_type_errors', []))
    
    print(f"Data type errors found: {type_errors}")
    
    if type_errors > 0:
        print("✓ Test 1 PASSED: Data type validation working")
        return True
    else:
        print("✗ Test 1 FAILED: Expected data type errors")
        return False


def test_range_validation():
    """Test 2: Range validation."""
    print("\n" + "="*80)
    print("TEST 2: Range Validation")
    print("="*80)
    
    test_file, _ = setup_test_environment()
    rules = define_validation_rules()
    
    validator = DataValidator(str(test_file), rules)
    validator.load_data()
    validator.validate_ranges()
    
    range_errors = len(validator.validation_results.get('range_errors', []))
    
    print(f"Range errors found: {range_errors}")
    
    if range_errors >= 3:  # Should find age and salary range errors
        print("✓ Test 2 PASSED: Range validation working")
        return True
    else:
        print(f"✗ Test 2 FAILED: Expected at least 3 range errors, got {range_errors}")
        return False


def test_mandatory_fields():
    """Test 3: Mandatory field validation."""
    print("\n" + "="*80)
    print("TEST 3: Mandatory Field Validation")
    print("="*80)
    
    test_file, _ = setup_test_environment()
    rules = define_validation_rules()
    
    validator = DataValidator(str(test_file), rules)
    validator.load_data()
    validator.validate_mandatory_fields()
    
    mandatory_errors = len(validator.validation_results.get('mandatory_field_errors', []))
    
    print(f"Mandatory field errors found: {mandatory_errors}")
    
    if mandatory_errors >= 2:  # Empty/null name and email
        print("✓ Test 3 PASSED: Mandatory field validation working")
        return True
    else:
        print(f"✗ Test 3 FAILED: Expected at least 2 mandatory field errors")
        return False


def test_uniqueness_validation():
    """Test 4: Uniqueness validation."""
    print("\n" + "="*80)
    print("TEST 4: Uniqueness Validation")
    print("="*80)
    
    test_file, _ = setup_test_environment()
    rules = define_validation_rules()
    
    validator = DataValidator(str(test_file), rules)
    validator.load_data()
    validator.validate_unique_fields()
    
    uniqueness_errors = len(validator.validation_results.get('uniqueness_errors', []))
    
    print(f"Uniqueness errors found: {uniqueness_errors}")
    
    if uniqueness_errors == 2:  # Duplicate ID 3 (2 occurrences)
        print("✓ Test 4 PASSED: Uniqueness validation working")
        return True
    else:
        print(f"✗ Test 4 FAILED: Expected 2 uniqueness errors, got {uniqueness_errors}")
        return False


def test_pattern_validation():
    """Test 5: Pattern validation."""
    print("\n" + "="*80)
    print("TEST 5: Pattern Validation")
    print("="*80)
    
    test_file, _ = setup_test_environment()
    rules = define_validation_rules()
    
    validator = DataValidator(str(test_file), rules)
    validator.load_data()
    validator.validate_patterns()
    
    pattern_errors = len(validator.validation_results.get('pattern_errors', []))
    
    print(f"Pattern errors found: {pattern_errors}")
    
    if pattern_errors >= 2:  # Invalid email and phone formats
        print("✓ Test 5 PASSED: Pattern validation working")
        return True
    else:
        print(f"✗ Test 5 FAILED: Expected at least 2 pattern errors")
        return False


def test_cross_field_validation():
    """Test 6: Cross-field validation."""
    print("\n" + "="*80)
    print("TEST 6: Cross-Field Validation")
    print("="*80)
    
    test_file, _ = setup_test_environment()
    rules = define_validation_rules()
    
    validator = DataValidator(str(test_file), rules)
    validator.load_data()
    validator.validate_cross_field_rules()
    
    cross_field_errors = len(validator.validation_results.get('cross_field_errors', []))
    
    print(f"Cross-field errors found: {cross_field_errors}")
    
    if cross_field_errors >= 1:  # Start date after end date
        print("✓ Test 6 PASSED: Cross-field validation working")
        return True
    else:
        print(f"✗ Test 6 FAILED: Expected at least 1 cross-field error")
        return False


def test_business_rules():
    """Test 7: Business rule validation."""
    print("\n" + "="*80)
    print("TEST 7: Business Rule Validation")
    print("="*80)
    
    test_file, _ = setup_test_environment()
    rules = define_validation_rules()
    
    validator = DataValidator(str(test_file), rules)
    validator.load_data()
    validator.validate_business_rules()
    
    business_errors = len(validator.validation_results.get('business_rule_errors', []))
    
    print(f"Business rule errors found: {business_errors}")
    
    if business_errors >= 1:  # Senior with low salary
        print("✓ Test 7 PASSED: Business rule validation working")
        return True
    else:
        print(f"✗ Test 7 FAILED: Expected at least 1 business rule error")
        return False


def test_quality_score():
    """Test 8: Quality score calculation."""
    print("\n" + "="*80)
    print("TEST 8: Quality Score Calculation")
    print("="*80)
    
    test_file, _ = setup_test_environment()
    rules = define_validation_rules()
    
    validator = DataValidator(str(test_file), rules)
    validator.validate()
    
    quality_score = validator.quality_metrics['overall_score']
    
    print(f"Quality score: {quality_score}/100")
    print(f"Completeness: {validator.quality_metrics['completeness']}/100")
    print(f"Consistency: {validator.quality_metrics['consistency']}/100")
    print(f"Validity: {validator.quality_metrics['validity']}/100")
    
    if 0 <= quality_score <= 100:
        print("✓ Test 8 PASSED: Quality score calculation working")
        return True
    else:
        print(f"✗ Test 8 FAILED: Invalid quality score: {quality_score}")
        return False


def test_report_generation():
    """Test 9: Report generation."""
    print("\n" + "="*80)
    print("TEST 9: Report Generation")
    print("="*80)
    
    test_file, _ = setup_test_environment()
    rules = define_validation_rules()
    
    validator = DataValidator(str(test_file), rules)
    validator.validate()
    
    # Check if reports were created
    report_folder = Path('./validation_reports')
    txt_reports = list(report_folder.glob('validation_report_*.txt'))
    json_reports = list(report_folder.glob('validation_report_*.json'))
    
    print(f"Text reports created: {len(txt_reports)}")
    print(f"JSON reports created: {len(json_reports)}")
    
    if txt_reports and json_reports:
        print("✓ Test 9 PASSED: Report generation working")
        return True
    else:
        print("✗ Test 9 FAILED: Reports not generated")
        return False


def cleanup_test_environment():
    """Remove test files and folders."""
    print("\n" + "="*80)
    print("CLEANING UP TEST ENVIRONMENT")
    print("="*80)
    
    # Clean up test data
    test_folder = Path('./validation_test')
    if test_folder.exists():
        shutil.rmtree(test_folder)
        print("✓ Test data cleaned up")
    
    # Optionally clean up reports
    # Uncomment if you want to remove reports after testing
    # report_folder = Path('./validation_reports')
    # if report_folder.exists():
    #     shutil.rmtree(report_folder)
    #     print("✓ Reports cleaned up")


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("DATA VALIDATION TOOL - TEST SUITE")
    print("="*80)
    
    # Run tests
    results = []
    
    results.append(("Data Type Validation", test_data_type_validation()))
    results.append(("Range Validation", test_range_validation()))
    results.append(("Mandatory Fields", test_mandatory_fields()))
    results.append(("Uniqueness Validation", test_uniqueness_validation()))
    results.append(("Pattern Validation", test_pattern_validation()))
    results.append(("Cross-Field Validation", test_cross_field_validation()))
    results.append(("Business Rules", test_business_rules()))
    results.append(("Quality Score", test_quality_score()))
    results.append(("Report Generation", test_report_generation()))
    
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
        print(f"\nTest files kept in: {Path('./validation_test').absolute()}")
        print(f"Reports kept in: {Path('./validation_reports').absolute()}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
