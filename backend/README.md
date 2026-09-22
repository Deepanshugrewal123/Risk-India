# RISK // INDIA — FastAPI Backend

FastAPI backend architecture for **RISK // INDIA: AI-Powered Disaster Risk Analyzer & Management System**.

## 🚀 Overview

The backend serves multi-hazard disaster risk assessments, telemetry factors, active incident monitoring, and verified relief directories across **all 28 States and 8 Union Territories of India**.

- **Framework**: FastAPI (Python 3.10+)
- **Database ORM**: SQLAlchemy 2.0 (PostgreSQL-ready with local SQLite fallback)
- **ML Interface**: Decoupled prediction interface loaded with trained Assam flood model prototype (`assam_flood_prototype_v1`)
- **Status**: Operational backend serving multi-hazard telemetry, live feeds, and ML inference

---

## 📁 Architecture

```
backend/
├── app/
│   ├── main.py                  # App entrypoint, CORS, exception handlers
│   ├── config.py                # Environment configuration
│   ├── database/
│   │   ├── database.py          # SQLAlchemy engine & session factory
│   │   └── init_db.py           # DB creation & seed script (36 locations)
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── location.py          # Location (28 States + 8 UTs)
│   │   ├── risk_assessment.py   # Multi-hazard assessments
│   │   ├── risk_factor.py       # SHAP-compatible explainability factors
│   │   ├── disaster_event.py    # Incidents & alerts
│   │   └── resource.py          # Helplines, shelters, verified NGOs
│   ├── schemas/                 # Pydantic validation schemas
│   ├── services/                # Decoupled business logic
│   ├── ml/                      # Abstract ML model interface
│   ├── utils/                   # Centralized provisional risk classifier
│   └── api/
│       ├── router.py            # Main API router
│       └── routes/              # Sub-routers (/health, /locations, /risk, etc.)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🛠️ Local Development Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default configuration uses SQLite (`risk_india.db`). To connect to PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/risk_india
```

### 3. Initialize & Seed Database
Seeds all 36 Indian States and Union Territories with baseline risk assessments:
```bash
python -m app.database.init_db
```

### 4. Start Development Server
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Operational health check |
| `GET` | `/api/locations` | All 36 Indian States & UTs (`?type=STATE` or `?type=UNION_TERRITORY`) |
| `GET` | `/api/locations/{id}` | State or UT details by ID (e.g. `assam`, `ladakh`) or code (`AS`, `DL`) |
| `GET` | `/api/risk/{location_id}` | Latest risk assessment and explainable factors |
| `POST` | `/api/risk/analyze` | Predictive risk analysis for feature inputs (e.g. rainfall, soil moisture) |
| `GET` | `/api/disasters` | Incident alerts with filters (`?state=`, `?type=`, `?status=`) |
| `GET` | `/api/disasters/{id}` | Single disaster event details |
| `GET` | `/api/resources` | Relief directory with filters (`?location=`, `?type=`, `?verification_status=`) |
| `GET` | `/docs` | Interactive Swagger / OpenAPI documentation |
| `GET` | `/redoc` | ReDoc API specification |

---

## 🔗 Frontend Connection

The existing React + Vite frontend communicates with this backend by configuring:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```
In `src/config/api.ts`, toggle `USE_MOCK_DATA = false` to switch from local mock service to live FastAPI responses.
