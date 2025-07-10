import json
import os

# --- Configuration ---
input_file_name = 'output.json'
output_file_name = 'output2.json'
# The base directory where your category folders are located.
# '.' means the current directory where the script is running.
image_base_directory = '.'

# This will hold the final, fully converted data
final_data = {}

try:
    # Open and read the entire input file
    with open(input_file_name, 'r') as f:
        data_list = json.load(f)

    # Loop through each record in the input list
    for record in data_list:
        base_filename = record.get("Filename")
        if not base_filename:
            print(f"⚠️ Skipping record due to missing 'Filename': {record}")
            continue

        # Format the category string to match the folder name
        category_formatted = record.get("Category", "").replace(" ", "")
        
        # --- File Cross-Reference Logic ---
        full_filename = None
        search_dir = os.path.join(image_base_directory, category_formatted)
        
        try:
            for f in os.listdir(search_dir):
                # Check if a filename in the directory starts with the base name + a dot
                # This correctly matches "EMP1.png" but not "EMP10.png"
                if f.startswith(base_filename + '.'):
                    full_filename = f
                    break # Found it, no need to look further
        except FileNotFoundError:
            print(f"⚠️ Warning: Directory not found: '{search_dir}'")
        
        # If no matching file was found, use the base name and print a warning
        if not full_filename:
            print(f"⚠️ Warning: Could not find image for '{base_filename}' in '{search_dir}'. Using base name.")
            full_filename = base_filename # Fallback to the name without extension
        # --- End of Cross-Reference Logic ---

        # Create the new data structure for this record
        transformed_record = {
            "path": f"{category_formatted}/{full_filename}", # Use the full name here
            "category": category_formatted,
            "question": record.get("Question", ""),
            "answers": record.get("Answer", ""),
            "distractor1": "",
            "distractor2": "",
            "distractor3": ""
        }

        # Use the full filename as the top-level key
        final_data[full_filename] = transformed_record

    # Write the entire final dictionary to the output file
    with open(output_file_name, 'w') as f:
        json.dump(final_data, f, indent=4)

    print(f"\n✅ Success! Converted {len(final_data)} records and cross-referenced file extensions.")

except FileNotFoundError:
    print(f"❌ Error: The input file '{input_file_name}' was not found.")
except json.JSONDecodeError:
    print(f"❌ Error: The input file '{input_file_name}' is not a valid JSON file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")