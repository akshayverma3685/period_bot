import requests

HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_API_TOKEN = ""  # optional for public models

def get_ai_advice(symptoms=None, mood=None, cycle_info=None):
    prompt = "You are a helpful menstrual health assistant.\n"
    if symptoms:
        prompt += f"Symptoms: {symptoms}\n"
    if mood:
        prompt += f"Mood: {mood}\n"
    if cycle_info:
        prompt += f"Last period: {cycle_info.get('last_period')}, Cycle length: {cycle_info.get('cycle_length')}\n"
    prompt += "Give simple, practical advice for this user."

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}
    payload = {"inputs": prompt, "parameters":{"max_new_tokens":100}}

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=15)
        result = response.json()
        if isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text']
        elif isinstance(result, dict) and 'error' in result:
            return "Sorry, AI advice unavailable right now."
        return "💡 Try relaxing and taking care of yourself today."
    except Exception as e:
        return f"💡 AI not reachable: {str(e)}"
