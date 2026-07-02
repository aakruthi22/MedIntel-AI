# evaluation/evaluate_rag.py
import time

def calculate_f1_score(precision, recall):
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def evaluate_retrieval(retrieved_chunks, ground_truth_keywords):
    """
    Evaluates the RAG retrieval phase using Precision and Recall.
    """
    relevant_retrieved = 0
    for chunk in retrieved_chunks:
        if any(kw.lower() in chunk.lower() for kw in ground_truth_keywords):
            relevant_retrieved += 1

    precision = relevant_retrieved / len(retrieved_chunks) if retrieved_chunks else 0
    recall = relevant_retrieved / len(ground_truth_keywords) if ground_truth_keywords else 0
    f1 = calculate_f1_score(precision, recall)

    return precision, recall, f1

if __name__ == "__main__":
    print("🧬 MedIntel AI: Clinical RAG Evaluation Suite\n")
    
    # Mock data representing a clinical query test run
    query = "What is the recommended dosage for pediatric Aspirin?"
    ground_truth = ["81mg", "pediatric", "Reye's syndrome", "contraindicated"]
    retrieved_docs = [
        "Aspirin is generally contraindicated in pediatric patients due to Reye's syndrome.",
        "Adult dosage is typically 325mg. Pediatric dosage should be heavily monitored."
    ]

    start_time = time.time()
    # Mocking the pipeline delay
    time.sleep(0.12) 
    latency = (time.time() - start_time) * 1000

    precision, recall, f1 = evaluate_retrieval(retrieved_docs, ground_truth)

    print(f"Query: '{query}'")
    print(f"⏱️  Latency: {latency:.2f} ms")
    print(f"🎯 Precision: {precision:.2f}")
    print(f"🔄 Recall: {recall:.2f}")
    print(f"📊 F1-Score: {f1:.2f}")
    print(f"🛡️  Hallucination Risk: {'LOW' if precision > 0.5 else 'HIGH'}")