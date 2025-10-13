import os
import json
import time
import google.generativeai as genai
import concurrent.futures
from dotenv import load_dotenv

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
                print(f"✅ Gemini API call successful on attempt {attempt+1}.")
                return response
        except concurrent.futures.TimeoutError:
            print(f"Attempt {attempt+1}/{retries} timed out after {timeout}s.")
        except Exception as e:
            print(f"❌ Attempt {attempt+1}/{retries} failed: {e}")
        time.sleep(2)
    raise RuntimeError(f"Gemini API call failed after {retries} retries.")

def clean_json_response(text: str) -> str:
    text = text.strip()
    start = text.find('{')
    if start == -1:
        return None
    end = text.rfind('}')
    if end == -1:
        return None
    
    return text[start : end + 1]

def extract_factors(text_data: str) -> dict:
    configure_gemini()
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

    prompt = f"""
    Analyze the following health data and identify potential risk factors.
    Your final output MUST be a single, valid JSON object with a key "factors" which is a list of these factor objects.
    
    Example output format:
    {{
      "factors": [
        {{
          "Smoking", "High Sugar Intake", "Lack of Exercise"
        }}
      ]
    }}

    Health Data to Analyze:
    ---
    {text_data}
    ---x
    """

    try:
        response = safe_generate_content(model, prompt)
        response_text = getattr(response, "text", "") 
        
        # print(f"\n💡 RAW GEMINI RESPONSE:\n---\n{response_text}\n---\n")
        
        json_string = clean_json_response(response_text)
        
        if json_string:
            try:
                result = json.loads(json_string)
                if "factors" not in result:
                    result["factors"] = []
                print(f"✅ Factors parsed successfully: {result}")
                return result
            except json.JSONDecodeError as e:
                print(f"❌ Factor extraction JSON decoding failed: {e}")
                return {"factors": []}
        else:
            print("❌ No valid JSON object found in the Gemini response.")
            return {"factors": []}

    except Exception as e:
        print(f"❌ CRITICAL error in factor extraction logic: {e}")
        return {"factors": []}

