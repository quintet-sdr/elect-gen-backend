import json
from sqlalchemy.orm import Session
from src.database import models


def get_json(db):
    students_json = [student.to_dict() for student in db.query(models.Student).all()]
    courses_json = [course.to_dict() for course in db.query(models.Course).all()]
    with open(f'.tmp/c.json', 'w') as f:
        json.dump(courses_json, f, indent=4)
    with open(f'.tmp/s.json', 'w') as f:
        json.dump(students_json, f, indent=4)
