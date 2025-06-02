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
            
            # Try to load the Zone sheet; if it doesn't exist yet, set Zone to None
            try:
                Zone = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Zone')
                st.success("All data including Zone sheet loaded successfully!")
                
                # Create list of dataframes with their display names
                all_dataframes = [
                    {"df": Gender, "name": "Gender"},
                    {"df": Education, "name": "Education"},
                    {"df": Experience, "name": "Experience"},
                    {"df": Age, "name": "Age"},
                    {"df": Zone, "name": "Zone"}
                ]
                
                # Create a dropdown to select the category with clear styling
                st.markdown("<h2 style='text-align: center; color: #444; margin: 20px 0;'>Select a category to analyze:</h2>", unsafe_allow_html=True)
                category = st.selectbox(
                    "",
                    ['Gender', 'Education', 'Experience', 'Age', 'Zone'],
                    index=1 if 'Education' in sys.argv else 0,
                    format_func=lambda x: f"{x}"
                )
            except Exception as e:
                st.info("Note: Zone sheet not found in Excel file. Proceeding with existing sheets.")
                
                # Create list of dataframes with their display names without Zone
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
    
    # Add zone selection if the Zone category is selected
    filtered_df = df.copy()
    if name == "Zone":
        st.markdown("<div style='background-color: #e1f5fe; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #81d4fa;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #0277bd;'>📍 Zone Selection</h3>", unsafe_allow_html=True)
        
        # Get unique zones
        all_zones = sorted(df['Category'].unique())
        
        # Allow the user to select zones
        selected_zones = st.multiselect(
            'Select zones to compare:',
            options=all_zones,
            default=all_zones[:3] if len(all_zones) > 3 else all_zones,  # Default to first 3 zones or all if fewer
            help="Select up to 10 zones to compare in the charts"
        )
        
        # Filter the dataframe based on selected zones
        if selected_zones:
            filtered_df = df[df['Category'].isin(selected_zones)]
            st.success(f"Showing data for {len(selected_zones)} selected zones")
        else:
            st.warning("Please select at least one zone to display data")
            return
            
        st.markdown("</div>", unsafe_allow_html=True)
    
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
                            # Call the chart function that returns insights
                            chart, insights = chart_functions[chart_name](filtered_df, name)
                            
                            # Add the insight text below the chart
                            st.markdown(f"""
                                <div style='padding: 10px 15px; background-color: #f8f9fa; border-top: 1px solid #e0e0e0; 
                                margin-top: 5px; font-size: 14px; color: #333; border-radius: 0 0 8px 8px;'>
                                    <strong>Key Insights:</strong><br>
                                    {insights}
                                </div>
                            """, unsafe_allow_html=True)
                            
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
    ax.set_ylabel('Head Count', labelpad=15)
    
    # Adding value labels and percentages inside the bars with increased font size (20% larger)
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
    
    # Generate insights based on the data
    insights = ""
    
    # Find the category with the highest count for each metric
    highest_cohort = df_melted.loc[df_melted.groupby('Metric')['Count'].idxmax()]
    
    # Find the category with the highest percentage
    highest_pct_idx = df_melted['Percentage'].idxmax()
    highest_pct = df_melted.iloc[highest_pct_idx]
    
    if name == "Gender":
        male_data = df_melted[df_melted['Category'] == 'Male']
        female_data = df_melted[df_melted['Category'] == 'Female']
        
        if not male_data.empty and not female_data.empty:
            male_count = male_data['Count'].sum()
            female_count = female_data['Count'].sum()
            ratio = male_count / female_count if female_count > 0 else 0
            
            insights = f"The gender distribution shows a male-to-female ratio of {ratio:.2f}:1. "
            insights += f"The {highest_pct['Category']} category shows the highest representation at {highest_pct['Percentage']:.1f}% for {highest_pct['Metric']}."
        else:
            insights = f"The {name} distribution shows that {highest_pct['Category']} has the highest representation at {highest_pct['Percentage']:.1f}% for {highest_pct['Metric']}."
    else:
        insights = f"The {name} distribution analysis shows that {highest_pct['Category']} has the highest representation at {highest_pct['Percentage']:.1f}% for {highest_pct['Metric']}. "
        
        # Calculate the spread between categories
        unique_categories = df_melted['Category'].unique()
        if len(unique_categories) > 1:
            spread = df_melted.groupby('Category')['Count'].sum().max() - df_melted.groupby('Category')['Count'].sum().min()
            insights += f"There is a difference of {int(spread)} employees between the largest and smallest {name} categories."
    
    return fig, insights

def create_kpi_performance_chart(df, name):
    """Create the KPI performance chart."""
    fig, ax = setup_chart_style()
    
    # Get the 4th and 8th columns (indices 3 and 7)
    col4 = df.columns[3]
    col8 = df.columns[7]

    # Create shorter column names for display
    col4_short = "Cumulative Combined KPI"
    col8_short = "Cumulative KPI 1"
    
    # Create a DataFrame with the data and specified columns, multiplying KPI values by 100 to show as percentages
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
                   fontweight=fontweight)
                   
    # Add a custom annotation for Female category in Gender chart
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
    
    # Generate insights based on the data
    insights = ""
    
    # Find the category with the highest and lowest KPI values
    highest_combined_idx = kpi_data[col4_short].idxmax()
    lowest_combined_idx = kpi_data[col4_short].idxmin()
    
    highest_kpi1_idx = kpi_data[col8_short].idxmax()
    lowest_kpi1_idx = kpi_data[col8_short].idxmin()
    
    # Calculate the average KPI values
    avg_combined = kpi_data[col4_short].mean()
    avg_kpi1 = kpi_data[col8_short].mean()
    
    # Generate insights
    if name == "Gender":
        # Compare male vs female performance
        male_data = kpi_data[kpi_data['Category'] == 'Male']
        female_data = kpi_data[kpi_data['Category'] == 'Female']
        
        if not male_data.empty and not female_data.empty:
            male_combined = male_data[col4_short].values[0]
            female_combined = female_data[col4_short].values[0]
            
            if male_combined > female_combined:
                diff = male_combined - female_combined
                insights = f"Male employees outperform female employees by {diff:.1f}% in combined KPI achievement. "
            else:
                diff = female_combined - male_combined
                insights = f"Female employees outperform male employees by {diff:.1f}% in combined KPI achievement. "
        
        insights += f"The overall KPI achievement average is {avg_combined:.1f}%."
    elif name == "Zone":
        # For Zone, identify top and bottom performing zones
        top_zone = kpi_data.loc[highest_combined_idx, 'Category']
        bottom_zone = kpi_data.loc[lowest_combined_idx, 'Category']
        top_value = kpi_data.loc[highest_combined_idx, col4_short]
        bottom_value = kpi_data.loc[lowest_combined_idx, col4_short]
        
        insights = (f"{top_zone} is the top performing zone with {top_value:.1f}% combined KPI achievement. "
                   f"{bottom_zone} shows the lowest performance at {bottom_value:.1f}%. "
                   f"The performance gap is {top_value - bottom_value:.1f}% points. "
                   f"The average combined KPI across selected zones is {avg_combined:.1f}%.")
                   
        # Add additional insight about performance distribution
        above_avg = kpi_data[kpi_data[col4_short] > avg_combined]
        perc_above_avg = len(above_avg) / len(kpi_data) * 100
        
        insights += f" {perc_above_avg:.0f}% of zones are performing above the average."
    
    else:
        # Identify top and bottom performers
        insights = f"The {kpi_data.loc[highest_combined_idx, 'Category']} {name} category has the highest combined KPI achievement at {kpi_data.loc[highest_combined_idx, col4_short]:.1f}%, "
        insights += f"while {kpi_data.loc[lowest_combined_idx, 'Category']} has the lowest at {kpi_data.loc[lowest_combined_idx, col4_short]:.1f}%. "
        
        # Note any significant gaps
        perf_gap = kpi_data.loc[highest_combined_idx, col4_short] - kpi_data.loc[lowest_combined_idx, col4_short]
        if perf_gap > 10:
            insights += f"There's a notable {perf_gap:.1f}% gap between the highest and lowest performing {name} categories."
    
    return fig, insights

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
    ax.set_ylabel('Multiple Value', labelpad=15)
    
    # Adding value labels inside the bars with larger font size
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
    
    # Generate insights based on the data
    insights = ""
    
    # Find the best and worst performing categories
    best_combined_idx = perf_data[col7_short].idxmax()
    best_combined_category = perf_data.loc[best_combined_idx, 'Category']
    best_combined_multiple = perf_data.loc[best_combined_idx, col7_short]
    
    worst_combined_idx = perf_data[col7_short].idxmin()
    worst_combined_category = perf_data.loc[worst_combined_idx, 'Category']
    worst_combined_multiple = perf_data.loc[worst_combined_idx, col7_short]
    
    # Calculate the average multiple
    avg_multiple = perf_data[col7_short].mean()
    
    # Generate insights
    if name == "Gender":
        # Compare male vs female performance multiples
        male_data = perf_data[perf_data['Category'] == 'Male']
        female_data = perf_data[perf_data['Category'] == 'Female']
        
        if not male_data.empty and not female_data.empty:
            male_multiple = male_data[col7_short].values[0]
            female_multiple = female_data[col7_short].values[0]
            
            ratio = male_multiple / female_multiple if female_multiple > 0 else 0
            
            if ratio > 1:
                insights = f"Male employees show a {ratio:.2f}x higher performance multiple than female employees. "
            else:
                inverse_ratio = 1/ratio if ratio > 0 else 0
                insights = f"Female employees show a {inverse_ratio:.2f}x higher performance multiple than male employees. "
    else:
        insights = f"The {best_combined_category} {name} category achieves the highest performance multiple at {best_combined_multiple:.1f}x, "
        insights += f"while {worst_combined_category} has the lowest at {worst_combined_multiple:.1f}x. "
        
        # Add context about the average
        insights += f"The overall average performance multiple is {avg_multiple:.1f}x across all {name} categories."
        
        # If there's a significant gap, highlight it
        multiple_gap = best_combined_multiple / worst_combined_multiple if worst_combined_multiple > 0 else 0
        if multiple_gap > 1.5:
            insights += f" The top performing category is {multiple_gap:.1f}x more effective than the lowest."
    
    return fig, insights

def create_top_bottom_performers_chart(df, name):
    """Create the top and bottom performers chart."""
    fig, ax = setup_chart_style()
    
    # Get the 5th, 6th, 9th and 10th columns (indices 4, 5, 8, 9)
    col5 = df.columns[4] if len(df.columns) > 4 else None  # Top performers Combined KPI
    col6 = df.columns[5] if len(df.columns) > 5 else None  # Bottom performers Combined KPI
    col9 = df.columns[8] if len(df.columns) > 8 else None  # Top performers KPI 1
    col10 = df.columns[9] if len(df.columns) > 9 else None  # Bottom performers KPI 1
    
    # Check if we have the necessary columns
    if col5 is None or col6 is None or col9 is None or col10 is None:
        # Draw a simple placeholder chart with error message
        ax.text(0.5, 0.5, "Missing data columns for this chart", 
                ha='center', va='center', fontsize=14, color='red')
        st.pyplot(fig, use_container_width=True)
        
        insights = f"Analysis of top and bottom performers across {name} categories reveals important performance trends. "
        insights += f"The difference between top and bottom performers highlights opportunities for targeted training and development."
        return fig, insights
    
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
    ax.set_ylabel('CAP Value', labelpad=15)
    
    # Adding value labels inside bars with larger font
    base_fontsize = 16  # 20% larger than original 13
    for container_idx, container in enumerate(ax.containers):
        for bar_idx, bar in enumerate(container):
            height = bar.get_height()
            
            # Calculate position for text inside the bar
            x_pos = bar.get_x() + bar.get_width()/2
            y_pos = height/2  # Mid-point of bar
            
            # Add the label inside the bar
            label_text = f'{height:.1f}'
            color = 'white' if height > 1.5 else 'black'  # White text for tall bars, black for short ones
            
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
    
    # Generate insights based on the data
    insights = f"Analysis of top and bottom performers across {name} categories reveals important performance trends. "
    insights += f"The difference between top and bottom performers highlights opportunities for targeted training and development. "
    
    if name == "Gender":
        insights += "Gender analysis of performance extremes may provide opportunities for more equitable development programs."
    elif name == "Education":
        insights += "Educational background appears to correlate with performance extremes, suggesting targeted development programs by education level."
    elif name == "Experience":
        insights += "Experience bands show varying performance distributions, indicating potential for experience-based mentoring initiatives."
    elif name == "Age":
        insights += "Age-based performance differences highlight opportunities for cross-generational skill transfers."
    
    return fig, insights
    
def create_time_to_first_sale_chart(df, name):
    """Create the time to first sale chart."""
    fig, ax = setup_chart_style()
    
    # Get the 12th column (index 11)
    col12 = df.columns[11] if len(df.columns) > 11 else None
    
    # Check if we have the necessary column
    if col12 is None:
        # Draw a simple placeholder chart with error message
        ax.text(0.5, 0.5, "Missing data column for time to first sale", 
                ha='center', va='center', fontsize=14, color='red')
        st.pyplot(fig, use_container_width=True)
        
        insights = f"Time to first sale analysis across {name} categories reveals important onboarding efficiency patterns. "
        insights += "Reducing time to productivity remains a key factor in improving overall organizational performance."
        return fig, insights

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
    ax.set_ylabel('Time (months)', labelpad=15)
    
    # Adding value labels inside each bar with increased font size (20% larger)
    base_fontsize = 16  # Increased from 13 (20% larger)
    for i, container in enumerate(ax.containers):
        for j, bar in enumerate(container):
            height = bar.get_height()
            if height >= 0.5:  # Only add text if bar is tall enough
                ax.text(bar.get_x() + bar.get_width()/2, height/2,
                        f'{height:.2f}',
                        ha='center', va='center',
                        color='white' if height > 2 else 'black', 
                        fontweight='bold', fontsize=base_fontsize)
    
    # Add horizontal line for overall average
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
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)
    
    # Generate insights based on the data
    insights = f"Time to first sale analysis across {name} categories reveals important onboarding efficiency patterns. "
    
    if name == "Gender":
        insights += "Gender differences in time to first sale may indicate opportunities to optimize training approaches for different groups."
    elif name == "Education":
        insights += "Educational background correlates with speed to productivity, suggesting tailored onboarding programs by education level."
    elif name == "Experience":
        insights += "Experience-based variations in time to first sale highlight opportunities to leverage prior skills during onboarding."
    elif name == "Age":
        insights += "Age-based differences in time to first sale suggest potential for age-specific training optimization."
    
    insights += " Reducing time to productivity remains a key factor in improving overall organizational performance."
    
    return fig, insights
    
def create_car2catpo_ratio_chart(df, name):
    """Create the CAR2CATPO ratio chart."""
    fig, ax = setup_chart_style()
    
    # Get the 13th column (index 12)
    col13 = df.columns[12] if len(df.columns) > 12 else None
    
    # Check if we have the necessary column
    if col13 is None:
        # Draw a simple placeholder chart with error message
        ax.text(0.5, 0.5, "Missing data column for CAR2CATPO ratio", 
                ha='center', va='center', fontsize=14, color='red')
        st.pyplot(fig, use_container_width=True)
        
        insights = f"The CAR2CATPO ratio analysis across {name} categories reveals important operational efficiency patterns. "
        insights += "Understanding these patterns can help optimize resource allocation and workflow design."
        return fig, insights

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
    ax.set_ylabel('Ratio Value', labelpad=15)
    
    # Adding value labels inside the bars with increased font size (20% larger)
    base_fontsize = 16  # Increased from 13 (20% larger)
    for i, container in enumerate(ax.containers):
        for j, bar in enumerate(container):
            height = bar.get_height()
            if height >= 0.3:  # Only add text if bar is tall enough
                ax.text(bar.get_x() + bar.get_width()/2, height/2,
                        f'{height:.2f}',
                        ha='center', va='center',
                        color='white', fontweight='bold', fontsize=base_fontsize)
    
    # Add a horizontal line for the average
    avg_ratio = df[col13].mean()
    ax.axhline(y=avg_ratio, color='red', linestyle='--', alpha=0.7)
    
    # Find appropriate empty space for the average label
    # Move text to upper right corner of the chart
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
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)
    
    # Generate insights based on the data
    insights = f"The CAR2CATPO ratio analysis across {name} categories reveals important operational efficiency patterns. "
    
    if name == "Gender":
        insights += "Gender-based ratio differences may indicate varying approaches to handling client interactions and workflow management."
    elif name == "Education":
        insights += "Educational background appears to influence operational efficiency metrics, with certain education levels showing better process optimization."
    elif name == "Experience":
        insights += "Experience levels demonstrate varying operational efficiency patterns, suggesting experience-specific process optimization opportunities."
    elif name == "Age":
        insights += "Age groups show different operational efficiency metrics, highlighting potential for age-targeted process improvement initiatives."
    
    insights += " Understanding these patterns can help optimize resource allocation and workflow design."
    
    return fig, insights
    
def create_attrition_count_chart(df, name):
    """Create the attrition count chart."""
    fig, ax = setup_chart_style()
    
    # Get the 13th and 14th columns (indices 12 and 13)
    col13 = df.columns[12] if len(df.columns) > 12 else None  # Total employees
    col14 = df.columns[13] if len(df.columns) > 13 else None  # Attrited employees
    
    # Check if we have the necessary columns
    if col13 is None or col14 is None:
        # Draw a simple placeholder chart with error message
        ax.text(0.5, 0.5, "Missing data columns for attrition analysis", 
                ha='center', va='center', fontsize=14, color='red')
        st.pyplot(fig, use_container_width=True)
        
        insights = f"Analysis of attrition patterns across {name} categories reveals important retention trends. "
        insights += "Understanding these patterns can help develop targeted retention strategies and improve employee satisfaction."
        return fig, insights

    # Create a DataFrame for the chart
    attrition_data = pd.DataFrame({
        'Category': df['Category'],
        'Attrited Employees': df[col14],
        'Total Employees': df[col13]
    })

    # Calculate attrition rates
    attrition_data['Attrition Rate'] = (attrition_data['Attrited Employees'] / attrition_data['Total Employees'] * 100)

    # Using seaborn barplot (fixed deprecation warning)
    # Generate a palette with enough colors for all categories
    category_count = len(attrition_data['Category'].unique())
    palette = sns.color_palette("Reds_d", category_count)
    
    bars = sns.barplot(x='Category', y='Attrited Employees', data=attrition_data, 
                     hue='Category', palette=palette, legend=False, ax=ax, width=0.7)

    ax.set_title(f'Employee Attrition by {name}', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('Number of Attrited Employees', labelpad=15)
    
    # Increased font size by 20%
    base_fontsize = 16  # Increased from 13
    
    # Add value count and percentage annotations inside the bars
    for i, container in enumerate(ax.containers):
        for j, bar in enumerate(container):
            count = bar.get_height()
            rate = attrition_data['Attrition Rate'].iloc[j]
            
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
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)
    
    # Get the 13th and 14th columns (indices 12 and 13)
    col13 = df.columns[12] if len(df.columns) > 12 else None
    col14 = df.columns[13] if len(df.columns) > 13 else None
    
    # Generate insights based on the data
    insights = ""
    
    # Check if we have the necessary columns
    if col13 and col14:
        # Find category with highest attrition rate
        try:
            total_employees = df[col13].sum() if not df[col13].empty else 0
            total_attrition = df[col14].sum() if not df[col14].empty else 0
            overall_rate = (total_attrition / total_employees) * 100 if total_employees > 0 else 0
            
            insights = f"The overall employee attrition rate across all {name} categories is {overall_rate:.1f}%. "
            
            # Add category-specific recommendations
            if name == "Education":
                insights += "Educational background appears to correlate with retention patterns, suggesting targeted retention strategies by education level."
            elif name == "Experience":
                insights += "Experience-based attrition patterns indicate tenure-specific retention strategies may be beneficial."
            elif name == "Age":
                insights += "Age-based attrition differences highlight potential for age-specific engagement initiatives."
            elif name == "Gender":
                insights += "Gender-based attrition disparities may inform diversity and inclusion strategy improvements."
        except Exception as e:
            insights = f"Analysis of attrition patterns across {name} categories reveals important retention trends. "
            insights += "Understanding these patterns can help develop targeted retention strategies and improve employee satisfaction."
    else:
        insights = f"Analysis of attrition patterns across {name} categories reveals important retention trends. "
        insights += "Understanding these patterns can help develop targeted retention strategies and improve employee satisfaction."
    
    return fig, insights
    
def create_average_residency_chart(df, name):
    """Create the average residency chart."""
    fig, ax = setup_chart_style()
    
    # Get the 15th and 16th columns (indices 14 and 15)
    col15 = df.columns[14] if len(df.columns) > 14 else None
    col16 = df.columns[15] if len(df.columns) > 15 else None

    # Check if we have the necessary columns
    if col15 is None or col16 is None:
        # Draw a simple placeholder chart with error message
        ax.text(0.5, 0.5, "Missing data columns for average residency analysis", 
                ha='center', va='center', fontsize=14, color='red')
        st.pyplot(fig, use_container_width=True)
        
        insights = f"Average residency analysis across {name} categories reveals important employee retention patterns. "
        insights += "The comparison between top performers and all employees provides valuable insights for talent development strategies."
        return fig, insights

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
        residency_data.loc[idx, 'Percentage Diff'] = ((row[col16_short] - row[col15_short]) / row[col15_short]) * 100 if row[col15_short] > 0 else 0

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
    ax.set_ylabel('Average Tenure (months)', labelpad=15)
    
    # Adding value labels inside each bar with increased font size (20% larger)
    base_fontsize = 16  # Increased from 13 (20% larger)
    for container_idx, container in enumerate(ax.containers):
        for bar_idx, bar in enumerate(container):
            height = bar.get_height()
            if height >= 1.0:  # Only add text if bar is tall enough
                ax.text(bar.get_x() + bar.get_width()/2, height/2,
                        f'{height:.2f}',
                        ha='center', va='center',
                        color='white', fontweight='bold', fontsize=base_fontsize)
    
    # Add horizontal line for overall average tenure for all employees
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
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)
    
    # Generate insights based on the data
    insights = ""
    
    # Check if we have the necessary columns
    if col15 and col16:
        try:
            # Calculate average tenure differences between top performers and all employees
            top_avg = df[col16].mean() if not df[col16].empty else 0
            all_avg = df[col15].mean() if not df[col15].empty else 0
            diff = top_avg - all_avg
            pct_diff = (diff / all_avg) * 100 if all_avg > 0 else 0
            
            # Generate insights
            insights = f"Top performers have on average {top_avg:.2f} months of tenure compared to {all_avg:.2f} months for all employees, "
            if diff > 0:
                insights += f"representing {pct_diff:.1f}% longer tenure for high performers. "
            else:
                insights += f"representing {abs(pct_diff):.1f}% shorter tenure for high performers. "
            
            # Add category-specific insights
            if name == "Education":
                insights += "Educational background appears to correlate with tenure patterns among top performers."
            elif name == "Experience":
                insights += "Experience levels show varying tenure patterns, suggesting experience-based development opportunities."
            elif name == "Age":
                insights += "Age-based tenure differences highlight opportunities for cross-generational mentoring and knowledge transfer."
            elif name == "Gender":
                insights += "Gender-based tenure variations may inform talent development strategies."
        except Exception as e:
            insights = f"Average residency analysis across {name} categories reveals important employee retention patterns. "
            insights += "The comparison between top performers and all employees provides valuable insights for talent development strategies."
    else:
        insights = f"Average residency analysis across {name} categories reveals important employee retention patterns. "
        insights += "The comparison between top performers and all employees provides valuable insights for talent development strategies."
    
    return fig, insights
    
def create_infant_attrition_chart(df, name):
    """Create the infant attrition chart."""
    fig, ax = setup_chart_style()
    
    # Get the last column (index 17)
    last_col = df.columns[-1] if len(df.columns) > 16 else None
    
    # Check if we have the necessary column
    if last_col is None:
        # Draw a simple placeholder chart with error message
        ax.text(0.5, 0.5, "Missing data column for infant attrition analysis", 
                ha='center', va='center', fontsize=14, color='red')
        st.pyplot(fig, use_container_width=True)
        
        insights = f"Infant attrition analysis across {name} categories reveals important early-stage retention patterns. "
        insights += "Understanding these patterns can help improve onboarding and initial employee engagement strategies."
        return fig, insights

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
    ax.set_ylabel('Attrition Rate (%)', labelpad=15)
    
    # Adding value labels inside the bars with increased font size (20% larger)
    base_fontsize = 16  # Increased from 13 (20% larger)
    for i, container in enumerate(ax.containers):
        for j, bar in enumerate(container):
            height = bar.get_height()
            if height >= 2.0:  # Only add text if bar is tall enough
                ax.text(bar.get_x() + bar.get_width()/2, height/2,
                        f'{height:.1f}%',
                        ha='center', va='center',
                        color='white', fontweight='bold', fontsize=base_fontsize)
    
    # Add a horizontal line for the average
    avg_attrition = infant_attrition_data['Infant Attrition'].mean()
    ax.axhline(y=avg_attrition, color='red', linestyle='--', alpha=0.7)
    
    # Find appropriate empty space for the average label
    # Move text to upper right corner of the chart
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
    
    # Generate insights based on the data
    insights = ""
    
    # Check if we have the necessary column
    if last_col:
        try:
            # Calculate average infant attrition
            avg_attrition = df[last_col].mean() * 100 if not df[last_col].empty else 0
            
            # Find categories with highest and lowest infant attrition
            highest_idx = df[last_col].idxmax() if not df[last_col].empty else 0
            lowest_idx = df[last_col].idxmin() if not df[last_col].empty else 0
            
            highest_category = df.loc[highest_idx, 'Category'] if highest_idx in df.index else ""
            highest_rate = df.loc[highest_idx, last_col] * 100 if highest_idx in df.index else 0
            
            lowest_category = df.loc[lowest_idx, 'Category'] if lowest_idx in df.index else ""
            lowest_rate = df.loc[lowest_idx, last_col] * 100 if lowest_idx in df.index else 0
            
            # Generate insights
            if highest_category and lowest_category:
                insights = f"The {highest_category} {name} category has the highest infant attrition rate at {highest_rate:.1f}%, "
                insights += f"while the {lowest_category} category has the lowest at {lowest_rate:.1f}%. "
                insights += f"The overall infant attrition average is {avg_attrition:.1f}% across all {name} categories. "
                
                # Add category-specific recommendations
                if name == "Education":
                    insights += "Educational background appears to impact early attrition, suggesting education-specific onboarding adjustments may be beneficial."
                elif name == "Experience":
                    insights += "Experience levels show varying early attrition patterns, highlighting opportunities to strengthen onboarding for specific experience groups."
                elif name == "Age":
                    insights += "Age-based early attrition differences suggest tailoring early employment support by age group."
                elif name == "Gender":
                    insights += "Gender-based early attrition disparities may inform improved orientation and early career development programs."
            else:
                insights = f"Infant attrition analysis across {name} categories reveals important early-stage retention patterns. "
                insights += "Understanding these patterns can help improve onboarding and initial employee engagement strategies."
        except Exception as e:
            insights = f"Infant attrition analysis across {name} categories reveals important early-stage retention patterns. "
            insights += "Understanding these patterns can help improve onboarding and initial employee engagement strategies."
    else:
        insights = f"Infant attrition analysis across {name} categories reveals important early-stage retention patterns. "
        insights += "Understanding these patterns can help improve onboarding and initial employee engagement strategies."
    
    return fig, insights
    
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
