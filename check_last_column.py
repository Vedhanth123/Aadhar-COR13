import pandas as pd

# Read the Gender dataframe
Gender = pd.read_excel('HDFC_modified.xlsx', sheet_name='Gender')

# Print all column names first
print("All columns in Gender dataframe:")
for i, col in enumerate(Gender.columns):
    print(f"{i}: {col}")

# Get the last column
last_index = len(Gender.columns) - 1
last_col = Gender.columns[last_index]

# Save to file instead of just printing
with open('last_column_info.txt', 'w') as f:
    f.write(f"Last column (index {last_index}): {last_col}\n\n")
    f.write("Data for this column:\n")
    f.write(str(Gender[['Category', last_col]]) + "\n\n")
    
    # Additional information
    f.write(f"Column data type: {Gender[last_col].dtype}\n")
    try:
        f.write(f"Min value: {Gender[last_col].min()}\n")
        f.write(f"Max value: {Gender[last_col].max()}\n")
        f.write(f"Mean value: {Gender[last_col].mean()}\n")
    except:
        f.write("Could not calculate min/max/mean - possibly non-numeric data\n")

print("Column information saved to last_column_info.txt")
