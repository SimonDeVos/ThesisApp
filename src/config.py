import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder paths
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'output')

# Chunking settings
CHUNK_SIZE = 1000  # characters
CHUNK_OVERLAP = 100

# Embedding model settings
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"  # 1536-dim
OPENAI_CHAT_MODEL = "gpt-3.5-turbo"

# FAISS paths
FAISS_INDEX_DIR = os.path.join(OUTPUT_DIR, 'faiss_index')
FAISS_INDEX_PATH = os.path.join(FAISS_INDEX_DIR, 'index.faiss')
FAISS_METADATA_PATH = os.path.join(FAISS_INDEX_DIR, 'metadata.json')

# Retrieval settings
TOP_K = 3