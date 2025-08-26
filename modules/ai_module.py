# modules/ai_module.py
import requests

# Hugging Face free inference API
API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Free GPT-2 model for text generation
API_TOKEN = "YOUR_HUGGINGFACE_API_KEY"  # Replace with your free Hugging Face token

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def get_ai_advice(prompt="How can I feel better during my period?"):
    """
    Generate AI-based advice for user using Hugging Face Inference API.
    """
    payload = {"inputs": prompt}
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, dict) and "error" in result:
            return "🤖 AI temporarily unavailable. Please try again later."
        return str(result)
    except Exception as e:
        return "🤖 AI service error. Try again later."
