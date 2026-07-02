import re
from app.ai.workflows.state import MedIntelState

async def safety_node(state: MedIntelState) -> dict:
    """
    Firewall Agent: Detects PII and Injection patterns.
    """
    query = state["original_query"]
    
    # 1. Basic PII Detection (Regex for emails/phones)
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    if re.search(email_pattern, query):
        return {"draft_answer": "SECURITY ALERT: Input contains potential PII. Request rejected.", "confidence_score": 0.0}

    # 2. Prompt Injection Detection
    injections = ["ignore previous instructions", "system override", "reveal system prompt"]
    if any(i in query.lower() for i in injections):
        return {"draft_answer": "SECURITY ALERT: Potential prompt injection detected.", "confidence_score": 0.0}
    
    return {} # If safe, pass through