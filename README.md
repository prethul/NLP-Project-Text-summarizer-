# Briefly — local text summarizer

This app serves the uploaded Hugging Face T5 checkpoint through FastAPI and a plain HTML/CSS/JavaScript UI. The checkpoint is loaded once during application startup; no pretrained model is downloaded or retrained.

## Project layout

```text
text-summarizer/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── model/                 # uploaded model.safetensors + tokenizer files
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md
```

## Run locally

From the project root in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
uvicorn backend.app:app --reload
```

Open http://127.0.0.1:8000. The API is available at `POST http://127.0.0.1:8000/api/summarize` with `{"text":"..."}`.

The server uses CUDA automatically when `torch.cuda.is_available()` is true; otherwise it runs on CPU. The uploaded checkpoint's saved summarization configuration is used: `summarize: ` prefix, 512-token input truncation, 4 beams, maximum output length 200, minimum output length 30, length penalty 2.0, and no repeated 3-grams.
