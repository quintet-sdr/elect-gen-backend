import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from core import app


def get_result():
    return app.run('src/database/students_old.json', 'src/database/courses_old.json', 'distribution.json')
