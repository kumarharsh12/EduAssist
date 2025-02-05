import os
import json
import shutil

def create_directories(paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' has been deleted.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Folder '{folder_path}' does not exist.")


def save_json(data, path):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)

def load_prompts(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def get_next_id(data_dir):
    existing_ids = [int(d) for d in os.listdir(data_dir) if d.isdigit()]
    if not existing_ids:
        return 1
    return max(existing_ids) + 1