import pandas as pd
import os
import re
import argparse

def get_simplified(file_path, output_dir):
    """
    Processes a single Excel file to calculate group-level and item-level accuracies.
    Returns the dataframe for summary creation.
    """
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"Error: The file was not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred reading {file_path}: {e}")
        return None

    # Group-level calculations
    groups = df.groupby('id')
    group_accuracies = {}
    group_true_false = {}
    for id, group in groups:
        correct_count = (group['answer'] == group['prediction']).sum()
        group_size = len(group)
        accuracy = correct_count / group_size if group_size > 0 else 0.0
        group_accuracies[id] = accuracy
        group_true_false[id] = (accuracy == 1.0)
    
    # Create group results DataFrame
    group_results_df = pd.DataFrame({
        'accuracy': group_accuracies,
        'all_correct': group_true_false
    })
    group_results_df.index.name = 'id'
    group_results_df = group_results_df.reset_index()

    # File handling
    base_filename = os.path.basename(file_path)
    file_stem = os.path.splitext(base_filename)[0]
    
    # Save group results
    group_csv_filename = f"{file_stem}_group_results.csv"
    group_output_path = os.path.join(output_dir, group_csv_filename)
    group_results_df.to_csv(group_output_path, index=False)

    print(f"Successfully saved group results to: {group_output_path}")
    return df

def create_summary(all_dfs, output_dir):
    """
    Creates a summary CSV file with total, per-file, and per-larger-group accuracies.
    """
    if not all_dfs:
        print("No dataframes to summarize.")
        return

    combined_df = pd.concat(all_dfs, ignore_index=True)

    # 1. Total accuracy
    total_accuracy = (combined_df['answer'] == combined_df['prediction']).sum() / len(combined_df)

    # 2. Accuracy of each file
    file_accuracies = combined_df.groupby('source_file').apply(
        lambda x: (x['answer'] == x['prediction']).sum() / len(x)
    ).to_dict()

    # 3. Accuracy of each larger group
    combined_df['larger_group'] = combined_df['id'].str.extract(r'([A-Za-z]+)')[0]
    larger_group_accuracies = combined_df.groupby('larger_group').apply(
        lambda x: (x['answer'] == x['prediction']).sum() / len(x)
    ).to_dict()

    # Create the summary DataFrame
    summary_data = []
    summary_data.append({'Metric Type': 'Total Accuracy', 'Group': 'Overall', 'Accuracy': total_accuracy})
    for file, acc in file_accuracies.items():
        summary_data.append({'Metric Type': 'File Accuracy', 'Group': file, 'Accuracy': acc})
    for group, acc in larger_group_accuracies.items():
        summary_data.append({'Metric Type': 'Larger Group Accuracy', 'Group': group, 'Accuracy': acc})
    
    summary_df = pd.DataFrame(summary_data)

    # Save the summary file
    summary_output_path = os.path.join(output_dir, 'summary_results.csv')
    summary_df.to_csv(summary_output_path, index=False)
    print(f"\nSuccessfully saved summary results to: {summary_output_path}")

def from_folders(input_dir, output_dir):
    """
    Processes all .xlsx files in an input directory and saves results to an output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        files = os.listdir(input_dir)
    except FileNotFoundError:
        print(f"Error: Input directory not found: {input_dir}")
        return
        
    excel_files = [f for f in files if f.endswith('.xlsx')]
    
    if not excel_files:
        print(f"No .xlsx files found in {input_dir}")
        return

    all_dataframes = []
    for file in excel_files:
        full_input_path = os.path.join(input_dir, file)
        print(f"\nProcessing file: {full_input_path}")
        df = get_simplified(full_input_path, output_dir)
        
        if df is not None:
            df['source_file'] = os.path.basename(file)
            all_dataframes.append(df)
            
    create_summary(all_dataframes, output_dir)

def main():
    """Main function to parse arguments and run the script."""
    parser = argparse.ArgumentParser(description="Process Excel files to calculate and summarize accuracies.")
    parser.add_argument("input_folder", help="The path to the folder containing the input .xlsx files.")
    
    args = parser.parse_args()
    input_folder_path = args.input_folder

    # --- MODIFIED SECTION ---
    # Define the fixed base directory for the output
    output_base_dir = "/Users/rx0/Desktop/Thesis/Experiment/JktDriveVLM/Eval/"
    # Extract the name of the input folder to append to the output base directory
    input_folder_name = os.path.basename(os.path.normpath(input_folder_path))
    
    # Construct the full, final output path
    output_folder_path = os.path.join(output_base_dir, input_folder_name)
    
    print("-" * 50)
    print(f"Input folder:  {input_folder_path}")
    print(f"Output folder: {output_folder_path}")
    print("-" * 50)
    # --- END OF MODIFIED SECTION ---

    # Run the main processing function
    from_folders(input_folder_path, output_folder_path)

# --- Main execution ---
if __name__ == "__main__":
    main()

# python Eval/getAccuracy.py /path/to/your/input/folder