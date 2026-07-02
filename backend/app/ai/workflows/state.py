from typing import List, TypedDict, Annotated
from app.domain.models.schemas import CitationDocument

# Reducer function to append chunks instead of overwriting them
def merge_citations(a: List[CitationDocument], b: List[CitationDocument]) -> List[CitationDocument]:
    return a + b

class MedIntelState(TypedDict):
    original_query: str
    search_queries: List[str]
    # Annotated ensures that if multiple agents retrieve chunks, they are combined
    retrieved_chunks: Annotated[List[CitationDocument], merge_citations]
    draft_answer: str
    confidence_score: float
    hallucination_index: float