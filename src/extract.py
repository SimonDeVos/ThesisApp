import pymupdf
import os
import json
from config import DATA_DIR, OUTPUT_DIR, CHUNK_SIZE, CHUNK_OVERLAP

def extract_text_chunks(pdf_path):
    doc = pymupdf.open(pdf_path)
    text = " ".join([page.get_text() for page in doc])
    chunks = []
    for i in range(0, len(text), CHUNK_SIZE - CHUNK_OVERLAP):
        chunks.append(text[i:i + CHUNK_SIZE])
    return chunks

def save_chunks(chunks, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

def main():
    thesis_pdf = os.path.join(DATA_DIR, 'thesis.pdf')
    resume_pdf = os.path.join(DATA_DIR, 'resume.pdf')

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    thesis_chunks = extract_text_chunks(thesis_pdf)
    save_chunks(thesis_chunks, os.path.join(OUTPUT_DIR, 'thesis_chunks.json'))

    resume_chunks = extract_text_chunks(resume_pdf)
    save_chunks(resume_chunks, os.path.join(OUTPUT_DIR, 'resume_chunks.json'))

if __name__ == '__main__':
    main()