import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys

# Set seaborn style
sns.set_theme(style="whitegrid")
def main():    # Set page configuration
    st.set_page_config(
        page_title="Aadhar Analysis Dashboard",
        page_icon="📊",
        layout="wide"
    )
    st.markdown("""
        <div style='text-align: center; margin-bottom: 40px;'>
            <h1 style='font-weight: 800; color: #0047AB; font-size: 46px; margin-bottom: 10px; text-shadow: 1px 1px 3px rgba(0,0,0,0.2);'>
                Aadhar Analysis Dashboard
            </h1>
            <div style='width: 100px; height: 5px; background-color: #0047AB; margin: 0 auto 10px auto; border-radius: 2px;'></div>
            <p style='color: #555; font-size: 18px; font-weight: 500;'>Executive Summary Report</p>
        </div>
    """, unsafe_allow_html=True)
      # Load all dataframes
    with st.spinner('Loading data from Aadhar_modified.xlsx...'):
        try:            
            st.info("Loading data from Excel file. This may take a moment...")
            Gender = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Gender')
            Education = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Education')
            Experience = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Experience')
            Age = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Age')
            st.success("Data loaded successfully!")
            
            # Create list of dataframes with their display names
            all_dataframes = [
                {"df": Gender, "name": "Gender"},
                {"df": Education, "name": "Education"},
                {"df": Experience, "name": "Experience"},
                {"df": Age, "name": "Age"}
            ]
              # Create a dropdown to select the category with clear styling
            st.markdown("<h2 style='text-align: center; color: #444; margin: 20px 0;'>Select a category to analyze:</h2>", unsafe_allow_html=True)
            category = st.selectbox(
                "",
                ['Gender', 'Education', 'Experience', 'Age'],
                index=1 if 'Education' in sys.argv else 0,
                format_func=lambda x: f"{x}"
            )
            
            # Find the corresponding dataframe
            selected_df = next(data for data in all_dataframes if data["name"] == category)
            
            # Create the dashboard for the selected category
            create_dashboard(selected_df["df"], selected_df["name"])
                    
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.exception(e)  # This will display the full traceback

def create_dashboard(df, name):
    """Create a dashboard visualization for the given dataframe in Streamlit."""
    st.markdown(f"<h1 style='text-align: center; font-weight: 800; color: #0A2472; margin-bottom: 20px; text-shadow: 1px 1px 2px #ccc;'>{name} Analysis Dashboard</h1>", unsafe_allow_html=True)
    
    # Show information about the data with improved styling
    st.markdown(f"<h3 style='text-align: center; color: #444; background-color: #f8f9fa; padding: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>Executive Dashboard • {len(df)} Data Points</h3>", unsafe_allow_html=True)
    
    # Enable user to select which charts to display with improved styling
    st.markdown("<div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    selected_charts = st.multiselect(
        '📊 Select visualizations to display:',
        ['Distribution', 'KPI Performance', 'Performance Multiple', 
         'Top vs Bottom Performers', 'Time to First Sale', 'CAR2CATPO Ratio',
         'Attrition Count', 'Average Residency', 'Infant Attrition'],
        default=['Distribution', 'KPI Performance', 'Performance Multiple']
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Create a list of chart creation functions
    chart_functions = {
        'Distribution': create_distribution_chart,
        'KPI Performance': create_kpi_performance_chart,
        'Performance Multiple': create_performance_multiple_chart,
        'Top vs Bottom Performers': create_top_bottom_performers_chart,
        'Time to First Sale': create_time_to_first_sale_chart,
        'CAR2CATPO Ratio': create_car2catpo_ratio_chart,
        'Attrition Count': create_attrition_count_chart,
        'Average Residency': create_average_residency_chart,
        'Infant Attrition': create_infant_attrition_chart
    }
      # Organize charts into rows with equal heights
    # Determine how many rows we need (3 charts per row)
    num_charts = len(selected_charts)
    num_rows = (num_charts + 2) // 3  # Integer division rounded up
      # Create each row of charts
    for row in range(num_rows):
        # Create columns for this row
        cols = st.columns(3)
        
        # Add charts to this row
        for col_idx in range(3):
            chart_idx = row * 3 + col_idx
            if chart_idx < num_charts:
                chart_name = selected_charts[chart_idx]
                with cols[col_idx]:
                    try:
                        with st.container():
                            st.markdown(f"""
                                <div style='border: 1px solid #e0e0e0; border-radius: 10px; overflow: hidden; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                                    <h2 style='text-align: center; font-weight: 700; color: #0A2472; background-color: #f0f2f6; 
                                    padding: 15px; margin: 0; border-bottom: 2px solid #e0e0e0;'>
                                    {chart_name}</h2>
                                    <div style='padding: 10px 0;'>
                            """, unsafe_allow_html=True)
                            chart_functions[chart_name](df, name)
                            st.markdown("</div></div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error generating {chart_name} chart: {str(e)}")

def create_distribution_chart(df, name):
    """Create the distribution chart."""
    fig, ax = setup_chart_style()
    
    # Extract the first 3 columns
    first_cols = df.columns[:3]
    # Reshape data for seaborn
    df_melted = pd.melt(df, 
                        id_vars=[first_cols[0]], 
                        value_vars=[first_cols[1], first_cols[2]], 
                        var_name='Metric', 
                        value_name='Count')

    # Calculate percentages for each cohort
    for metric in [first_cols[1], first_cols[2]]:
        total = df[metric].sum()
        df_melted.loc[df_melted['Metric'] == metric, 'Percentage'] = df_melted.loc[df_melted['Metric'] == metric, 'Count'] / total * 100    
    
    # Using seaborn barplot with grouped bars and better colors
    bars = sns.barplot(x='Category', y='Count', hue='Metric', 
                      data=df_melted, 
                      palette=['#1f77b4', '#9ecae1'], 
                      ax=ax, width=0.7)

    ax.set_title(f'{name} Distribution by Cohort', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('Head Count', labelpad=15)    # Adding value labels and percentages inside the bars with increased font size (20% larger)
    base_fontsize = 16  # Increased from 13 (20% larger)
    for container_idx, container in enumerate(ax.containers):
        for bar_idx, bar in enumerate(container):
            count = bar.get_height()
            percentage = df_melted.iloc[container_idx*2+bar_idx if container_idx < 2 else bar_idx]['Percentage']
            
            # Calculate position for text inside the bar
            x_pos = bar.get_x() + bar.get_width()/2
            y_pos = count/2  # Mid-point of bar
            
            # Add the label inside the bar with white text for better visibility
            label_text = f'{int(count)}\n({percentage:.1f}%)'
            color = 'white' if count > 30 else 'black'  # White text for tall bars, black for short ones
            
            ax.text(x_pos, y_pos, label_text, 
                   ha='center', va='center', 
                   color=color, 
                   fontsize=base_fontsize,
                   fontweight='bold',
                   linespacing=1.3)

    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust legend with better styling
    legend = ax.legend(title='Cohort Type', fontsize=14)
    plt.setp(legend.get_title(), fontsize=16, fontweight='bold')
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)

def create_kpi_performance_chart(df, name):
    """Create the KPI performance chart."""
    fig, ax = setup_chart_style()
    
    # Get the 4th and 8th columns (indices 3 and 7)
    col4 = df.columns[3]
    col8 = df.columns[7]

    # Create shorter column names for display
    col4_short = "Cumulative Combined KPI"
    col8_short = "Cumulative KPI 1"# Create a DataFrame with the data and specified columns, multiplying KPI values by 100 to show as percentages
    kpi_data = pd.DataFrame({
        'Category': df['Category'],
        col4_short: df[col4] * 100,  # Multiply by 100 to convert to percentage
        col8_short: df[col8] * 100   # Multiply by 100 to convert to percentage
    })

    # Reshape data for seaborn
    kpi_melted = pd.melt(kpi_data, 
                         id_vars=['Category'], 
                         value_vars=[col4_short, col8_short],
                         var_name='KPI Type', 
                         value_name='Achievement %')
    
    # Prepare custom colors - highlight Female in Gender dashboard
    if name == "Gender":
        # Create a list to store the colors for each bar
        bar_colors = []
        for category in kpi_melted['Category'].unique():
            # Brighter colors for Female, regular colors for Male
            if category == 'Female':
                bar_colors.extend(['#ff5500', '#ff7733'])  # Brighter orange shades for Female
            else:
                bar_colors.extend(['#ff7f0e', '#ff9e4a'])  # Regular orange shades
                
        # Using seaborn barplot with custom colors
        bars = sns.barplot(x='Category', y='Achievement %', hue='KPI Type',
                          data=kpi_melted,
                          palette=bar_colors if len(bar_colors) > 0 else ['#ff7f0e', '#ff9e4a'],
                          ax=ax, width=0.7)
    else:
        # Regular coloring for non-Gender dashboards
        bars = sns.barplot(x='Category', y='Achievement %', hue='KPI Type', 
                          data=kpi_melted, 
                          palette=['#ff7f0e', '#ff9e4a'], 
                          ax=ax, width=0.7)

    ax.set_title(f'KPI Performance by {name} CAP LRM', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('Achievement %', labelpad=15)
    
    # Increased font size by 20% (from 13 to 16)
    base_fontsize = 16  # Increased from 13
    
    # Adding value labels INSIDE the bars
    for container_idx, container in enumerate(ax.containers):
        labels = []
        for bar_idx, bar in enumerate(container):
            height = bar.get_height()
            # Format with no decimal places now that we've multiplied by 100
            labels.append(f'{height:.0f}%')
            
            # Calculate position for text inside the bar
            x_pos = bar.get_x() + bar.get_width()/2
            y_pos = height/2  # Mid-point of bar
            
            # Add the label inside the bar
            color = 'white' if height > 30 else 'black'  # White text for tall bars, black for short ones
            fontweight = 'bold'
            
            ax.text(x_pos, y_pos, f'{height:.0f}%', 
                   ha='center', va='center', 
                   color=color, 
                   fontsize=base_fontsize,
                   fontweight=fontweight)    # Add a custom annotation for Female category in Gender chart
    if name == "Gender":
        # Find the Female category in the data
        female_indices = [i for i, cat in enumerate(kpi_melted['Category'].unique()) if cat == 'Female']
        
        if female_indices:  # If Female category exists in the data
            female_index = female_indices[0]
            
            # Highlight Female category with a subtle effect
            for container_idx, container in enumerate(ax.containers):
                # Get the bar corresponding to Female category
                bar = container[female_index]  # Female bar in current container
                
                # Get bar dimensions
                height = bar.get_height()
                x_pos = bar.get_x() + bar.get_width() / 2
                
                # Add a subtle highlight effect around the Female bar
                # Draw a rectangle around the Female bar
                rect = plt.Rectangle((bar.get_x() - bar.get_width()*0.05, -1), 
                                    bar.get_width()*1.1, height + 2,
                                    fill=False, linestyle='--', 
                                    linewidth=2, edgecolor='red', alpha=0.8, zorder=5)
                ax.add_patch(rect)
                  # Add a "Female" text label above the bar (without arrow)
                if container_idx == 0:  # Only add once
                    ax.text(x_pos, height + 5, 'Female',
                           ha='center', fontsize=16, fontweight='bold',
                           color='darkred',
                           bbox=dict(boxstyle='round,pad=0.3', 
                                    fc='white', ec='red', alpha=0.8))

    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust legend with better styling
    legend = ax.legend(title='Performance Metric', fontsize=14)
    plt.setp(legend.get_title(), fontsize=16, fontweight='bold')
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.3)  # Increased from 0.2 to 0.3 to make room for ticks and annotations
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)

# Helper function to setup consistent chart styling
def setup_chart_style():
    """Set up consistent styling for all charts with executive-level polish."""
    # Set global font size and weight - make everything bolder and more professional
    plt.rcParams.update({
        'font.size': 14,
        'font.weight': 'bold',
        'axes.titlesize': 20,
        'axes.titleweight': 'bold',
        'axes.labelsize': 16,
        'axes.labelweight': 'bold',
        'xtick.labelsize': 14,
        'ytick.labelsize': 14,
        'figure.constrained_layout.use': True,  # Use constrained layout for better spacing
        'axes.grid': True,
        'grid.alpha': 0.3,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.edgecolor': '#333333',
        'axes.linewidth': 1.5,
        'figure.facecolor': '#ffffff',
        'axes.facecolor': '#f9f9f9',
    })
    
    # Create figure with consistent size for all charts
    # Using a fixed aspect ratio to ensure all charts have the same height
    fig, ax = plt.subplots(figsize=(12, 8), dpi=120)  # Increased DPI for sharper images
    
    # Set figure face color to white for better appearance
    fig.set_facecolor('white')
    
    # Adjust the bottom margin to create more space for x-axis labels
    plt.subplots_adjust(bottom=0.15)
    
    # Add a subtle background color to enhance readability
    ax.set_facecolor('#f9f9f9')
    
    # Add a border to the figure for a more polished look
    fig.patch.set_edgecolor('#e0e0e0')
    fig.patch.set_linewidth(2)
    
    return fig, ax

def extend_y_limits(ax, top_extension=0.2):
    """Extend the y-axis limits to add more room at the top for labels."""
    y_min, y_max = ax.get_ylim()
    y_range = y_max - y_min
    ax.set_ylim(y_min, y_max + y_range * top_extension)
    return ax

def create_performance_multiple_chart(df, name):
    """Create the performance multiple chart."""
    fig, ax = setup_chart_style()
    
    # Get the 7th and 11th columns (indices 6 and 10)
    col7 = df.columns[6]
    col11 = df.columns[10]

    # Create shorter column names for display
    col7_short = "Performance Multiple KPI Combined"
    col11_short = "Performance Multiple KPI 1"

    # Create a DataFrame with the data and specified columns
    perf_data = pd.DataFrame({
        'Category': df['Category'],
        col7_short: df[col7],
        col11_short: df[col11]
    })

    # Reshape data for seaborn
    perf_melted = pd.melt(perf_data, 
                          id_vars=['Category'], 
                          value_vars=[col7_short, col11_short],
                          var_name='Performance Type', 
                          value_name='Multiple')    
    
    # Using seaborn barplot with grouped bars
    bars = sns.barplot(x='Category', y='Multiple', hue='Performance Type', 
                      data=perf_melted, 
                      palette=['#2ca02c', '#98df8a'], 
                      ax=ax, width=0.7)

    ax.set_title(f'Performance Multiple by {name}', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('Multiple Value', labelpad=15)    # Adding value labels inside the bars with larger font size
    base_fontsize = 16  # Increased from 13 (20% larger)
    for container_idx, container in enumerate(ax.containers):
        for bar in container:
            height = bar.get_height()
            
            # Calculate position for text inside the bar
            x_pos = bar.get_x() + bar.get_width()/2
            y_pos = height/2  # Mid-point of bar
            
            # Add the label inside the bar
            label_text = f'{height:.1f}x'
            color = 'white' if height > 1.5 else 'black'  # White text for tall bars, black for short ones
            
            ax.text(x_pos, y_pos, label_text, 
                   ha='center', va='center', 
                   color=color, 
                   fontsize=base_fontsize,
                   fontweight='bold')

    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust legend with better styling
    legend = ax.legend(title='Multiple Type', fontsize=14)
    plt.setp(legend.get_title(), fontsize=16, fontweight='bold')
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)

def create_top_bottom_performers_chart(df, name):
    """Create the top and bottom performers chart."""
    fig, ax = setup_chart_style()
    
    # Get the 5th, 6th, 9th and 10th columns (indices 4, 5, 8, 9)
    col5 = df.columns[4]  # Top performers Combined KPI
    col6 = df.columns[5]  # Bottom performers Combined KPI
    col9 = df.columns[8]  # Top performers KPI 1
    col10 = df.columns[9]  # Bottom performers KPI 1

    # Create shorter column names for display
    col5_short = "Top 10% (Combined)"
    col6_short = "Bottom 10% (Combined)" 
    col9_short = "Top 10% (KPI 1)"
    col10_short = "Bottom 10% (KPI 1)"

    # Create a DataFrame with the data and specified columns
    performer_data = pd.DataFrame({
        'Category': df['Category'],
        col5_short: df[col5],
        col6_short: df[col6],
        col9_short: df[col9],
        col10_short: df[col10]
    })

    # Reshape data for seaborn - first combine top performers
    top_performers = pd.melt(performer_data, 
                         id_vars=['Category'], 
                         value_vars=[col5_short, col9_short],
                         var_name='KPI Type', 
                         value_name='Value')
    top_performers['Performance'] = 'Top 10%'
    
    # Ensure unique index to avoid reindexing issues
    top_performers = top_performers.reset_index(drop=True)

    # Then combine bottom performers
    bottom_performers = pd.melt(performer_data, 
                         id_vars=['Category'], 
                         value_vars=[col6_short, col10_short],
                         var_name='KPI Type', 
                         value_name='Value')
    bottom_performers['Performance'] = 'Bottom 10%'
    
    # Ensure unique index to avoid reindexing issues
    bottom_performers = bottom_performers.reset_index(drop=True)

    # Combine both datasets
    all_performers = pd.concat([top_performers, bottom_performers], ignore_index=True)    
    
    # Using seaborn barplot with grouped bars with enhanced colors
    bars = sns.barplot(x='Category', y='Value', hue='Performance', 
                      data=all_performers, 
                      palette=['#9467bd', '#d8b2ff'],
                      ax=ax, width=0.7)

    ax.set_title(f'Top vs Bottom Performers by {name}', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('CAP Value', labelpad=15)    # Adding value labels inside bars with larger font
    base_fontsize = 16  # 20% larger than original 13
    for container_idx, container in enumerate(ax.containers):
        for bar_idx, bar in enumerate(container):
            height = bar.get_height()
            
            # Calculate position for text inside the bar
            x_pos = bar.get_x() + bar.get_width()/2
            y_pos = height/2  # Mid-point of bar
            
            # Add the label inside the bar
            label_text = f'{height:.1f}'
            color = 'white' if container_idx == 0 else 'black'  # Top performers white, bottom black
            
            ax.text(x_pos, y_pos, label_text, 
                   ha='center', va='center', 
                   color=color, 
                   fontsize=base_fontsize,
                   fontweight='bold')

    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust legend with better styling
    legend = ax.legend(title='Performance Group', fontsize=14)
    plt.setp(legend.get_title(), fontsize=16, fontweight='bold')
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)

def create_time_to_first_sale_chart(df, name):
    """Create the time to first sale chart."""
    fig, ax = setup_chart_style()
    
    # Get the 12th column (index 11)
    col12 = df.columns[11]

    # Create a DataFrame for the chart
    first_sale_data = pd.DataFrame({
        'Category': df['Category'],
        'Time to First Sale': df[col12]
    })

    # Using seaborn barplot (fixed deprecation warning)    
    # Generate a palette with enough colors for all categories
    category_count = len(first_sale_data['Category'].unique())
    palette = sns.color_palette("Blues_d", category_count)
    
    bars = sns.barplot(x='Category', y='Time to First Sale', data=first_sale_data, 
                     hue='Category', palette=palette, legend=False, ax=ax, width=0.7)

    ax.set_title(f'Time to Make First Sale by {name}', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('Time (months)', labelpad=15)    # Adding value labels inside each bar with increased font size (20% larger)
    base_fontsize = 16  # Increased from 13 (20% larger)
    for i, container in enumerate(ax.containers):
        for j, bar in enumerate(container):
            height = bar.get_height()
            if height >= 0.5:  # Only add text if bar is tall enough
                ax.text(bar.get_x() + bar.get_width()/2, height/2,
                        f'{height:.2f} months',
                        ha='center', va='center',
                        color='white', fontweight='bold', fontsize=base_fontsize)    # Add a horizontal line for the average with larger font size
    avg_time = df[col12].mean()
    ax.axhline(y=avg_time, color='red', linestyle='--', alpha=0.7)
      # Find appropriate empty space for the average label
    # Move text to upper right corner of the chart instead of directly on the line
    right_edge = ax.get_xlim()[1]
    y_min, y_max = ax.get_ylim()
    y_position = y_max * 0.9  # Position at 90% of chart height
    
    ax.text(right_edge * 0.8, y_position, f'Average: {avg_time:.2f} months', 
            color='red', ha='right', va='center', fontsize=14, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='red', alpha=0.7, pad=5, boxstyle='round'))
    
    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)

def create_car2catpo_ratio_chart(df, name):
    """Create the CAR2CATPO ratio chart."""
    fig, ax = setup_chart_style()
    
    # Get the 13th column (index 12)
    col13 = df.columns[12]

    # Create a DataFrame for the chart
    ratio_data = pd.DataFrame({
        'Category': df['Category'],
        'CAR2CATPO Ratio': df[col13]
    })

    # Using seaborn barplot (fixed deprecation warning)
    # Generate a palette with enough colors for all categories
    category_count = len(ratio_data['Category'].unique())
    palette = sns.color_palette("Greens_d", category_count)    
    bars = sns.barplot(x='Category', y='CAR2CATPO Ratio', data=ratio_data, 
                      hue='Category', palette=palette, legend=False, ax=ax, width=0.7)

    ax.set_title(f'CAR2CATPO Ratio by {name}', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('Ratio Value', labelpad=15)    # Adding value labels inside the bars with increased font size (20% larger)
    base_fontsize = 16  # Increased from 13 (20% larger)
    for i, container in enumerate(ax.containers):
        for j, bar in enumerate(container):
            height = bar.get_height()
            if height >= 0.3:  # Only add text if bar is tall enough
                ax.text(bar.get_x() + bar.get_width()/2, height/2,
                        f'{height:.2f}',
                        ha='center', va='center',
                        color='white', fontweight='bold', fontsize=base_fontsize)    # Add a horizontal line for the average with larger font size
    avg_ratio = df[col13].mean()
    ax.axhline(y=avg_ratio, color='red', linestyle='--', alpha=0.7)
      # Find appropriate empty space for the average label
    # Move text to upper right corner of the chart instead of directly on the line
    right_edge = ax.get_xlim()[1]
    y_min, y_max = ax.get_ylim()
    y_position = y_max * 0.9  # Position at 90% of chart height
    
    ax.text(right_edge * 0.8, y_position, f'Average: {avg_ratio:.2f}', 
            color='red', ha='right', va='center', fontsize=14, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='red', alpha=0.7, pad=5, boxstyle='round'))
    
    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)

def create_attrition_count_chart(df, name):
    """Create the attrition count chart."""
    fig, ax = setup_chart_style()
    
    # Get the 14th column (index 13)
    col14 = df.columns[13]

    # Create a DataFrame for the chart
    attrition_data = pd.DataFrame({
        'Category': df['Category'],
        'Attrited Employees': df[col14]
    })

    # Using seaborn barplot (fixed deprecation warning)
    # Generate a palette with enough colors for all categories
    category_count = len(attrition_data['Category'].unique())
    palette = sns.color_palette("Reds_d", category_count)
    
    bars = sns.barplot(x='Category', y='Attrited Employees', data=attrition_data, 
                     hue='Category', palette=palette, legend=False, ax=ax, width=0.7)

    ax.set_title(f'Employee Attrition by {name}', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('Number of Attrited Employees', labelpad=15)    # Calculate and display attrition percentages
    total_per_category = df['CAP LRM cohort'].values
    attrition_per_category = df[col14].values
    attrition_rates = attrition_per_category / total_per_category * 100

    # Increased font size by 20%
    base_fontsize = 16  # Increased from 13
    
    # Add value count and percentage annotations inside the bars
    for i, container in enumerate(ax.containers):
        for j, bar in enumerate(container):
            count = bar.get_height()
            rate = attrition_rates[j]
            
            if count >= 1:  # Only add text if bar is tall enough
                # Position for the value at top third of the bar
                ax.text(bar.get_x() + bar.get_width()/2, count*0.7, 
                        f'{int(count)}', 
                        ha='center', va='center', color='white',
                        fontweight='bold', fontsize=base_fontsize)
                
                # Position for the percentage at bottom third of the bar
                ax.text(bar.get_x() + bar.get_width()/2, count*0.3, 
                        f'{rate:.1f}%', 
                        ha='center', va='center', color='white',
                        fontweight='bold', fontsize=base_fontsize-2)
                    
    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)

    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)

def create_average_residency_chart(df, name):
    """Create the average residency chart."""
    fig, ax = setup_chart_style()
    
    # Get the 15th and 16th columns (indices 14 and 15)
    col15 = df.columns[14]  # Average Residency of all employees
    col16 = df.columns[15]  # Average Residency of TOP 100 employees

    # Create shorter column names for display
    col15_short = "All Employees"
    col16_short = "Top 100 Performers"

    # Create a DataFrame for the chart
    residency_data = pd.DataFrame({
        'Category': df['Category'],
        col15_short: df[col15],
        col16_short: df[col16]
    })

    # Calculate the percentage differences between Top 100 and All employees
    for idx, row in residency_data.iterrows():
        residency_data.loc[idx, 'Percentage Diff'] = ((row[col16_short] - row[col15_short]) / row[col15_short]) * 100

    # Reshape data for seaborn
    residency_melted = pd.melt(residency_data, 
                             id_vars=['Category'], 
                             value_vars=[col15_short, col16_short],
                             var_name='Employee Group', 
                             value_name='Average Residency')

    # Using seaborn barplot with grouped bars - improved color palette
    bars = sns.barplot(x='Category', y='Average Residency', hue='Employee Group', 
                      data=residency_melted, 
                      palette=['#4472C4', '#8FAADC'], 
                      ax=ax, width=0.7)

    ax.set_title(f'Employment Tenure by {name}', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('Average Tenure (months)', labelpad=15)    # Adding value labels inside each bar with increased font size (20% larger)
    base_fontsize = 16  # Increased from 13 (20% larger)
    for container_idx, container in enumerate(ax.containers):
        for bar_idx, bar in enumerate(container):
            height = bar.get_height()
            if height >= 1.0:  # Only add text if bar is tall enough
                ax.text(bar.get_x() + bar.get_width()/2, height/2,
                        f'{height:.2f}',
                        ha='center', va='center',
                        color='white', fontweight='bold', fontsize=base_fontsize)    # Add horizontal line for overall average tenure for all employees with larger font size
    overall_avg = df[col15].mean()
    ax.axhline(y=overall_avg, color='red', linestyle='--', alpha=0.7)
    
    # Find appropriate empty space for the average label
    right_edge = ax.get_xlim()[1]
    y_min, y_max = ax.get_ylim()
    y_position = y_max * 0.9  # Position at 90% of chart height
    
    ax.text(right_edge * 0.8, y_position, f'Average: {overall_avg:.2f}', 
            color='red', ha='right', va='center', fontsize=14, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='red', alpha=0.7, pad=5, boxstyle='round'))

    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Adjust legend with better positioning
    ax.legend(title='Employee Group', loc='upper right')
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)

def create_infant_attrition_chart(df, name):
    """Create the infant attrition chart."""
    fig, ax = setup_chart_style()
    
    # Get the last column (index 17)
    last_col = df.columns[-1]  # Using -1 to access the last column

    # Create a DataFrame for the chart with a shorter column name for display
    infant_attrition_data = pd.DataFrame({
        'Category': df['Category'],
        'Infant Attrition': df[last_col] * 100  # Convert to percentage
    })

    # Using seaborn barplot (fixed deprecation warning)
    # Generate a palette with enough colors for all categories
    category_count = len(infant_attrition_data['Category'].unique())
    palette = sns.color_palette("Blues_d", category_count)    
    bars = sns.barplot(x='Category', y='Infant Attrition', data=infant_attrition_data, 
                      hue='Category', palette=palette, legend=False, ax=ax, width=0.7)

    ax.set_title(f'Infant Attrition Rate by {name}', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('Attrition Rate (%)', labelpad=15)    # Adding value labels inside the bars with increased font size (20% larger)
    base_fontsize = 16  # Increased from 13 (20% larger)
    for i, container in enumerate(ax.containers):
        for j, bar in enumerate(container):
            height = bar.get_height()
            if height >= 2.0:  # Only add text if bar is tall enough
                ax.text(bar.get_x() + bar.get_width()/2, height/2,
                        f'{height:.1f}%',
                        ha='center', va='center',
                        color='white', fontweight='bold', fontsize=base_fontsize)    # Add a horizontal line for the average with larger font size
    avg_attrition = infant_attrition_data['Infant Attrition'].mean()
    ax.axhline(y=avg_attrition, color='red', linestyle='--', alpha=0.7)
      # Find appropriate empty space for the average label
    # Move text to upper right corner of the chart instead of directly on the line
    right_edge = ax.get_xlim()[1]
    y_min, y_max = ax.get_ylim()
    y_position = y_max * 0.9  # Position at 90% of chart height
    
    ax.text(right_edge * 0.8, y_position, f'Average: {avg_attrition:.1f}%', 
            color='red', ha='right', va='center', fontsize=14, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='red', alpha=0.7, pad=5, boxstyle='round'))
    
    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    # Extend y-axis to provide more space for labels
    extend_y_limits(ax, 0.2)
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)

if __name__ == "__main__":
    main()
