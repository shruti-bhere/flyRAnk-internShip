from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import AgentState

# Local Ollama Inference Model Initializer
llm = OllamaLLM(model="llama3")

# Prompt Template for Research Execution
RESEARCH_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert Social Media Researcher. Analyze the requested topic and generate concise, high-impact key points tailored for the target platform. Focus on accuracy, relevance, and current trends."),
    ("human", "Topic: {topic}\nTarget Platform: {target_platform}\n\nProvide 3 key research insights and bullet points to include in the post:")
])

def research_node(state: AgentState) -> dict:
    """
    Executes social media research based on topic and platform parameters.
    Updates the 'research_notes' key in the shared LangGraph state.
    """
    chain = RESEARCH_PROMPT | llm
    
    notes = chain.invoke({
        "topic": state["topic"],
        "target_platform": state["target_platform"]
    })
    
    return {"research_notes": notes}