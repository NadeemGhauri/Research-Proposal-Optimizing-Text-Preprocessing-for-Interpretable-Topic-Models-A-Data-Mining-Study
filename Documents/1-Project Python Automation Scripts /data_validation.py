#!/usr/bin/env python3
"""
Data Validation Script
Comprehensive data validation tool with type checking, range validation, 
mandatory fields, cross-field rules, and quality scoring.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json
import re
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataValidator:
    """Class to handle comprehensive data validation."""
    
    def __init__(self, data_path, validation_rules=None):
        """
        Initialize the Data Validator.
        
        Args:
            data_path (str): Path to CSV file to validate
            validation_rules (dict): Dictionary of validation rules
        """
        self.data_path = Path(data_path)
        self.df = None
        self.validation_results = defaultdict(list)
        self.quality_metrics = {}
        
        # Default validation rules
        self.rules = {
            'data_types': {},           # Column: expected type
            'range_rules': {},          # Column: (min, max)
            'mandatory_fields': [],     # List of required columns
            'unique_fields': [],        # List of columns that must be unique
            'regex_patterns': {},       # Column: regex pattern
            'cross_field_rules': [],    # List of cross-field validation functions
            'business_rules': [],       # List of business logic validation functions
            'allowed_values': {},       # Column: list of allowed values
            'date_formats': {},         # Column: expected date format
            'string_lengths': {},       # Column: (min_length, max_length)
        }
        
        if validation_rules:
            self.rules.update(validation_rules)
        
        # Statistics
        self.stats = {
            'total_rows': 0,
            'total_columns': 0,
            'valid_rows': 0,
            'invalid_rows': 0,
            'errors_by_type': defaultdict(int),
            'errors_by_column': defaultdict(int),
        }
    
    def load_data(self):
        """Load CSV data file."""
        try:
            logger.info(f"Loading data from: {self.data_path}")
            self.df = pd.read_csv(self.data_path)
            
            self.stats['total_rows'] = len(self.df)
            self.stats['total_columns'] = len(self.df.columns)
            
            logger.info(f"Loaded {self.stats['total_rows']} rows and {self.stats['total_columns']} columns")
            return True
        
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def validate_data_types(self):
        """Validate data type consistency across columns."""
        logger.info("Validating data types...")
        
        for column, expected_type in self.rules.get('data_types', {}).items():
            if column not in self.df.columns:
                self.validation_results['missing_columns'].append({
                    'column': column,
                    'error': f"Column '{column}' not found in dataset"
                })
                continue
            
            # Check each value in the column
            for idx, value in enumerate(self.df[column]):
                if pd.isna(value):
                    continue  # Handle null values separately
                
                is_valid = False
                error_msg = None
                
                try:
                    if expected_type == 'int':
                        is_valid = isinstance(value, (int, np.integer)) or (
                            isinstance(value, (float, np.floating)) and value.is_integer()
                        )
                        if not is_valid:
                            error_msg = f"Expected integer, got {type(value).__name__}: {value}"
                    
                    elif expected_type == 'float':
                        is_valid = isinstance(value, (int, float, np.number))
                        if not is_valid:
                            error_msg = f"Expected numeric, got {type(value).__name__}: {value}"
                    
                    elif expected_type == 'string':
                        is_valid = isinstance(value, str)
                        if not is_valid:
                            error_msg = f"Expected string, got {type(value).__name__}: {value}"
                    
                    elif expected_type == 'bool':
                        is_valid = isinstance(value, (bool, np.bool_))
                        if not is_valid:
                            error_msg = f"Expected boolean, got {type(value).__name__}: {value}"
                    
                    elif expected_type == 'date':
                        try:
                            pd.to_datetime(value)
                            is_valid = True
                        except:
                            is_valid = False
                            error_msg = f"Expected date, got invalid date: {value}"
                    
                    if not is_valid:
                        self.validation_results['data_type_errors'].append({
                            'row': idx,
                            'column': column,
                            'value': value,
                            'expected_type': expected_type,
                            'error': error_msg
                        })
                        self.stats['errors_by_type']['data_type'] += 1
                        self.stats['errors_by_column'][column] += 1
                
                except Exception as e:
                    logger.error(f"Error validating type for {column}[{idx}]: {e}")
    
    def validate_ranges(self):
        """Validate range constraints for numerical data."""
        logger.info("Validating numerical ranges...")
        
        for column, (min_val, max_val) in self.rules.get('range_rules', {}).items():
            if column not in self.df.columns:
                continue
            
            for idx, value in enumerate(self.df[column]):
                if pd.isna(value):
                    continue
                
                try:
                    num_value = float(value)
                    
                    if min_val is not None and num_value < min_val:
                        self.validation_results['range_errors'].append({
                            'row': idx,
                            'column': column,
                            'value': value,
                            'min': min_val,
                            'max': max_val,
                            'error': f"Value {value} is below minimum {min_val}"
                        })
                        self.stats['errors_by_type']['range'] += 1
                        self.stats['errors_by_column'][column] += 1
                    
                    if max_val is not None and num_value > max_val:
                        self.validation_results['range_errors'].append({
                            'row': idx,
                            'column': column,
                            'value': value,
                            'min': min_val,
                            'max': max_val,
                            'error': f"Value {value} exceeds maximum {max_val}"
                        })
                        self.stats['errors_by_type']['range'] += 1
                        self.stats['errors_by_column'][column] += 1
                
                except (ValueError, TypeError) as e:
                    logger.debug(f"Could not convert {column}[{idx}] to number: {e}")
    
    def validate_mandatory_fields(self):
        """Validate mandatory field completeness."""
        logger.info("Validating mandatory fields...")
        
        mandatory_fields = self.rules.get('mandatory_fields', [])
        
        for column in mandatory_fields:
            if column not in self.df.columns:
                self.validation_results['missing_columns'].append({
                    'column': column,
                    'error': f"Mandatory column '{column}' not found"
                })
                continue
            
            # Check for null/empty values
            null_mask = self.df[column].isna()
            empty_mask = self.df[column].astype(str).str.strip() == ''
            
            missing_indices = self.df[null_mask | empty_mask].index
            
            for idx in missing_indices:
                self.validation_results['mandatory_field_errors'].append({
                    'row': int(idx),
                    'column': column,
                    'error': f"Mandatory field '{column}' is empty"
                })
                self.stats['errors_by_type']['mandatory'] += 1
                self.stats['errors_by_column'][column] += 1
    
    def validate_unique_fields(self):
        """Validate uniqueness constraints."""
        logger.info("Validating unique fields...")
        
        unique_fields = self.rules.get('unique_fields', [])
        
        for column in unique_fields:
            if column not in self.df.columns:
                continue
            
            # Find duplicates
            duplicates = self.df[self.df.duplicated(subset=[column], keep=False)]
            
            for idx, row in duplicates.iterrows():
                self.validation_results['uniqueness_errors'].append({
                    'row': int(idx),
                    'column': column,
                    'value': row[column],
                    'error': f"Duplicate value '{row[column]}' in unique field '{column}'"
                })
                self.stats['errors_by_type']['uniqueness'] += 1
                self.stats['errors_by_column'][column] += 1
    
    def validate_patterns(self):
        """Validate regex patterns."""
        logger.info("Validating regex patterns...")
        
        for column, pattern in self.rules.get('regex_patterns', {}).items():
            if column not in self.df.columns:
                continue
            
            regex = re.compile(pattern)
            
            for idx, value in enumerate(self.df[column]):
                if pd.isna(value):
                    continue
                
                str_value = str(value)
                
                if not regex.match(str_value):
                    self.validation_results['pattern_errors'].append({
                        'row': idx,
                        'column': column,
                        'value': value,
                        'pattern': pattern,
                        'error': f"Value '{value}' does not match pattern '{pattern}'"
                    })
                    self.stats['errors_by_type']['pattern'] += 1
                    self.stats['errors_by_column'][column] += 1
    
    def validate_allowed_values(self):
        """Validate allowed value constraints."""
        logger.info("Validating allowed values...")
        
        for column, allowed in self.rules.get('allowed_values', {}).items():
            if column not in self.df.columns:
                continue
            
            for idx, value in enumerate(self.df[column]):
                if pd.isna(value):
                    continue
                
                if value not in allowed:
                    self.validation_results['allowed_value_errors'].append({
                        'row': idx,
                        'column': column,
                        'value': value,
                        'allowed_values': allowed,
                        'error': f"Value '{value}' not in allowed values: {allowed}"
                    })
                    self.stats['errors_by_type']['allowed_value'] += 1
                    self.stats['errors_by_column'][column] += 1
    
    def validate_string_lengths(self):
        """Validate string length constraints."""
        logger.info("Validating string lengths...")
        
        for column, (min_len, max_len) in self.rules.get('string_lengths', {}).items():
            if column not in self.df.columns:
                continue
            
            for idx, value in enumerate(self.df[column]):
                if pd.isna(value):
                    continue
                
                str_len = len(str(value))
                
                if min_len is not None and str_len < min_len:
                    self.validation_results['string_length_errors'].append({
                        'row': idx,
                        'column': column,
                        'value': value,
                        'length': str_len,
                        'min_length': min_len,
                        'max_length': max_len,
                        'error': f"String length {str_len} is below minimum {min_len}"
                    })
                    self.stats['errors_by_type']['string_length'] += 1
                    self.stats['errors_by_column'][column] += 1
                
                if max_len is not None and str_len > max_len:
                    self.validation_results['string_length_errors'].append({
                        'row': idx,
                        'column': column,
                        'value': value,
                        'length': str_len,
                        'min_length': min_len,
                        'max_length': max_len,
                        'error': f"String length {str_len} exceeds maximum {max_len}"
                    })
                    self.stats['errors_by_type']['string_length'] += 1
                    self.stats['errors_by_column'][column] += 1
    
    def validate_cross_field_rules(self):
        """Validate cross-field validation rules."""
        logger.info("Validating cross-field rules...")
        
        cross_field_rules = self.rules.get('cross_field_rules', [])
        
        for rule in cross_field_rules:
            rule_name = rule.get('name', 'Unnamed Rule')
            rule_func = rule.get('function')
            
            if not callable(rule_func):
                logger.warning(f"Cross-field rule '{rule_name}' has no valid function")
                continue
            
            for idx, row in self.df.iterrows():
                try:
                    is_valid, error_msg = rule_func(row)
                    
                    if not is_valid:
                        self.validation_results['cross_field_errors'].append({
                            'row': int(idx),
                            'rule': rule_name,
                            'error': error_msg
                        })
                        self.stats['errors_by_type']['cross_field'] += 1
                
                except Exception as e:
                    logger.error(f"Error applying cross-field rule '{rule_name}' at row {idx}: {e}")
    
    def validate_business_rules(self):
        """Validate business logic compliance."""
        logger.info("Validating business rules...")
        
        business_rules = self.rules.get('business_rules', [])
        
        for rule in business_rules:
            rule_name = rule.get('name', 'Unnamed Business Rule')
            rule_func = rule.get('function')
            
            if not callable(rule_func):
                logger.warning(f"Business rule '{rule_name}' has no valid function")
                continue
            
            for idx, row in self.df.iterrows():
                try:
                    is_valid, error_msg = rule_func(row)
                    
                    if not is_valid:
                        self.validation_results['business_rule_errors'].append({
                            'row': int(idx),
                            'rule': rule_name,
                            'error': error_msg
                        })
                        self.stats['errors_by_type']['business_rule'] += 1
                
                except Exception as e:
                    logger.error(f"Error applying business rule '{rule_name}' at row {idx}: {e}")
    
    def calculate_quality_score(self):
        """Calculate data quality score."""
        logger.info("Calculating data quality score...")
        
        total_cells = self.stats['total_rows'] * self.stats['total_columns']
        total_errors = sum(self.stats['errors_by_type'].values())
        
        if total_cells == 0:
            quality_score = 0
        else:
            # Calculate error rate
            error_rate = (total_errors / total_cells) * 100
            
            # Quality score (0-100, where 100 is perfect)
            quality_score = max(0, 100 - error_rate)
        
        # Calculate metrics
        self.quality_metrics = {
            'overall_score': round(quality_score, 2),
            'total_cells': total_cells,
            'total_errors': total_errors,
            'error_rate': round((total_errors / total_cells * 100) if total_cells > 0 else 0, 2),
            'valid_rows': self.stats['total_rows'] - len(set(
                error['row'] for error_type in self.validation_results.values()
                if isinstance(error_type, list)
                for error in error_type
                if 'row' in error
            )),
            'completeness': self._calculate_completeness(),
            'consistency': self._calculate_consistency(),
            'validity': self._calculate_validity(),
        }
        
        self.stats['valid_rows'] = self.quality_metrics['valid_rows']
        self.stats['invalid_rows'] = self.stats['total_rows'] - self.stats['valid_rows']
    
    def _calculate_completeness(self):
        """Calculate completeness score (mandatory fields filled)."""
        if not self.rules.get('mandatory_fields'):
            return 100.0
        
        mandatory_errors = len(self.validation_results.get('mandatory_field_errors', []))
        total_mandatory_cells = self.stats['total_rows'] * len(self.rules['mandatory_fields'])
        
        if total_mandatory_cells == 0:
            return 100.0
        
        completeness = ((total_mandatory_cells - mandatory_errors) / total_mandatory_cells) * 100
        return round(completeness, 2)
    
    def _calculate_consistency(self):
        """Calculate consistency score (data types, patterns)."""
        type_errors = self.stats['errors_by_type'].get('data_type', 0)
        pattern_errors = self.stats['errors_by_type'].get('pattern', 0)
        
        total_consistency_checks = self.stats['total_rows'] * (
            len(self.rules.get('data_types', {})) + 
            len(self.rules.get('regex_patterns', {}))
        )
        
        if total_consistency_checks == 0:
            return 100.0
        
        consistency = ((total_consistency_checks - type_errors - pattern_errors) / 
                      total_consistency_checks) * 100
        return round(consistency, 2)
    
    def _calculate_validity(self):
        """Calculate validity score (range, allowed values, business rules)."""
        range_errors = self.stats['errors_by_type'].get('range', 0)
        allowed_errors = self.stats['errors_by_type'].get('allowed_value', 0)
        business_errors = self.stats['errors_by_type'].get('business_rule', 0)
        
        total_validity_checks = self.stats['total_rows'] * (
            len(self.rules.get('range_rules', {})) +
            len(self.rules.get('allowed_values', {})) +
            len(self.rules.get('business_rules', []))
        )
        
        if total_validity_checks == 0:
            return 100.0
        
        total_validity_errors = range_errors + allowed_errors + business_errors
        validity = ((total_validity_checks - total_validity_errors) / 
                   total_validity_checks) * 100
        return round(validity, 2)
    
    def generate_report(self, output_folder='./validation_reports'):
        """Generate comprehensive validation report."""
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = output_folder / f"validation_report_{timestamp}.txt"
        json_file = output_folder / f"validation_report_{timestamp}.json"
        
        # Generate text report
        lines = [
            "=" * 80,
            "DATA VALIDATION REPORT",
            "=" * 80,
            f"Data Source: {self.data_path}",
            f"Validation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "DATASET SUMMARY:",
            f"  Total Rows: {self.stats['total_rows']:,}",
            f"  Total Columns: {self.stats['total_columns']}",
            f"  Valid Rows: {self.stats['valid_rows']:,}",
            f"  Invalid Rows: {self.stats['invalid_rows']:,}",
            "",
            "DATA QUALITY SCORE:",
            f"  Overall Score: {self.quality_metrics['overall_score']}/100",
            f"  Completeness: {self.quality_metrics['completeness']}/100",
            f"  Consistency: {self.quality_metrics['consistency']}/100",
            f"  Validity: {self.quality_metrics['validity']}/100",
            "",
            "ERROR SUMMARY:",
            f"  Total Errors: {self.quality_metrics['total_errors']:,}",
            f"  Error Rate: {self.quality_metrics['error_rate']}%",
            "",
        ]
        
        # Errors by type
        if self.stats['errors_by_type']:
            lines.append("ERRORS BY TYPE:")
            for error_type, count in sorted(self.stats['errors_by_type'].items(), 
                                          key=lambda x: x[1], reverse=True):
                lines.append(f"  {error_type.replace('_', ' ').title()}: {count:,}")
            lines.append("")
        
        # Errors by column
        if self.stats['errors_by_column']:
            lines.append("ERRORS BY COLUMN:")
            for column, count in sorted(self.stats['errors_by_column'].items(), 
                                       key=lambda x: x[1], reverse=True)[:10]:
                lines.append(f"  {column}: {count:,}")
            if len(self.stats['errors_by_column']) > 10:
                lines.append(f"  ... and {len(self.stats['errors_by_column']) - 10} more")
            lines.append("")
        
        # Detailed errors (first 20 of each type)
        for error_type, errors in self.validation_results.items():
            if not errors:
                continue
            
            lines.append("=" * 80)
            lines.append(f"{error_type.replace('_', ' ').upper()} ({len(errors)} total):")
            lines.append("=" * 80)
            
            for error in errors[:20]:
                lines.append(f"  Row {error.get('row', 'N/A')}: {error.get('error', str(error))}")
                if 'column' in error:
                    lines.append(f"    Column: {error['column']}")
                if 'value' in error:
                    lines.append(f"    Value: {error['value']}")
            
            if len(errors) > 20:
                lines.append(f"  ... and {len(errors) - 20} more errors")
            lines.append("")
        
        lines.append("=" * 80)
        
        # Save text report
        report_content = "\n".join(lines)
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        logger.info(f"Validation report saved: {report_file}")
        
        # Save JSON report
        json_data = {
            'metadata': {
                'data_source': str(self.data_path),
                'validation_date': datetime.now().isoformat(),
                'total_rows': self.stats['total_rows'],
                'total_columns': self.stats['total_columns'],
            },
            'quality_metrics': self.quality_metrics,
            'statistics': dict(self.stats),
            'validation_results': {
                k: v for k, v in self.validation_results.items()
            }
        }
        
        with open(json_file, 'w') as f:
            json.dump(json_data, f, indent=2, default=str)
        
        logger.info(f"JSON report saved: {json_file}")
        
        return report_file, json_file
    
    def validate(self):
        """Execute all validation checks."""
        logger.info("=" * 80)
        logger.info("STARTING DATA VALIDATION")
        logger.info("=" * 80)
        
        # Load data
        if not self.load_data():
            return False
        
        # Run all validations
        self.validate_data_types()
        self.validate_ranges()
        self.validate_mandatory_fields()
        self.validate_unique_fields()
        self.validate_patterns()
        self.validate_allowed_values()
        self.validate_string_lengths()
        self.validate_cross_field_rules()
        self.validate_business_rules()
        
        # Calculate quality score
        self.calculate_quality_score()
        
        # Generate reports
        report_file, json_file = self.generate_report()
        
        # Print summary
        logger.info("=" * 80)
        logger.info("VALIDATION COMPLETE")
        logger.info(f"Quality Score: {self.quality_metrics['overall_score']}/100")
        logger.info(f"Total Errors: {self.quality_metrics['total_errors']:,}")
        logger.info(f"Report: {report_file}")
        logger.info("=" * 80)
        
        return True


def main():
    """Main execution function with example validation rules."""
    
    # Example validation rules
    validation_rules = {
        # Data type validation
        'data_types': {
            'id': 'int',
            'name': 'string',
            'email': 'string',
            'age': 'int',
            'salary': 'float',
            'is_active': 'bool',
            'created_date': 'date',
        },
        
        # Range validation
        'range_rules': {
            'age': (18, 100),
            'salary': (0, 1000000),
        },
        
        # Mandatory fields
        'mandatory_fields': ['id', 'name', 'email'],
        
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
        },
        
        # String lengths
        'string_lengths': {
            'name': (2, 100),
            'description': (10, 500),
        },
        
        # Cross-field validation
        'cross_field_rules': [
            {
                'name': 'Start Date Before End Date',
                'function': lambda row: (
                    (pd.to_datetime(row.get('start_date', '')) < pd.to_datetime(row.get('end_date', '')), 
                     "Start date must be before end date")
                    if 'start_date' in row and 'end_date' in row
                    else (True, None)
                )
            },
        ],
        
        # Business rules
        'business_rules': [
            {
                'name': 'Minimum Salary for Seniors',
                'function': lambda row: (
                    (row.get('salary', 0) >= 50000, 
                     f"Senior employees must have salary >= 50000 (got {row.get('salary')})")
                    if row.get('level') == 'senior'
                    else (True, None)
                )
            },
        ],
    }
    
    # Get input file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "./data/sample_data.csv"
        logger.info(f"No input file specified, using default: {input_file}")
    
    try:
        # Create validator
        validator = DataValidator(input_file, validation_rules)
        
        # Run validation
        success = validator.validate()
        
        if success:
            print(f"\n✓ Validation completed successfully!")
            print(f"  Quality Score: {validator.quality_metrics['overall_score']}/100")
            print(f"  Total Errors: {validator.quality_metrics['total_errors']:,}")
            print(f"  Error Rate: {validator.quality_metrics['error_rate']}%")
        else:
            print("\n✗ Validation failed!")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
