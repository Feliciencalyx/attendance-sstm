import numpy as np
import logging
from typing import Optional, Tuple, Dict, Any
from app.config import settings
from app.db import supabase, mock_db
from app.schemas import BiometricScanRequest

logger = logging.getLogger("attendance.biometric")

def calculate_cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Computes Cosine Similarity between two 128-d floating point embedding vectors using NumPy.
    Returns float value between -1.0 and 1.0 (1.0 = identical direction).
    """
    a = np.array(vec_a, dtype=np.float32)
    b = np.array(vec_b, dtype=np.float32)
    
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    similarity = np.dot(a, b) / (norm_a * norm_b)
    return float(similarity)

def find_user_by_fingerprint(template: str) -> Tuple[Optional[Dict[str, Any]], float]:
    """
    Matches fingerprint template string against database records.
    """
    if supabase:
        try:
            res = supabase.table("users").select("*").eq("fingerprint_template", template).eq("is_active", True).execute()
            if res.data and len(res.data) > 0:
                return res.data[0], 1.0
        except Exception as e:
            logger.error(f"Supabase fingerprint lookup error: {e}")

    # Fallback / Mock DB lookup
    for user in mock_db.users:
        if user.get("is_active") and user.get("fingerprint_template") == template:
            return user, 1.0
            
    return None, 0.0

def find_user_by_face_embedding(query_vector: list[float]) -> Tuple[Optional[Dict[str, Any]], float]:
    """
    Matches 128-d facial vector embedding using Supabase pgvector stored RPC procedure or NumPy vector distance calculation.
    """
    best_match: Optional[Dict[str, Any]] = None
    highest_score: float = 0.0

    if supabase:
        try:
            # Invoke RPC stored procedure match_face_embeddings defined in 01_schema.sql
            res = supabase.rpc("match_face_embeddings", {
                "query_embedding": query_vector,
                "match_threshold": settings.FACE_MATCH_THRESHOLD,
                "match_count": 1
            }).execute()

            if res.data and len(res.data) > 0:
                top_match = res.data[0]
                # Retrieve full user profile
                user_res = supabase.table("users").select("*").eq("id", top_match["id"]).execute()
                if user_res.data:
                    return user_res.data[0], float(top_match["similarity"])
        except Exception as e:
            logger.error(f"Supabase pgvector match error: {e}. Falling back to NumPy vector comparison.")

    # NumPy Fallback matching over loaded user profiles
    for user in mock_db.users:
        if not user.get("is_active") or not user.get("face_embedding"):
            continue
            
        score = calculate_cosine_similarity(query_vector, user["face_embedding"])
        if score > highest_score:
            highest_score = score
            best_match = user

    if highest_score >= settings.FACE_MATCH_THRESHOLD:
        return best_match, highest_score

    return None, highest_score

def match_biometric_data(scan_req: BiometricScanRequest) -> Tuple[Optional[Dict[str, Any]], float, str]:
    """
    Identifies a user from scan request payload via facial embeddings or fingerprint template.
    Returns (user_dict, similarity_score, match_method).
    """
    if scan_req.face_embedding is not None:
        user, score = find_user_by_face_embedding(scan_req.face_embedding)
        return user, score, "FACE_RECOGNITION"
    elif scan_req.fingerprint_template is not None:
        user, score = find_user_by_fingerprint(scan_req.fingerprint_template)
        return user, score, "FINGERPRINT_MATCH"
    else:
        raise ValueError("Scan request must contain either face_embedding or fingerprint_template.")
