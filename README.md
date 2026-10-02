# 📝 Text Summarizer

A lightweight **local text summarization web application** powered by a fine-tuned **Hugging Face T5 model**. The application uses **FastAPI** for the backend and a simple, modern **HTML/CSS/JavaScript** frontend.

The trained T5 checkpoint is loaded once when the application starts. The model is **not retrained** and no external pretrained model is downloaded at runtime.

## 🚀 Live Demo

🔗 **[Try the Text Summarizer](https://text-summarizer-g0cw.onrender.com)**

---

## ✨ Features

* 🤖 T5-based text summarization
* ⚡ FastAPI backend
* 🎨 Simple and responsive web interface
* 💻 Runs locally without model retraining
* 🧠 Loads the uploaded Hugging Face checkpoint at startup
* 🚀 Automatically uses **GPU (CUDA)** when available
* 🖥️ Falls back to **CPU** when CUDA is unavailable
* 🔌 REST API endpoint for summarization

---

## 🛠️ Tech Stack

**Backend**

* Python
* FastAPI
* Uvicorn
* PyTorch
* Hugging Face Transformers

**Frontend**

* HTML
* CSS
* JavaScript

**Model**

* Fine-tuned T5 checkpoint
* `model.safetensors`
* Hugging Face tokenizer files

---

## 📂 Project Structure

```text
text-summarizer/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── model/
│       ├── model.safetensors
│       ├── tokenizer files
│       └── configuration files
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
```

---

## ⚙️ Model Configuration

The application uses the summarization configuration saved with the trained checkpoint:

| Parameter             |        Value |
| --------------------- | -----------: |
| Task Prefix           | `summarize:` |
| Maximum Input Length  |   512 tokens |
| Number of Beams       |            4 |
| Maximum Output Length |   200 tokens |
| Minimum Output Length |    30 tokens |
| Length Penalty        |          2.0 |
| No Repeat N-Gram Size |            3 |

These settings are applied during text generation to produce concise and readable summaries.

---

## 💻 Run Locally

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd text-summarizer
```

### 2. Create a Virtual Environment

```powershell
py -m venv .venv
```

### 3. Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 5. Install Dependencies

```powershell
pip install -r backend\requirements.txt
```

### 6. Start the FastAPI Server

```powershell
uvicorn backend.app:app --reload
```

### 7. Open the Application

Open your browser and visit:

```text
http://127.0.0.1:8000
```

---

## 🔌 API

The summarization API is available at:

```text
POST /api/summarize
```

### Request

```json
{
  "text": "Your long text goes here..."
}
```

### Example

```bash
curl -X POST "http://127.0.0.1:8000/api/summarize" ^
-H "Content-Type: application/json" ^
-d "{\"text\":\"Your long text goes here...\"}"
```

### Response

```json
{
  "summary": "Generated summary of the input text."
}
```

---

## 🧠 How It Works

```text
User Input
    ↓
Frontend (HTML/CSS/JS)
    ↓
FastAPI Backend
    ↓
T5 Tokenizer
    ↓
Fine-Tuned T5 Model
    ↓
Text Generation
    ↓
Generated Summary
    ↓
Frontend UI
```

The model is loaded once during application startup and reused for incoming summarization requests.

---

## 📌 Notes

* The application uses the uploaded trained checkpoint located in `backend/model/`.
* No model retraining is performed when the application starts.
* CUDA is automatically selected when a compatible GPU is available.
* CPU is used as a fallback when CUDA is unavailable.
* Input text is truncated to a maximum of **512 tokens** according to the saved model configuration.

---

## 🌐 Deployment

The application is deployed online using **Render**.

🔗 **Live Application:**
https://text-summarizer-g0cw.onrender.com

---

## 👨‍💻 Author

Developed as a machine learning and web deployment project using **T5, PyTorch, FastAPI, and JavaScript**.

⭐ Feel free to explore the project and try the live demo.
