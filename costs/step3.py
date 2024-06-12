import os
import fitz  # PyMuPDF
from datetime import datetime
import re

def extract_pages_with_clt_number(src_file, dest_file, clt_number):
    # Open the source PDF file
    pdf_document = fitz.open(src_file)
    
    # Create a new PDF to store the extracted pages
    output_pdf = fitz.open()
    
    # Prepare a regex pattern to match the CLT number
    clt_pattern = re.compile(re.escape(clt_number).replace(r"\ ", r"\s*"))
    
    # Iterate over each page and search for the CLT number
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        
        # Debugging: Print text of the page
        print(f"Page {page_num + 1} text: {text}")
        
        if clt_pattern.search(text):
            output_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
    
    # Save the output PDF if it contains any pages
    if len(output_pdf) > 0:
        output_pdf.save(dest_file)
        print(f"Saved the new PDF with pages containing '{clt_number}' to '{dest_file}'")
    else:
        print(f"No pages containing '{clt_number}' found in '{src_file}'")
    
    # Close the documents
    pdf_document.close()
    output_pdf.close()

def find_matching_file(src_folder, pattern):
    files = os.listdir(src_folder)
    regex = re.compile(pattern)
    for file in files:
        if regex.match(file):
            return file
    return None

def main():
    current_date = datetime.now()
    dest_folder_name = current_date.strftime("%m-%Y") + "LCS"
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    src_folder = os.path.join(desktop_path, dest_folder_name)
    
    pattern = r"^\d{2}\.\d{2}\.\d{2} TR 1 CC\.pdf$"
    clt_number = "CLT #: 1724-00"
    
    matching_file = find_matching_file(src_folder, pattern)
    if not matching_file:
        print(f"No file matching the pattern '{pattern}' found in '{src_folder}'")
        return
    
    src_file_path = os.path.join(src_folder, matching_file)
    dest_folder = r'LocationSCHANGEME'
    dest_file_path = os.path.join(dest_folder, matching_file)
    
    if not os.path.exists(dest_folder):
        print("The destination path 'CHANGEME' does not exist. Please check the path.")
        return
    
    extract_pages_with_clt_number(src_file_path, dest_file_path, clt_number)

if __name__ == "__main__":
    main()
