import fitz  # PyMuPDF for PDF processing
import re

def extract_text_from_pdf(pdf):
    """Extracts title, abstract, students group, and guide's name from a given PDF document."""
    
    # Check if the document is empty
    if pdf.page_count == 0:
        return "Error: PDF has no pages", "Error: PDF has no pages", "Error: No students found", "Error: No guide found"

    # Extract Title, Students, and Guide from First Page
    try:
        first_page_text = pdf[0].get_text("text")
        first_page_text_upper = first_page_text.upper()  # Convert to uppercase for case-insensitivity

        # Extract Title
        title_match = re.search(r"A\s+FINAL\s+PROJECT\s+REPORT\s+ON\s*(.*?)\s*SUBMITTED\s+TO", first_page_text_upper, re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Title not found"

        # Extract Students Group Names
        students_match = re.search(r"BACHELOR OF ENGINEERING\s+INFORMATION TECHNOLOGY\s+BY\s*(.*?)\s*UNDER THE GUIDANCE OF", first_page_text_upper, re.DOTALL)
        students = students_match.group(1).strip() if students_match else "Students not found"

        # Extract Guide's Name
        guide_match = re.search(r"UNDER THE GUIDANCE OF\s*(.*?)\n", first_page_text_upper)
        guide = guide_match.group(1).strip() if guide_match else "Guide not found"
    
    except Exception as e:
        title, students, guide = f"Error extracting title: {str(e)}", "Error extracting students", "Error extracting guide"

    # Extract Abstract from 4th Page
    try:
        abstract_page = 3  # Page numbers start from 0, so 4th page is index 3
        if abstract_page >= pdf.page_count:
            abstract = "Abstract page not found"
        else:
            abstract_text = pdf[abstract_page].get_text("text")
            abstract_cleaned = re.split(r"\bKEYWORDS\b", abstract_text, flags=re.IGNORECASE)[0].strip()
            abstract = abstract_cleaned if abstract_cleaned else "Abstract not found"
    except Exception as e:
        abstract = f"Error extracting abstract: {str(e)}"

    try:
        last_lines = first_page_text.strip().split('\n')[-5:]  # Check bottom few lines
        academic_year = "Year not found"
        for line in last_lines:
            match = re.search(r"(20\d{2}-20\d{2})", line)
            if match:
                academic_year = match.group(1)
                break
    except Exception as e:
        academic_year = f"Error extracting year: {str(e)}"

    return title, abstract, students, guide, academic_year

