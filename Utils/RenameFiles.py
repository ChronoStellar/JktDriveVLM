import os
import json
import re
from collections import defaultdict

# --- Configuration ---
# The root folder containing the image subdirectories.
folder_path = r'Dataset' 
# The full path to your JSON annotation file.
annotation_path = "/Users/rx0/Desktop/Thesis/Experiment/JktDriveVLM/Dataset/annotation.json"

# Dictionary mapping old prefixes to new prefixes.
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

def natural_sort_key(s):
    """
    Creates a key for natural sorting (e.g., 'image10.png' comes after 'image2.png').
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def rename_and_recount_all(root_path, json_path, mapping):
    """
    Gathers all image files, creates a comprehensive rename and re-count plan,
    executes the file renaming, and updates the JSON annotation file.
    """
    print("--- Stage 1: Gathering and grouping files ---")
    
    file_groups = defaultdict(list)
    
    # Walk through the directory to find all image files
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue

            match = re.match(r"([a-zA-Z]+)", filename)
            if not match:
                continue
            
            old_prefix = match.group(1)
            new_prefix = mapping.get(old_prefix, old_prefix)
            
            group_key = (dirpath, new_prefix)
            file_groups[group_key].append(os.path.join(dirpath, filename))

    print(f"Found and grouped files into {len(file_groups)} groups.\n")

    # --- Stage 2: Create a detailed rename plan ---
    print("--- Stage 2: Generating rename and re-count plan ---")
    rename_plan = {}
    
    for (dirpath, new_prefix), files in file_groups.items():
        sorted_files = sorted(files, key=lambda f: natural_sort_key(os.path.basename(f)))
        
        for i, old_filepath in enumerate(sorted_files):
            counter = i + 1
            extension = os.path.splitext(old_filepath)[1]
            
            # --- MODIFIED LINE ---
            # Format the counter with a leading zero to ensure it is two digits (e.g., 1 -> "01")
            new_filename = f"{new_prefix}{counter:02d}{extension}"
            
            new_filepath = os.path.join(dirpath, new_filename)
            rename_plan[old_filepath] = new_filepath
            
    print(f"Generated a plan to rename/re-count {len(rename_plan)} files.\n")

    # --- Stage 3: Execute file renaming (safe two-pass method) ---
    print("--- Stage 3: Renaming files on disk ---")
    try:
        for old_path in rename_plan.keys():
            if os.path.exists(old_path):
                os.rename(old_path, old_path + ".tmp")
    except OSError as e:
        print(f"❌ Error during temporary rename pass: {e}")
        return

    renamed_count = 0
    try:
        for old_path, new_path in rename_plan.items():
            if os.path.exists(old_path + ".tmp"):
                os.rename(old_path + ".tmp", new_path)
                renamed_count += 1
    except OSError as e:
        print(f"❌ Error during final rename pass: {e}")
        return
        
    print(f"✅ Successfully renamed {renamed_count} files on disk.\n")

    # --- Stage 4: Update and sort the JSON file ---
    print("--- Stage 4: Updating JSON annotation file ---")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Annotation file not found at '{json_path}'")
        return

    updated_data = {}
    updated_count = 0
    
    for old_key, value in data.items():
        relative_path_from_json = os.path.normpath(value.get("path", ""))
        old_abs_path = os.path.join(root_path, relative_path_from_json)

        if old_abs_path in rename_plan:
            new_abs_path = rename_plan[old_abs_path]
            new_key = os.path.basename(new_abs_path)
            new_relative_path = os.path.relpath(new_abs_path, root_path).replace('\\', '/')

            value['path'] = new_relative_path
            updated_data[new_key] = value
            updated_count += 1
        else:
            updated_data[old_key] = value
            
    sorted_updated_data = dict(sorted(updated_data.items(), key=lambda item: natural_sort_key(item[0])))

    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_updated_data, f, indent=4)
        print(f"✅ Successfully updated {updated_count} entries and saved sorted JSON.\n")
    except IOError as e:
        print(f"❌ Error writing to JSON file '{json_path}': {e}")


# --- Main Execution ---
if __name__ == "__main__":
    rename_and_recount_all(folder_path, annotation_path, rename_map)
    print("Script finished successfully. ✨")