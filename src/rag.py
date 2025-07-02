
import os
import faiss
import openai
import numpy as np
import json
from dotenv import load_dotenv
from src.config import FAISS_INDEX_PATH, FAISS_METADATA_PATH, OPENAI_CHAT_MODEL, OPENAI_EMBEDDING_MODEL, TOP_K, DATA_DIR

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load FAISS index and metadata
index = faiss.read_index(FAISS_INDEX_PATH)
with open(FAISS_METADATA_PATH, 'r', encoding='utf-8') as f:
    metadata = json.load(f)

metadata_keys = list(metadata.keys())

# Embed the query
def embed_query(query):
    response = openai.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=[query]
    )
    return np.array(response.data[0].embedding).astype("float32").reshape(1, -1)

# Retrieve top-k chunks
def retrieve_chunks(query):
    query_vec = embed_query(query)
    distances, indices = index.search(query_vec, TOP_K)
    context_chunks = []
    for idx in indices[0]:
        key = metadata_keys[idx]
        context_chunks.append(metadata[key])
    return context_chunks

# Call GPT with context
def answer_question(query):
    context_chunks = retrieve_chunks(query)
    context = "\n\n".join(context_chunks)

    # Load system prompt from file
    system_prompt_path = os.path.join(DATA_DIR, 'systemprompt.txt')
    with open(system_prompt_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()

    user_prompt = f"Context:\n{context}\n\nQuestion: {query}"

    response = openai.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

#if __name__ == '__main__':
#    print("\U0001F50D Ask a question about your thesis or resume (type 'exit' to quit):\n")
#    while True:
#        query = input("\U0001F9E0 > ")
#        if query.lower() == 'exit':
#            break
#        answer = answer_question(query)
#        print("\n\U0001F4DA Answer:")
#        print(answer)
#        print()
