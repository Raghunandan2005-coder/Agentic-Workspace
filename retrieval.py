from pathlib import Path
from unittest import result
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


BASE_DIR = Path(__file__).resolve().parent

CHROMA_DIR = BASE_DIR/"chroma_db"

embeddings=OllamaEmbeddings(model="nomic-embed-text")

db=Chroma(
    collection_name="Appointment_booking_project",
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR)
    
)

def retrieve_project_knowledge(query:str ,k: int=4):
   
    results=db.similarity_search(query=query,k=k)
    
    return results
if __name__ == "__main__":
    
    query = "What is the project Overview?"

    results = retrieve_project_knowledge(query)
    print("\nRetrieved Results:\n")

    for i, doc in enumerate(results, start=1):
        print(f"--- Result {i} ---")
        print(doc.page_content)
        print()