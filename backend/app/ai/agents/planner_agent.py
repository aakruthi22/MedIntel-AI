from app.ai.workflows.state import MedIntelState

async def planner_node(state: MedIntelState) -> dict:
    """
    Analyzes the user's complex medical query and breaks it down into 
    specific, vector-searchable sub-queries.
    """
    query = state["original_query"]
    
    # In production, you would call an LLM here to generate these.
    # For now, we simulate the LLM's intelligent extraction.
    sub_queries = [
        f"{query} etiology and pathophysiology",
        f"{query} clinical guidelines WHO CDC",
        f"{query} primary pharmacotherapy treatments"
    ]
    
    print(f"🧠 [Planner Agent] Decomposed query into {len(sub_queries)} sub-queries.")
    
    # Whatever dictionary we return is merged into the master MedIntelState
    return {"search_queries": sub_queries}