import os
import shutil
from datetime import datetime
import re

def find_matching_file(src_folder, pattern):
    files = os.listdir(src_folder)
    regex = re.compile(pattern)
    for file in files:
        if regex.match(file):
            return file
    return None

def copy_file_to_destination(src_folder, file_name, dest_folder):
    src_file_path = os.path.join(src_folder, file_name)
    if not os.path.isfile(src_file_path):
        print(f"File '{file_name}' not found in '{src_folder}'")
        return
    
    os.makedirs(dest_folder, exist_ok=True)
    dest_file_path = os.path.join(dest_folder, file_name)
    shutil.copy2(src_file_path, dest_file_path)
    print(f"Copied '{file_name}' to '{dest_folder}'")

def main():
    current_date = datetime.now()
    dest_folder_name = current_date.strftime("%m-%Y") + "LCS"  # Ensure this matches the folder name from step 1
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    src_folder = os.path.join(desktop_path, dest_folder_name)
    
    pattern = r"^\d{2}\.\d{2}\.\d{2} TR 31 CC\.pdf$"
    
    matching_file = find_matching_file(src_folder, pattern)
    if not matching_file:
        print(f"No file matching the pattern '{pattern}' found in '{src_folder}'")
        return
    
    dest_folder = r'CHANGEME'
    
    if not os.path.exists(dest_folder):
        print("The destination path 'CHANGEME' does not exist. Please check the path.")
        return
    
    copy_file_to_destination(src_folder, matching_file, dest_folder)

if __name__ == "__main__":
    main()
