import pandas as pd

# Read the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Print info about the 16th column (index 15)
if len(Gender.columns) > 15:
    print("16th column (index 15):", Gender.columns[15])
    print("\nData for this column:")
    print(Gender[['Category', Gender.columns[15]]].head())
    
    # Print additional information about column type and values
    print("\nColumn data type:", Gender[Gender.columns[15]].dtype)
    print("Min value:", Gender[Gender.columns[15]].min())
    print("Max value:", Gender[Gender.columns[15]].max())
    print("Mean value:", Gender[Gender.columns[15]].mean())
else:
    print(f"There are only {len(Gender.columns)} columns in the dataframe. Can't access column 16.")
    print("Available columns:")
    for i, col in enumerate(Gender.columns):
        print(f"{i}: {col}")
