import os
import json
from groq import Groq
from app.schema import ImageMetadata

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

def process_image_with_vision(image_url: str) -> dict:
    try:
        # Groq uses an OpenAI-compatible interface
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", # or active Groq vision model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "Analyze this image and return JSON with keys: subject, category, attributes (list), caption, and confidence (float 0.0-1.0)."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"}
        )

        raw_json = response.choices[0].message.content
        parsed_data = json.loads(raw_json)

        # Schema validation
        validated_metadata = ImageMetadata(**parsed_data)

        return {
            "status": "SUCCESS",
            "data": validated_metadata.model_dump(),
            "estimated_cost_usd": 0.0000  # Groq Free Tier
        }

    except Exception as e:
        return {
            "status": "FAILED",
            "error": str(e),
            "estimated_cost_usd": 0.0000
        }