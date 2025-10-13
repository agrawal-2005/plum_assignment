import os
import json
from PIL import Image
import google.generativeai as genai
from .factors import configure_gemini, safe_generate_content

def parse_image(image_path: str) -> str:
    """
    Uses Gemini Vision to perform OCR on a survey image.
    """
    configure_gemini()
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
    
    try:
        img = Image.open(image_path)
        prompt = """
        Analyze the image of this lifestyle or medical survey form.
        Extract all key fields and their corresponding values as plain text.
        Combine them into a single, comma-separated string.
        Example: "age: 42, smoker: true, exercise: rarely, diet: high sugar"
        If no relevant text is found, return an empty string.
        """
        
        response = safe_generate_content(model, [prompt, img])
        
        text_from_image = getattr(response, "text", "").strip()
        print(f"✅ Gemini Vision extracted: {text_from_image}")
        return text_from_image

    except Exception as e:
        print(f"❌ Error in Gemini Vision API call: {e}")
        return ""

def parse_text_to_json(text_input: str) -> dict:
    """
    Uses a generative model to parse raw text and then constructs a valid
    JSON object in Python, which is more reliable than asking the model
    to return perfect JSON.
    """
    configure_gemini()
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

    # A simpler prompt asking for a predictable key-value format.
    prompt = f"""
    Analyze the text below. Extract values for 'age', 'smoker', 'exercise', and 'diet'.
    Return the result as a single line of semicolon-separated key:value pairs.
    
    Example: age:42;smoker:true;exercise:rarely;diet:high sugar

    Input Text:
    ---
    {text_input}
    ---
    """

    try:
        response = safe_generate_content(model, prompt)
        response_text = response.text.strip()
        print(f"✅ Gemini simple string response: {response_text}")

        # --- START: RELIABLE JSON CONSTRUCTION ---
        answers = {}
        target_fields = ['age', 'smoker', 'exercise', 'diet']
        
        # Parse the model's simple string response
        pairs = response_text.split(';')
        for pair in pairs:
            if ':' in pair:
                key, value = [p.strip() for p in pair.split(':', 1)]
                if key in target_fields:
                    # Perform type conversion
                    if key == 'age':
                        answers[key] = int(value)
                    elif key == 'smoker':
                        answers[key] = value.lower() in ['true', 'yes']
                    else:
                        answers[key] = value

        missing_fields = [field for field in target_fields if field not in answers]
        
        # Apply the guardrail condition
        if len(answers) < 2:
            print("❌ Guardrail triggered: >50% fields missing.")
            return {"status": "incomplete_profile", "reason": ">50% fields missing"}

        # Construct the final, guaranteed-valid JSON object
        result = {
            "answers": answers,
            "missing_fields": missing_fields,
            "confidence": 0.95  # Static confidence for this reliable method
        }
        print(f"✅ Successfully constructed JSON: {result}")
        return result
        # --- END: RELIABLE JSON CONSTRUCTION ---

    except Exception as e:
        print(f"❌ Error during manual JSON construction: {e}")
        return {
            "status": "error",
            "reason": "Failed to process the model's response."
        }

