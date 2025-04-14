import gradio as gr
import shutil
import os
from createFolders import folders  # folders = ['cat1/sub1', 'cat1/sub2', 'cat2/sub1', ...]

unsorted = './unsorted'
data_folder = './data'

# List images in unsorted
image_paths = [os.path.join(unsorted, f) for f in os.listdir(unsorted)
               if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
# Flatten folders dictionary into a list like: ['common/OppositeDirection', 'indonesian/StreetPeddler', ...]
folder_choices = [f"{category}/{sub}" for category, subs in folders.items() for sub in subs]


# Function to move file and get next image
def move_and_next(current_index, selected_folder, new_name):
    if current_index >= len(image_paths):
        return None, current_index, "No more images!"

    current_image = image_paths[current_index]
    original_filename = os.path.basename(current_image)
    ext = os.path.splitext(original_filename)[1]  # Keep the file extension

    # Use new name if provided, else keep original
    filename = new_name.strip() + ext if new_name.strip() else original_filename

    # Construct target path
    target_path = os.path.join(data_folder, selected_folder, filename)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    shutil.move(current_image, target_path)

    # Update index
    new_index = current_index + 1
    if new_index < len(image_paths):
        return image_paths[new_index], new_index, f"Moved and renamed to: {filename}"
    else:
        return None, new_index, "All images sorted!"

with gr.Blocks() as demo:
    gr.Markdown("### Image Sorter & Renamer")
    state = gr.State(0)

    img = gr.Image()
    folder_dropdown = gr.Dropdown(choices=folder_choices, label="Move to folder:")
    new_name_box = gr.Textbox(label="Rename file (optional, no extension)")
    move_btn = gr.Button("Move & Next")

    move_btn.click(fn=move_and_next,
                   inputs=[state, folder_dropdown, new_name_box],
                   outputs=[img, state])

    def load_first():
        if image_paths:
            return image_paths[0], 0, ""
        return None, 0, "No images found in unsorted folder."

    demo.load(fn=load_first, outputs=[img, state])

if __name__ == "__main__":
    demo.launch(show_api=False)
