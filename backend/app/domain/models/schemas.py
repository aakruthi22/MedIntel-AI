from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class MedicalQueryRequest(BaseModel):
    query: str = Field(..., example="What are the primary first-line treatments for Type 2 Diabetes according to WHO guidelines?")
    specialty_filter: Optional[str] = Field(None, example="Endocrinology")

class CitationDocument(BaseModel):
    id: str
    source_name: str
    chunk_content: str
    confidence_score: float
    page_number: Optional[int] = None

class MedicalQueryResponse(BaseModel):
    answer: str
    confidence_score: float
    citations: List[CitationDocument]
    hallucination_index: float
    medical_disclaimer: str = "DISCLAIMER: This system is an evidence-based research tool and does not replace qualified clinical consultation."