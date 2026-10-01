$ErrorActionPreference = "Stop"

py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env. Add your GEMINI_API_KEY before starting the server."
}

Write-Host ""
Write-Host "Setup complete."
Write-Host "Run: .\.venv\Scripts\python.exe -m uvicorn main:app --reload"
