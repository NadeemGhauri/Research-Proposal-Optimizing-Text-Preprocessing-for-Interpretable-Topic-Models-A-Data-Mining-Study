#!/usr/bin/env python3
"""
CSV Data Cleaning Script
Automated data cleaning with validation, standardization, and reporting.
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path
import pandas as pd
from dateutil import parser
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CSVDataCleaner:
    """Class to handle automated CSV data cleaning operations."""
    
    def __init__(self, input_file, output_folder=None, config=None):
        """
        Initialize the CSV Data Cleaner.
        
        Args:
            input_file (str): Path to input CSV file
            output_folder (str): Path to output folder (defaults to input file location)
            config (dict): Configuration for cleaning operations
        """
        self.input_file = Path(input_file)
        self.output_folder = Path(output_folder) if output_folder else self.input_file.parent
        self.df = None
        self.original_shape = None
        self.cleaning_report = {
            'original_rows': 0,
            'original_columns': 0,
            'duplicates_removed': 0,
            'dates_standardized': 0,
            'missing_values_filled': 0,
            'invalid_emails': 0,
            'invalid_phones': 0,
            'special_chars_removed': 0,
            'final_rows': 0,
            'final_columns': 0
        }
        
        # Default configuration
        self.config = {
            'key_columns': [],  # Columns to check for duplicates
            'date_columns': [],  # Columns containing dates
            'date_format': '%Y-%m-%d',  # Output date format
            'email_columns': [],  # Columns containing emails
            'phone_columns': [],  # Columns containing phone numbers
            'text_columns': [],  # Columns to clean special characters from
            'missing_value_strategy': 'intelligent',  # 'intelligent', 'mean', 'median', 'mode', 'drop'
        }
        
        if config:
            self.config.update(config)
        
        # Validate input file
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")
        
        # Create output folder
        self.output_folder.mkdir(parents=True, exist_ok=True)
    
    def load_data(self):
        """Load CSV data into DataFrame."""
        logger.info(f"Loading data from: {self.input_file}")
        try:
            self.df = pd.read_csv(self.input_file)
            self.original_shape = self.df.shape
            self.cleaning_report['original_rows'] = self.df.shape[0]
            self.cleaning_report['original_columns'] = self.df.shape[1]
            logger.info(f"Loaded {self.df.shape[0]} rows and {self.df.shape[1]} columns")
            return True
        except Exception as e:
            logger.error(f"Error loading CSV file: {str(e)}")
            return False
    
    def remove_duplicates(self):
        """Remove duplicate rows based on key columns."""
        if not self.config['key_columns']:
            logger.info("No key columns specified, checking all columns for duplicates")
            subset = None
        else:
            subset = self.config['key_columns']
            logger.info(f"Checking for duplicates based on columns: {subset}")
        
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep='first')
        duplicates_removed = initial_count - len(self.df)
        
        self.cleaning_report['duplicates_removed'] = duplicates_removed
        logger.info(f"Removed {duplicates_removed} duplicate rows")
    
    def standardize_dates(self):
        """Standardize date formats across specified columns."""
        if not self.config['date_columns']:
            logger.info("No date columns specified, skipping date standardization")
            return
        
        logger.info(f"Standardizing dates in columns: {self.config['date_columns']}")
        dates_standardized = 0
        
        for col in self.config['date_columns']:
            if col not in self.df.columns:
                logger.warning(f"Date column '{col}' not found in data")
                continue
            
            # Track successful conversions
            converted = 0
            
            for idx, value in self.df[col].items():
                if pd.isna(value):
                    continue
                
                try:
                    # Try to parse the date using dateutil parser
                    parsed_date = parser.parse(str(value), fuzzy=True)
                    self.df.at[idx, col] = parsed_date.strftime(self.config['date_format'])
                    converted += 1
                except Exception as e:
                    logger.warning(f"Could not parse date '{value}' in column '{col}': {str(e)}")
                    self.df.at[idx, col] = None
            
            dates_standardized += converted
            logger.info(f"  - Standardized {converted} dates in column '{col}'")
        
        self.cleaning_report['dates_standardized'] = dates_standardized
    
    def fill_missing_values(self):
        """Fill missing values with intelligent defaults."""
        logger.info("Filling missing values")
        
        missing_before = self.df.isna().sum().sum()
        
        for col in self.df.columns:
            missing_count = self.df[col].isna().sum()
            if missing_count == 0:
                continue
            
            # Determine the best strategy based on data type
            if self.config['missing_value_strategy'] == 'intelligent':
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    # For numeric columns, use median
                    fill_value = self.df[col].median()
                    self.df[col].fillna(fill_value, inplace=True)
                    logger.info(f"  - Filled {missing_count} missing values in '{col}' with median: {fill_value}")
                elif pd.api.types.is_string_dtype(self.df[col]) or self.df[col].dtype == 'object':
                    # For text columns, use mode (most frequent value)
                    if not self.df[col].mode().empty:
                        fill_value = self.df[col].mode()[0]
                        self.df[col].fillna(fill_value, inplace=True)
                        logger.info(f"  - Filled {missing_count} missing values in '{col}' with mode: '{fill_value}'")
                    else:
                        self.df[col].fillna('Unknown', inplace=True)
                        logger.info(f"  - Filled {missing_count} missing values in '{col}' with 'Unknown'")
                else:
                    # For other types, fill with 'Unknown'
                    self.df[col].fillna('Unknown', inplace=True)
                    logger.info(f"  - Filled {missing_count} missing values in '{col}' with 'Unknown'")
            
            elif self.config['missing_value_strategy'] == 'drop':
                self.df.dropna(subset=[col], inplace=True)
                logger.info(f"  - Dropped {missing_count} rows with missing values in '{col}'")
        
        missing_after = self.df.isna().sum().sum()
        self.cleaning_report['missing_values_filled'] = missing_before - missing_after
    
    def validate_email(self, email):
        """
        Validate email format.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if pd.isna(email):
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, str(email)))
    
    def validate_phone(self, phone):
        """
        Validate phone number format.
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if pd.isna(phone):
            return False
        
        # Remove common separators
        phone_clean = re.sub(r'[\s\-\(\)\.]', '', str(phone))
        
        # Check if it's a valid phone number (10-15 digits, may start with +)
        pattern = r'^\+?\d{10,15}$'
        return bool(re.match(pattern, phone_clean))
    
    def validate_emails_and_phones(self):
        """Validate and flag invalid email and phone number formats."""
        logger.info("Validating email and phone number formats")
        
        # Validate emails
        for col in self.config['email_columns']:
            if col not in self.df.columns:
                logger.warning(f"Email column '{col}' not found in data")
                continue
            
            invalid_count = 0
            for idx, value in self.df[col].items():
                if not self.validate_email(value) and not pd.isna(value):
                    invalid_count += 1
                    # Option 1: Set to None
                    self.df.at[idx, col] = None
                    # Option 2: Add validation flag column
                    # self.df.at[idx, f'{col}_valid'] = False
            
            self.cleaning_report['invalid_emails'] += invalid_count
            logger.info(f"  - Found and cleared {invalid_count} invalid emails in '{col}'")
        
        # Validate phone numbers
        for col in self.config['phone_columns']:
            if col not in self.df.columns:
                logger.warning(f"Phone column '{col}' not found in data")
                continue
            
            invalid_count = 0
            for idx, value in self.df[col].items():
                if not self.validate_phone(value) and not pd.isna(value):
                    invalid_count += 1
                    # Standardize phone format
                    self.df.at[idx, col] = None
            
            self.cleaning_report['invalid_phones'] += invalid_count
            logger.info(f"  - Found and cleared {invalid_count} invalid phone numbers in '{col}'")
    
    def remove_special_characters(self):
        """Remove special characters from text fields."""
        if not self.config['text_columns']:
            logger.info("No text columns specified, skipping special character removal")
            return
        
        logger.info(f"Removing special characters from columns: {self.config['text_columns']}")
        chars_removed = 0
        
        for col in self.config['text_columns']:
            if col not in self.df.columns:
                logger.warning(f"Text column '{col}' not found in data")
                continue
            
            for idx, value in self.df[col].items():
                if pd.isna(value):
                    continue
                
                original = str(value)
                # Remove special characters, keep only alphanumeric and spaces
                cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', original)
                # Remove extra whitespace
                cleaned = ' '.join(cleaned.split())
                
                if original != cleaned:
                    chars_removed += 1
                    self.df.at[idx, col] = cleaned
            
            logger.info(f"  - Cleaned {chars_removed} values in column '{col}'")
        
        self.cleaning_report['special_chars_removed'] = chars_removed
    
    def save_cleaned_data(self):
        """Save cleaned data to CSV file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"cleaned_{self.input_file.stem}_{timestamp}.csv"
        output_path = self.output_folder / output_filename
        
        logger.info(f"Saving cleaned data to: {output_path}")
        self.df.to_csv(output_path, index=False)
        
        self.cleaning_report['final_rows'] = self.df.shape[0]
        self.cleaning_report['final_columns'] = self.df.shape[1]
        
        return output_path
    
    def generate_report(self, report_path=None):
        """
        Generate a detailed cleaning report.
        
        Args:
            report_path (str): Path to save the report (optional)
            
        Returns:
            str: Report text
        """
        report_lines = [
            "=" * 70,
            "CSV DATA CLEANING REPORT",
            "=" * 70,
            f"Input File: {self.input_file}",
            f"Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "ORIGINAL DATA:",
            f"  - Rows: {self.cleaning_report['original_rows']:,}",
            f"  - Columns: {self.cleaning_report['original_columns']:,}",
            "",
            "CLEANING OPERATIONS:",
            f"  - Duplicate rows removed: {self.cleaning_report['duplicates_removed']:,}",
            f"  - Date values standardized: {self.cleaning_report['dates_standardized']:,}",
            f"  - Missing values filled: {self.cleaning_report['missing_values_filled']:,}",
            f"  - Invalid emails found: {self.cleaning_report['invalid_emails']:,}",
            f"  - Invalid phone numbers found: {self.cleaning_report['invalid_phones']:,}",
            f"  - Special characters removed: {self.cleaning_report['special_chars_removed']:,}",
            "",
            "FINAL DATA:",
            f"  - Rows: {self.cleaning_report['final_rows']:,}",
            f"  - Columns: {self.cleaning_report['final_columns']:,}",
            f"  - Data quality improvement: {self._calculate_improvement()}%",
            "=" * 70,
        ]
        
        report_text = "\n".join(report_lines)
        
        # Save report to file if path provided
        if report_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_path = self.output_folder / f"cleaning_report_{timestamp}.txt"
        
        with open(report_path, 'w') as f:
            f.write(report_text)
        
        logger.info(f"Report saved to: {report_path}")
        return report_text
    
    def _calculate_improvement(self):
        """Calculate data quality improvement percentage."""
        total_issues = (
            self.cleaning_report['duplicates_removed'] +
            self.cleaning_report['missing_values_filled'] +
            self.cleaning_report['invalid_emails'] +
            self.cleaning_report['invalid_phones'] +
            self.cleaning_report['special_chars_removed']
        )
        
        if self.cleaning_report['original_rows'] == 0:
            return 0.0
        
        improvement = (total_issues / (self.cleaning_report['original_rows'] * self.cleaning_report['original_columns'])) * 100
        return round(improvement, 2)
    
    def clean(self):
        """
        Execute the complete cleaning pipeline.
        
        Returns:
            tuple: (cleaned_file_path, report_text)
        """
        logger.info("=" * 70)
        logger.info("STARTING CSV DATA CLEANING PROCESS")
        logger.info("=" * 70)
        
        # Load data
        if not self.load_data():
            return None, None
        
        # Execute cleaning steps
        self.remove_duplicates()
        self.standardize_dates()
        self.fill_missing_values()
        self.validate_emails_and_phones()
        self.remove_special_characters()
        
        # Save cleaned data
        cleaned_file = self.save_cleaned_data()
        
        # Generate report
        report = self.generate_report()
        
        logger.info("=" * 70)
        logger.info("CLEANING PROCESS COMPLETE")
        logger.info("=" * 70)
        
        return cleaned_file, report


def main():
    """Main execution function."""
    
    # Example configuration - modify based on your data
    config = {
        'key_columns': ['id', 'email'],  # Columns to check for duplicates
        'date_columns': ['created_date', 'last_login'],  # Date columns
        'date_format': '%Y-%m-%d',  # Output date format
        'email_columns': ['email', 'contact_email'],  # Email columns
        'phone_columns': ['phone', 'mobile'],  # Phone columns
        'text_columns': ['name', 'address', 'company'],  # Text columns to clean
        'missing_value_strategy': 'intelligent',  # Strategy for missing values
    }
    
    # Get input file from command line or use default
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "./data/sample_data.csv"
        logger.info(f"No input file specified, using default: {input_file}")
    
    # Get output folder from command line or use default
    if len(sys.argv) > 2:
        output_folder = sys.argv[2]
    else:
        output_folder = "./cleaned_data"
    
    try:
        # Create cleaner instance
        cleaner = CSVDataCleaner(input_file, output_folder, config)
        
        # Run cleaning process
        cleaned_file, report = cleaner.clean()
        
        if cleaned_file:
            print("\n" + report)
            print(f"\n✓ Success! Cleaned file: {cleaned_file}")
        else:
            print("\n✗ Cleaning process failed.")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
