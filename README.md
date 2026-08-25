# WatchSphere AI – Customer Insights Platform Version 3.0

> **AI Powered Enterprise Customer Analytics & Business Intelligence Platform**
> 
> **Author**: Powered by Saniya Maner  
> **Program**: Infosys Internship Project 2026  
> **Phase**: Phase 1 Enterprise Foundation & Architecture

---

## 🌟 Executive Overview

**WatchSphere AI Version 3.0** is an enterprise-grade customer intelligence and analytics platform engineered to deliver real-time business intelligence, predictive customer behavior insights, and automated analytics. 

Phase 1 establishes the production-grade foundation, clean architecture, security middleware, database abstraction layer, modular configuration, and Streamlit presentation shell.

---

## 🚀 Tech Stack

### Frontend Stack
* **Language**: Python 3.10+
* **Framework**: Streamlit `v1.32+`
* **Navigation**: `streamlit-option-menu`
* **UI Components & Extras**: `streamlit-extras`
* **Data Visualization Prep**: Plotly, Pandas, AgGrid
* **Styling**: Custom Glassmorphism CSS (`assets/css/style.css`)

### Backend Stack
* **API Framework**: FastAPI `v0.110+`
* **ORM & Database**: SQLAlchemy `2.0+`, SQLite (default), Alembic
* **Validation & Settings**: Pydantic `v2`, `pydantic-settings`
* **Security & Auth**: JWT (`python-jose`), Passlib (`bcrypt`), OAuth2
* **Server**: Uvicorn (ASGI Driver)
* **Logging & Monitoring**: Loguru (Daily rotating system & error log streams)

---

## 📁 Complete Folder Structure

```text
WatchSphereAI/
│
├── assets/                  # Static design & branding assets
│   ├── css/
│   │   └── style.css        # Enterprise glassmorphism & design system tokens
│   ├── js/                  # Frontend scripts
│   ├── icons/               # Platform icon set
│   └── images/              # Branding graphics
│
├── backend/                 # Asynchronous FastAPI Backend Application
│   ├── api/
│   │   ├── __init__.py
│   │   └── router.py        # Centralized v1 API routing hub
│   ├── auth/                # Security dependencies & role validators
│   │   ├── dependencies.py  # OAuth2 & RBAC role checkers
│   │   ├── jwt.py           # Token creation & decoding helpers
│   │   └── password.py      # Passlib bcrypt hashing
│   ├── core/                # Core exception hierarchy & system configs
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── database/            # SQLAlchemy 2.0 metadata & migration Base
│   │   └── base.py
│   ├── middleware/          # HTTP request logging & error handling
│   │   ├── error_handler.py
│   │   └── logging_middleware.py
│   ├── models/              # SQLAlchemy 2.0 ORM Entity Models
│   │   ├── base_model.py    # UUID, audit timestamp base model
│   │   └── user.py          # User & Role entity model
│   ├── routes/              # FastAPI Router Controllers
│   │   ├── auth_routes.py   # Login, registration, & user profile endpoints
│   │   └── health_routes.py # System vitality health check
│   ├── schemas/             # Pydantic v2 Data Transfer Objects (DTOs)
│   │   ├── auth_schema.py
│   │   ├── response_schema.py
│   │   └── user_schema.py
│   └── services/            # Repository pattern service layer
│       ├── auth_service.py
│       └── user_service.py
│
├── frontend/                # Streamlit Presentation Framework
│   ├── components/          # Reusable UI widgets
│   │   ├── alerts.py
│   │   ├── cards.py
│   │   ├── footer.py
│   │   └── header.py
│   ├── layouts/             # Page structural wrappers
│   │   ├── main_layout.py
│   │   ├── navigation.py
│   │   └── theme.py
│   ├── pages/               # (Phase 2 Dashboard Pages Placeholder)
│   └── utils/               # Frontend utility helpers
│       ├── config.py
│       ├── css_loader.py
│       └── session.py       # Session State Manager
│
├── config/                  # Global Enterprise Configuration
│   ├── constants.py         # Application metadata & roles
│   ├── database.py          # Engine & SessionLocal sessionmaker
│   ├── logging.py           # Loguru rotating logger configuration
│   ├── security.py          # Security tokens & bcrypt hashing
│   └── settings.py          # Pydantic v2 environment settings loader
│
├── analytics/               # (Phase 2 Analytics Engine Placeholder)
├── ml/                      # (Phase 3 ML Models Placeholder)
├── reports/                 # (Phase 2 Export & Report Services Placeholder)
├── uploads/                 # Uploaded dataset storage
├── datasets/                # Sample data store
├── logs/                    # Automated daily log storage (system.log, error.log)
├── migrations/              # Alembic Database Migration Management
│   ├── alembic.ini
│   └── env.py
│
├── tests/                   # Automated Pytest Test Suite
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_config.py
│   └── test_database.py
│
├── .env.example             # Environment template
├── .env                     # Local environment file
├── .gitignore               # Git ignore rules
├── requirements.txt         # Production dependency manifest
├── README.md                # Platform documentation
└── app.py                   # Main Streamlit Application Entry Point
```

---

## ⚡ Quick Start & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Virtual Environment Setup
```bash
# Clone or navigate to the repository
cd WatchSphereAI

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Linux/macOS)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚦 Execution Instructions

### Running the FastAPI Backend Engine
Launch the backend REST API server on `http://127.0.0.1:8000`:
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
* **Interactive OpenAPI Docs**: `http://127.0.0.1:8000/api/v1/docs`
* **ReDoc Documentation**: `http://127.0.0.1:8000/api/v1/redoc`
* **Health Check**: `http://127.0.0.1:8000/api/v1/health`

### Running the Streamlit Frontend Application
Launch the web interface on `http://localhost:8501`:
```bash
streamlit run app.py
```

### Running Automated Test Suite
Execute unit tests validating configuration, database models, and auth security:
```bash
pytest tests/ -v
```

---

## 🗄️ Database Architecture & Modular Switch

Phase 1 runs on **SQLite** by default (`watchsphere.db`). The database module (`config/database.py`) uses **SQLAlchemy 2.0** abstraction, allowing seamless transition to enterprise relational databases without altering any Python application code:

* **PostgreSQL Switch**: Change `DATABASE_URL` in `.env`:
  ```env
  DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/watchsphere_db"
  ```
* **MySQL Switch**: Change `DATABASE_URL` in `.env`:
  ```env
  DATABASE_URL="mysql+pymysql://user:password@localhost:3306/watchsphere_db"
  ```

---

## 🔮 Future Roadmap

* **Phase 2 (Analytics & Dashboards)**:
  * Customer Churn & Cohort Analysis dashboards.
  * Interactive Plotly & AgGrid financial & sentiment charts.
  * Automated CSV/PDF report generation engine in `reports/`.
* **Phase 3 (AI/ML Predictive Suite)**:
  * Customer Lifetime Value (CLV) machine learning models in `ml/`.
  * Real-time recommendation engine and NLP sentiment pipeline.
* **Phase 4 (Enterprise Deployment)**:
  * Docker containerization, Kubernetes manifests, and Cloud Run integration.

---

## 👤 Author & Acknowledgments

* **Developer**: Saniya Maner
* **Program**: Infosys Internship Project 2026
* **Project**: WatchSphere AI – Customer Insights Platform Version 3.0
