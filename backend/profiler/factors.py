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
            print(f"⚠️ Attempt {attempt+1}/{retries} timed out after {timeout}s.")
        except Exception as e:
            print(f"❌ Attempt {attempt+1}/{retries} failed: {e}")
        time.sleep(2)
    raise RuntimeError(f"Gemini API call failed after {retries} retries.")

def clean_json_response(text: str) -> str:
    text = text.strip()
    start_brace = text.find('{')
    start_bracket = text.find('[')
    if start_brace == -1 and start_bracket == -1:
        raise ValueError("No JSON object or array found in the response.")
    if start_brace != -1 and (start_bracket == -1 or start_brace < start_bracket):
        start_index = start_brace
        end_char = '}'
    else:
        start_index = start_bracket
        end_char = ']'
    end_index = text.rfind(end_char)
    if end_index == -1:
        raise ValueError("Malformed JSON string in response.")
    return text[start_index : end_index + 1]

def extract_factors(text_data: str) -> dict:
    configure_gemini()
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Based on the following health data, identify potential risk factors.
    The output MUST be a valid JSON object:
    {{
      "factors": [
        {{
          "factor": "example",
          "confidence": 0.87
        }}
      ]
    }}
    Health Data:
    \"\"\"{text_data}\"\"\"
    """

    try:
        response = safe_generate_content(model, prompt)
        response_text = getattr(response, "text", str(response))
        
        try:
            # Attempt to clean and parse JSON
            json_response = clean_json_response(response_text)
            result = json.loads(json_response)
            if "factors" not in result:
                result["factors"] = []
        except Exception as parse_error:
            print(f"❌ Factor extraction parsing failed: {parse_error}")
            result = {"factors": []}

        return result

    except Exception as e:
        print(f"❌ Error in Gemini API call for factor extraction: {e}")
        return {"factors": []}
