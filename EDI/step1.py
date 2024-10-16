import os
import pandas as pd
from datetime import datetime

def find_most_recent_directory(base_path):
    dirs = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    latest_dir = max(dirs, key=os.path.getmtime)
    return latest_dir

def find_most_recent_file(directory, file_extension=".xlsx"):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(file_extension)]
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def process_excel_file(file_path):
    df = pd.read_excel(file_path, index_col=0)
    blank_column = df.columns[1]
    modified_rows = []
    arf_count = 0

    for index, row in df.iterrows():
        if pd.isna(row[blank_column]) or row[blank_column] == "":
            print(f"Would modify FILE: {index}, CRNO: {row['CRNO']}, adding ARF.")
            modified_rows.append((index, row['CRNO'], '', '', '', ''))
            arf_count += 1
            if arf_count == 20:
                break

    print("Last checked row:", index, row.to_dict())
    return modified_rows

def save_to_csv(modified_rows):
    output_file = datetime.now().strftime("%m-%d-%Y") + "_Workload.csv"
    df = pd.DataFrame(modified_rows, columns=['Scrubs1337'])
    df.to_csv(output_file, index=False)
    print(f"Data written to {output_file}")

def main():
    base_path = "Scrubs1337"
    latest_dir = find_most_recent_directory(base_path)
    print(f"Most recent directory found: {latest_dir}")
    
    latest_file = find_most_recent_file(latest_dir)
    print(f"Most recent file found: {latest_file}")

    modified_rows = process_excel_file(latest_file)
    if modified_rows:
        save_to_csv(modified_rows)
    else:
        print("No rows needed modification.")

if __name__ == "__main__":
    main()
