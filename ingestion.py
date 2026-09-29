from pathlib import Path
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR =Path(__file__).resolve().parent
DOCUMENT_PATH=(BASE_DIR/ "Appointment_Booking_System_Detailed_Requirements.docx")
CHROMA_DIR=BASE_DIR/"chroma_db"



def ingest_project_documents():
    
    # Loader document 
    loader=Docx2txtLoader(str(DOCUMENT_PATH))
    documents=loader.load()

    print("number of dcuments:",len(documents))

    # text splitter

    text_splitter= RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100)
    chunks=text_splitter.split_documents(documents) # type: ignore

    print("Number of chunks:",len(chunks))

    # enbedding Model

    embeddings=OllamaEmbeddings(model="nomic-embed-text")

    db=Chroma.from_documents(
          documents=chunks,
          embedding=embeddings,
          persist_directory=str(CHROMA_DIR),
          collection_name="Appointment_booking_project"
    )


    print("Documents sucessfully stored in ChromaDB")
    
    return db


if __name__ == "__main__":
    ingest_project_documents()