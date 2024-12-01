
import os
import pandas as pd

def merge_all_csv_in_directory(base_directory, output_file):
    """
    Recursively merges all CSV files in a directory and its subdirectories into a single DataFrame.
    
    Parameters:
        base_directory (str): The root directory to start the search.
        output_file (str): The path to save the merged CSV file.
    """
    all_csv_files = []
    
    # Walk through the directory and subdirectories to find CSV files
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.csv'):
                all_csv_files.append(os.path.join(root, file))
    
    # Merge all CSV files
    merged_data = pd.DataFrame()
    for csv_file in all_csv_files:
        try:
            print(f"Reading {csv_file}...")
            data = pd.read_csv(csv_file)
            merged_data = pd.concat([merged_data, data], ignore_index=True)
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
    
    # Save merged data to a single CSV file
    try:
        merged_data.to_csv(output_file, index=False)
        print(f"Successfully merged {len(all_csv_files)} files into {output_file}")
    except Exception as e:
        print(f"Error saving merged file: {e}")

if __name__ == "__main__":
    # Update these paths accordingly
    BASE_DIRECTORY = "shows/"  # Replace with your directory path
    OUTPUT_FILE = "merged_episodes.csv"         # Replace with your desired output file name
    
    merge_all_csv_in_directory(BASE_DIRECTORY, OUTPUT_FILE)
