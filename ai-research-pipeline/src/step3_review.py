import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def step3_review_and_format(draft_text: str) -> str:
    prompt = f"""
    Act as a senior editor. Review the draft below for logical flow, clarity, and precision.
    
    DRAFT:
    {draft_text}
    
    TASKS:
    1. Add a brief 'Human Review Needed' note identifying potential hallucination risks.
    2. Format the output into clean, professional Markdown.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content