import os
import json
import faiss
import openai
import numpy as np
from config import OPENAI_EMBEDDING_MODEL, FAISS_INDEX_PATH, FAISS_METADATA_PATH, OUTPUT_DIR
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_text(texts):
    embeddings = []
    for i in range(0, len(texts), 100):
        response = openai.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=texts[i:i + 100]
        )
        embeddings.extend([e.embedding for e in response.data])
    return np.array(embeddings).astype("float32")

def main():
    with open(os.path.join(OUTPUT_DIR, 'thesis_chunks.json'), 'r', encoding='utf-8') as f:
        thesis_chunks = json.load(f)
    with open(os.path.join(OUTPUT_DIR, 'resume_chunks.json'), 'r', encoding='utf-8') as f:
        resume_chunks = json.load(f)

    all_chunks = thesis_chunks + resume_chunks
    embeddings = embed_text(all_chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)

    metadata = {str(i): chunk for i, chunk in enumerate(all_chunks)}
    with open(FAISS_METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()