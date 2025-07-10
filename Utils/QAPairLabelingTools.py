import gradio as gr
import os
import json
from CreateFolders import folders

# --- Configuration ---
# Get the directory of the script, handling __pycache__
script_dir = os.path.dirname(__file__)
if os.path.basename(script_dir) == '__pycache__':
    script_dir = os.path.dirname(script_dir)  # Move up to Utils
BASE_DIR = os.path.abspath(os.path.join(script_dir, '..'))  # Move up to JktDriveVLM
DIRECTORY = os.path.join(BASE_DIR, 'Dataset')
JSON_OUTPUT_FILE = os.path.join(BASE_DIR, './UrbanFlow.json')

# Debug paths
print(f"Current working directory: {os.getcwd()}")
print(f"Script directory: {script_dir}")
print(f"Dataset directory: {DIRECTORY}")
print(f"Does dataset directory exist? {os.path.exists(DIRECTORY)}")
print(f"Dataset directory contents: {os.listdir(DIRECTORY) if os.path.exists(DIRECTORY) else 'Directory not found'}")

# --- Helper Functions & Initial Setup ---

def create_categorized_image_dict(base_directory, category_choices):
    """Scans a directory recursively and groups image paths by their category folder."""
    print("Indexing images by category...")
    categorized_images = {category: [] for category in category_choices}
    if not os.path.exists(base_directory):
        print(f"WARNING: Base directory '{base_directory}' not found.")
        return categorized_images

    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(root, file)
                # Determine category from path, e.g., ".../common/RoadDamage/img.jpg" -> "common/RoadDamage"
                # This works by taking the last two directory components of the image's path.
                parent_dir = os.path.basename(os.path.dirname(path))
                grandparent_dir = os.path.basename(os.path.dirname(os.path.dirname(path)))
                category_key = f"{grandparent_dir}/{parent_dir}"

                if category_key in categorized_images:
                    categorized_images[category_key].append(path)
    
    # Sort images within each category
    for category in categorized_images:
        categorized_images[category].sort()
        
    print("Image indexing complete.")
    return categorized_images

def load_json_data(filepath):
    """Loads JSON data from a file, returning an empty dict if it doesn't exist."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# --- Main Application Logic ---

# Create the list of category choices from your `folders` import
folder_choices = [f"{category}/{sub}" for category, subs in folders.items() for sub in subs]

# Pre-load and categorize all images at startup
categorized_images = create_categorized_image_dict(DIRECTORY, folder_choices)
# Load existing JSON data into memory
image_data = load_json_data(JSON_OUTPUT_FILE)

def switch_category(selected_category):
    """Called when the dropdown changes. Loads images for the selected category."""
    image_list = categorized_images.get(selected_category, [])
    
    if not image_list:
        status = f"No images found for category: '{selected_category}'"
        return [], 0, None, status, "", "", "", "", ""

    first_image = image_list[0]
    # Check if the first image has already been annotated
    filename = os.path.basename(first_image)
    existing_data = image_data.get(filename, {})
    question = existing_data.get("question", "")
    answers = existing_data.get("answers", "")
    distractor1 = existing_data.get("distractor1", "")
    distractor2 = existing_data.get("distractor2", "")
    distractor3 = existing_data.get("distractor3", "")

    status = f"Loaded category '{selected_category}'. Image 1 of {len(image_list)}."
    return image_list, 0, first_image, status, question, answers, distractor1, distractor2, distractor3

def save_and_next_in_category(current_image_list, current_index, selected_category, question, answers, distractor1, distractor2, distractor3):
    """Saves data for the current image and loads the next one within the category."""
    global image_data
    
    # Save data for the current image
    current_image_path = current_image_list[current_index]
    filename = os.path.basename(current_image_path)

    relative_image_path = os.path.relpath(current_image_path, DIRECTORY).replace(os.path.sep, '/')
    
    image_data[filename] = {
        "path": relative_image_path,
        "category": selected_category,
        "question": question,
        "answers": answers,
        "distractor1": distractor1,
        "distractor2": distractor2,
        "distractor3": distractor3
    }

    with open(JSON_OUTPUT_FILE, 'w') as f:
        json.dump(image_data, f, indent=4)
    
    # Move to the next image
    new_index = current_index + 1
    if new_index < len(current_image_list):
        next_image_path = current_image_list[new_index]
        status = f"✅ Saved {filename}. Now showing image {new_index + 1} of {len(current_image_list)}."
        
        # Load existing data for the next image, if any
        next_filename = os.path.basename(next_image_path)
        existing_data = image_data.get(next_filename, {})
        next_question = existing_data.get("question", "")
        next_answers = existing_data.get("answers", "")
        next_distractor1 = existing_data.get("distractor1", "")
        next_distractor2 = existing_data.get("distractor2", "")
        next_distractor3 = existing_data.get("distractor3", "")

        return new_index, next_image_path, status, next_question, next_answers, next_distractor1, next_distractor2, next_distractor3, json.dumps(image_data, indent=4)
    else:
        status = f"✅ Saved {filename}. 🎉 Category '{selected_category}' complete!"
        return new_index, None, status, "", "", "", "", "", json.dumps(image_data, indent=4)

def save_json_from_editor(json_string):
    """Saves changes from the JSON editor back to the file."""
    global image_data
    try:
        new_data = json.loads(json_string)
        with open(JSON_OUTPUT_FILE, 'w') as f:
            json.dump(new_data, f, indent=4)
        image_data = new_data
        return "✅ JSON saved successfully!"
    except json.JSONDecodeError as e:
        return f"❌ Error: Invalid JSON format. Details: {e}"

# --- Gradio User Interface ---

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🖼️ Road Image Annotator")
    
    # State variables to manage the current session
    state_current_image_list = gr.State([])
    state_category_index = gr.State(0)

    with gr.Tabs():
        with gr.TabItem("Image Tagger"):
            with gr.Row():
                with gr.Column(scale=2):
                    image_display = gr.Image(label="Current Image")
                    tagger_status = gr.Markdown(label="Status", value="Select a category to begin.")
                
                with gr.Column(scale=1):
                    folder_dropdown = gr.Dropdown(choices=folder_choices, label="Select Category")
                    question_input = gr.Textbox(label="Questions", interactive=True)
                    answers_input = gr.Textbox(label="Answers", interactive=True)
                    distractor_1_input = gr.Textbox(label="Distractor 1", interactive=True)
                    distractor_2_input = gr.Textbox(label="Distractor 2", interactive=True)
                    distractor_3_input = gr.Textbox(label="Distractor 3", interactive=True)
                    save_button = gr.Button("Save & Next Image", variant="primary")

        with gr.TabItem("JSON Editor"):
            gr.Markdown(f"View and manually edit the `{JSON_OUTPUT_FILE}` file.")
            json_editor = gr.Code(
                value=json.dumps(image_data, indent=4), 
                label=JSON_OUTPUT_FILE, 
                language="json", 
                interactive=True
            )
            save_json_button = gr.Button("Save JSON Changes")
            editor_status = gr.Markdown()

    # --- Component Interactions ---
    
    # When the user changes the category in the dropdown
    folder_dropdown.change(
        fn=switch_category,
        inputs=[folder_dropdown],
        outputs=[
            state_current_image_list, 
            state_category_index, 
            image_display, 
            tagger_status, 
            question_input, 
            answers_input,
            distractor_1_input,
            distractor_2_input,
            distractor_3_input
        ]
    )
    
    # When the user clicks "Save & Next"
    save_button.click(
        fn=save_and_next_in_category,
        inputs=[
            state_current_image_list, 
            state_category_index, 
            folder_dropdown, 
            question_input, 
            answers_input,
            distractor_1_input,
            distractor_2_input,
            distractor_3_input
        ],
        outputs=[
            state_category_index, 
            image_display, 
            tagger_status, 
            question_input, 
            answers_input,
            distractor_1_input,
            distractor_2_input,
            distractor_3_input,
            json_editor
        ]
    )

    # When the user saves in the JSON editor
    save_json_button.click(
        fn=save_json_from_editor,
        inputs=[json_editor],
        outputs=[editor_status]
    )

if __name__ == "__main__":
    demo.launch(show_api=False)