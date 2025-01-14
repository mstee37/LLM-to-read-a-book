import pandas as pd
import re
from PyPDF2 import PdfReader

def extract_questions_to_dataframe(pdf_path, pages):
    """
    Extract text from specific pages in a PDF and store it in a DataFrame.

    Args:
        pdf_path (str): Path to the PDF file.
        pages (list): List of page numbers (1-indexed) to extract text from.

    Returns:
        pd.DataFrame: DataFrame containing page numbers and extracted text.
    """
    data = []

    try:
        # Open the PDF file
        reader = PdfReader(pdf_path)
        for page_number in pages:
            # Adjust for 0-indexing in PyPDF2
            page_index = page_number - 1
            if page_index < len(reader.pages):
                text = reader.pages[page_index].extract_text()
                data.append({"Page": page_number, "Content": text})
            else:
                print(f"Page {page_number} is out of range.")
    
    except Exception as e:
        print(f"Error while reading the PDF: {e}")
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    return df

def parse_questions(text):
    # Regex pattern to match questions
    pattern = r"(Question\s+\d+\.\d+:.*?)(?=Question\s+\d+\.\d+:|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    
    # Process each match to extract question number and content
    questions_data = []
    for match in matches:
        # Extract the question number and content
        question_number_match = re.search(r"(Question\s+\d+\.\d+:)", match)
        question_number = question_number_match.group(0) if question_number_match else ""
        question_content = match.replace(question_number, "").strip()
        
        # Add to list
        questions_data.append({"Question Number": question_number.strip(":"), "Content": question_content})
    
    # Convert to DataFrame
    df = pd.DataFrame(questions_data)
    return df


