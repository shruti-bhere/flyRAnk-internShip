from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import AgentState
from app.config import OLLAMA_HOST, LLM_MODEL

llm = OllamaLLM(model=LLM_MODEL, base_url=OLLAMA_HOST)

WRITER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert Social Media Content Creator. Craft engaging, platform-tailored posts based on research notes and reviewer feedback."),
    ("human", "Platform: {target_platform}\nResearch Notes:\n{research_notes}\n\nReviewer Feedback to fix (if any): {feedback}\n\nDraft the complete post:")
])

def writer_node(state: AgentState) -> dict:
    chain = WRITER_PROMPT | llm
    draft = chain.invoke({
        "target_platform": state["target_platform"],
        "research_notes": state["research_notes"],
        "feedback": state.get("feedback", "None")
    })
    return {"draft_content": draft}