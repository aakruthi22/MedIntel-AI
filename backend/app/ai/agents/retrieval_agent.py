from app.ai.workflows.state import MedIntelState
from app.rag.retrievers.medical_retriever import EnterpriseMedicalRetriever
from app.domain.models.schemas import MedicalQueryRequest

retriever = EnterpriseMedicalRetriever()

async def retrieval_node(state: MedIntelState) -> dict:
    """
    Iterates over the generated search queries and pulls dense vector chunks from ChromaDB.
    """
    all_chunks = []
    
    for q in state["search_queries"]:
        payload = MedicalQueryRequest(query=q)
        # Fetch chunks from our previously built retriever
        chunks = await retriever.retrieve_relevant_evidence(payload)
        all_chunks.extend(chunks)
        
    print(f"🔎 [Retrieval Agent] Retrieved {len(all_chunks)} chunks of evidence.")
        
    return {"retrieved_chunks": all_chunks}