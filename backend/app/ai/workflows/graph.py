from langgraph.graph import StateGraph, START, END
from app.ai.workflows.state import MedIntelState
from app.ai.agents.planner_agent import planner_node
from app.ai.agents.retrieval_agent import retrieval_node
from app.ai.agents.medical_expert import medical_expert_node
from app.ai.agents.safety_agent import safety_node  
def build_medintel_graph():
    """
    Compiles the Multi-Agent directed graph for the RAG pipeline.
    """
    builder = StateGraph(MedIntelState)
    # In build_medintel_graph():
    builder.add_node("SafetyCheck", safety_node)
    builder.add_edge(START, "SafetyCheck")
    builder.add_conditional_edges("SafetyCheck", lambda s: "STOP" if s.get("confidence_score") == 0 else "Planner")
    
    # 1. Register all nodes (Agents)
    builder.add_node("Planner", planner_node)
    builder.add_node("Retrieval", retrieval_node)
    builder.add_node("MedicalExpert", medical_expert_node)
    
    # 2. Define the Execution Flow (Edges)
    builder.add_edge(START, "Planner")
    builder.add_edge("Planner", "Retrieval")
    builder.add_edge("Retrieval", "MedicalExpert")
    builder.add_edge("MedicalExpert", END)
    
    # 3. Compile into an executable LangChain application
    return builder.compile()

# Instantiate the pipeline singleton
medintel_rag_pipeline = build_medintel_graph()