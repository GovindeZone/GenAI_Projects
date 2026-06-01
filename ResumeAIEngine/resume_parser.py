import os
from PyPDF2 import PdfReader
from docx import Document

def read_pdf(path):

    text = ""

    reader = PdfReader(path)

    for page in reader.pages:
        text += page.extract_text()

    return text


def read_docx(path):

    doc = Document(path)

    return "\n".join(
        [p.text for p in doc.paragraphs]
    )


def load_resumes(folder_path):

    resumes = []

    for file in os.listdir(folder_path):

        full_path = os.path.join(folder_path, file)

        try:

            if file.endswith(".pdf"):
                text = read_pdf(full_path)

            elif file.endswith(".docx"):
                text = read_docx(full_path)

            else:
                continue

            resumes.append({
                "file_name": file,
                "content": text
            })

        except Exception as e:

            print(f"Error reading {file}: {e}")

    return resumes