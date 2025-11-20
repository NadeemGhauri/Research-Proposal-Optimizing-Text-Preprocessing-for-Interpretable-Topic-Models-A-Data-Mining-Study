#!/usr/bin/env python3
"""
PDF Report Generator - Professional PDF Report Creation

This script generates professional PDF reports with:
- Multiple data sources (CSV, Excel, JSON, API)
- Professional templates with branding
- Charts and tables with styling
- Headers, footers, and page numbers
- Automatic table of contents
- Batch processing capability
- Customizable branding and styling

Author: PDF Report Generator Team
Date: 2024-11-21
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
import io

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, legal
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, Image, KeepTogether, Frame, PageTemplate,
    NextPageTemplate, Indenter, ListFlowable, ListItem
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


@dataclass
class BrandingConfig:
    """Branding configuration for consistent styling"""
    
    # Colors (hex or RGB tuple)
    primary_color: Union[str, Tuple] = "#1f77b4"
    secondary_color: Union[str, Tuple] = "#ff7f0e"
    accent_color: Union[str, Tuple] = "#2ca02c"
    text_color: Union[str, Tuple] = "#333333"
    
    # Logo
    logo_path: Optional[str] = None
    logo_width: float = 2 * inch
    logo_height: float = 0.5 * inch
    
    # Fonts
    title_font: str = "Helvetica-Bold"
    heading_font: str = "Helvetica-Bold"
    body_font: str = "Helvetica"
    
    # Font sizes
    title_size: int = 24
    heading1_size: int = 18
    heading2_size: int = 14
    heading3_size: int = 12
    body_size: int = 10
    
    # Company info
    company_name: str = "Company Name"
    report_footer: str = "Confidential - Internal Use Only"


@dataclass
class ChartConfig:
    """Configuration for a chart in the report"""
    
    chart_type: str  # bar, line, pie, scatter, heatmap, box
    title: str
    data_column_x: Optional[str] = None
    data_column_y: Optional[str] = None
    data_columns: Optional[List[str]] = None  # For multi-series
    aggregation: str = "sum"  # sum, count, avg, min, max, none
    width: float = 6 * inch
    height: float = 4 * inch
    color_scheme: str = "Set2"  # matplotlib/seaborn color palette
    show_legend: bool = True
    show_grid: bool = True
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None


@dataclass
class TableConfig:
    """Configuration for a table in the report"""
    
    title: str
    columns: Optional[List[str]] = None  # None = all columns
    max_rows: Optional[int] = None  # None = all rows
    show_index: bool = False
    alternate_row_colors: bool = True
    header_bg_color: Union[str, Tuple] = "#1f77b4"
    header_text_color: Union[str, Tuple] = colors.white
    col_widths: Optional[List[float]] = None  # Column widths in inches


@dataclass
class SectionConfig:
    """Configuration for a report section"""
    
    title: str
    content_type: str  # text, chart, table, custom
    content: Any  # Text string, ChartConfig, TableConfig, or custom data
    page_break_before: bool = False
    page_break_after: bool = False


@dataclass
class ReportConfig:
    """Configuration for PDF report generation"""
    
    # Data sources
    data_sources: List[Dict[str, str]] = field(default_factory=list)  # [{"name": "sales", "path": "data.csv", "type": "csv"}]
    
    # Report metadata
    title: str = "Professional Report"
    subtitle: str = ""
    author: str = ""
    subject: str = ""
    date: Optional[str] = None  # None = today's date
    
    # Page settings
    page_size: str = "letter"  # letter, A4, legal
    orientation: str = "portrait"  # portrait, landscape
    
    # Sections
    sections: List[Dict[str, Any]] = field(default_factory=list)
    
    # Branding
    branding: Optional[Dict[str, Any]] = None
    
    # TOC settings
    include_toc: bool = True
    toc_title: str = "Table of Contents"
    
    # Cover page
    include_cover_page: bool = True
    cover_subtitle: str = ""
    cover_image: Optional[str] = None
    
    # Headers and footers
    include_header: bool = True
    include_footer: bool = True
    include_page_numbers: bool = True
    
    # Output settings
    output_folder: str = "./reports"
    output_filename: str = "report.pdf"
    
    # Batch processing
    batch_mode: bool = False
    batch_data_sources: List[str] = field(default_factory=list)


class NumberedCanvas(canvas.Canvas):
    """Canvas with automatic page numbering and headers/footers"""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self.branding = None
        self.config = None
        
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        """Add page numbers and headers/footers to all pages"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_page_decorations(self, page_count):
        """Draw headers, footers, and page numbers"""
        page_num = self._pageNumber
        
        # Skip decorations on cover page
        if page_num == 1 and self.config and self.config.include_cover_page:
            return
            
        if not self.config:
            return
            
        # Header
        if self.config.include_header and page_num > 1:
            self.saveState()
            self.setFont('Helvetica', 9)
            self.setFillColor(colors.grey)
            
            # Logo in header (if available)
            if self.branding and self.branding.logo_path and os.path.exists(self.branding.logo_path):
                try:
                    logo = ImageReader(self.branding.logo_path)
                    self.drawImage(logo, 0.5*inch, self._pagesize[1] - 0.7*inch,
                                 width=1*inch, height=0.3*inch, preserveAspectRatio=True, mask='auto')
                except:
                    pass
            
            # Report title in header
            self.drawRightString(self._pagesize[0] - 0.5*inch, 
                                self._pagesize[1] - 0.5*inch, 
                                self.config.title)
            
            # Header line
            self.setStrokeColor(colors.grey)
            self.setLineWidth(0.5)
            self.line(0.5*inch, self._pagesize[1] - 0.75*inch, 
                     self._pagesize[0] - 0.5*inch, self._pagesize[1] - 0.75*inch)
            
            self.restoreState()
        
        # Footer
        if self.config.include_footer:
            self.saveState()
            self.setFont('Helvetica', 8)
            self.setFillColor(colors.grey)
            
            # Footer line
            self.setStrokeColor(colors.grey)
            self.setLineWidth(0.5)
            self.line(0.5*inch, 0.75*inch, 
                     self._pagesize[0] - 0.5*inch, 0.75*inch)
            
            # Footer text (left)
            if self.branding:
                footer_text = self.branding.report_footer
            else:
                footer_text = f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            self.drawString(0.5*inch, 0.5*inch, footer_text)
            
            # Page numbers (right)
            if self.config.include_page_numbers:
                self.drawRightString(self._pagesize[0] - 0.5*inch, 
                                    0.5*inch,
                                    f"Page {page_num - 1} of {page_count - 1}")
            
            self.restoreState()


class PDFReportGenerator:
    """Generate professional PDF reports with charts, tables, and branding"""
    
    def __init__(self, config: ReportConfig):
        self.config = config
        self.data = {}  # Loaded data sources
        self.elements = []  # Report elements (flowables)
        self.styles = getSampleStyleSheet()
        
        # Create output folder
        Path(config.output_folder).mkdir(parents=True, exist_ok=True)
        
        # Initialize branding
        if config.branding:
            self.branding = BrandingConfig(**config.branding)
        else:
            self.branding = BrandingConfig()
        
        # Setup custom styles
        self._setup_styles()
        
        # Page size
        self.page_size = self._get_page_size()
        
    def _get_page_size(self):
        """Get page size from config"""
        sizes = {
            'letter': letter,
            'a4': A4,
            'legal': legal
        }
        size = sizes.get(self.config.page_size.lower(), letter)
        
        if self.config.orientation.lower() == 'landscape':
            return (size[1], size[0])
        return size
        
    def _setup_styles(self):
        """Setup custom paragraph styles with branding"""
        # Convert hex colors to reportlab colors
        primary = self._hex_to_color(self.branding.primary_color)
        text_color = self._hex_to_color(self.branding.text_color)
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontName=self.branding.title_font,
            fontSize=self.branding.title_size,
            textColor=primary,
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        # Heading styles
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontName=self.branding.heading_font,
            fontSize=self.branding.heading1_size,
            textColor=primary,
            spaceAfter=12,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontName=self.branding.heading_font,
            fontSize=self.branding.heading2_size,
            textColor=primary,
            spaceAfter=10,
            spaceBefore=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading3',
            parent=self.styles['Heading3'],
            fontName=self.branding.heading_font,
            fontSize=self.branding.heading3_size,
            textColor=text_color,
            spaceAfter=8,
            spaceBefore=8
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontName=self.branding.body_font,
            fontSize=self.branding.body_size,
            textColor=text_color,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
    def _hex_to_color(self, hex_or_tuple):
        """Convert hex color to reportlab Color"""
        if isinstance(hex_or_tuple, tuple):
            if len(hex_or_tuple) == 3:
                return colors.Color(hex_or_tuple[0]/255, hex_or_tuple[1]/255, hex_or_tuple[2]/255)
            return hex_or_tuple
        
        if isinstance(hex_or_tuple, str) and hex_or_tuple.startswith('#'):
            hex_or_tuple = hex_or_tuple.lstrip('#')
            r = int(hex_or_tuple[0:2], 16) / 255
            g = int(hex_or_tuple[2:4], 16) / 255
            b = int(hex_or_tuple[4:6], 16) / 255
            return colors.Color(r, g, b)
        
        return hex_or_tuple
        
    def load_data(self):
        """Load all data sources"""
        print("📊 Loading data sources...")
        
        for source in self.config.data_sources:
            name = source.get('name', 'data')
            path = source.get('path')
            source_type = source.get('type', 'csv')
            
            if not os.path.exists(path):
                print(f"⚠️  Data source not found: {path}")
                continue
            
            print(f"  Loading {name} from {path} ({source_type})")
            
            if source_type == 'csv':
                self.data[name] = pd.read_csv(path)
            elif source_type == 'excel':
                self.data[name] = pd.read_excel(path)
            elif source_type == 'json':
                self.data[name] = pd.read_json(path)
            else:
                print(f"⚠️  Unsupported source type: {source_type}")
                
        print(f"✅ Loaded {len(self.data)} data sources")
        
    def create_cover_page(self):
        """Create report cover page"""
        # Logo (if available)
        if self.branding.logo_path and os.path.exists(self.branding.logo_path):
            try:
                logo = Image(self.branding.logo_path, 
                           width=self.branding.logo_width, 
                           height=self.branding.logo_height)
                logo.hAlign = 'CENTER'
                self.elements.append(logo)
                self.elements.append(Spacer(1, 0.5*inch))
            except Exception as e:
                print(f"⚠️  Could not load logo: {e}")
        
        # Cover image (if specified)
        if self.config.cover_image and os.path.exists(self.config.cover_image):
            try:
                cover_img = Image(self.config.cover_image, width=5*inch, height=3*inch)
                cover_img.hAlign = 'CENTER'
                self.elements.append(cover_img)
                self.elements.append(Spacer(1, 0.5*inch))
            except Exception as e:
                print(f"⚠️  Could not load cover image: {e}")
        
        # Spacer to center title
        self.elements.append(Spacer(1, 2*inch))
        
        # Title
        title = Paragraph(self.config.title, self.styles['CustomTitle'])
        self.elements.append(title)
        
        # Subtitle
        if self.config.subtitle:
            subtitle = Paragraph(self.config.subtitle, self.styles['CustomHeading2'])
            self.elements.append(subtitle)
        
        if self.config.cover_subtitle:
            cover_sub = Paragraph(self.config.cover_subtitle, self.styles['CustomBody'])
            self.elements.append(cover_sub)
        
        self.elements.append(Spacer(1, 1*inch))
        
        # Metadata
        date_str = self.config.date or datetime.now().strftime("%B %d, %Y")
        
        meta_style = ParagraphStyle(
            'MetaData',
            parent=self.styles['CustomBody'],
            alignment=TA_CENTER,
            fontSize=12
        )
        
        if self.config.author:
            author = Paragraph(f"<b>Prepared by:</b> {self.config.author}", meta_style)
            self.elements.append(author)
        
        date_para = Paragraph(f"<b>Date:</b> {date_str}", meta_style)
        self.elements.append(date_para)
        
        if self.branding.company_name:
            company = Paragraph(f"<b>{self.branding.company_name}</b>", meta_style)
            self.elements.append(Spacer(1, 0.5*inch))
            self.elements.append(company)
        
        # Page break after cover
        self.elements.append(PageBreak())
        
    def create_toc(self):
        """Create table of contents"""
        # TOC title
        toc_title = Paragraph(self.config.toc_title, self.styles['CustomHeading1'])
        self.elements.append(toc_title)
        self.elements.append(Spacer(1, 0.3*inch))
        
        # Create TOC object
        toc = TableOfContents()
        toc.levelStyles = [
            ParagraphStyle(
                'TOCHeading1',
                parent=self.styles['CustomBody'],
                fontSize=12,
                leftIndent=0,
                spaceBefore=5,
                spaceAfter=5
            ),
            ParagraphStyle(
                'TOCHeading2',
                parent=self.styles['CustomBody'],
                fontSize=10,
                leftIndent=20,
                spaceBefore=3,
                spaceAfter=3
            ),
        ]
        
        self.elements.append(toc)
        self.elements.append(PageBreak())
        
    def create_chart(self, chart_config: ChartConfig, data: pd.DataFrame) -> Optional[Image]:
        """Create a chart and return as Image flowable"""
        try:
            # Create figure
            fig, ax = plt.subplots(figsize=(chart_config.width/inch, chart_config.height/inch), dpi=100)
            
            # Prepare data
            chart_data = data.copy()
            
            # Apply aggregation if needed
            if chart_config.aggregation != 'none' and chart_config.data_column_x and chart_config.data_column_y:
                agg_funcs = {
                    'sum': 'sum',
                    'count': 'count',
                    'avg': 'mean',
                    'min': 'min',
                    'max': 'max'
                }
                agg_func = agg_funcs.get(chart_config.aggregation, 'sum')
                chart_data = data.groupby(chart_config.data_column_x)[chart_config.data_column_y].agg(agg_func).reset_index()
            
            # Set color palette
            if chart_config.color_scheme:
                try:
                    palette = sns.color_palette(chart_config.color_scheme)
                    colors_list = palette.as_hex()
                except:
                    colors_list = None
            else:
                colors_list = None
            
            # Create chart based on type
            if chart_config.chart_type == 'bar':
                if colors_list:
                    ax.bar(chart_data[chart_config.data_column_x], 
                          chart_data[chart_config.data_column_y],
                          color=colors_list)
                else:
                    ax.bar(chart_data[chart_config.data_column_x], 
                          chart_data[chart_config.data_column_y])
                
            elif chart_config.chart_type == 'line':
                if chart_config.data_columns:
                    for col in chart_config.data_columns:
                        ax.plot(chart_data[chart_config.data_column_x], chart_data[col], marker='o', label=col)
                else:
                    ax.plot(chart_data[chart_config.data_column_x], 
                           chart_data[chart_config.data_column_y], marker='o')
                
            elif chart_config.chart_type == 'pie':
                ax.pie(chart_data[chart_config.data_column_y], 
                      labels=chart_data[chart_config.data_column_x],
                      autopct='%1.1f%%',
                      colors=colors_list if colors_list else None)
                
            elif chart_config.chart_type == 'scatter':
                ax.scatter(chart_data[chart_config.data_column_x], 
                          chart_data[chart_config.data_column_y],
                          alpha=0.6,
                          color=colors_list[0] if colors_list else None)
                
            elif chart_config.chart_type == 'heatmap':
                # Create pivot table for heatmap
                if len(chart_data.columns) >= 3:
                    pivot = chart_data.pivot_table(
                        index=chart_data.columns[0],
                        columns=chart_data.columns[1],
                        values=chart_data.columns[2],
                        aggfunc='sum'
                    )
                    sns.heatmap(pivot, ax=ax, cmap=chart_config.color_scheme, annot=True, fmt='.0f')
                    
            elif chart_config.chart_type == 'box':
                data_to_plot = [chart_data[col].dropna() for col in chart_config.data_columns] if chart_config.data_columns else [chart_data[chart_config.data_column_y].dropna()]
                ax.boxplot(data_to_plot)
                if chart_config.data_columns:
                    ax.set_xticklabels(chart_config.data_columns)
            
            # Styling
            ax.set_title(chart_config.title, fontsize=14, fontweight='bold', pad=15)
            
            if chart_config.xlabel and chart_config.chart_type != 'pie':
                ax.set_xlabel(chart_config.xlabel, fontsize=10)
            elif chart_config.data_column_x and chart_config.chart_type not in ['pie', 'heatmap']:
                ax.set_xlabel(chart_config.data_column_x, fontsize=10)
                
            if chart_config.ylabel and chart_config.chart_type != 'pie':
                ax.set_ylabel(chart_config.ylabel, fontsize=10)
            elif chart_config.data_column_y and chart_config.chart_type not in ['pie', 'heatmap']:
                ax.set_ylabel(chart_config.data_column_y, fontsize=10)
            
            if chart_config.show_grid and chart_config.chart_type not in ['pie', 'heatmap']:
                ax.grid(True, alpha=0.3, linestyle='--')
            
            if chart_config.show_legend and chart_config.chart_type in ['line'] and chart_config.data_columns:
                ax.legend()
            
            # Rotate x-axis labels if needed
            if chart_config.chart_type in ['bar', 'line']:
                plt.xticks(rotation=45, ha='right')
            
            plt.tight_layout()
            
            # Save to bytes
            img_buffer = io.BytesIO()
            fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close(fig)
            
            # Create Image flowable
            img = Image(img_buffer, width=chart_config.width, height=chart_config.height)
            img.hAlign = 'CENTER'
            
            return img
            
        except Exception as e:
            print(f"⚠️  Error creating chart '{chart_config.title}': {e}")
            return None
        
    def create_table(self, table_config: TableConfig, data: pd.DataFrame) -> Optional[KeepTogether]:
        """Create a styled table and return as flowable"""
        try:
            # Select columns
            if table_config.columns:
                table_data = data[table_config.columns].copy()
            else:
                table_data = data.copy()
            
            # Limit rows
            if table_config.max_rows:
                table_data = table_data.head(table_config.max_rows)
            
            # Prepare data for reportlab table
            if table_config.show_index:
                table_array = [['Index'] + list(table_data.columns)]
                for idx, row in table_data.iterrows():
                    table_array.append([str(idx)] + [str(val) for val in row])
            else:
                table_array = [list(table_data.columns)]
                for _, row in table_data.iterrows():
                    table_array.append([str(val) for val in row])
            
            # Column widths
            if table_config.col_widths:
                col_widths = [w * inch for w in table_config.col_widths]
            else:
                # Auto-calculate column widths
                available_width = self.page_size[0] - 1*inch  # Account for margins
                col_widths = [available_width / len(table_array[0])] * len(table_array[0])
            
            # Create table
            table = Table(table_array, colWidths=col_widths, repeatRows=1)
            
            # Table styling
            header_bg = self._hex_to_color(table_config.header_bg_color)
            header_text = table_config.header_text_color
            
            style_commands = [
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), header_bg),
                ('TEXTCOLOR', (0, 0), (-1, 0), header_text),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                
                # Data rows
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 1), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
                
                # Borders
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ]
            
            # Alternating row colors
            if table_config.alternate_row_colors:
                for i in range(1, len(table_array)):
                    if i % 2 == 0:
                        style_commands.append(
                            ('BACKGROUND', (0, i), (-1, i), colors.Color(0.95, 0.95, 0.95))
                        )
            
            table.setStyle(TableStyle(style_commands))
            
            # Title
            elements = []
            if table_config.title:
                title = Paragraph(table_config.title, self.styles['CustomHeading3'])
                elements.append(title)
                elements.append(Spacer(1, 0.1*inch))
            
            elements.append(table)
            elements.append(Spacer(1, 0.2*inch))
            
            # Keep together on same page
            return KeepTogether(elements)
            
        except Exception as e:
            print(f"⚠️  Error creating table '{table_config.title}': {e}")
            return None
        
    def generate_report(self) -> str:
        """Generate the PDF report"""
        print(f"🚀 Generating report: {self.config.title}")
        
        # Load data
        self.load_data()
        
        # Setup document
        output_path = os.path.join(self.config.output_folder, self.config.output_filename)
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=self.page_size,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=1*inch,
            title=self.config.title,
            author=self.config.author,
            subject=self.config.subject
        )
        
        # Cover page
        if self.config.include_cover_page:
            print("  Creating cover page...")
            self.create_cover_page()
        
        # Table of contents
        if self.config.include_toc:
            print("  Creating table of contents...")
            self.create_toc()
        
        # Sections
        print(f"  Creating {len(self.config.sections)} sections...")
        for i, section_dict in enumerate(self.config.sections, 1):
            print(f"    Section {i}: {section_dict.get('title', 'Untitled')}")
            
            # Page break before (if specified)
            if section_dict.get('page_break_before', False):
                self.elements.append(PageBreak())
            
            # Section title
            title = section_dict.get('title', '')
            if title:
                heading = Paragraph(f'<a name="section_{i}"/>{title}', self.styles['CustomHeading1'])
                self.elements.append(heading)
                self.elements.append(Spacer(1, 0.2*inch))
            
            # Section content
            content_type = section_dict.get('content_type', 'text')
            content = section_dict.get('content')
            data_source = section_dict.get('data_source', list(self.data.keys())[0] if self.data else None)
            
            if content_type == 'text':
                # Text paragraph
                if content:
                    para = Paragraph(content, self.styles['CustomBody'])
                    self.elements.append(para)
                    self.elements.append(Spacer(1, 0.1*inch))
                    
            elif content_type == 'chart':
                # Chart
                if data_source and data_source in self.data:
                    chart_config = ChartConfig(**content)
                    chart_img = self.create_chart(chart_config, self.data[data_source])
                    if chart_img:
                        self.elements.append(chart_img)
                        self.elements.append(Spacer(1, 0.2*inch))
                        
            elif content_type == 'table':
                # Table
                if data_source and data_source in self.data:
                    table_config = TableConfig(**content)
                    table_flowable = self.create_table(table_config, self.data[data_source])
                    if table_flowable:
                        self.elements.append(table_flowable)
            
            # Page break after (if specified)
            if section_dict.get('page_break_after', False):
                self.elements.append(PageBreak())
        
        # Build PDF with custom canvas (for headers/footers)
        print("  Building PDF...")
        
        def on_page(canvas, doc):
            """Called for each page"""
            canvas.saveState()
            canvas.restoreState()
        
        # Use custom canvas class
        doc.canvasmaker = NumberedCanvas
        
        # Pass config to canvas (hacky but works)
        original_build = doc.build
        
        def custom_build(elements, *args, **kwargs):
            doc._canv = doc.canvasmaker(doc.filename, pagesize=doc.pagesize)
            doc._canv.branding = self.branding
            doc._canv.config = self.config
            return original_build(elements, *args, **kwargs)
        
        doc.build = custom_build
        doc.build(self.elements, onFirstPage=on_page, onLaterPages=on_page)
        
        print(f"✅ Report saved: {output_path}")
        return output_path


def load_config(config_path: str) -> ReportConfig:
    """Load report configuration from JSON file"""
    with open(config_path, 'r') as f:
        data = json.load(f)
    return ReportConfig(**data)


def main():
    parser = argparse.ArgumentParser(description='Generate professional PDF reports')
    parser.add_argument('--config', type=str, help='Path to JSON configuration file')
    parser.add_argument('--output', type=str, help='Output folder (overrides config)')
    parser.add_argument('--batch', action='store_true', help='Enable batch processing mode')
    
    args = parser.parse_args()
    
    if args.config:
        config = load_config(args.config)
        
        if args.output:
            config.output_folder = args.output
        
        if args.batch:
            config.batch_mode = True
        
        generator = PDFReportGenerator(config)
        output_path = generator.generate_report()
        
        print(f"\n🎉 Done! Report: {output_path}")
        
    else:
        print("Usage: python pdf_report_generator.py --config config/report_config.json")
        print("\nExample config structure:")
        print(json.dumps({
            "title": "Sales Report",
            "data_sources": [
                {"name": "sales", "path": "data/sales_data.csv", "type": "csv"}
            ],
            "sections": [
                {
                    "title": "Revenue Analysis",
                    "content_type": "chart",
                    "data_source": "sales",
                    "content": {
                        "chart_type": "bar",
                        "title": "Revenue by Product",
                        "data_column_x": "Product",
                        "data_column_y": "Revenue",
                        "aggregation": "sum"
                    }
                }
            ]
        }, indent=2))


if __name__ == "__main__":
    main()
