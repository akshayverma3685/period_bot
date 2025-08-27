import requests

HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_API_TOKEN = "your hugging api token"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def get_ai_advice(prompt: str) -> str:
    """
    Returns AI-based advice based on user's input.
    """
    try:
        payload = {"inputs": prompt}
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data[0]['generated_text'] if data else "Take rest and stay hydrated!"
        else:
            return "AI service is unavailable. Try again later."
    except Exception as e:
        return f"Error fetching AI advice: {str(e)}"
