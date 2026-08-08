import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def step2_generate_draft(keypoints: str) -> str:
    prompt = f"""
    You are a technical content strategist. Take the key points below and expand them into 
    a structured study note / industry brief draft.
    
    KEY POINTS:
    {keypoints}
    
    STRUCTURE REQUIRED:
    1. Executive Summary
    2. Detailed Breakdown (with 3 subheadings)
    3. Practical Takeaways / Next Steps
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content