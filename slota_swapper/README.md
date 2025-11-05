SlotSwapper Backend (FastAPI + SQLAlchemy + PostgreSQL)

Prerequisites
- Python 3.10+
- PostgreSQL 13+

Setup
1) Create and activate a virtual environment
```bash
python -m venv .venv
. .venv/Scripts/activate
```

2) Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3) Configure environment
- Copy `.env.example` to `.env` and fill values:
  - `DATABASE_URL` example: `postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DBNAME`
  - `SECRET_KEY` any strong random string
  - `ACCESS_TOKEN_EXPIRE_MINUTES` e.g. `60`

4) Run the app
```bash
uvicorn slota_swapper.main:app --reload
```

Project Structure
```
slota_swapper/
├── .env.example
├── README.md
├── requirements.txt
├── main.py
├── database.py
├── models/
│   └── user.py
├── schemas/
│   ├── user_schemas.py
│   └── auth_schemas.py
├── auth/
│   ├── jwt_handler.py
│   └── security.py
└── routers/
    └── auth.py
```

Notes
- On first start, tables are created automatically on app startup.
- Default token algorithm: HS256. Update `SECRET_KEY` and rotate if needed.


