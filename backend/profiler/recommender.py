import os
import google.generativeai as genai
import json

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment.")
    genai.configure(api_key=api_key)

def get_recommendations(risk_profile: dict) -> dict:
    configure_gemini()
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    factors_str = ", ".join(risk_profile.get("rationale", []))
    risk_level = risk_profile.get("risk_level", "Unknown")

    prompt = f"""
    A person has a "{risk_level}" health risk level, with contributing factors: {factors_str}.
    Generate 3-5 actionable, supportive health improvement recommendations.
    Output format:
    {{"recommendations": ["..."]}}
    """
    try:
        response = model.generate_content(prompt)
        json_response = response.text.strip().replace('```json', '').replace('```', '').strip()
        return json.loads(json_response)
    except Exception as e:
        print(f"Error in Gemini API call for recommendations: {e}")
        return {"recommendations": ["Could not generate recommendations at this time."]}
