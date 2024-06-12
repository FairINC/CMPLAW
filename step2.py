import os
import pandas as pd
import pyautogui
import time

def find_most_recent_csv(directory):
    """Find the most recent CSV file in the specified directory."""
    csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]
    if not csv_files:
        return None
    latest_csv = max(csv_files, key=os.path.getmtime)
    return latest_csv

def read_csv(file_path):
    """Read the CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)

def automate_keystrokes(data_frame):
    """Automate the keystrokes in the application for each row in the DataFrame."""
    for index, row in data_frame.iterrows():
        file_code = row['FILE'].split('-')
        if len(file_code) == 3:
            xx, yyyy, z = file_code
            print(f"Processing: XX={xx}, YYYY={yyyy}, Z={z}")
            # Sequence of keyboard actions
            pyautogui.typewrite('S1')
            pyautogui.press('enter')
            pyautogui.typewrite('N')
            pyautogui.press('enter')
            pyautogui.press('enter')
            pyautogui.typewrite(xx)
            pyautogui.press('enter')
            pyautogui.typewrite(yyyy)
            pyautogui.press('enter')
            pyautogui.typewrite(z)
            pyautogui.press('enter')
            # Sleep to prevent too fast input
            time.sleep(1)

def main():
    directory = '.'  # Change this to the directory you want to search
    csv_file = find_most_recent_csv(directory)
    if csv_file:
        print(f"Most recent CSV found: {csv_file}")
        data_frame = read_csv(csv_file)
        automate_keystrokes(data_frame)
    else:
        print("No CSV files found in the directory.")

if __name__ == "__main__":
    main()
