from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    topic: str
    target_platform: str
    research_notes: str
    draft_content: str
    review_status: str  # "APPROVED" or "REJECTED"
    feedback: str
    revision_count: int