import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys
from datetime import datetime
from recommendation_storage import init_recommendations, save_recommendation, export_recommendations, import_recommendations

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
            
            # Try to load the Zone sheet if it exists
            try:
                Zone = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Zone')
                return Gender, Education, Experience, Age, Zone
            except Exception:
                # Zone sheet doesn't exist yet
                return Gender, Education, Experience, Age
        except FileNotFoundError:
            st.error("The file Aadhar_modified.xlsx was not found.")
            st.stop()
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.exception(e)  # This will display the full traceback

def main():
    # Set page configuration
    st.set_page_config(
        layout="wide",
        page_title="Aadhar Analysis Dashboard",
        page_icon="📊"
    )
    
    # Initialize session state for storing recommendations from persistent storage
    init_recommendations()
        
    st.title('Aadhar Analysis Dashboard')
    
    # Load all dataframes
    data_frames = load_data()
    
    # Check if Zone data was loaded
    if len(data_frames) == 5:
        Gender, Education, Experience, Age, Zone = data_frames
        # Create list of dataframes with their display names
        all_dataframes = [
            {"df": Gender, "name": "Gender"},
            {"df": Education, "name": "Education"},
            {"df": Experience, "name": "Experience"},
            {"df": Age, "name": "Age"},
            {"df": Zone, "name": "Zone"}
        ]
        # Create tabs for each category
        tabs = st.tabs(["Gender", "Education", "Experience", "Age", "Zone"])
    else:
        Gender, Education, Experience, Age = data_frames
        # Create list of dataframes with their display names
        all_dataframes = [
            {"df": Gender, "name": "Gender"},
            {"df": Education, "name": "Education"},
            {"df": Experience, "name": "Experience"},
            {"df": Age, "name": "Age"}
        ]
        # Create tabs for each category
        tabs = st.tabs(["Gender", "Education", "Experience", "Age"])
      
    # Generate dashboard for each tab
    for i, data in enumerate(all_dataframes):
        with tabs[i]:
            try:
                st.info(f"Generating {data['name']} dashboard with {len(data['df'])} rows of data...")
                create_dashboard(data["df"], data["name"])
                st.success(f"{data['name']} dashboard completed!")
            except Exception as e:
                st.error(f"Error generating {data['name']} dashboard: {str(e)}")
                st.exception(e)  # This will display the full traceback
            
def create_dashboard(df, name):
    """Create a dashboard visualization for the given dataframe in Streamlit."""
    st.header(f'{name} Analysis Dashboard')
    
    # Add export recommendations functionality
    with st.expander("Export/Import Recommendations"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Export button - save recommendations to file
            if st.button("Export All Recommendations"):
                filename = export_recommendations(name)
                if filename:
                    st.success(f"Recommendations exported to {filename}")
        
        with col2:
            # Import button - load recommendations from file
            uploaded_file = st.file_uploader("Import recommendations from JSON", type="json")
            if uploaded_file is not None:
                if import_recommendations(uploaded_file.getvalue().decode('utf-8')):
                    st.success("Recommendations imported successfully!")
                    st.rerun()  # Refresh the UI to show imported recommendations
    
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
    
    # Set optimal figure size for the charts
    plt.rcParams['figure.figsize'] = [8, 5]  # Slightly smaller to load faster
    plt.rcParams['figure.autolayout'] = True  # Better layout
    plt.rcParams['figure.dpi'] = 100  # Good balance between quality and performance
    
    # Create three columns for the first row of charts
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Chart 1: Distribution (first 3 columns)
        st.subheader(f'{name} Distribution by Cohort')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Extract the first 3 columns
        first_cols = filtered_df.columns[:3]
        # Reshape data for seaborn
        df_melted = pd.melt(filtered_df, 
                            id_vars=[first_cols[0]], 
                            value_vars=[first_cols[1], first_cols[2]], 
                            var_name='Metric', 
                            value_name='Count')

        # Calculate percentages for each cohort
        for metric in [first_cols[1], first_cols[2]]:
            total = filtered_df[metric].sum()
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
        if name == "Education":
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
        plt.tight_layout()
        st.pyplot(fig)
        
        # Custom recommendation input for Distribution chart
        input_key = f"{name}_Distribution_recommendation"
        # Initialize session state for this recommendation if it doesn't exist
        if input_key not in st.session_state:
            st.session_state[input_key] = "Enter your insights about distribution here..."
            
        # Add text area for custom recommendations
        st.markdown("<div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-top: 10px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin: 0px 0px 5px 0px; color: #444;'>Your Recommendation:</h4>", unsafe_allow_html=True)
        custom_insight = st.text_area(
            "Enter your custom recommendation for Distribution:",
            value=st.session_state[input_key],
            height=100,
            key=f"textarea_{input_key}",
            label_visibility="collapsed"
        )
        
        # Save button for the recommendation
        if st.button("Save", key=f"save_{input_key}"):
            st.session_state[input_key] = custom_insight
            st.success("Recommendation saved!")
        
    with col2:
        # Chart 2: KPI Performance
        st.subheader(f'KPI Performance by {name}')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Get the 4th and 8th columns (indices 3 and 7)
        col4 = filtered_df.columns[3]
        col8 = filtered_df.columns[7]

        # Create shorter column names for display
        col4_short = "Cumulative Combined KPI"
        col8_short = "Cumulative KPI 1"

        # Create a DataFrame with the data and specified columns
        kpi_data = pd.DataFrame({
            'Category': filtered_df['Category'],
            col4_short: filtered_df[col4],
            col8_short: filtered_df[col8]
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
        if name == "Education":
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
        plt.tight_layout()
        st.pyplot(fig)
        
        # Custom recommendation input
        input_key = f"{name}_KPI_Performance_recommendation"
        # Initialize session state for this recommendation if it doesn't exist
        if input_key not in st.session_state:
            st.session_state[input_key] = "Enter your insights about KPI performance here..."
            
        # Add text area for custom recommendations
        st.markdown("<div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-top: 10px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin: 0px 0px 5px 0px; color: #444;'>Your Recommendation:</h4>", unsafe_allow_html=True)
        custom_insight = st.text_area(
            "Enter your custom recommendation for KPI Performance:",
            value=st.session_state[input_key],
            height=100,
            key=f"textarea_{input_key}",
            label_visibility="collapsed"
        )
        
        # Save button for the recommendation
        if st.button("Save", key=f"save_{input_key}"):
            st.session_state[input_key] = custom_insight
            st.success("Recommendation saved!")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        # Chart 3: Performance Multiple
        st.subheader(f'Performance Multiple by {name}')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Get the 7th and 11th columns (indices 6 and 10)
        col7 = filtered_df.columns[6]
        col11 = filtered_df.columns[10]

        # Create shorter column names for display
        col7_short = "Performance Multiple KPI Combined"
        col11_short = "Performance Multiple KPI 1"

        # Create a DataFrame with the data and specified columns
        perf_data = pd.DataFrame({
            'Category': filtered_df['Category'],
            col7_short: filtered_df[col7],
            col11_short: filtered_df[col11]
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
        if name == "Education":
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
        plt.tight_layout()
        st.pyplot(fig)

        # Custom recommendation input for Performance Multiple chart
        input_key = f"{name}_Performance_Multiple_recommendation"
        # Initialize session state for this recommendation if it doesn't exist
        
        # Add text area for custom recommendations
        st.markdown("<div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-top: 10px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin: 0px 0px 5px 0px; color: #444;'>Your Recommendation:</h4>", unsafe_allow_html=True)
        custom_insight = st.text_area(
            "Enter your custom recommendation for Performance Multiple:",
            value=st.session_state.get(input_key, "Enter your insights about performance multiple here..."),
            height=100,
            key=f"textarea_{input_key}",
            label_visibility="collapsed"
        )
        
        # Save button for the recommendation
        if st.button("Save", key=f"save_{input_key}"):
            save_recommendation(input_key, custom_insight)
            st.success("Recommendation saved and will persist between sessions!")
        st.markdown("</div>", unsafe_allow_html=True)

    # Create three columns for the second row of charts
    st.markdown("---")
    col4, col5, col6 = st.columns(3)
    
    with col4:
        # Chart 4: Top and Bottom Performers
        st.subheader(f'Top vs Bottom Performers by {name}')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Get the 5th, 6th, 9th and 10th columns (indices 4, 5, 8, 9)
        col5 = filtered_df.columns[4]  # Top performers Combined KPI
        col6 = filtered_df.columns[5]  # Bottom performers Combined KPI
        col9 = filtered_df.columns[8]  # Top performers KPI 1
        col10 = filtered_df.columns[9]  # Bottom performers KPI 1

        # Create shorter column names for display
        col5_short = "Top 10% (Combined)"
        col6_short = "Bottom 10% (Combined)" 
        col9_short = "Top 10% (KPI 1)"
        col10_short = "Bottom 10% (KPI 1)"

        # Create a DataFrame with the data and specified columns
        performer_data = pd.DataFrame({
            'Category': filtered_df['Category'],
            col5_short: filtered_df[col5],
            col6_short: filtered_df[col6],
            col9_short: filtered_df[col9],
            col10_short: filtered_df[col10]
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
        if name == "Education":
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
        plt.tight_layout()
        st.pyplot(fig)

    with col5:
        # Chart 5: Time to First Sale
        st.subheader(f'Time to First Sale by {name}')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Get the 12th column (index 11)
        col12 = filtered_df.columns[11]

        # Create a DataFrame for the chart
        first_sale_data = pd.DataFrame({
            'Category': filtered_df['Category'],
            'Time to First Sale': filtered_df[col12]
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
        avg_time = filtered_df[col12].mean()
        ax.axhline(y=avg_time, color='red', linestyle='--', alpha=0.7)
        ax.text(ax.get_xlim()[1] * 0.6, avg_time * 1.02, f'Avg: {avg_time:.2f} months', 
                color='red', ha='center', va='bottom')
        
        # Rotate x-axis labels for Education dashboard
        if name == "Education":
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
        plt.tight_layout()
        st.pyplot(fig)

    with col6:
        # Chart 6: CAR2CATPO Ratio
        st.subheader(f'CAR2CATPO Ratio by {name}')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Get the 13th column (index 12)
        col13 = filtered_df.columns[12]

        # Create a DataFrame for the chart
        ratio_data = pd.DataFrame({
            'Category': filtered_df['Category'],
            'CAR2CATPO Ratio': filtered_df[col13]
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
        avg_ratio = filtered_df[col13].mean()
        ax.axhline(y=avg_ratio, color='red', linestyle='--', alpha=0.7)
        ax.text(ax.get_xlim()[1] * 0.6, avg_ratio * 1.02, f'Avg: {avg_ratio:.2f}', 
                color='red', ha='center', va='bottom')
        
        # Rotate x-axis labels for Education dashboard
        if name == "Education":
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
        plt.tight_layout()
        st.pyplot(fig)

    # Create three columns for the third row of charts
    st.markdown("---")
    col7, col8, col9 = st.columns(3)
    
    with col7:
        # Chart 7: Attrition Count
        st.subheader(f'Employee Attrition by {name}')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Get the 14th column (index 13)
        col14 = filtered_df.columns[13]

        # Create a DataFrame for the chart
        attrition_data = pd.DataFrame({
            'Category': filtered_df['Category'],
            'Attrited Employees': filtered_df[col14]
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
        total_per_category = filtered_df['CAP LRM cohort'].values
        attrition_per_category = filtered_df[col14].values
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

    with col8:
        # Chart 8: Average Residency
        st.subheader(f'Employment Tenure by {name}')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Get the 15th and 16th columns (indices 14 and 15)
        col15 = filtered_df.columns[14]  # Average Residency of all employees
        col16 = filtered_df.columns[15]  # Average Residency of TOP 100 employees

        # Create shorter column names for display
        col15_short = "All Employees"
        col16_short = "Top 100 Performers"

        # Create a DataFrame for the chart
        residency_data = pd.DataFrame({
            'Category': filtered_df['Category'],
            col15_short: filtered_df[col15],
            col16_short: filtered_df[col16]
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
        overall_avg = filtered_df[col15].mean()
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
        if name == "Education":
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
        plt.tight_layout()
        st.pyplot(fig)

    with col9:
        # Chart 9: Infant Attrition
        st.subheader(f'Infant Attrition Rate by {name}')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Get the last column (index 17)
        last_col = filtered_df.columns[-1]  # Using -1 to access the last column

        # Create a DataFrame for the chart with a shorter column name for display
        infant_attrition_data = pd.DataFrame({
            'Category': filtered_df['Category'],
            'Infant Attrition': filtered_df[last_col] * 100  # Convert to percentage
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

    # Add a footer
    st.markdown("---")
    st.caption(f"Generated: {datetime.now().strftime('%B %d, %Y')} | Aadhar {name} Analysis")

if __name__ == "__main__":
    main()
