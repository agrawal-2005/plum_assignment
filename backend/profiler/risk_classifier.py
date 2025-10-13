import os
import json
import time
import google.generativeai as genai
import concurrent.futures
from dotenv import load_dotenv

# It's good practice to have configure_gemini and other helpers available here too.
load_dotenv()

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment.")
    genai.configure(api_key=api_key)

def safe_generate_content(model, prompt, retries=3, timeout=60):
    for attempt in range(retries):
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(model.generate_content, prompt)
                response = future.result(timeout=timeout)
                print(f"✅ Risk classification Gemini call successful on attempt {attempt+1}.")
                return response
        except concurrent.futures.TimeoutError:
            print(f"Attempt {attempt+1}/{retries} timed out.")
        except Exception as e:
            print(f"❌ Attempt {attempt+1}/{retries} failed: {e}")
        time.sleep(2)
    raise RuntimeError(f"Gemini API call failed after {retries} retries.")

def clean_json_response(text: str) -> str:
    """Finds and extracts a JSON object from a string."""
    start = text.find('{')
    if start == -1:
        return None
    end = text.rfind('}')
    if end == -1:
        return None
    return text[start : end + 1]

def classify_risk(factors):
    """
    Dynamically computes risk level, score, and rationale using a generative model.
    """
    if not factors:
        return {
            "risk_level": "unknown",
            "score": 0,
            "rationale": ["No factors provided."],
            "status": "incomplete_profile"
        }

    # Configure the model for this specific task
    configure_gemini()
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

    # Convert the factor data into a simple string for the prompt
    factors_string = json.dumps(factors[0] if factors else {})

    prompt = f"""
    Analyze the following health risk factors and generate a risk profile.
    
    Instructions:
    1.  Calculate a numerical "score" from 0 to 100, where 100 is the highest risk.
    2.  Determine a "risk_level" (low, medium, or high) based on the score.
    3.  Provide a "rationale" as a list of short strings, explaining the main reasons for the score.
    
    Your final output MUST be a single, valid JSON object containing only these three keys: "risk_level", "score", and "rationale".
    
    Example Output:
    {{
      "risk_level": "high",
      "score": 78,
      "rationale": ["Smoking is a major risk factor.", "Diet is high in sugar.", "Lack of regular exercise."]
    }}
    
    Factors to Analyze:
    ---
    {factors_string}
    ---
    """

    try:
        response = safe_generate_content(model, prompt)
        response_text = getattr(response, "text", "")
        
        json_string = clean_json_response(response_text)
        
        if json_string:
            try:
                result = json.loads(json_string)
                # Ensure all required keys are present
                if all(key in result for key in ["risk_level", "score", "rationale"]):
                    print(f"✅ Risk profile generated successfully: {result}")
                    return result
                else:
                     raise ValueError("Model response was missing required keys.")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"❌ Risk classification JSON parsing failed: {e}")
        
        return {
            "risk_level": "error",
            "score": -1,
            "rationale": ["Failed to generate a valid risk profile from the model."]
        }

    except Exception as e:
        print(f"❌ CRITICAL error during risk classification: {e}")
        return {
            "risk_level": "error",
            "score": -1,
            "rationale": ["An unexpected server error occurred."]
        }

if __name__ == "__main__":
    test_factors = [{"Smoking": True, "High Sugar Intake": True, "Lack of Exercise": True}]
    output = classify_risk(test_factors)
    print("\n--- TEST OUTPUT ---")
    print(json.dumps(output, indent=4))
    print("--- END TEST ---\n")

