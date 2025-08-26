# modules/ai_module.py
import requests

# Free AI advice source using Hugging Face Inference API (no OpenAI key required)
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_API_TOKEN = "YOUR_HUGGINGFACE_TOKEN"  # Replace with your free Hugging Face token

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def get_ai_advice(prompt: str) -> str:
    """
    Get AI-based advice based on user's input.
    For example: prompt can be 'cramps' or 'mood low'.
    """
    try:
        payload = {"inputs": prompt}
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            # GPT-2 returns text under data[0]['generated_text']
            return data[0]['generated_text'] if data else "Here’s some advice: Take rest and stay hydrated!"
        else:
            return "AI service is unavailable. Try again later."
    except Exception as e:
        return f"Error fetching AI advice: {str(e)}"
