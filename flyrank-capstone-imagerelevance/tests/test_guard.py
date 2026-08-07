import pytest
from app.matcher import check_mismatch_guard

def test_successful_match():
    # Fox post with a high-confidence Fox image
    metadata = {"subject": "red fox", "confidence": 0.95}
    result = check_mismatch_guard(
        post_topic="Behavior of Red Foxes in Forests",
        candidate_metadata=metadata,
        similarity_score=0.88
    )
    assert result["approved"] is True
    assert "Match verified" in result["reason"]

def test_mismatch_guard_wolf_rejection():
    # PROBE 3: Force a wolf image on a fox post -> MUST REJECT
    metadata = {"subject": "gray wolf", "confidence": 0.92}
    result = check_mismatch_guard(
        post_topic="Behavior of Red Foxes in Forests",
        candidate_metadata=metadata,
        similarity_score=0.82
    )
    assert result["approved"] is False
    assert "detected wolf" in result["reason"]

def test_low_similarity_rejection():
    # PROBE 4: Match score below threshold -> MUST REJECT
    metadata = {"subject": "generic dog", "confidence": 0.85}
    result = check_mismatch_guard(
        post_topic="Behavior of Red Foxes in Forests",
        candidate_metadata=metadata,
        similarity_score=0.45  # Below 0.65 threshold
    )
    assert result["approved"] is False
    assert "below threshold" in result["reason"]

def test_low_confidence_flagging():
    # PROBE 1: Image confidence too low -> MUST REJECT
    metadata = {"subject": "red fox", "confidence": 0.50}  # Below 0.70 confidence
    result = check_mismatch_guard(
        post_topic="Behavior of Red Foxes in Forests",
        candidate_metadata=metadata,
        similarity_score=0.90
    )
    assert result["approved"] is False
    assert "Low image classification confidence" in result["reason"]