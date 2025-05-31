import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys

# Set seaborn style
sns.set_theme(style="whitegrid")

def main():
    # Load all dataframes
    print("Loading data from HDFC_modified.xlsx...")
    Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')
    Education = pd.read_excel('HDFC_modified.xlsx', sheet_name='Education')
    Experience = pd.read_excel('HDFC_modified.xlsx', sheet_name='Experience')
    Age = pd.read_excel('HDFC_modified.xlsx', sheet_name='Age')
    
    # Create list of dataframes with their display names
    all_dataframes = [
        {"df": Gender, "name": "Gender"},
        {"df": Education, "name": "Education"},
        {"df": Experience, "name": "Experience"},
        {"df": Age, "name": "Age"}
    ]
    
    # Check command line arguments
    if len(sys.argv) > 1:
        # Filter dataframes based on command line arguments
        requested_categories = [arg.lower() for arg in sys.argv[1:]]
        dataframes = [df for df in all_dataframes if df["name"].lower() in requested_categories]
        
        if not dataframes:
            print("No valid categories specified. Available categories: gender, education, experience, age")
            print("Usage: python dashboards.py [category1] [category2] ...")
            return
    else:
        # No arguments - process all dataframes
        dataframes = all_dataframes
        print("Generating dashboards for all categories: Gender, Education, Experience, Age")
    
    # Process each selected dataframe
    for data in dataframes:
        create_dashboard(data["df"], data["name"])

    print("All requested dashboards created successfully!")

def create_dashboard(df, name):
    """Create a dashboard visualization for the given dataframe."""
    print(f"Creating dashboard for {name}...")
    
    # Create a figure with a 3x3 grid of subplots
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))

    # Add a main title to the entire figure
    fig.suptitle(f'HDFC {name} Analysis Dashboard', fontsize=16, fontweight='bold', y=0.98)

    # Initialize all subplots with empty charts and labels
    for row in range(3):
        for col in range(3):
            ax = axes[row, col]
            ax.set_title(f'Plot {row+1},{col+1}')
            ax.grid(True)
    
    # Flag to check if we need to rotate x-axis labels (for Education dashboard)
    rotate_xlabels = (name == "Education")
            
    # Chart 1: Distribution (first 3 columns) using Seaborn
    ax = axes[0, 0]

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

    # Using seaborn barplot with grouped bars
    bars = sns.barplot(x='Category', y='Count', hue='Metric', 
                      data=df_melted, 
                      palette=['blue', 'lightblue'], 
                      ax=ax)

    ax.set_title(f'{name} Distribution by Cohort')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Head Count')

    # Adding value labels and percentages on top of each bar
    for container_idx, container in enumerate(ax.containers):
        labels = []
        for bar_idx, bar in enumerate(container):
            count = bar.get_height()
            percentage = df_melted.iloc[container_idx*2+bar_idx if container_idx < 2 else bar_idx]['Percentage']
            labels.append(f'{int(count)}\n({percentage:.1f}%)')
        ax.bar_label(container, labels=labels, padding=5)

    # Adjust legend
    ax.legend(title='Cohort Type')
    
    # Rotate x-axis labels for Education dashboard
    if rotate_xlabels:
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Chart 2: KPI Performance (top-middle)
    ax = axes[0, 1]

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
                         value_name='Achievement %')

    # Using seaborn barplot with grouped bars
    bars = sns.barplot(x='Category', y='Achievement %', hue='KPI Type', 
                      data=kpi_melted, 
                      palette=['orange', 'coral'], 
                      ax=ax)

    ax.set_title(f'KPI Performance by {name} CAP LRM')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Achievement %')

    # Adding value labels on top of each bar
    for container_idx, container in enumerate(ax.containers):
        labels = []
        for bar in container:
            height = bar.get_height()
            labels.append(f'{height:.2f}%')
        ax.bar_label(container, labels=labels, padding=5)

    # Adjust legend
    ax.legend(title='Performance Metric')
    
    # Rotate x-axis labels for Education dashboard
    if rotate_xlabels:
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Chart 3: Performance Multiple (top-right)
    ax = axes[0, 2]

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
                      palette=['green', 'lightgreen'], 
                      ax=ax)

    ax.set_title(f'Performance Multiple by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('Multiple Value')

    # Adding value labels on top of each bar
    for container_idx, container in enumerate(ax.containers):
        labels = []
        for bar in container:
            height = bar.get_height()
            labels.append(f'{height:.1f}x')
        ax.bar_label(container, labels=labels, padding=5)

    # Adjust legend
    ax.legend(title='Multiple Type')
    
    # Rotate x-axis labels for Education dashboard
    if rotate_xlabels:
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Chart 4: Top and Bottom Performers (middle-left) using Seaborn
    ax = axes[1, 0]

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

    # Using seaborn barplot with grouped bars
    bars = sns.barplot(x='Category', y='Value', hue='Performance', 
                      data=all_performers, 
                      palette=['purple', 'lavender'],
                      ax=ax)

    ax.set_title(f'Top vs Bottom Performers by {name}')
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('CAP Value')

    # Adding value labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f', padding=5)

    # Adjust legend
    ax.legend(title='Performance Group')
    
    # Rotate x-axis labels for Education dashboard
    if rotate_xlabels:
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Chart 5: Time to First Sale (middle-center) using Seaborn
    ax = axes[1, 1]

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
    if rotate_xlabels:
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Chart 6: CAR2CATPO Ratio (middle-right)
    ax = axes[1, 2]

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
    if rotate_xlabels:
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Chart 7: Attrition Count (bottom-left) using Seaborn
    ax = axes[2, 0]

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
    if rotate_xlabels:
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Chart 8: Average Residency (bottom-middle) using Seaborn
    ax = axes[2, 1]

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

    ax.set_title(f'Employment Tenure by {name}', fontsize=11, fontweight='bold')
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

    # Add percentage difference annotations with improved styling
    for point_idx, category_value in enumerate(residency_data['Category']):
        diff_pct = residency_data.loc[residency_data['Category'] == category_value, 'Percentage Diff'].values[0]
        top_val = residency_data.loc[residency_data['Category'] == category_value, col16_short].values[0]
        # Add an arrow showing the increase from general to top performers
        ax.annotate(f'+{diff_pct:.1f}%', 
                    xy=(point_idx, top_val), 
                    xytext=(point_idx, top_val + 0.6),
                    ha='center', 
                    va='bottom',
                    color='darkgreen', 
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', fc='honeydew', ec='green', alpha=0.7))

    # Add business insight annotation
    if len(residency_data) >= 2:  # Make sure there are at least 2 categories to compare
        # Find the category with highest tenure
        max_idx = residency_data[col15_short].idxmax()
        min_idx = residency_data[col15_short].idxmin()
        
        if max_idx != min_idx:  # Make sure there are different values
            higher_category = residency_data.loc[max_idx, 'Category'] 
            lower_category = residency_data.loc[min_idx, 'Category']
            cat_diff = residency_data.loc[max_idx, col15_short] - residency_data.loc[min_idx, col15_short]
            cat_diff_pct = (cat_diff / residency_data.loc[min_idx, col15_short]) * 100
            
            # For certain categories like Education or Age, we might need to customize pluralization
            suffix = ""
            if name == "Gender":
                suffix = "s"
            
            ax.text(0.5, 0.02, 
                    f"{higher_category}{suffix} stay {cat_diff_pct:.1f}% longer than {lower_category}{suffix}",
                    transform=ax.transAxes, ha='center', fontsize=9, fontstyle='italic', 
                    bbox=dict(facecolor='lightyellow', alpha=0.5, boxstyle='round,pad=0.5'))

    # Adjust legend with better positioning
    ax.legend(title='Employee Group', loc='upper right')
    
    # Rotate x-axis labels for Education dashboard
    if rotate_xlabels:
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Chart 9: Infant Attrition (bottom-right) using Seaborn
    ax = axes[2, 2]

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
    if rotate_xlabels:
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Adjust layout to prevent overlapping with more space for the title
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Add a subtle watermark with the date
    fig.text(0.99, 0.01, f'Generated: May 31, 2025', fontsize=8, color='gray', 
             ha='right', va='bottom', alpha=0.7)

    # Save the figure with higher resolution
    output_filename = f'{name.lower()}_dashboard.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Dashboard saved as '{output_filename}'")
    
    # Show the plot (comment this out if you don't want to display each plot)
    plt.show()

if __name__ == "__main__":
    main()
