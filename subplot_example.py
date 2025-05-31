import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set seaborn style
sns.set_theme(style="whitegrid")

Gender = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Gender')
Education = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Education')
Experience = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Experience')
Age = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Age')


# Create a figure with a 3x3 grid of subplots
fig, axes = plt.subplots(3, 3, figsize=(15, 12))

# Add a main title to the entire figure
fig.suptitle('Aadhar Gender Analysis Dashboard', fontsize=16, fontweight='bold', y=0.98)

# Initialize all subplots with empty charts and labels
for i in range(3):
    for j in range(3):
        ax = axes[i, j]
        ax.set_title(f'Plot {i+1},{j+1}')
        ax.grid(True)
        
# Now we'll add charts one by one
# Chart 1: Gender Distribution (first 3 columns) using Seaborn
ax = axes[0, 0]

# Extract the first 3 columns
first_cols = Gender.columns[:3]
# Reshape data for seaborn
gender_melted = pd.melt(Gender, 
                        id_vars=[first_cols[0]], 
                        value_vars=[first_cols[1], first_cols[2]], 
                        var_name='Metric', 
                        value_name='Count')

# Calculate percentages for each cohort
for metric in [first_cols[1], first_cols[2]]:
    total = Gender[metric].sum()
    gender_melted.loc[gender_melted['Metric'] == metric, 'Percentage'] = gender_melted.loc[gender_melted['Metric'] == metric, 'Count'] / total * 100

# Using seaborn barplot with grouped bars
bars = sns.barplot(x='Category', y='Count', hue='Metric', 
                  data=gender_melted, 
                  palette=['blue', 'lightblue'], 
                  ax=ax)

ax.set_title('Gender Distribution by Cohort')
ax.set_xlabel('Gender')
ax.set_ylabel('Head Count')

# Adding value labels and percentages on top of each bar
for i, container in enumerate(ax.containers):
    labels = []
    for j, bar in enumerate(container):
        count = bar.get_height()
        percentage = gender_melted.iloc[i*2+j if i < 2 else j]['Percentage']
        labels.append(f'{int(count)}\n({percentage:.1f}%)')
    ax.bar_label(container, labels=labels, padding=5)

# Adjust legend
ax.legend(title='Cohort Type')

# Chart 2: KPI Performance by Gender (top-middle)
ax = axes[0, 1]

# Get the 4th and 8th columns (indices 3 and 7)
col4 = Gender.columns[3]
col8 = Gender.columns[7]

# Create shorter column names for display
col4_short = "Cumulative Combined KPI"
col8_short = "Cumulative KPI 1"

# Create a DataFrame with the gender data and specified columns
kpi_data = pd.DataFrame({
    'Category': Gender['Category'],
    col4_short: Gender[col4],
    col8_short: Gender[col8]
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

ax.set_title('KPI Performance by Gender CAP LRM')
ax.set_xlabel('Gender')
ax.set_ylabel('Achievement %')

# Adding value labels on top of each bar
for i, container in enumerate(ax.containers):
    labels = []
    for bar in container:
        height = bar.get_height()
        labels.append(f'{height:.2f}%')
    ax.bar_label(container, labels=labels, padding=5)

# Adjust legend
ax.legend(title='Performance Metric')

# Chart 3: Performance Multiple by Gender (top-right)
ax = axes[0, 2]

# Get the 7th and 11th columns (indices 6 and 10)
col7 = Gender.columns[6]
col11 = Gender.columns[10]

# Create shorter column names for display
col7_short = "Performance Multiple KPI Combined"
col11_short = "Performance Multiple KPI 1"

# Create a DataFrame with the gender data and specified columns
perf_data = pd.DataFrame({
    'Category': Gender['Category'],
    col7_short: Gender[col7],
    col11_short: Gender[col11]
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

ax.set_title('Performance Multiple by Gender')
ax.set_xlabel('Gender')
ax.set_ylabel('Multiple Value')

# Adding value labels on top of each bar
for i, container in enumerate(ax.containers):
    labels = []
    for bar in container:
        height = bar.get_height()
        labels.append(f'{height:.1f}x')
    ax.bar_label(container, labels=labels, padding=5)

# Adjust legend
ax.legend(title='Multiple Type')

# Chart 4: Top and Bottom Performers (middle-left) using Seaborn
ax = axes[1, 0]

# Get the 5th, 6th, 9th and 10th columns (indices 4, 5, 8, 9)
col5 = Gender.columns[4]  # Top performers Combined KPI
col6 = Gender.columns[5]  # Bottom performers Combined KPI
col9 = Gender.columns[8]  # Top performers KPI 1
col10 = Gender.columns[9]  # Bottom performers KPI 1

# Create shorter column names for display
col5_short = "Top 10% (Combined)"
col6_short = "Bottom 10% (Combined)" 
col9_short = "Top 10% (KPI 1)"
col10_short = "Bottom 10% (KPI 1)"

# Create a DataFrame with the gender data and specified columns
performer_data = pd.DataFrame({
    'Category': Gender['Category'],
    col5_short: Gender[col5],
    col6_short: Gender[col6],
    col9_short: Gender[col9],
    col10_short: Gender[col10]
})

# Reshape data for seaborn - first combine top performers
top_performers = pd.melt(performer_data, 
                     id_vars=['Category'], 
                     value_vars=[col5_short, col9_short],
                     var_name='KPI Type', 
                     value_name='Value')
top_performers['Performance'] = 'Top 10%'

# Then combine bottom performers
bottom_performers = pd.melt(performer_data, 
                     id_vars=['Category'], 
                     value_vars=[col6_short, col10_short],
                     var_name='KPI Type', 
                     value_name='Value')
bottom_performers['Performance'] = 'Bottom 10%'

# Combine both datasets
all_performers = pd.concat([top_performers, bottom_performers])

# Using seaborn barplot with grouped bars
bars = sns.barplot(x='Category', y='Value', hue='Performance', 
                  data=all_performers, 
                  palette=['purple', 'lavender'],
                  ax=ax)

ax.set_title('Top vs Bottom Performers by Gender')
ax.set_xlabel('Gender')
ax.set_ylabel('CAP Value')

# Adding value labels on top of each bar
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f', padding=5)

# Adjust legend
ax.legend(title='Performance Group')

# Chart 5: Time to First Sale by Gender (middle-center) using Seaborn
ax = axes[1, 1]

# Get the 12th column (index 11)
col12 = Gender.columns[11]

# Create a DataFrame for the chart
first_sale_data = pd.DataFrame({
    'Category': Gender['Category'],
    'Time to First Sale': Gender[col12]
})

# Using seaborn barplot (fixed deprecation warning)
bars = sns.barplot(x='Category', y='Time to First Sale', data=first_sale_data, 
                  hue='Category', palette=['teal', 'lightseagreen'], legend=False, ax=ax)

ax.set_title('Time to Make First Sale by Gender')
ax.set_xlabel('Gender')
ax.set_ylabel('Time (months)')

# Adding value labels on top of each bar
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f months', padding=5)

# Add a horizontal line for the average
avg_time = Gender[col12].mean()
ax.axhline(y=avg_time, color='red', linestyle='--', alpha=0.7)
ax.text(ax.get_xlim()[1] * 0.6, avg_time * 1.02, f'Avg: {avg_time:.2f} months', 
        color='red', ha='center', va='bottom')

# Chart 6: CAR2CATPO Ratio by Gender (middle-right)
ax = axes[1, 2]

# Get the 13th column (index 12)
col13 = Gender.columns[12]

# Create a DataFrame for the chart
ratio_data = pd.DataFrame({
    'Category': Gender['Category'],
    'CAR2CATPO Ratio': Gender[col13]
})

# Using seaborn barplot (fixed deprecation warning)
bars = sns.barplot(x='Category', y='CAR2CATPO Ratio', data=ratio_data, 
                  hue='Category', palette=['darkgreen', 'mediumseagreen'], legend=False, ax=ax)

ax.set_title('CAR2CATPO Ratio by Gender')
ax.set_xlabel('Gender')
ax.set_ylabel('Ratio Value')

# Adding value labels on top of each bar
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f', padding=5)

# Add a horizontal line for the average
avg_ratio = Gender[col13].mean()
ax.axhline(y=avg_ratio, color='red', linestyle='--', alpha=0.7)
ax.text(ax.get_xlim()[1] * 0.6, avg_ratio * 1.02, f'Avg: {avg_ratio:.2f}', 
        color='red', ha='center', va='bottom')

# Chart 7: Attrition Count by Gender (bottom-left) using Seaborn
ax = axes[2, 0]

# Get the 14th column (index 13)
col14 = Gender.columns[13]

# Create a DataFrame for the chart
attrition_data = pd.DataFrame({
    'Category': Gender['Category'],
    'Attrited Employees': Gender[col14]
})

# Using seaborn barplot (fixed deprecation warning)
bars = sns.barplot(x='Category', y='Attrited Employees', data=attrition_data, 
                  hue='Category', palette=['crimson', 'lightcoral'], legend=False, ax=ax)

ax.set_title('Employee Attrition by Gender')
ax.set_xlabel('Gender')
ax.set_ylabel('Number of Attrited Employees')

# Adding value labels on top of each bar
for container in ax.containers:
    ax.bar_label(container, fmt='%d', padding=5)

# Calculate and display attrition percentages
total_per_gender = Gender['CAP LRM cohort'].values
attrition_per_gender = Gender[col14].values
attrition_rates = attrition_per_gender / total_per_gender * 100

# Add percentage annotations
for i, (count, rate) in enumerate(zip(attrition_per_gender, attrition_rates)):
    ax.text(i, count/2, f'{rate:.1f}%', 
            ha='center', va='center', color='white', fontweight='bold')

# Chart 8: Average Residency by Gender (bottom-middle) using Seaborn
ax = axes[2, 1]

# Get the 15th and 16th columns (indices 14 and 15)
col15 = Gender.columns[14]  # Average Residency of all employees
col16 = Gender.columns[15]  # Average Residency of TOP 100 employees

# Create shorter column names for display
col15_short = "All Employees"
col16_short = "Top 100 Performers"

# Create a DataFrame for the chart
residency_data = pd.DataFrame({
    'Category': Gender['Category'],
    col15_short: Gender[col15],
    col16_short: Gender[col16]
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

ax.set_title('Employment Tenure by Gender', fontsize=11, fontweight='bold')
ax.set_xlabel('Gender')
ax.set_ylabel('Average Tenure (months)')

# Adding value labels on top of each bar
for i, container in enumerate(ax.containers):
    labels = []
    for j, bar in enumerate(container):
        height = bar.get_height()
        labels.append(f'{height:.2f}')
    ax.bar_label(container, labels=labels, padding=5)

# Add horizontal line for overall average tenure for all employees
overall_avg = Gender[col15].mean()
ax.axhline(y=overall_avg, color='red', linestyle='--', alpha=0.7)
ax.text(ax.get_xlim()[1] * 0.7, overall_avg * 0.95, f'Org avg: {overall_avg:.2f}', 
        color='red', ha='center', va='bottom', fontsize=9)

# Add percentage difference annotations with improved styling
for i, gender in enumerate(residency_data['Category']):
    diff_pct = residency_data.loc[residency_data['Category'] == gender, 'Percentage Diff'].values[0]
    top_val = residency_data.loc[residency_data['Category'] == gender, col16_short].values[0]
    # Add an arrow showing the increase from general to top performers
    ax.annotate(f'+{diff_pct:.1f}%', 
                xy=(i, top_val), 
                xytext=(i, top_val + 0.6),
                ha='center', 
                va='bottom',
                color='darkgreen', 
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', fc='honeydew', ec='green', alpha=0.7))

# Add business insight annotation
if residency_data.loc[0, col15_short] > residency_data.loc[1, col15_short]:
    gender_diff = residency_data.loc[0, col15_short] - residency_data.loc[1, col15_short]
    higher_gender = residency_data.loc[0, 'Category']
    lower_gender = residency_data.loc[1, 'Category']
else:
    gender_diff = residency_data.loc[1, col15_short] - residency_data.loc[0, col15_short]
    higher_gender = residency_data.loc[1, 'Category']
    lower_gender = residency_data.loc[0, 'Category']

gender_diff_pct = (gender_diff / residency_data.loc[residency_data['Category'] == lower_gender, col15_short].values[0]) * 100

ax.text(0.5, 0.02, 
        f"{higher_gender}s stay {gender_diff_pct:.1f}% longer than {lower_gender}s",
        transform=ax.transAxes, ha='center', fontsize=9, fontstyle='italic', 
        bbox=dict(facecolor='lightyellow', alpha=0.5, boxstyle='round,pad=0.5'))

# Adjust legend with better positioning
ax.legend(title='Employee Group', loc='upper right')

# Chart 9: Infant Attrition by Gender (bottom-right) using Seaborn
ax = axes[2, 2]

# Get the last column (index 17)
last_col = Gender.columns[-1]  # Using -1 to access the last column

# Create a DataFrame for the chart with a shorter column name for display
infant_attrition_data = pd.DataFrame({
    'Category': Gender['Category'],
    'Infant Attrition': Gender[last_col] * 100  # Convert to percentage
})

# Using seaborn barplot (fixed deprecation warning)
bars = sns.barplot(x='Category', y='Infant Attrition', data=infant_attrition_data, 
                  hue='Category', palette=['darkblue', 'royalblue'], legend=False, ax=ax)

ax.set_title('Infant Attrition Rate by Gender')
ax.set_xlabel('Gender')
ax.set_ylabel('Attrition Rate (%)')

# Adding value labels on top of each bar
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', padding=5)

# Add a horizontal line for the average
avg_attrition = infant_attrition_data['Infant Attrition'].mean()
ax.axhline(y=avg_attrition, color='red', linestyle='--', alpha=0.7)
ax.text(ax.get_xlim()[1] * 0.6, avg_attrition * 1.02, f'Avg: {avg_attrition:.1f}%', 
        color='red', ha='center', va='bottom')

# Adjust layout to prevent overlapping with more space for the title
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Add a subtle watermark with the date
fig.text(0.99, 0.01, f'Generated: May 31, 2025', fontsize=8, color='gray', 
         ha='right', va='bottom', alpha=0.7)

# Show the plot
plt.show()

# Save the figure with higher resolution
plt.savefig('gender_dashboard.png', dpi=300, bbox_inches='tight')
print("Dashboard saved as 'gender_dashboard.png'")
