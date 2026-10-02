from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = Path(__file__).resolve().parent / "model"
FRONTEND_DIR = BASE_DIR / "frontend"
MAX_INPUT_CHARS = 30_000


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_INPUT_CHARS)


class SummarizeResponse(BaseModel):
    summary: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not MODEL_DIR.exists():
        raise RuntimeError(f"Model directory not found: {MODEL_DIR}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR, local_files_only=True)
    model.to(device)
    model.eval()

    app.state.tokenizer = tokenizer
    app.state.model = model
    app.state.device = device
    yield
    del app.state.model
    del app.state.tokenizer
    if device.type == "cuda":
        torch.cuda.empty_cache()


app = FastAPI(title="Text Summarizer API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health() -> dict[str, str]:
    device = getattr(app.state, "device", None)
    return {"status": "ok", "device": str(device) if device else "loading"}


@app.post("/api/summarize", response_model=SummarizeResponse)
async def summarize(payload: SummarizeRequest) -> SummarizeResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Text must not be empty.")

    tokenizer: Any = app.state.tokenizer
    model: Any = app.state.model
    device = app.state.device

    try:
        # The checkpoint was trained as a T5 summarizer with this task prefix.
        inputs = tokenizer(
            "summarize: " + text,
            max_length=512,
            truncation=True,
            return_tensors="pt",
        )
        inputs = {key: value.to(device) for key, value in inputs.items()}
        with torch.inference_mode():
            output_ids = model.generate(
                **inputs,
                max_length=200,
                min_length=30,
                num_beams=4,
                length_penalty=2.0,
                no_repeat_ngram_size=3,
                early_stopping=True,
            )
        summary = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
        if not summary:
            raise RuntimeError("The model returned an empty summary.")
        return SummarizeResponse(summary=summary)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Summarization failed.") from exc


if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")
