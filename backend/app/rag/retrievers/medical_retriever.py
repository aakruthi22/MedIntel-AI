from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings
from app.domain.models.schemas import CitationDocument, MedicalQueryRequest
from typing import List

class EnterpriseMedicalRetriever:
    def __init__(self):
        # Using the updated LangChain HuggingFace package
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Initialize connection to the persistent vector store
        self.vector_store = Chroma(
            collection_name="medical_knowledge_base",
            embedding_function=self.embeddings,
            persist_directory=settings.CHROMA_DB_PATH
        )

    async def retrieve_relevant_evidence(
        self, 
        payload: MedicalQueryRequest, 
        user_id: str = "default_user"
    ) -> List[CitationDocument]:
        """
        Executes a semantic vector search restricted by user_id metadata 
        to ensure multi-tenant data isolation.
        """
        print(f"🔎 Executing Vector Search for: '{payload.query}' (User: {user_id})")
        
        # Perform similarity search with filter for tenant isolation
        results = self.vector_store.similarity_search_with_relevance_scores(
            query=payload.query, 
            k=3,
            filter={"user_id": user_id} 
        )
        
        citations = []
        for doc, score in results:
            citations.append(
                CitationDocument(
                    id=doc.metadata.get("chunk_id", "unknown-id"),
                    source_name=doc.metadata.get("source_name", "Unknown Source"),
                    chunk_content=doc.page_content,
                    confidence_score=round(float(score), 4),
                    page_number=doc.metadata.get("page", 0)
                )
            )
            
        return citations