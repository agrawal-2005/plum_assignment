import os
import json
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from profiler import parser, factors as factors_module, risk_classifier, recommender
from profiler.factors import configure_gemini

load_dotenv()
configure_gemini()

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/parse', methods=['POST'])
def parse_api():
    try:
        text_input = request.form.get('textInput', '')
        image_file = request.files.get('imageInput')
        combined_text = text_input

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            text_from_image = parser.parse_image(image_path)
            combined_text = f"{text_input} {text_from_image}".strip()

        if not combined_text:
            return jsonify({
                "status": "incomplete_profile",
                "reason": "No text or valid image was provided."
            }), 400

        parsed_data = parser.parse_text_to_json(combined_text)

        if parsed_data.get("status") in ["incomplete_profile", "error"]:
            return jsonify(parsed_data), 400 if parsed_data.get("status") == "incomplete_profile" else 500

        return jsonify(parsed_data)

    except Exception as e:
        print(f"CRITICAL Error in /api/parse: {e}")
        return jsonify({"error": "Internal server error. Check backend logs."}), 500


@app.route('/api/factors', methods=['POST'])
def extract_factors_api():
    try:
        data = request.get_json()
        if not data or "answers" not in data:
            return jsonify({
                "status": "incomplete_profile",
                "reason": "Missing 'answers' field in input."
            }), 400

        text_data = json.dumps(data["answers"], indent=2)
        extracted = factors_module.extract_factors(text_data)

        if extracted is None or "factors" not in extracted:
             raise ValueError("Failed to get a valid response from the extraction model.")

        result = {
            "factors": extracted.get("factors", []),
            "confidence": extracted.get("confidence", 0.88)
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "Internal server error during factor extraction."}), 500


@app.route('/api/risk', methods=['POST'])
def classify_risk_api():
    try:
        data = request.get_json()
        factors_list = data.get("factors", [])
        if not factors_list:
            return jsonify({
                "status": "incomplete_profile",
                "reason": "No factors provided for risk classification."
            }), 400
        result = risk_classifier.classify_risk(factors_list)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Internal server error during risk classification."}), 500


@app.route('/api/recommendations', methods=['POST'])
def generate_recommendations_api():
    try:
        data = request.get_json()
        # FIXED: Check for 'factors' instead of 'rationale'
        if not data or "risk_level" not in data or "factors" not in data:
            return jsonify({
                "status": "incomplete_profile",
                "reason": "Missing required fields: risk_level or factors."
            }), 400
        recs = recommender.get_recommendations(data)
        return jsonify(recs)
    except Exception as e:
        return jsonify({"error": "Internal server error during recommendation generation."}), 500


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

