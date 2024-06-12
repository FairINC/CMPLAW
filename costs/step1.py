import os
import shutil
from datetime import datetime

def get_most_recent_pdf(directory):
    # Get list of files in the directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.pdf')]
    
    # Return None if no PDF files are found
    if not files:
        return None
    
    # Find the most recent file based on modification time
    most_recent_file = max(files, key=os.path.getmtime)
    return most_recent_file

def move_file_to_desktop(file_path, dest_folder):
    # Get the file name
    file_name = os.path.basename(file_path)
    
    # Create the destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)
    
    # Move the file
    dest_path = os.path.join(dest_folder, file_name)
    shutil.move(file_path, dest_path)

def main():
    # Define source directories
    source_dirs = [
        r'sourceCHANGEME',
        r'source2CHANGEME'
    ]
    
    # Define the destination directory
    current_date = datetime.now()
    dest_folder_name = current_date.strftime("%m-%Y") + "LCS"  # Use hyphen instead of colon
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    dest_folder = os.path.join(desktop_path, dest_folder_name)
    
    # Iterate through source directories and move the most recent PDF
    for source_dir in source_dirs:
        most_recent_pdf = get_most_recent_pdf(source_dir)
        if most_recent_pdf:
            move_file_to_desktop(most_recent_pdf, dest_folder)
        else:
            print(f"No PDF files found in {source_dir}")

if __name__ == "__main__":
    main()
