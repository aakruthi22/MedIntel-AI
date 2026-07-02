import os
import uuid
from typing import List
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings

class DocumentIngestionEngine:
    def __init__(self):
        # Using a fast, local, open-source medical/scientific capable embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Initialize ChromaDB connection
        self.vector_store = Chroma(
            collection_name="medical_knowledge_base",
            embedding_function=self.embeddings,
            persist_directory=settings.CHROMA_DB_PATH
        )
        
        # Enterprise chunking strategy to preserve context (overlap is crucial)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    async def process_and_store_pdf(self, file: UploadFile) -> dict:
        """
        Saves an uploaded PDF, extracts text, chunks it, and embeds it into ChromaDB.
        """
        # 1. Save uploaded file temporarily to disk
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        try:
            # 2. Load and parse the PDF
            print(f"📄 Loading {file.filename}...")
            loader = PyPDFLoader(temp_file_path)
            documents = loader.load()

            # 3. Chunk the document into smaller semantic pieces
            print(f"✂️ Splitting document into chunks...")
            chunks = self.text_splitter.split_documents(documents)

            # 4. Add metadata to track the source
            for chunk in chunks:
                chunk.metadata["source_name"] = file.filename
                chunk.metadata["chunk_id"] = str(uuid.uuid4())

            # 5. Generate embeddings and store in ChromaDB
            print(f"🧠 Generating embeddings for {len(chunks)} chunks and saving to ChromaDB...")
            self.vector_store.add_documents(chunks)
            
            return {
                "status": "success",
                "filename": file.filename,
                "chunks_processed": len(chunks)
            }

        finally:
            # 6. Cleanup temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)