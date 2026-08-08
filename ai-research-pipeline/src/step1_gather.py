import os
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def step1_gather_keypoints(raw_text: str) -> str:
    prompt = f"""
    You are an expert research assistant. Analyze the following raw text and extract 
    the top 5 key concepts, facts, and main themes.
    
    RAW TEXT:
    {raw_text[:4000]}
    
    OUTPUT FORMAT: Bullet points highlighting core takeaways.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content