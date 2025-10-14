# 🧠 Health Risk Assessment API

An intelligent **Flask-based backend** that analyzes user health inputs, extracts key risk factors, determines overall risk level, and generates **personalized health recommendations** using **Google Gemini AI**.

---

## 📜 Problem Statement

Health-related data collected from individuals (like lifestyle habits, diet, and activity levels) is often unstructured and difficult to interpret.
This project aims to simplify that by providing a pipeline that can:

* Parse user health data (text or image)
* Extract risk-related factors using AI
* Classify the health risk level (Low, Medium, or High)
* Generate short, actionable health recommendations

All these functionalities are implemented as **modular Flask APIs** integrated with **Google Gemini AI**.

---

## 🚀 Features

✅ Parse user input (text or image)
✅ Extract risk factors using Gemini AI
✅ Classify user’s health risk level
✅ Generate AI-driven health recommendations
✅ Modular and easy to extend for medical or lifestyle data

---

## 🧩 Architecture Overview

```mermaid
flowchart TD
    A[User Input (Text/Image)] --> B[/api/parse]
    B --> C[/api/factors]
    C --> D[/api/risk]
    D --> E[/api/recommendations]
    E --> F[Final JSON Response]
```

### 🔍 Module Overview

| Module               | Description                                             |
| -------------------- | ------------------------------------------------------- |
| `parser.py`          | Extracts text from images using Gemini Vision           |
| `factors.py`         | Extracts key health-related factors from text           |
| `risk_classifier.py` | Classifies health risk level based on extracted factors |
| `recommender.py`     | Generates AI-driven health recommendations              |
| `app.py`             | Flask app integrating all modules into RESTful APIs     |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
https://github.com/agrawal-2005/plum_assignment.git
cd plum_assignment/backend
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Rename `.env.example` → `.env` and add your **Gemini API key**:

```
GEMINI_API_KEY=your_google_gemini_api_key
```

### Example `.env.example`

```
# Google Gemini API configuration
GEMINI_API_KEY=your_api_key_here

# Flask configuration
FLASK_ENV=development
```

### 5️⃣ Run the Flask Server

```bash
python app.py
```

Server will start at:

```
http://127.0.0.1:5000
```

### 6️⃣ (Optional) Expose Locally via ngrok

```bash
ngrok http 5000
```

Use the generated public link to test your APIs in Postman or your demo video.

---

## 🧰 Folder Structure

```
health-risk-assessment-api/
│
├── profiler/
│   ├── __init__.py
│   ├── parser.py
│   ├── factors.py
│   ├── risk_classifier.py
│   ├── recommender.py
│
├── uploads/                 # Uploaded images
├── app.py                   # Flask main entry point
├── requirements.txt
├── .env.example
├── README.md
└── tests/
    └── postman_collection.json
```

---

## 🌐 API Endpoints

| Endpoint               | Method | Description                                                           |
| ---------------------- | ------ | --------------------------------------------------------------------- |
| `/api/parse`           | `POST` | Parses user input (text or image) and extracts structured health data |
| `/api/factors`         | `POST` | Extracts key health-related risk factors                              |
| `/api/risk`            | `POST` | Classifies health risk level as *Low*, *Medium*, or *High*            |
| `/api/recommendations` | `POST` | Generates AI-based health recommendations                             |

---

## 🧪 Sample API Usage

### 🧠 1. Parse Image or Text

```bash
curl -X POST http://127.0.0.1:5000/api/parse \
```

### ⚙️ 2. Extract Risk Factors

```bash
curl -X POST http://127.0.0.1:5000/api/factors \
  -H "Content-Type: application/json" \
  -d '{"text": "Patient smokes occasionally and consumes high-sugar foods."}'
```

---

### 🔥 3. Classify Risk

```bash
curl -X POST http://127.0.0.1:5000/api/risk \
  -H "Content-Type: application/json" \
  -d '{"factors": ["smoking", "high sugar diet", "low activity"]}'
```

---

### 💡 4. Generate Recommendations

```bash
curl -X POST http://127.0.0.1:5000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"risk_profile": {"risk_level": "high", "factors": ["smoking", "low activity"]}}'
```

---

## 🧾 Postman Collection

You can import the file:

```
tests/postman_collection.json
```

This collection contains all four endpoints pre-configured and ready to run in sequence.

---

## 🎥 Demo Video

🎬 **Demo:** [[https://drive.google.com/file/d/1E5Y70hMg2R-muBn_z9HOuCZ2Yyl4rzq-/view?usp=sharing](https://drive.google.com/file/d/1E5Y70hMg2R-muBn_z9HOuCZ2Yyl4rzq-/view?usp=sharing)]
*(Shows all APIs working end-to-end on a local Flask server via ngrok)*

---

## 🧱 Tech Stack

* **Flask** – Lightweight Python web framework
* **Google Gemini AI** – For text and image-based health analysis
* **Python-dotenv** – For secure environment management
* **Pillow (PIL)** – For image processing
* **Requests / JSON** – For API data handling

---

## 📜 License

This project is licensed under the **MIT License** © 2025 **Prashant Agrawal**.

---

## 📬 Contact

**Prashant Agrawal**
📧 [agrawalprashant906@gmail.com](mailto:agrawalprashant906@gmail.com)
🔗 [GitHub](https://github.com/agrawal-2005)
🔗 [LinkedIn](https://www.linkedin.com/in/pr-shant26/)

---