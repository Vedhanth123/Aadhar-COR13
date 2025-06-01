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
        
    else:
        # Identify top and bottom performers
        insights = f"The {kpi_data.loc[highest_combined_idx, 'Category']} {name} category has the highest combined KPI achievement at {kpi_data.loc[highest_combined_idx, col4_short]:.1f}%, "
        insights += f"while {kpi_data.loc[lowest_combined_idx, 'Category']} has the lowest at {kpi_data.loc[lowest_combined_idx, col4_short]:.1f}%. "
        
        # Note any significant gaps
        perf_gap = kpi_data.loc[highest_combined_idx, col4_short] - kpi_data.loc[lowest_combined_idx, col4_short]
        if perf_gap > 10:
            insights += f"There's a notable {perf_gap:.1f}% gap between the highest and lowest performing {name} categories."
    
    return fig, insights

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
    
    # Find the category with the highest performance multiple
    highest_combined_idx = perf_data[col7_short].idxmax()
    highest_combined_cat = perf_data.loc[highest_combined_idx, 'Category']
    highest_combined_val = perf_data.loc[highest_combined_idx, col7_short]
    
    # Find the category with the lowest performance multiple
    lowest_combined_idx = perf_data[col7_short].idxmin()
    lowest_combined_cat = perf_data.loc[lowest_combined_idx, 'Category']
    lowest_combined_val = perf_data.loc[lowest_combined_idx, col7_short]
    
    # Calculate average multiples
    avg_combined = perf_data[col7_short].mean()
    avg_kpi1 = perf_data[col11_short].mean()
    
    # Generate insights
    insights = f"The {highest_combined_cat} {name} category shows the highest performance multiple at {highest_combined_val:.1f}x, "
    insights += f"while {lowest_combined_cat} shows the lowest at {lowest_combined_val:.1f}x. "
    
    # Add insight about the relationship between the two KPI multiples
    if avg_combined > avg_kpi1:
        insights += f"Overall, the Combined KPI multiple ({avg_combined:.1f}x) is higher than the KPI 1 multiple ({avg_kpi1:.1f}x), "
        insights += "indicating stronger collective performance versus individual metrics."
    else:
        insights += f"Overall, the KPI 1 multiple ({avg_kpi1:.1f}x) is higher than the Combined KPI multiple ({avg_combined:.1f}x), "
        insights += "suggesting individual metrics are stronger than collective performance."
    
    return fig, insights

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
    
    # Generate insights based on the data
    insights = ""
    
    # Calculate the gap between top and bottom performers
    top_combined = performer_data[col5_short].mean()
    bottom_combined = performer_data[col6_short].mean()
    performance_gap = top_combined - bottom_combined
    
    # Find categories with the biggest gap
    performer_data['Gap'] = performer_data[col5_short] - performer_data[col6_short]
    max_gap_idx = performer_data['Gap'].idxmax()
    max_gap_category = performer_data.loc[max_gap_idx, 'Category']
    max_gap_value = performer_data.loc[max_gap_idx, 'Gap']
    
    # Generate insights
    insights = f"Across all {name} categories, there is an average {performance_gap:.1f} point gap between top and bottom performers. "
    insights += f"The {max_gap_category} category shows the largest disparity with a {max_gap_value:.1f} point difference between top and bottom performers. "
    
    # Add specific insight based on the category type
    if name == "Education":
        insights += "Education level appears to correlate with performance variations, suggesting targeted development may benefit specific education groups."
    elif name == "Experience":
        insights += "Experience levels show significant performance variations, highlighting the importance of tenure-based skill development."
    elif name == "Age":
        insights += "Age-based performance variations indicate potential for targeted coaching across different generational groups."
    elif name == "Gender":
        insights += "Gender-based performance analysis shows important variations that may inform diversity and inclusion initiatives."
    
    return fig, insights

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
    ax.set_ylabel('Time (months)', labelpad=15)
    
    # Adding value labels inside each bar with increased font size (20% larger)
    base_fontsize = 16  # Increased from 13 (20% larger)
    for i, container in enumerate(ax.containers):
        for j, bar in enumerate(container):
            height = bar.get_height()
            if height >= 0.5:  # Only add text if bar is tall enough
                ax.text(bar.get_x() + bar.get_width()/2, height/2,
                        f'{height:.2f} months',
                        ha='center', va='center',
                        color='white', fontweight='bold', fontsize=base_fontsize)
    
    # Add a horizontal line for the average with larger font size
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
    
    # Generate insights based on the data
    insights = ""
    
    # Find the fastest and slowest categories
    fastest_idx = first_sale_data['Time to First Sale'].idxmin()
    slowest_idx = first_sale_data['Time to First Sale'].idxmax()
    
    fastest_category = first_sale_data.loc[fastest_idx, 'Category']
    fastest_time = first_sale_data.loc[fastest_idx, 'Time to First Sale']
    
    slowest_category = first_sale_data.loc[slowest_idx, 'Category']
    slowest_time = first_sale_data.loc[slowest_idx, 'Time to First Sale']
    
    # Calculate the time difference
    time_diff = slowest_time - fastest_time
    
    # Generate insights
    insights = f"The {fastest_category} {name} category achieves their first sale fastest at {fastest_time:.2f} months, "
    insights += f"while the {slowest_category} category takes {slowest_time:.2f} months on average. "
    
    if time_diff > 1.0:
        insights += f"This represents a significant difference of {time_diff:.2f} months in time to productivity. "
    
    # Add specific insights based on category type
    if name == "Education":
        insights += "Educational background appears to influence early sales capability, suggesting potential adjustments to onboarding programs."
    elif name == "Experience":
        insights += "Prior experience significantly impacts time to first sale, highlighting the value of experience-based training for new hires."
    elif name == "Age":
        insights += "Age groups show varying ramp-up speeds, which may inform age-specific onboarding strategies."
    elif name == "Gender":
        insights += "The gender-based differences in time to first sale may indicate opportunities to review training and support programs."
    
    return fig, insights

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
    
    # Add a horizontal line for the average with larger font size
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
    
    # Generate insights based on the data
    insights = ""
    
    # Find the highest and lowest ratio categories
    highest_idx = ratio_data['CAR2CATPO Ratio'].idxmax()
    lowest_idx = ratio_data['CAR2CATPO Ratio'].idxmin()
    
    highest_category = ratio_data.loc[highest_idx, 'Category']
    highest_ratio = ratio_data.loc[highest_idx, 'CAR2CATPO Ratio']
    
    lowest_category = ratio_data.loc[lowest_idx, 'Category']
    lowest_ratio = ratio_data.loc[lowest_idx, 'CAR2CATPO Ratio']
    
    # Generate insights
    insights = f"The {highest_category} {name} category has the highest CAR2CATPO ratio at {highest_ratio:.2f}, "
    insights += f"while the {lowest_category} category has the lowest at {lowest_ratio:.2f}. "
    
    # Explain what the ratio means
    insights += "A higher CAR2CATPO ratio indicates better efficiency in converting client approvals to production orders. "
    
    # Add category-specific insights
    if name == "Education":
        insights += "Educational background appears to influence client approval to order conversion efficiency."
    elif name == "Experience":
        insights += "Experience level correlates with ability to convert approvals to orders, suggesting expertise plays a key role in closing sales."
    elif name == "Age":
        insights += "Different age groups show varying abilities to convert client approvals to orders, which may inform targeted sales coaching."
    elif name == "Gender":
        insights += "Gender-based differences in conversion efficiency may highlight opportunities to share best practices across teams."
    
    return fig, insights

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
    ax.set_ylabel('Number of Attrited Employees', labelpad=15)
    
    # Calculate and display attrition percentages
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
    
    # Generate insights based on the data
    insights = ""
    
    # Find categories with highest and lowest attrition rates
    highest_rate_idx = np.argmax(attrition_rates)
    lowest_rate_idx = np.argmin(attrition_rates)
    
    highest_category = df['Category'].iloc[highest_rate_idx]
    highest_rate = attrition_rates[highest_rate_idx]
    
    lowest_category = df['Category'].iloc[lowest_rate_idx]
    lowest_rate = attrition_rates[lowest_rate_idx]
    
    # Calculate overall attrition rate
    total_employees = df['CAP LRM cohort'].sum()
    total_attrition = df[col14].sum()
    overall_rate = (total_attrition / total_employees) * 100 if total_employees > 0 else 0
    
    # Generate insights
    insights = f"The {highest_category} {name} category has the highest attrition rate at {highest_rate:.1f}%, "
    insights += f"while the {lowest_category} category has the lowest at {lowest_rate:.1f}%. "
    insights += f"The overall employee attrition rate across all {name} categories is {overall_rate:.1f}%. "
    
    # Add category-specific recommendations
    if name == "Education":
        insights += "Educational background appears to correlate with retention patterns, suggesting targeted retention strategies by education level."
    elif name == "Experience":
        insights += "Experience-based attrition patterns indicate tenure-specific retention strategies may be beneficial."
    elif name == "Age":
        insights += "Age-based attrition differences highlight potential for age-specific engagement initiatives."
    elif name == "Gender":
        insights += "Gender-based attrition disparities may inform diversity and inclusion strategy improvements."
    
    return fig, insights

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
    
    # Add horizontal line for overall average tenure for all employees with larger font size
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
    
    # Generate insights based on the data
    insights = ""
    
    # Calculate average tenure differences between top performers and all employees
    top_avg = residency_data[col16_short].mean()
    all_avg = residency_data[col15_short].mean()
    diff = top_avg - all_avg
    pct_diff = (diff / all_avg) * 100 if all_avg > 0 else 0
    
    # Find category with greatest tenure gap between top performers and all employees
    max_diff_idx = residency_data['Percentage Diff'].idxmax()
    max_diff_category = residency_data.loc[max_diff_idx, 'Category']
    max_diff_value = residency_data.loc[max_diff_idx, 'Percentage Diff']
    
    # Generate insights
    insights = f"Top 100 performers have on average {top_avg:.2f} months of tenure compared to {all_avg:.2f} months for all employees, "
    if diff > 0:
        insights += f"representing {pct_diff:.1f}% longer tenure for high performers. "
    else:
        insights += f"representing {abs(pct_diff):.1f}% shorter tenure for high performers. "
    
    insights += f"The {max_diff_category} {name} category shows the largest difference, with top performers having {max_diff_value:.1f}% "
    insights += "different tenure compared to the category average. "
    
    # Add category-specific insights
    if name == "Education":
        insights += "Educational background appears to correlate with tenure patterns among top performers."
    elif name == "Experience":
        insights += "Experience levels show varying tenure patterns, suggesting experience-based development opportunities."
    elif name == "Age":
        insights += "Age-based tenure differences highlight opportunities for cross-generational mentoring and knowledge transfer."
    elif name == "Gender":
        insights += "Gender-based tenure variations may inform talent development strategies."
    
    return fig, insights

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
    
    # Add a horizontal line for the average with larger font size
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
    
    # Generate insights based on the data
    insights = ""
    
    # Find categories with highest and lowest infant attrition
    highest_idx = infant_attrition_data['Infant Attrition'].idxmax()
    lowest_idx = infant_attrition_data['Infant Attrition'].idxmin()
    
    highest_category = infant_attrition_data.loc[highest_idx, 'Category']
    highest_rate = infant_attrition_data.loc[highest_idx, 'Infant Attrition']
    
    lowest_category = infant_attrition_data.loc[lowest_idx, 'Category']
    lowest_rate = infant_attrition_data.loc[lowest_idx, 'Infant Attrition']
    
    # Generate insights
    insights = f"The {highest_category} {name} category has the highest infant attrition rate at {highest_rate:.1f}%, "
    insights += f"while the {lowest_category} category has the lowest at {lowest_rate:.1f}%. "
    
    # Calculate how the rates compare to the average
    high_diff = highest_rate - avg_attrition
    low_diff = avg_attrition - lowest_rate
    
    insights += f"The highest rate is {high_diff:.1f}% above average, while the lowest is {low_diff:.1f}% below average. "
    
    # Add category-specific recommendations
    if name == "Education":
        insights += "Educational background appears to impact early attrition, suggesting education-specific onboarding adjustments may be beneficial."
    elif name == "Experience":
        insights += "Experience levels show varying early attrition patterns, highlighting opportunities to strengthen onboarding for specific experience groups."
    elif name == "Age":
        insights += "Age-based early attrition differences suggest tailoring early employment support by age group."
    elif name == "Gender":
        insights += "Gender-based early attrition disparities may inform improved orientation and early career development programs."
    
    return fig, insights
