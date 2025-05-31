import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys

# Set seaborn style
sns.set_theme(style="whitegrid")

@st.cache_data
def load_data():
    with st.spinner('Loading data from Aadhar_modified.xlsx...'):
        try:
            Gender = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Gender')
            Education = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Education')
            Experience = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Experience')
            Age = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Age')
            return Gender, Education, Experience, Age
        except FileNotFoundError:
            st.error("The file Aadhar_modified.xlsx was not found.")
            st.stop()
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.exception(e)  # This will display the full traceback

# ...existing code...

def main():    # Set page configuration
    st.set_page_config(
        layout="wide",
        page_title="Aadhar Analysis Dashboard",
        page_icon="📊"
    )
    st.markdown("<h1 style='text-align: center; font-weight: 800; color: #0047AB; margin-bottom: 30px; font-size: 46px;'>Aadhar Analysis Dashboard</h1>", unsafe_allow_html=True)

    # Load data
    Gender, Education, Experience, Age = load_data()
    
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
                    
def create_dashboard(df, name):
    """Create a dashboard visualization for the given dataframe in Streamlit."""
    st.markdown(f"<h1 style='text-align: center; font-weight: 700; color: #1E3A8A;'>{name} Analysis Dashboard</h1>", unsafe_allow_html=True)
    
    # Show information about the data
    st.markdown(f"<h3 style='text-align: center;'>Dataset contains {len(df)} rows</h3>", unsafe_allow_html=True)
    
    # Enable user to select which charts to display
    selected_charts = st.multiselect(
        'Select charts to display:',
        ['Distribution', 'KPI Performance', 'Performance Multiple', 
         'Top vs Bottom Performers', 'Time to First Sale', 'CAR2CATPO Ratio',
         'Attrition Count', 'Average Residency', 'Infant Attrition'],
        default=['Distribution', 'KPI Performance', 'Performance Multiple']
    )
    
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
    
    # Create 3-column layout for charts
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3] * 3  # Repeat columns for 9 charts
      # Display the selected charts
    for i, chart_name in enumerate(selected_charts):
        with columns[i % 3]:
            try:
                with st.container():
                    st.markdown(f"<h2 style='text-align: center; font-weight: 600; color: #333; background-color: #f0f2f6; padding: 10px; border-radius: 5px;'>{chart_name}</h2>", unsafe_allow_html=True)
                    chart_functions[chart_name](df, name)
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
        df_melted.loc[df_melted['Metric'] == metric, 'Percentage'] = df_melted.loc[df_melted['Metric'] == metric, 'Count'] / total * 100    # Using seaborn barplot with grouped bars and better colors
    bars = sns.barplot(x='Category', y='Count', hue='Metric', 
                      data=df_melted, 
                      palette=['#1f77b4', '#9ecae1'], 
                      ax=ax)

    ax.set_title(f'{name} Distribution by Cohort', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('Head Count', labelpad=15)    # Adding value labels and percentages on top of each bar with larger font size
    for container_idx, container in enumerate(ax.containers):
        labels = []
        for bar_idx, bar in enumerate(container):
            count = bar.get_height()
            percentage = df_melted.iloc[container_idx*2+bar_idx if container_idx < 2 else bar_idx]['Percentage']
            labels.append(f'{int(count)}\n({percentage:.1f}%)')
        ax.bar_label(container, labels=labels, padding=10, fontsize=14, fontweight='bold')

    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust legend with better styling
    legend = ax.legend(title='Cohort Type', fontsize=14)
    plt.setp(legend.get_title(), fontsize=16, fontweight='bold')
    
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
    col8_short = "Cumulative KPI 1"

    # Create a DataFrame with the data and specified columns
    kpi_data = pd.DataFrame({
        'Category': df['Category'],
        col4_short: df[col4],
        col8_short: df[col8]
    })

    # Reshape data for seaborn
    kpi_melted = pd.melt(kpi_data, 
                         id_vars=['Category'], 
                         value_vars=[col4_short, col8_short],
                         var_name='KPI Type', 
                         value_name='Achievement %')    # Using seaborn barplot with grouped bars
    bars = sns.barplot(x='Category', y='Achievement %', hue='KPI Type', 
                      data=kpi_melted, 
                      palette=['#ff7f0e', '#ff9e4a'], 
                      ax=ax)

    ax.set_title(f'KPI Performance by {name} CAP LRM', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('Achievement %', labelpad=15)    # Adding value labels on top of each bar with larger font size
    for container_idx, container in enumerate(ax.containers):
        labels = []
        for bar in container:
            height = bar.get_height()
            labels.append(f'{height:.2f}%')
        ax.bar_label(container, labels=labels, padding=10, fontsize=14, fontweight='bold')

    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust legend with better styling
    legend = ax.legend(title='Performance Metric', fontsize=14)
    plt.setp(legend.get_title(), fontsize=16, fontweight='bold')
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)

# Helper function to setup consistent chart styling
def setup_chart_style():
    """Set up consistent styling for all charts."""
    # Set global font size and weight
    plt.rcParams.update({
        'font.size': 14,
        'font.weight': 'bold',
        'axes.titlesize': 18,
        'axes.titleweight': 'bold',
        'axes.labelsize': 16,
        'axes.labelweight': 'bold',
        'xtick.labelsize': 14,
        'ytick.labelsize': 14
    })
    
    # Create larger figure
    fig, ax = plt.subplots(figsize=(14, 9))
    return fig, ax

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
                          value_name='Multiple')    # Using seaborn barplot with grouped bars
    bars = sns.barplot(x='Category', y='Multiple', hue='Performance Type', 
                      data=perf_melted, 
                      palette=['#2ca02c', '#98df8a'], 
                      ax=ax)

    ax.set_title(f'Performance Multiple by {name}', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('Multiple Value', labelpad=15)    # Adding value labels on top of each bar with larger font size
    for container_idx, container in enumerate(ax.containers):
        labels = []
        for bar in container:
            height = bar.get_height()
            labels.append(f'{height:.1f}x')
        ax.bar_label(container, labels=labels, padding=10, fontsize=14, fontweight='bold')

    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust legend with better styling
    legend = ax.legend(title='Multiple Type', fontsize=14)
    plt.setp(legend.get_title(), fontsize=16, fontweight='bold')
    
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
    all_performers = pd.concat([top_performers, bottom_performers], ignore_index=True)    # Using seaborn barplot with grouped bars with enhanced colors
    bars = sns.barplot(x='Category', y='Value', hue='Performance', 
                      data=all_performers, 
                      palette=['#9467bd', '#d8b2ff'],
                      ax=ax)

    ax.set_title(f'Top vs Bottom Performers by {name}', pad=20)
    ax.set_xlabel(f'{name}', labelpad=15)
    ax.set_ylabel('CAP Value', labelpad=15)    # Adding value labels on top of each bar with larger font
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f', padding=10, fontsize=14, fontweight='bold')

    # Enhance grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust legend with better styling
    legend = ax.legend(title='Performance Group', fontsize=14)
    plt.setp(legend.get_title(), fontsize=16, fontweight='bold')
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    # Add more padding around figure
    plt.tight_layout(pad=3.0)
    
    # Use full width in Streamlit
    st.pyplot(fig, use_container_width=True)

def create_time_to_first_sale_chart(df, name):
    """Create the time to first sale chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
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
                      hue='Category', palette=palette, legend=False, ax=ax)

    ax.set_title(f'Time to Make First Sale by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Time (months)')

    # Adding value labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f months', padding=5)

    # Add a horizontal line for the average
    avg_time = df[col12].mean()
    ax.axhline(y=avg_time, color='red', linestyle='--', alpha=0.7)
    ax.text(ax.get_xlim()[1] * 0.6, avg_time * 1.02, f'Avg: {avg_time:.2f} months', 
            color='red', ha='center', va='bottom')
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    plt.tight_layout()
    st.pyplot(fig)

def create_car2catpo_ratio_chart(df, name):
    """Create the CAR2CATPO ratio chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
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
                      hue='Category', palette=palette, legend=False, ax=ax)

    ax.set_title(f'CAR2CATPO Ratio by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Ratio Value')

    # Adding value labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=5)

    # Add a horizontal line for the average
    avg_ratio = df[col13].mean()
    ax.axhline(y=avg_ratio, color='red', linestyle='--', alpha=0.7)
    ax.text(ax.get_xlim()[1] * 0.6, avg_ratio * 1.02, f'Avg: {avg_ratio:.2f}', 
            color='red', ha='center', va='bottom')
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    plt.tight_layout()
    st.pyplot(fig)

def create_attrition_count_chart(df, name):
    """Create the attrition count chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
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
                      hue='Category', palette=palette, legend=False, ax=ax)

    ax.set_title(f'Employee Attrition by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Number of Attrited Employees')

    # Adding value labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%d', padding=5)

    # Calculate and display attrition percentages
    total_per_category = df['CAP LRM cohort'].values
    attrition_per_category = df[col14].values
    attrition_rates = attrition_per_category / total_per_category * 100

    # Add percentage annotations
    for ann_idx, (count, rate) in enumerate(zip(attrition_per_category, attrition_rates)):
        ax.text(ann_idx, count/2, f'{rate:.1f}%', 
                ha='center', va='center', color='white', fontweight='bold')
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    plt.tight_layout()
    st.pyplot(fig)

def create_average_residency_chart(df, name):
    """Create the average residency chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
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
                      ax=ax)

    ax.set_title(f'Employment Tenure by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Average Tenure (months)')

    # Adding value labels on top of each bar
    for container_idx, container in enumerate(ax.containers):
        labels = []
        for bar_idx, bar in enumerate(container):
            height = bar.get_height()
            labels.append(f'{height:.2f}')
        ax.bar_label(container, labels=labels, padding=5)

    # Add horizontal line for overall average tenure for all employees
    overall_avg = df[col15].mean()
    ax.axhline(y=overall_avg, color='red', linestyle='--', alpha=0.7)
    ax.text(ax.get_xlim()[1] * 0.7, overall_avg * 0.95, f'Org avg: {overall_avg:.2f}', 
            color='red', ha='center', va='bottom', fontsize=9)

    # Adjust legend with better positioning
    ax.legend(title='Employee Group', loc='upper right')
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    plt.tight_layout()
    st.pyplot(fig)

def create_infant_attrition_chart(df, name):
    """Create the infant attrition chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
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
                      hue='Category', palette=palette, legend=False, ax=ax)

    ax.set_title(f'Infant Attrition Rate by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Attrition Rate (%)')

    # Adding value labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=5)

    # Add a horizontal line for the average
    avg_attrition = infant_attrition_data['Infant Attrition'].mean()
    ax.axhline(y=avg_attrition, color='red', linestyle='--', alpha=0.7)
    ax.text(ax.get_xlim()[1] * 0.6, avg_attrition * 1.02, f'Avg: {avg_attrition:.1f}%', 
            color='red', ha='center', va='bottom')
    
    # Rotate x-axis labels for Education dashboard
    if name == "Education":
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
    plt.tight_layout()
    st.pyplot(fig)

if __name__ == "__main__":
    main()
