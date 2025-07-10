import pandas as pd

# --- Configuration ---
# Replace 'your_file.xlsx' with the actual name of your Excel file.
xlsx_file_name = 'Annotated Urban.xlsx' 
# You can change the desired output JSON file name here.
json_file_name = 'output.json'

try:
    df = pd.read_excel(xlsx_file_name)
    df.to_json(json_file_name, orient='records', indent=4)
    print(f"✅ Successfully converted '{xlsx_file_name}' to '{json_file_name}'!")

except FileNotFoundError:
    print(f"❌ Error: The file '{xlsx_file_name}' was not found. Make sure it's in the same directory as the script.")
except Exception as e:
    print(f"An error occurred: {e}")