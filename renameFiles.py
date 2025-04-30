import os

prefix = "vincent-"

folder_path = r'Dataset'
for subfolder in os.listdir(folder_path):
    subfolder_path = os.path.join(folder_path, subfolder)

    for category in os.listdir(subfolder_path):
        categories_path = os.path.join(subfolder_path, category)

        for idx, filename in enumerate(os.listdir(categories_path)):
            file_path = os.path.join(categories_path, filename)
            
            print(file_path)
            if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                # Create the new filename
                new_filename = f"{prefix}{idx}{os.path.splitext(filename)[1]}"
                new_file_path = os.path.join(categories_path, new_filename)
                
                # Rename the file
                os.rename(file_path, new_file_path)

print("Files renamed successfully.")