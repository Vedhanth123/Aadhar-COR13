"""
HDFC Interactive Dashboard
-------------------------
Streamlit application for interactive exploration of HDFC data with customizable visualizations.

Usage:
    streamlit run hdfc_dashboard.py

Requirements:
    streamlit (can be installed with: pip install streamlit)
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from hdfc_viz import plot_bar_chart, COLOR_SCHEMES, BG_STYLES

# Set page config
st.set_page_config(
    page_title="HDFC Interactive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for better appearance
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 100%;  /* Use full width of the screen */
        margin: 0;
    }
    h1, h2, h3 {
        color: #004080;
    }
    .stSidebar {
        background-color: #f0f3f7;
        padding-top: 1rem;
        min-width: 300px !important;  /* Ensure sidebar has adequate width */
    }
    /* Improve container styling */
    .css-1aumxhk, .css-keje6w, .css-1r6slb0 {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    /* Make charts take more space */
    .element-container {
        width: 100%;
    }
    /* Give the main content more room by reducing padding */
    .block-container {
        padding-top: 1rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("HDFC Interactive Dashboard")
st.markdown("""
This interactive dashboard allows you to explore HDFC data with customizable visualizations.
Use the sidebar options to configure your charts and analyze different aspects of the data.
""")

# Function to load data
@st.cache_data
def load_data(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name, index_col="Category")

# Sidebar for controls
st.sidebar.header("Dashboard Controls")

# File selection
excel_file = st.sidebar.selectbox(
    "Select Excel file",
    ["HDFC_modified.xlsx", "HDFC.xlsx", "HDFC_backup.xlsx"]
)

try:
    # Get available sheets
    excel = pd.ExcelFile(excel_file)
    available_sheets = excel.sheet_names
    
    # Sheet selection
    selected_sheet = st.sidebar.selectbox(
        "Select sheet",
        available_sheets
    )
    
    # Load the data
    data = load_data(excel_file, selected_sheet)
      # Show data overview
    with st.expander("Data Overview", expanded=False):
        st.dataframe(data, use_container_width=True)  # Use full container width
    
    # Chart customization section
    st.sidebar.header("Chart Customization")
    
    # Column selection (multi-select)
    all_columns = data.columns.tolist()
      # Group columns with meaningful names
    # Define the group names and the mapping logic
    group_names = [
        "1) Head Count",
        "2) Performance Indicators KPI Combined",
        "3) Performance Indicators KPI 1",
        "4) Revenue Indicators",
        "5) Attrition Indicators"
    ]
    
    # Create column groups with meaningful names
    column_groups = {}
    
    # Intelligent column grouping based on content
    if len(all_columns) <= 2:
        # Simple case: Just one group for small datasets
        column_groups[group_names[0]] = all_columns
    else:
        # Map columns into groups based on their names and positions
        # Group 1: Head Count - first 2 columns
        head_count_cols = all_columns[:2]
        column_groups[group_names[0]] = head_count_cols
        
        # Group 2: Performance Indicators KPI Combined - columns with "combined" or similar terms
        kpi_combined_cols = [col for col in all_columns if any(term in col.lower() for term in ["combined", "cap on combined", "performance multiple"])]
        if not kpi_combined_cols:  # If no matching columns, use position
            start_idx = min(2, len(all_columns))
            end_idx = min(6, len(all_columns))
            kpi_combined_cols = all_columns[start_idx:end_idx]
        column_groups[group_names[1]] = kpi_combined_cols
        
        # Group 3: Performance Indicators KPI 1 - columns with "kpi 1" or similar
        kpi_1_cols = [col for col in all_columns if any(term in col.lower() for term in ["kpi 1", "kpi  1", "kpi-1"])]
        if not kpi_1_cols:  # If no matching columns, use position
            start_idx = min(6, len(all_columns))
            end_idx = min(10, len(all_columns))
            kpi_1_cols = all_columns[start_idx:end_idx]
        column_groups[group_names[2]] = kpi_1_cols
        
        # Group 4: Revenue Indicators - columns with revenue terms
        revenue_cols = [col for col in all_columns if any(term in col.lower() for term in ["time", "sale", "ratio", "car2catpo"])]
        if not revenue_cols:  # If no matching columns, use position
            start_idx = min(10, len(all_columns))
            end_idx = min(12, len(all_columns))
            revenue_cols = all_columns[start_idx:end_idx]
        column_groups[group_names[3]] = revenue_cols
        
        # Group 5: Attrition Indicators - remaining columns or those with attrition terms
        attrition_cols = [col for col in all_columns if any(term in col.lower() for term in ["attrition", "residency", "attrited"])]
        if not attrition_cols:  # If no matching columns, use position
            attrition_cols = all_columns[12:]
        column_groups[group_names[4]] = attrition_cols
        
        # Remove any empty groups
        column_groups = {k: v for k, v in column_groups.items() if v}
    
    # Group selection
    selected_group = st.sidebar.selectbox(
        "Select column group",
        list(column_groups.keys())
    )
      # Column selection within group
    selected_columns = st.sidebar.multiselect(
        "Select columns to display",
        column_groups[selected_group],
        default=column_groups[selected_group][:min(4, len(column_groups[selected_group]))]
    )
    
    if not selected_columns:
        st.warning("Please select at least one column to display")
    else:        # Check if we're working with sheets that need special handling for long names
        is_designation_sheet = selected_sheet == 'Designation'
        is_education_sheet = selected_sheet == 'Education'
        needs_label_handling = is_designation_sheet or is_education_sheet
        
        # Label display options for sheets with potentially long labels
        if needs_label_handling:
            sheet_type = "Designation" if is_designation_sheet else "Education"
            st.sidebar.subheader(f"{sheet_type} Display Options")
            
            label_display = st.sidebar.radio(
                f"How to display {sheet_type.lower()} names:",
                ["Full Names", "Abbreviated Names", "Rotated Labels (45°)", "Rotated Labels (90°)", "Horizontal Scroll"],
                index=2  # Default to rotated labels for better readability
            )
            
            if label_display == "Horizontal Scroll":
                st.info(f"Chart will use horizontal scrolling for better visibility of {sheet_type.lower()} names. Use the scrollbar below the chart to view all entries.")
            
            if label_display == "Abbreviated Names":
                # Create abbreviated versions of names
                label_mapping = {}
                for label in data.index:
                    words = label.split()
                    if len(words) > 2:
                        # Create abbreviation (first letter of each word)
                        abbr = ''.join([word[0].upper() for word in words])
                        label_mapping[label] = abbr
                    else:
                        # For short names, just use the original
                        label_mapping[label] = label
                
                # Show the mapping so users know what the abbreviations mean
                with st.expander(f"{sheet_type} Name Abbreviations", expanded=False):
                    for full, abbr in label_mapping.items():
                        st.write(f"**{abbr}**: {full}")
        
        # Visualization options
        st.sidebar.subheader("Visual Style")
          # Title and subtitle
        chart_title = st.sidebar.text_input("Chart Title", f"HDFC {selected_sheet} Analysis")
        chart_subtitle = st.sidebar.text_input("Chart Subtitle", "Interactive Dashboard View")
        
        # Axis labels
        x_label = st.sidebar.text_input("X-axis Label", data.index.name or "Category")
        y_label = st.sidebar.text_input("Y-axis Label", "Value")
        
        # Color scheme selection
        color_scheme = st.sidebar.selectbox(
            "Color scheme",
            list(COLOR_SCHEMES.keys())
        )
        
        # Background style
        bg_style = st.sidebar.selectbox(
            "Background style",
            list(BG_STYLES.keys())
        )
        
        # Bar style options
        st.sidebar.subheader("Bar Style")
        bar_width = st.sidebar.slider("Bar width", 0.5, 0.9, 0.7, 0.05)
        bar_alpha = st.sidebar.slider("Bar opacity", 0.7, 1.0, 0.9, 0.05)
        show_edges = st.sidebar.checkbox("Show bar edges", True)
        bar_edge_color = "white" if show_edges else None
        bar_edge_width = 0.5 if show_edges else 0
          # Value display options
        st.sidebar.subheader("Value Display")
        show_values = st.sidebar.checkbox("Show values on bars", True)
        value_rotation = st.sidebar.slider("Value label rotation", 0, 90, 0, 5)
        
        # Column title customization
        st.sidebar.subheader("Column Titles")
        custom_titles = st.sidebar.checkbox("Customize column titles", False)
        
        column_titles = {}
        if custom_titles:
            for col in selected_columns:
                # Format default title with line breaks for long names
                default_title = col.replace('_', ' ')
                if len(default_title) > 20:
                    words = default_title.split()
                    if len(words) > 2:
                        midpoint = len(words) // 2
                        default_title = ' '.join(words[:midpoint]) + '\n' + ' '.join(words[midpoint:])
                
                custom_title = st.sidebar.text_input(f"Title for {col}", default_title)
                column_titles[col] = custom_title
        
        # Layout options
        st.sidebar.subheader("Layout")
        layout_options = {
            "Auto": None,
            "1 row": (1, len(selected_columns)),
            "2x2 grid": (2, 2),
            "2x3 grid": (2, 3)
        }
        selected_layout = st.sidebar.selectbox(
            "Chart layout",
            list(layout_options.keys())
        )
        layout = layout_options[selected_layout]
        
        # Value formatting
        st.sidebar.subheader("Value Formatting")
        
        # Auto-detect percentage columns
        percentage_cols = [col for col in selected_columns if '%' in col.lower()]
        
        # Create value format dict
        value_format = {}
        for col in selected_columns:
            is_percentage = col in percentage_cols
            value_format[col] = {
                'is_percentage': is_percentage,
                'precision': 1 if is_percentage else None  # Auto-detect for non-percentage
            }
          # Main area - Generate the chart
        st.header("Visualization")
        
        # Create container for the chart
        chart_container = st.container()
        with chart_container:
            try:                # Calculate larger figure size based on layout with increased height
                if layout is None:  # Auto layout
                    if len(selected_columns) <= 2:
                        figsize = (12, 8 * len(selected_columns))
                    else:
                        cols = min(2, len(selected_columns))
                        rows = (len(selected_columns) + cols - 1) // cols
                        figsize = (16, 9 * rows)
                else:
                    # Layout is specified as (rows, cols)
                    figsize = (16, 10 * layout[0])  # Make height proportional to number of rows with extra space# Special handling for Designation sheet
                plot_data = data.copy()
                  # Apply special display options if applicable
                x_rotation = 0
                use_horizontal_scroll = False
                
                if needs_label_handling:
                    if label_display == "Abbreviated Names":
                        # Use abbreviated index names
                        plot_data.index = [label_mapping.get(idx, idx) for idx in plot_data.index]
                    elif label_display == "Rotated Labels (45°)":
                        x_rotation = 45
                    elif label_display == "Rotated Labels (90°)":
                        x_rotation = 90
                    elif label_display == "Horizontal Scroll":
                        use_horizontal_scroll = True
                        # For horizontal scroll, make the figure wider
                        figsize = (max(16, len(plot_data.index) * 2), figsize[1])
                        
                    # For sheets with long labels, we need more height per row for readability
                    figsize = (figsize[0], figsize[1] * 1.2)
                
                fig, axes = plot_bar_chart(
                    df=plot_data,
                    columns=selected_columns,
                    title=chart_title,
                    subtitle=chart_subtitle,
                    column_titles=column_titles if custom_titles else None,
                    xlabel=x_label,
                    ylabels=y_label,
                    color_scheme=color_scheme,
                    bg_style=bg_style,
                    show_values=show_values,
                    value_format=value_format,
                    value_rotation=value_rotation,
                    layout=layout,
                    figsize=figsize,  # Use our calculated figure size
                    bar_width=bar_width,
                    bar_edge_color=bar_edge_color,
                    bar_edge_width=bar_edge_width,
                    bar_alpha=bar_alpha,
                    show_plot=False  # Don't show the plot, we'll display it with st.pyplot
                )
                  # Apply x-axis rotation directly to the plot if needed
                if needs_label_handling and x_rotation > 0:
                    for ax in (axes if isinstance(axes, np.ndarray) else [axes]):
                        plt.sca(ax)
                        plt.xticks(rotation=x_rotation, ha='right' if x_rotation < 90 else 'center')# Display the plot
                if needs_label_handling and label_display == "Horizontal Scroll":
                    # Create a horizontal scrollable container for the plot
                    st.markdown("""
                    <style>
                    .scroll-container {
                        overflow-x: auto;
                        white-space: nowrap;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Save figure to a BytesIO object
                    import io
                    from PIL import Image
                    
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
                    buf.seek(0)
                    img = Image.open(buf)
                    
                    # Calculate appropriate width
                    img_width = len(plot_data.index) * 100  # Scale based on number of items
                    
                    # Create scrollable container with the image
                    st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
                    st.image(img, width=img_width)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add appropriate caption based on the sheet type
                    caption_text = "Scroll horizontally to see all designations" if is_designation_sheet else "Scroll horizontally to see all education categories"
                    st.caption(caption_text)
                else:
                    # Regular display
                    st.pyplot(fig)
                
                # Export options
                st.subheader("Export Options")
                col1, col2 = st.columns(2)
                
                with col1:
                    export_filename = st.text_input("Export filename", "hdfc_chart")
                
                with col2:
                    export_format = st.selectbox("Export format", ["png", "jpg", "pdf", "svg"])
                
                if st.button("Export Chart"):
                    export_path = f"exports/{export_filename}.{export_format}"
                    fig.savefig(export_path, bbox_inches='tight', dpi=300)
                    st.success(f"Chart exported to {export_path}")
                    
            except Exception as e:
                st.error(f"Error generating chart: {e}")
                st.info("Try selecting different columns or adjusting the layout.")
    
    # Advanced analysis section
    st.header("Data Analysis")
      # Show basic statistics
    with st.expander("Statistical Summary"):
        st.dataframe(data.describe(), use_container_width=True)  # Use full width
    
    # Compare columns
    if len(selected_columns) >= 2:
        with st.expander("Column Comparison"):
            # Select columns to compare
            col1, col2 = st.columns(2)
            with col1:
                compare_col1 = st.selectbox("Select first column", selected_columns, index=0)
            with col2:
                compare_col2 = st.selectbox("Select second column", selected_columns, index=min(1, len(selected_columns)-1))
            
            # Calculate correlation
            correlation = data[compare_col1].corr(data[compare_col2])
            st.metric("Correlation", f"{correlation:.4f}")
              # Plot comparison
            fig, ax = plt.subplots(figsize=(14, 8))  # Larger figure size
            ax.scatter(data[compare_col1], data[compare_col2], alpha=0.7, s=120)  # Larger point size
            for i, txt in enumerate(data.index):
                ax.annotate(txt, (data[compare_col1].iloc[i], data[compare_col2].iloc[i]), 
                           xytext=(5, 5), textcoords='offset points')
            ax.set_xlabel(compare_col1)
            ax.set_ylabel(compare_col2)
            ax.set_title(f"Comparison: {compare_col1} vs {compare_col2}")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
    
except Exception as e:
    st.error(f"Error: {e}")
    st.info("Please check if the selected Excel file exists and has the expected structure.")

# Footer
st.markdown("---")
st.markdown("HDFC Data Analysis Dashboard | Created with Streamlit")