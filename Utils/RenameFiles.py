import os

folder_path = r'Dataset'
annotarion_path = "/Users/rx0/Desktop/Thesis/Experiment/JktDriveVLM/Dataset/annotation.json"

rename = {
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

for subfolder in os.listdir(folder_path):
    subfolder_path = os.path.join(folder_path, subfolder)
    
    if os.path.isdir(subfolder_path):
        
        for category in os.listdir(subfolder_path):
            prefix = "".join(char for char in category if char.isupper())
            category_path = os.path.join(subfolder_path, category)
            
            if os.path.isdir(category_path):
                for idx, filename in enumerate(os.listdir(category_path), 1):
                    file_path = os.path.join(category_path, filename)
                    
                    if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                        # Create the new filename with prefix and index
                        new_filename = f"{prefix}{idx}{os.path.splitext(filename)[1]}"
                        new_file_path = os.path.join(category_path, new_filename)
                        
                        # Rename the file
                        os.rename(file_path, new_file_path)

print("Files renamed successfully.")