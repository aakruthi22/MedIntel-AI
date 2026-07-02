from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.domain.models.schemas import MedicalQueryRequest, MedicalQueryResponse
from app.ai.workflows.graph import medintel_rag_pipeline

router = APIRouter()
from fastapi import APIRouter, Depends
from app.infrastructure.security.jwt import get_current_user_id
from app.domain.models.schemas import MedicalQueryRequest
from app.ai.workflows.graph import medintel_rag_pipeline

router = APIRouter()

@router.post("/query")
async def research(
    payload: MedicalQueryRequest, 
    user_id: str = Depends(get_current_user_id) 
):
    # Pass user_id into the graph state for tenant-scoped retrieval
    return await medintel_rag_pipeline.ainvoke({
        "original_query": payload.query, 
        "user_id": user_id
    })
@router.post("/query", response_model=MedicalQueryResponse, status_code=status.HTTP_200_OK)
async def process_medical_inquiry(payload: MedicalQueryRequest, db: Session = Depends(get_db)):
    """
    Executes the full LangGraph Multi-Agent RAG pipeline.
    """
    try:
        # 1. Initialize the State payload for LangGraph
        initial_state = {
            "original_query": payload.query,
            "search_queries": [],
            "retrieved_chunks": [],
            "draft_answer": "",
            "confidence_score": 0.0,
            "hallucination_index": 0.0
        }
        
        # 2. Invoke the compiled LangGraph execution loop asynchronously
        final_state = await medintel_rag_pipeline.ainvoke(initial_state)
        
        # 3. Map the LangGraph state back to our strictly typed Pydantic response
        return MedicalQueryResponse(
            answer=final_state["draft_answer"],
            confidence_score=final_state["confidence_score"],
            citations=final_state["retrieved_chunks"],
            hallucination_index=final_state["hallucination_index"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An execution fault occurred in the Multi-Agent pipeline: {str(e)}"
        )