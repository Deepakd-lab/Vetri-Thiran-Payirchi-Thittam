# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight FastAPI + HTML/CSS educational assistant based on the supplied project documentation.

## Features

- Question answering
- Simple concept explanations
- Three-question MCQ quiz generation with four options per question
- Educational text summarization
- Personalized beginner-to-advanced learning paths
- Responsive web interface
- JSON APIs for every feature
- Optional local LaMini-Flan-T5 explanation module

## Architecture

```text
EduGenie/
├── main.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
└── README.md
```

## Quick start — Windows

Open the project folder in VS Code, then open a terminal:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and put your Gemini API key in:

```text
GEMINI_API_KEY=your_key_here
```

Start the server:

```powershell
python -m uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000`.

## Test the server

Health check:

```text
GET http://127.0.0.1:8000/health
```

Question-answer example:

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"Which is the largest ocean?\"}"
```

Quiz example:

```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"The Earth has seven continents and five oceans.\",\"count\":3}"
```

## Optional local explanation model

The supplied documentation specifies LaMini-Flan-T5-783M for concept explanations. The project therefore keeps a compatible local implementation, but it is disabled by default so that the normal setup stays lightweight.

Install the optional dependencies:

```powershell
pip install -r requirements-local.txt
```

Then set:

```text
USE_LOCAL_EXPLANATION=true
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first local explanation can take longer because the model is downloaded and loaded. If local loading fails, EduGenie automatically falls back to Gemini.

## Troubleshooting

### "GEMINI_API_KEY is not configured"

Make sure `.env` exists in the project root and contains:

```text
GEMINI_API_KEY=your_real_key
```

Restart Uvicorn after changing `.env`.

### Port 8000 is already in use

Run:

```powershell
python -m uvicorn main:app --reload --port 8001
```

Then visit `http://127.0.0.1:8001`.

### API quota or model error

Check the Gemini API key, enabled API access, account limits, and the value of `GEMINI_MODEL` in `.env`.

### Windows PowerShell execution policy

You can avoid activating the virtual environment and call its Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```
