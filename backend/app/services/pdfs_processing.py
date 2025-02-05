import os
from typing import List

from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file.
    """
    with open(pdf_path, "rb") as f:
        pdf = PdfReader(f)
        text = ""
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text()
    return text

def get_text_from_pdfs(pdfs_dir: str) -> List[str]:
    """
    Extract text from PDF files.
    """
    pdfs = []
    for pdf_file in os.listdir(pdfs_dir):
        pdf_path = os.path.join(pdfs_dir, pdf_file)
        pdf_text = extract_text_from_pdf(pdf_path)
        pdfs.append(pdf_text)
    return pdfs