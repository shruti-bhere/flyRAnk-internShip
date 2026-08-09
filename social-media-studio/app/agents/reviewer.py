from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import AgentState
from app.config import OLLAMA_HOST, LLM_MODEL

llm = OllamaLLM(model=LLM_MODEL, base_url=OLLAMA_HOST)

REVIEWER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a Quality Assurance Editor for social media content. Evaluate tone, clarity, and formatting."),
    ("human", "Target Platform: {target_platform}\nDraft Post:\n{draft_content}\n\nReview the post. If acceptable, respond EXACTLY with 'STATUS: APPROVED'. Otherwise, respond with 'STATUS: REJECTED' followed by concise actionable feedback.")
])

def reviewer_node(state: AgentState) -> dict:
    chain = REVIEWER_PROMPT | llm
    review_result = chain.invoke({
        "target_platform": state["target_platform"],
        "draft_content": state["draft_content"]
    })
    
    revision_count = state.get("revision_count", 0) + 1
    
    if "STATUS: APPROVED" in review_result or revision_count >= 3:
        return {
            "review_status": "APPROVED",
            "feedback": "Approved",
            "revision_count": revision_count
        }
    else:
        return {
            "review_status": "REJECTED",
            "feedback": review_result,
            "revision_count": revision_count
        }