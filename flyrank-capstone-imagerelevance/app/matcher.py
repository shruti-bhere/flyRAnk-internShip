import numpy as np

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def check_mismatch_guard(post_topic: str, candidate_metadata: dict, similarity_score: float, threshold=0.65):
    # Rule 1: Confidence score check
    if candidate_metadata.get("confidence", 0) < 0.7:
        return {"approved": False, "reason": "Low image classification confidence."}
    
    # Rule 2: Similarity score check
    if similarity_score < threshold:
        return {"approved": False, "reason": f"Similarity below threshold: {similarity_score:.2f}"}
    
    # Rule 3: Category Mismatch Guard (e.g., Fox vs Wolf)
    subject = candidate_metadata.get("subject", "").lower()
    if "fox" in post_topic.lower() and "wolf" in subject:
        return {"approved": False, "reason": "Animal category mismatch: expected fox, detected wolf."}
        
    return {"approved": True, "reason": "Match verified with high confidence."}