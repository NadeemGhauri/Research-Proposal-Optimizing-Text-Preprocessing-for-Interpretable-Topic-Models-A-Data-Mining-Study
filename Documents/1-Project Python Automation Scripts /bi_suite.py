"""
Business Intelligence Suite - Unified Report Generation Platform
Combines Dashboard Generator, PDF Reports, and Excel Automation

This suite provides a unified interface for generating comprehensive business intelligence
reports with interactive dashboards, PDF documents, and Excel workbooks from a single
configuration file.

Author: Dr. Mahad Nadeem (dr_mahad_nadeem)
Version: 1.0.0
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
from pathlib import Path

# Import individual tools
from dashboard_generator import DashboardGenerator, DashboardConfig
from pdf_report_generator import PDFReportGenerator, ReportConfig
from generate_excel_report import ExcelReportGenerator


class BISuiteConfig:
    """Unified configuration for Business Intelligence Suite"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.validate_config()
    
    def validate_config(self):
        """Validate configuration structure"""
        required_fields = ['project_name', 'data_sources', 'outputs']
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required field: {field}")
        
        if not self.config['outputs']:
            raise ValueError("At least one output type must be specified")
    
    @property
    def project_name(self) -> str:
        return self.config['project_name']
    
    @property
    def data_sources(self) -> List[Dict[str, Any]]:
        return self.config['data_sources']
    
    @property
    def outputs(self) -> Dict[str, Any]:
        return self.config['outputs']
    
    @property
    def branding(self) -> Dict[str, Any]:
        return self.config.get('branding', {})
    
    @property
    def output_folder(self) -> str:
        return self.config.get('output_folder', './bi_suite_output')
    
    @property
    def dashboard_enabled(self) -> bool:
        return 'dashboard' in self.outputs and self.outputs['dashboard'].get('enabled', False)
    
    @property
    def pdf_enabled(self) -> bool:
        return 'pdf' in self.outputs and self.outputs['pdf'].get('enabled', False)
    
    @property
    def excel_enabled(self) -> bool:
        return 'excel' in self.outputs and self.outputs['excel'].get('enabled', False)


class BusinessIntelligenceSuite:
    """
    Unified Business Intelligence Suite
    Generates dashboards, PDF reports, and Excel workbooks from a single configuration
    """
    
    def __init__(self, config: BISuiteConfig):
        self.config = config
        self.data_cache: Dict[str, pd.DataFrame] = {}
        self.output_files: Dict[str, str] = {}
        self.execution_log: List[Dict[str, Any]] = []
        
        # Create output directory
        os.makedirs(self.config.output_folder, exist_ok=True)
    
    def load_data_sources(self) -> Dict[str, pd.DataFrame]:
        """Load all data sources into memory"""
        print("\n📊 Loading Data Sources...")
        
        for source in self.config.data_sources:
            name = source['name']
            path = source['path']
            file_type = source.get('type', 'auto')
            
            try:
                # Auto-detect file type from extension
                if file_type == 'auto':
                    ext = Path(path).suffix.lower()
                    if ext == '.csv':
                        file_type = 'csv'
                    elif ext in ['.xlsx', '.xls']:
                        file_type = 'excel'
                    elif ext == '.json':
                        file_type = 'json'
                    else:
                        raise ValueError(f"Unknown file type: {ext}")
                
                # Load data based on type
                if file_type == 'csv':
                    df = pd.read_csv(path)
                elif file_type == 'excel':
                    df = pd.read_excel(path)
                elif file_type == 'json':
                    df = pd.read_json(path)
                else:
                    raise ValueError(f"Unsupported file type: {file_type}")
                
                self.data_cache[name] = df
                print(f"  ✓ Loaded: {name} ({len(df):,} rows, {len(df.columns)} columns)")
                
                self._log_action('data_load', name, 'success', 
                               f"Loaded {len(df):,} rows from {path}")
            
            except Exception as e:
                print(f"  ✗ Error loading {name}: {e}")
                self._log_action('data_load', name, 'error', str(e))
                raise
        
        return self.data_cache
    
    def generate_dashboard(self) -> Optional[str]:
        """Generate interactive HTML dashboard"""
        if not self.config.dashboard_enabled:
            return None
        
        print("\n🎨 Generating Interactive Dashboard...")
        
        try:
            dashboard_config = self.config.outputs['dashboard']
            
            # Build dashboard configuration
            dash_conf = DashboardConfig(
                title=dashboard_config.get('title', f"{self.config.project_name} - Dashboard"),
                data_source=None,  # We'll use cached data
                charts=dashboard_config.get('charts', []),
                filters=dashboard_config.get('filters', []),
                theme=dashboard_config.get('theme', 'plotly_white'),
                color_palette=self.config.branding.get('color_palette'),
                show_data_table=dashboard_config.get('show_data_table', True),
                enable_export=dashboard_config.get('enable_export', True),
                auto_refresh=dashboard_config.get('auto_refresh', False),
                refresh_interval=dashboard_config.get('refresh_interval', 300)
            )
            
            # Create dashboard generator
            generator = DashboardGenerator(dash_conf)
            
            # Override data with cached data
            primary_source = dashboard_config.get('primary_data_source')
            if primary_source and primary_source in self.data_cache:
                generator.data = self.data_cache[primary_source]
            
            # Generate dashboard
            output_path = os.path.join(
                self.config.output_folder,
                dashboard_config.get('filename', f"{self.config.project_name}_dashboard.html")
            )
            
            dashboard_path = generator.save_dashboard(output_path)
            self.output_files['dashboard'] = dashboard_path
            
            print(f"  ✓ Dashboard saved: {dashboard_path}")
            self._log_action('dashboard_generation', 'dashboard', 'success', 
                           f"Generated: {dashboard_path}")
            
            return dashboard_path
        
        except Exception as e:
            print(f"  ✗ Dashboard generation failed: {e}")
            self._log_action('dashboard_generation', 'dashboard', 'error', str(e))
            raise
    
    def generate_pdf_report(self) -> Optional[str]:
        """Generate PDF report"""
        if not self.config.pdf_enabled:
            return None
        
        print("\n📄 Generating PDF Report...")
        
        try:
            pdf_config = self.config.outputs['pdf']
            
            # Build PDF configuration
            report_conf = ReportConfig(
                title=pdf_config.get('title', f"{self.config.project_name} - Report"),
                subtitle=pdf_config.get('subtitle', ''),
                author=pdf_config.get('author', 'Business Intelligence Suite'),
                data_sources=[],  # We'll use cached data
                sections=pdf_config.get('sections', []),
                branding=self.config.branding,
                include_cover_page=pdf_config.get('include_cover_page', True),
                include_toc=pdf_config.get('include_toc', True),
                include_header=pdf_config.get('include_header', True),
                include_footer=pdf_config.get('include_footer', True),
                include_page_numbers=pdf_config.get('include_page_numbers', True)
            )
            
            # Create PDF generator
            generator = PDFReportGenerator(report_conf)
            
            # Override data with cached data
            generator.data_sources = self.data_cache
            
            # Generate report
            output_path = os.path.join(
                self.config.output_folder,
                pdf_config.get('filename', f"{self.config.project_name}_report.pdf")
            )
            
            pdf_path = generator.generate_report(output_path)
            self.output_files['pdf'] = pdf_path
            
            print(f"  ✓ PDF report saved: {pdf_path}")
            self._log_action('pdf_generation', 'pdf_report', 'success', 
                           f"Generated: {pdf_path}")
            
            return pdf_path
        
        except Exception as e:
            print(f"  ✗ PDF generation failed: {e}")
            self._log_action('pdf_generation', 'pdf_report', 'error', str(e))
            raise
    
    def generate_excel_report(self) -> Optional[str]:
        """Generate Excel workbook with multiple sheets"""
        if not self.config.excel_enabled:
            return None
        
        print("\n📊 Generating Excel Report...")
        
        try:
            excel_config = self.config.outputs['excel']
            
            output_path = os.path.join(
                self.config.output_folder,
                excel_config.get('filename', f"{self.config.project_name}_report.xlsx")
            )
            
            # Create Excel generator
            generator = ExcelReportGenerator()
            
            # Set data sources from cache
            generator.data_sources = self.data_cache
            
            # Configure sheets
            sheets_config = excel_config.get('sheets', [])
            
            for sheet_conf in sheets_config:
                sheet_name = sheet_conf['name']
                data_source = sheet_conf.get('data_source')
                
                if data_source and data_source in self.data_cache:
                    df = self.data_cache[data_source]
                    
                    # Apply filters if specified
                    filters = sheet_conf.get('filters', {})
                    if filters:
                        for col, value in filters.items():
                            if col in df.columns:
                                df = df[df[col] == value]
                    
                    # Apply column selection
                    columns = sheet_conf.get('columns')
                    if columns:
                        df = df[columns]
                    
                    # Add to workbook
                    generator.add_sheet(sheet_name, df)
                    
                    # Add pivot table if specified
                    pivot_config = sheet_conf.get('pivot_table')
                    if pivot_config:
                        generator.add_pivot_table(
                            sheet_name=f"{sheet_name}_Pivot",
                            source_sheet=sheet_name,
                            rows=pivot_config.get('rows', []),
                            cols=pivot_config.get('cols', []),
                            values=pivot_config.get('values', []),
                            aggfunc=pivot_config.get('aggfunc', 'sum')
                        )
                    
                    # Add chart if specified
                    chart_config = sheet_conf.get('chart')
                    if chart_config:
                        generator.add_chart(
                            sheet_name=sheet_name,
                            chart_type=chart_config.get('type', 'bar'),
                            title=chart_config.get('title', ''),
                            data_range=chart_config.get('data_range', 'A1:B10'),
                            position=chart_config.get('position', 'D2')
                        )
            
            # Add summary sheet if specified
            if excel_config.get('include_summary', False):
                generator.add_summary_sheet(
                    kpis=excel_config.get('kpis', [])
                )
            
            # Apply formatting
            if excel_config.get('apply_formatting', True):
                generator.apply_formatting()
            
            # Save workbook
            generator.save(output_path)
            self.output_files['excel'] = output_path
            
            print(f"  ✓ Excel report saved: {output_path}")
            self._log_action('excel_generation', 'excel_report', 'success', 
                           f"Generated: {output_path}")
            
            return output_path
        
        except Exception as e:
            print(f"  ✗ Excel generation failed: {e}")
            self._log_action('excel_generation', 'excel_report', 'error', str(e))
            raise
    
    def generate_all(self) -> Dict[str, str]:
        """Generate all enabled outputs"""
        print(f"\n{'='*80}")
        print(f"  BUSINESS INTELLIGENCE SUITE - {self.config.project_name}")
        print(f"{'='*80}")
        
        start_time = datetime.now()
        
        # Load data
        self.load_data_sources()
        
        # Generate outputs
        if self.config.dashboard_enabled:
            self.generate_dashboard()
        
        if self.config.pdf_enabled:
            self.generate_pdf_report()
        
        if self.config.excel_enabled:
            self.generate_excel_report()
        
        # Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n{'='*80}")
        print(f"  ✅ GENERATION COMPLETE")
        print(f"{'='*80}")
        print(f"\n📁 Output Folder: {self.config.output_folder}")
        print(f"⏱️  Total Time: {duration:.2f} seconds")
        print(f"\n📊 Generated Files:")
        
        for output_type, filepath in self.output_files.items():
            file_size = os.path.getsize(filepath) / 1024  # KB
            print(f"  • {output_type.upper()}: {filepath} ({file_size:.1f} KB)")
        
        # Save execution log
        self._save_execution_log()
        
        return self.output_files
    
    def _log_action(self, action_type: str, target: str, status: str, message: str):
        """Log execution action"""
        self.execution_log.append({
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'target': target,
            'status': status,
            'message': message
        })
    
    def _save_execution_log(self):
        """Save execution log to JSON file"""
        log_path = os.path.join(
            self.config.output_folder,
            f"{self.config.project_name}_execution_log.json"
        )
        
        with open(log_path, 'w') as f:
            json.dump({
                'project_name': self.config.project_name,
                'execution_time': datetime.now().isoformat(),
                'output_files': self.output_files,
                'log': self.execution_log
            }, f, indent=2)
        
        print(f"\n📝 Execution log saved: {log_path}")


class ExcelReportGenerator:
    """Simplified Excel Report Generator for BI Suite integration"""
    
    def __init__(self):
        self.data_sources: Dict[str, pd.DataFrame] = {}
        self.sheets: Dict[str, pd.DataFrame] = {}
        self.workbook = None
    
    def add_sheet(self, name: str, data: pd.DataFrame):
        """Add a sheet to the workbook"""
        self.sheets[name] = data
    
    def add_pivot_table(self, sheet_name: str, source_sheet: str, 
                       rows: List[str], cols: List[str], 
                       values: List[str], aggfunc: str = 'sum'):
        """Add a pivot table sheet"""
        if source_sheet in self.sheets:
            df = self.sheets[source_sheet]
            pivot = pd.pivot_table(
                df, 
                index=rows, 
                columns=cols if cols else None,
                values=values, 
                aggfunc=aggfunc
            )
            self.sheets[sheet_name] = pivot
    
    def add_chart(self, sheet_name: str, chart_type: str, title: str,
                  data_range: str, position: str):
        """Add chart to sheet (placeholder - requires openpyxl)"""
        pass  # Implemented in full version
    
    def add_summary_sheet(self, kpis: List[Dict[str, Any]]):
        """Add summary sheet with KPIs"""
        summary_data = []
        for kpi in kpis:
            summary_data.append({
                'Metric': kpi['name'],
                'Value': kpi.get('value', 'N/A'),
                'Target': kpi.get('target', 'N/A'),
                'Status': kpi.get('status', 'N/A')
            })
        self.sheets['Summary'] = pd.DataFrame(summary_data)
    
    def apply_formatting(self):
        """Apply Excel formatting (placeholder)"""
        pass  # Implemented in full version
    
    def save(self, filepath: str):
        """Save workbook to file"""
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for sheet_name, df in self.sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=True)


def load_config(config_path: str) -> BISuiteConfig:
    """Load configuration from JSON file"""
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    return BISuiteConfig(config_data)


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Business Intelligence Suite - Unified Report Generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all outputs from config
  python bi_suite.py --config config/bi_suite_config.json
  
  # Generate only specific outputs
  python bi_suite.py --config config/bi_suite_config.json --outputs dashboard pdf
  
  # Specify custom output folder
  python bi_suite.py --config config/bi_suite_config.json --output ./reports
        """
    )
    
    parser.add_argument('--config', required=True, help='Path to BI Suite configuration JSON file')
    parser.add_argument('--outputs', nargs='+', choices=['dashboard', 'pdf', 'excel'],
                       help='Specific outputs to generate (default: all enabled in config)')
    parser.add_argument('--output', help='Output folder path (overrides config)')
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Override output folder if specified
        if args.output:
            config.config['output_folder'] = args.output
        
        # Override enabled outputs if specified
        if args.outputs:
            for output_type in ['dashboard', 'pdf', 'excel']:
                if output_type in config.outputs:
                    config.outputs[output_type]['enabled'] = output_type in args.outputs
        
        # Create BI Suite instance
        bi_suite = BusinessIntelligenceSuite(config)
        
        # Generate all outputs
        output_files = bi_suite.generate_all()
        
        print(f"\n{'='*80}")
        print("✅ SUCCESS - All reports generated successfully!")
        print(f"{'='*80}\n")
        
        return 0
    
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"❌ ERROR: {e}")
        print(f"{'='*80}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
