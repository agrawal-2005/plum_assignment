import os
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_TRACE"] = ""

import logging
logging.getLogger("google.auth.transport.requests").setLevel(logging.ERROR)

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from profiler import parser, factors, risk_classifier, recommender
from profiler.factors import configure_gemini
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger('google.auth.transport.requests')
log.setLevel(logging.ERROR)

configure_gemini()

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_health_data():
    try:
        text_input = request.form.get('textInput', '')
        image_file = request.files.get('imageInput')
        combined_text = text_input

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            text_from_image = parser.parse_image(image_path)
            combined_text = f"{text_input}\n{text_from_image}".strip()

        if not combined_text:
            return jsonify({"error": "No text or valid image was provided."}), 400

        extracted_factors = factors.extract_factors(combined_text)
        factors_list = extracted_factors.get("factors", [])

        risk_profile = risk_classifier.classify_risk(factors_list)
        recs = recommender.get_recommendations(risk_profile)
        recs = recs if isinstance(recs,list) else [str(recs)] if recs else []

        return jsonify({
            "extracted_text": combined_text,
            "factors": factors_list,
            "risk_level": risk_profile.get("risk_level", "Unknown"),
            "score": risk_profile.get("score", 0),
            "recommendations": recs
        })

    except Exception as e:
        print(f"Error in /api/analyze: {e}")
        return jsonify({"error": "Internal server error. Check backend logs."}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)