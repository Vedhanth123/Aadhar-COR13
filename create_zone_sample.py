import pandas as pd
import numpy as np
import os

def create_sample_zone_data():
    """
    Create a sample Zone sheet for the Aadhar data Excel file.
    This generates realistic-looking zone data based on the structure of the other sheets.
    """
    print("Creating sample Zone sheet for Aadhar data...")
    
    # Check if the Excel file exists
    if not os.path.exists('Aadhar_modified.xlsx'):
        print("Error: Aadhar_modified.xlsx not found!")
        return
    
    # Try to read the other sheets to understand the structure
    try:
        gender_df = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Gender')
        column_names = gender_df.columns
    except Exception as e:
        print(f"Error reading existing sheets: {str(e)}")
        return
        
    # Define zone names (using Indian regions)
    zones = [
        'Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'Bengaluru', 
        'Hyderabad', 'Ahmedabad', 'Pune', 'Jaipur', 'Lucknow',
        'Kanpur', 'Nagpur', 'Patna', 'Indore', 'Thane', 
        'Bhopal', 'Visakhapatnam', 'Vadodara', 'Ghaziabad', 'Ludhiana',
        'Agra', 'Nashik', 'Ranchi', 'Faridabad', 'Guwahati',
        'Chandigarh', 'Thiruvananthapuram', 'Dehradun', 'Jammu'
    ]
    
    # Create the Zone dataframe with the same structure as Gender
    zone_df = pd.DataFrame(columns=column_names)
    zone_df['Category'] = zones
    
    # Helper function for random data with some correlation
    def generate_correlated_data(n, base, variance, correlation=0.7, min_val=0, max_val=None):
        """Generate n data points correlated with a base value"""
        base_value = base
        # Generate values with some correlation to base_value
        values = np.random.normal(base_value, variance, n)
        # Apply correlation
        correlated = base_value * correlation + values * (1-correlation)
        # Apply min/max constraints
        if min_val is not None:
            correlated = np.maximum(correlated, min_val)
        if max_val is not None:
            correlated = np.minimum(correlated, max_val)
        return correlated
    
    # Generate cohort data
    n_zones = len(zones)
    
    # Column 1: Cohort data (assuming this is count data)
    cohort_base = np.random.randint(300, 800)
    zone_df[column_names[1]] = generate_correlated_data(n_zones, cohort_base, cohort_base/5, min_val=100).astype(int)
    
    # Column 2: Another cohort data column
    cohort2_base = np.random.randint(200, 400)
    zone_df[column_names[2]] = generate_correlated_data(n_zones, cohort2_base, cohort2_base/5, min_val=50).astype(int)
    
    # Generate KPI achievement percentages
    kpi_base = np.random.uniform(85, 110)
    zone_df[column_names[3]] = generate_correlated_data(n_zones, kpi_base, 15, min_val=70, max_val=130)
    zone_df[column_names[7]] = generate_correlated_data(n_zones, kpi_base, 15, min_val=70, max_val=130)
    
    # Top and bottom performers
    zone_df[column_names[4]] = generate_correlated_data(n_zones, np.random.randint(30, 50), 10, min_val=20, max_val=70)
    zone_df[column_names[5]] = generate_correlated_data(n_zones, np.random.randint(10, 20), 5, min_val=5, max_val=35)
    zone_df[column_names[8]] = generate_correlated_data(n_zones, np.random.randint(30, 50), 10, min_val=20, max_val=70)
    zone_df[column_names[9]] = generate_correlated_data(n_zones, np.random.randint(10, 20), 5, min_val=5, max_val=35)
    
    # Performance multiples
    zone_df[column_names[6]] = generate_correlated_data(n_zones, np.random.uniform(1.5, 3), 0.5, min_val=1.0, max_val=4.0)
    zone_df[column_names[10]] = generate_correlated_data(n_zones, np.random.uniform(1.5, 3), 0.5, min_val=1.0, max_val=4.0)
    
    # Time to first sale
    zone_df[column_names[11]] = generate_correlated_data(n_zones, np.random.uniform(1.5, 3), 0.7, min_val=0.5, max_val=6)
    
    # CAR2CATPO Ratio
    zone_df[column_names[12]] = generate_correlated_data(n_zones, np.random.uniform(1.2, 2.5), 0.4, min_val=0.5, max_val=3.5)
    
    # Attrition numbers
    attrition_base = np.random.randint(20, 40)
    zone_df[column_names[13]] = generate_correlated_data(n_zones, attrition_base, attrition_base/3, min_val=5).astype(int)
    
    # Average residency
    residency_base = np.random.uniform(15, 24)
    zone_df[column_names[14]] = generate_correlated_data(n_zones, residency_base, 4, min_val=6)
    zone_df[column_names[15]] = generate_correlated_data(n_zones, residency_base*1.2, 5, min_val=8)  # Top performers stay longer
    
    # Infant attrition
    zone_df[column_names[16]] = generate_correlated_data(n_zones, np.random.uniform(0.15, 0.25), 0.07, min_val=0.05, max_val=0.45)
    
    # Read the existing Excel file
    try:
        with pd.ExcelWriter('Aadhar_modified.xlsx', engine='openpyxl', mode='a') as writer:
            # Write the zone dataframe to the Excel file
            zone_df.to_excel(writer, sheet_name='Zone', index=False)
            print("Zone sheet created successfully!")
    except Exception as e:
        print(f"Error saving Zone sheet: {str(e)}")
        print("Creating a new file with all sheets...")
        
        try:
            # If we can't append, we'll create a new file with all the sheets
            all_sheets = pd.read_excel('Aadhar_modified.xlsx', sheet_name=None)
            all_sheets['Zone'] = zone_df
            
            # Write all sheets to a new Excel file
            with pd.ExcelWriter('Aadhar_modified_with_zone.xlsx') as writer:
                for sheet_name, sheet in all_sheets.items():
                    sheet.to_excel(writer, sheet_name=sheet_name, index=False)
            print("Created new file: Aadhar_modified_with_zone.xlsx")
        except Exception as e2:
            print(f"Error creating new file: {str(e2)}")

if __name__ == "__main__":
    create_sample_zone_data()
    print("Done! You can now run the dashboard with the Zone tab.")
