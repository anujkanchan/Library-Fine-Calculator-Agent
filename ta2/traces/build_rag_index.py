"""Validate/build the local policy corpus used by the TA2 RAG layer."""
from ta2.rag_policy import load_chunks

if __name__ == "__main__":
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} policy chunks from ta2/docs/library_rules.txt")
    for i, chunk in enumerate(chunks, 1):
        print(f"\nCHUNK {i}\n{chunk}")
