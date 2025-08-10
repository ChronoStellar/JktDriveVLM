import os
import json
import re

# --- Configuration ---
# The root folder containing the image subdirectories.
folder_path = r'Dataset' 
# The full path to your JSON annotation file.
annotation_path = "/Users/rx0/Desktop/Thesis/Experiment/JktDriveVLM/Dataset/annotation.json"

# Dictionary mapping old prefixes to new prefixes.
# The script will change filenames starting with a key to start with the corresponding value.
# e.g., "VRUCI" -> "VRU", "VR" -> "VRE", etc.
rename_map = {
    "EMP" : "EMP",
    "VRUCI" : "VRU",
    "VCI" : "VCI",
    "VR" : "VRE",
    "NR" : "NRO",
    "UT" : "UTR",
    "LR" : "LRE",
    "NDM" : "NDM",
    "OR" : "ORE",
    "LSP" : "LSP",
    "IRC" : "IRC",
    "TPS" : "TPS",
    "TSR" : "TSR",
    "RSR" : "RSR",
}

def rename_files_on_disk(root_path, mapping):
    """
    Walks through the directory and renames image files based on the mapping.
    """
    print("--- Starting File Renaming Process ---")
    renamed_count = 0
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            # Continue only if it's an image file
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                continue

            # Extract the alphabetical prefix from the filename (e.g., "VRUCI" from "VRUCI25.png")
            match = re.match(r"([a-zA-Z]+)", filename)
            if not match:
                continue
            
            old_prefix = match.group(1)

            # Check if this prefix needs to be renamed
            if old_prefix in mapping:
                new_prefix = mapping[old_prefix]
                # Avoid renaming if the new name is the same as the old one
                if old_prefix == new_prefix:
                    continue

                # Create the new filename
                new_filename = filename.replace(old_prefix, new_prefix, 1)
                
                # Get full old and new file paths
                old_filepath = os.path.join(dirpath, filename)
                new_filepath = os.path.join(dirpath, new_filename)
                
                # Rename the file
                try:
                    os.rename(old_filepath, new_filepath)
                    print(f"✅ Renamed: {filename} -> {new_filename}")
                    renamed_count += 1
                except OSError as e:
                    print(f"❌ Error renaming {filename}: {e}")

    if renamed_count == 0:
        print("No files needed renaming on disk.")
    else:
        print(f"\nSuccessfully renamed {renamed_count} files.")
    print("--- File Renaming Process Complete ---\n")


def update_and_sort_json(json_path, mapping):
    """
    Updates the JSON file's keys and paths, then sorts and saves it.
    """
    print("--- Starting JSON Annotation Update Process ---")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Annotation file not found at '{json_path}'")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: Could not decode JSON from '{json_path}'. Check for syntax errors.")
        return

    updated_data = {}
    updated_count = 0

    for old_key, value in data.items():
        # Extract the alphabetical prefix from the JSON key
        match = re.match(r"([a-zA-Z]+)", old_key)
        if not match:
            # If no match, keep the original entry
            updated_data[old_key] = value
            continue

        old_prefix = match.group(1)
        new_key = old_key
        
        # If the prefix is in our map, create the new key
        if old_prefix in mapping:
            new_prefix = mapping[old_prefix]
            if old_prefix != new_prefix:
                new_key = old_key.replace(old_prefix, new_prefix, 1)
                updated_count += 1

                # Update the path inside the JSON value
                if 'path' in value and old_key in value['path']:
                    value['path'] = value['path'].replace(old_key, new_key)
        
        # Add the (possibly updated) entry to our new dictionary
        updated_data[new_key] = value

    # Sort the dictionary by its new keys
    # Dictionaries in Python 3.7+ maintain insertion order.
    # We create a new dictionary from sorted items.
    sorted_updated_data = dict(sorted(updated_data.items()))

    # Write the updated and sorted data back to the JSON file
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_updated_data, f, indent=4)
        if updated_count == 0:
             print("No entries needed updating in the JSON file.")
        else:
            print(f"✅ Successfully updated {updated_count} entries and sorted the JSON file.")
    except IOError as e:
        print(f"❌ Error writing to JSON file '{json_path}': {e}")
        
    print("--- JSON Annotation Update Complete ---")


# --- Main Execution ---
if __name__ == "__main__":
    rename_files_on_disk(folder_path, rename_map)
    update_and_sort_json(annotation_path, rename_map)
    print("\nScript finished successfully. ✨")