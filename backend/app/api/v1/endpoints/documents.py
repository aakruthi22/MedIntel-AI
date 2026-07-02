from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.rag.embeddings.document_processor import DocumentIngestionEngine

router = APIRouter()
ingestion_engine = DocumentIngestionEngine()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_medical_document(file: UploadFile = File(...)):
    """
    Ingests a medical PDF, chunks the text, and stores vectors in ChromaDB.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Only PDF documents are supported."
        )
    
    try:
        result = await ingestion_engine.process_and_store_pdf(file)
        return result
    except Exception as e:
        print(f"Error processing document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )

@router.get("/list", status_code=status.HTTP_200_OK)
async def list_documents():
    """
    Queries ChromaDB directly to extract unique source_name keys 
    for visual state updates in the presentation layer.
    """
    try:
        # Retrieve all records from the collection
        results = ingestion_engine.vector_store.get(include=['metadatas'])
        
        # Guard against empty collections
        if not results or 'metadatas' not in results or not results['metadatas']:
            return {"documents": []}
            
        # Parse out matching source names dynamically
        unique_sources = set(
            meta.get("source_name") 
            for meta in results['metadatas'] 
            if meta and meta.get("source_name")
        )
        return {"documents": sorted(list(unique_sources))}
    except Exception as e:
        print(f"Failed to query knowledge base: {e}")
        return {"documents": []}