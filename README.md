# 🧠 Health Profiler — AI-Powered Health Risk Analysis using Gemini

## 📘 Problem Statement

In modern healthcare, individuals often lack personalized insights into their health risks unless they undergo professional consultations or diagnostic tests.
However, with advancements in **AI and large language models**, it’s now possible to analyze user responses or medical data to identify potential **risk factors** and generate **personalized recommendations** — even from natural language or image-based inputs.

The **Health Profiler** project addresses this by building an **end-to-end AI-driven system** that:

* Extracts potential health risk factors from user input (text or image),
* Classifies the user's overall health risk level,
* Generates short, actionable recommendations using Gemini.

---

## 🚀 Project Overview

The **Health Profiler** uses **Google Gemini 2.5 Flash**, **Flask**, and **Python** to create an intelligent, interactive backend that performs:

| Step | Module               | Description                                                                                           |
| ---- | -------------------- | ----------------------------------------------------------------------------------------------------- |
| 1️⃣  | `parser.py`          | Extracts health-related text from uploaded images (using Gemini Vision).                              |
| 2️⃣  | `factors.py`         | Extracts possible risk factors (like “smoking”, “poor diet”, etc.) from text or parsed image content. |
| 3️⃣  | `risk_classifier.py` | Assigns a risk score and risk level (`low`, `medium`, or `high`) based on extracted factors.          |
| 4️⃣  | `recommender.py`     | Uses prompt engineering to generate diverse, actionable health recommendations per risk profile.      |
| 5️⃣  | `app.py`             | Flask backend that orchestrates all steps and exposes REST APIs for frontend or testing.              |

---

## 🧩 System Architecture

```
                ┌─────────────────────────────┐
                │        User Interface        │
                │  (Frontend or API Client)    │
                └──────────────┬───────────────┘
                               │
                               ▼
                    ┌───────────────────┐
                    │      app.py       │
                    │ Flask Orchestration│
                    └─────────┬─────────┘
                              │
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                                                                         │
 │   Step 1: parser.py   → Extracts text from image inputs (Gemini Vision) │
 │   Step 2: factors.py  → Finds risk factors via Gemini LLM               │
 │   Step 3: risk_classifier.py → Classifies user risk (rule-based)        │
 │   Step 4: recommender.py → Generates unique recommendations             │
 │                                                                         │
 └─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ JSON API Response │
                    └───────────────────┘
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/health-profiler.git
cd health-profiler/backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Environment Variables

Create a `.env` file in the backend directory:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run the Flask App

```bash
python app.py
```

It runs at:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧠 API Endpoints

### **1️⃣ /api/parse**

**Description:** Accepts text and/or image input → Extracts risk factors → Classifies risk → Generates recommendations.

**Method:** `POST`
**Body (form-data):**

```
textInput: "I smoke occasionally and eat fast food."
imageInput: <optional .jpg/.png image>
```

**Response:**

```json
{
  "extracted_text": "I smoke occasionally and eat fast food.",
  "factors": ["smoking", "poor diet"],
  "risk_level": "high",
  "score": 78,
  "recommendations": [
    "Reduce smoking frequency and seek medical help.",
    "Add fresh fruits and vegetables to your daily meals.",
    "Schedule regular exercise sessions at least 3 times per week."
  ]
}
```

---

### **2️⃣ /api/factors**

**Description:** Extracts risk factors from structured user answers (Step 2).

**Method:** `POST`
**JSON Input:**

```json
{
  "answers": {
    "diet": "I eat a lot of junk food.",
    "exercise": "I rarely work out.",
    "habits": "I smoke occasionally."
  }
}
```

**Response:**

```json
{
  "factors": ["smoking", "poor diet", "low exercise"],
  "confidence": 0.88
}
```

---

### **3️⃣ /api/risk**

**Description:** Classifies risk level from extracted factors.

**Method:** `POST`
**Input:**

```json
{
  "factors": ["smoking", "poor diet", "low exercise"]
}
```

**Response:**

```json
{
  "risk_level": "high",
  "score": 78,
  "rationale": ["smoking", "poor diet", "low exercise"]
}
```

---

### **4️⃣ /api/recommendations**

**Description:** Generates multiple diverse recommendations using prompt engineering.

**Method:** `POST`
**Input:**

```json
{
  "risk_level": "high",
  "rationale": ["smoking", "poor diet", "low activity"]
}
```

**Response:**

```json
{
  "risk_level": "high",
  "factors": ["smoking", "poor diet", "low activity"],
  "recommendations": [
    "Reduce smoking gradually over two weeks.",
    "Add fresh vegetables and fiber to your meals.",
    "Start a daily 15-minute walk routine."
  ],
  "status": "ok"
}
```

---

## 🧰 Folder Structure

```
health-profiler/
│
├── backend/
│   ├── app.py                 # Flask main file (API orchestration)
│   ├── profiler/
│   │   ├── parser.py          # Image-to-text using Gemini Vision
│   │   ├── factors.py         # Factor extraction via Gemini LLM
│   │   ├── risk_classifier.py # Rule-based health risk scoring
│   │   ├── recommender.py     # Prompt-engineered recommendations
│   │   └── __init__.py
│   ├── uploads/               # Stores uploaded user images
│   ├── .env                   # Gemini API key
│   └── requirements.txt
│
└── frontend/
    ├── index.html
    ├── static/
    ├── scripts/
    └── styles/
```

---

## 🧪 Example Workflow

1️⃣ User submits health text or uploads image →
2️⃣ Backend extracts possible **risk factors** using Gemini →
3️⃣ Risk score is calculated (rule-based classifier) →
4️⃣ **Unique recommendations** are generated (Gemini prompt engineering) →
5️⃣ Results returned as JSON to frontend.

---

## 💡 Features

✅ Accepts **both text and image inputs**
✅ Uses **Gemini 2.5 Flash API** for fast, multimodal processing
✅ Follows a modular **4-step pipeline** (Extract → Classify → Recommend)
✅ Generates **unique recommendations per loop** using prompt engineering
✅ Provides **REST APIs** for easy frontend or mobile integration

---

## 🧠 Future Improvements

* Integrate **user profile history** for trend analysis
* Add **nutrition & fitness tracking APIs**
* Deploy using **Docker + Gunicorn + GCP Cloud Run**
* Implement **database logging (PostgreSQL)** for analytics

---

## 👨‍💻 Author

**Prashant Agrawal**
B.Tech (ECE) @ IIIT Allahabad

* 🔗 [GitHub](https://github.com/agrawal-2005)
* 🔗 [LinkedIn](https://www.linkedin.com/in/pr-shant26/)
* 📧 [agrawalprashant906@gmail.com](mailto:agrawalprashant906@gmail.com)