# recommender.py
import os
import google.generativeai as genai
from profiler import factors as factors_module  # <- import your factor.py module

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment.")
    genai.configure(api_key=api_key)

def get_recommendations(risk_profile: dict) -> dict:
    """
    Generate 3 short, actionable recommendations based on risk_level and factors.
    Uses the factors returned from factor.py instead of 'rationale'.
    """
    configure_gemini()
    model = genai.GenerativeModel('gemini-2.5-flash')

    # ✅ Use the factors list from risk_profile
    factors_list = risk_profile.get("factors", [])
    factors_str = ", ".join(factors_list) if factors_list else "No factors provided"
    risk_level = risk_profile.get("risk_level", "Unknown")
    num_recs = 3
    recommendations = []

    for i in range(num_recs):
        previous_recs = "; ".join(recommendations) if recommendations else "None"
        prompt = f"""
        A person has a "{risk_level}" health risk level, with contributing factors: {factors_str}.
        Generate 1 **short, actionable recommendation** (1 sentence only) in plain text.
        Make it different from previous recommendations: {previous_recs}.
        Do NOT write paragraphs. Output only the recommendation text.
        """
        try:
            response = model.generate_content(prompt)
            rec_text = getattr(response, "text", "").strip().replace('```', '').replace('\n', ' ').strip()
            if rec_text:
                recommendations.append(rec_text)
        except Exception as e:
            print(f"❌ Error generating recommendation {i+1}: {e}")
            recommendations.append("No recommendation available.")

    return {
        "risk_level": risk_level,
        "factors": factors_list,  # ✅ now returns the correct factors
        "recommendations": recommendations,
        "status": "ok" if recommendations else "error"
    }
