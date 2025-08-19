Run local
python -m venv .venv
..venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
Docs at /docs
