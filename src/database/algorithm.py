import sys
from pathlib import Path
from .database import get_db
from .crud import get_students, get_courses
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from core import app


def get_result(db: Session):
    return app.run(get_students(db, 0, 5000), get_courses(db, 0, 5000))  # Use db here
