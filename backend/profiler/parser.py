import os
import json
from PIL import Image
import google.generativeai as genai
from .factors import configure_gemini, safe_generate_content

def parse_image(image_path: str) -> str:
    configure_gemini()
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    try:
        print("🖼️  Opening image for Gemini Vision...")
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

