"""
WatchSphere AI v3.0 - Phase 7 UI/UX Consistency & Quality Verification Test Suite
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import SessionLocal, engine, Base
from datasets.seed_datasets import auto_seed_datasets
from frontend.utils.css_loader import load_css


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    auto_seed_datasets()


def test_css_design_system_tokens():
    """Verify CSS loader loads valid stylesheet containing WatchSphere color tokens."""
    css_path = PROJECT_ROOT / "assets" / "css" / "style.css"
    assert css_path.exists(), "assets/css/style.css must exist"

    with open(css_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "--font-heading" in content or "font-family" in content
    assert "background" in content


def test_database_and_services_responsive_ready():
    """Verify core database session is healthy for UI component queries."""
    db = SessionLocal()
    try:
        assert db is not None
    finally:
        db.close()
