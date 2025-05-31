import pandas as pd

# Read the Gender dataframe
Gender = pd.read_excel('Aadhar_modified.xlsx', sheet_name='Gender')

# Save column info to a text file for better visibility
with open('gender_columns_info.txt', 'w') as f:
    f.write("Gender DataFrame Column Information:\n")
    f.write(f"Shape: {Gender.shape}\n\n")
    f.write("Column indices and names:\n")
    for i, col in enumerate(Gender.columns):
        f.write(f"{i}: {col}\n")
    
    # Get sample data
    f.write("\nSample data for columns 4, 5, 8, 9 (indices start at 0):\n")
    cols = [Gender.columns[0], Gender.columns[4], Gender.columns[5], Gender.columns[8], Gender.columns[9]]
    f.write(str(Gender[cols].head()))
