import json
from sqlalchemy.orm import Session
from src.database import models
from src.database.crud import get_courses_by_group

import json
from sqlalchemy.orm import Session
from src.database import models
from src.database.crud import get_courses_by_group


def get_json(db: Session, elective: str):
    if elective == 'hum':
        students_db = [student.to_dict() for student in db.query(models.StudentHum).all()]
        courses_db = [course.to_dict() for course in db.query(models.CourseHum).all()]
    elif elective == 'tech':
        students_db = [student.to_dict() for student in db.query(models.StudentTech).all()]
        courses_db = [course.to_dict() for course in db.query(models.CourseTech).all()]
    else:
        raise ValueError("Invalid elective type")
    students_json = []
    for student in students_db:
        available_courses = get_courses_by_group(db, student["group"], elective)
        available_courses_dicts = [course.to_dict() for course in available_courses]
        available_course_codenames = [course['codename'] for course in available_courses_dicts]
        # print(f"Available course codenames for group {student['group']}: {available_course_codenames}")
        completed_course_codenames = student['completed'] if student['completed'] else []
        available = set(available_course_codenames) - set(completed_course_codenames)
        # print(f"Truly available courses for student {student['email']}: {available}")
        available_courses_full_details = [course['codename'] for course in courses_db if
                                          course['codename'] in available]

        student_json = {
            "email": student["email"],
            "gpa": student["gpa"],
            "priority_1": student["priority_1"],
            "priority_2": student["priority_2"],
            "priority_3": student["priority_3"],
            "priority_4": student["priority_4"],
            "priority_5": student["priority_5"],
            "group": student["group"],
            "completed": student["completed"],
            "available": available_courses_full_details,
        }
        students_json.append(student_json)

    with open(f".tmp/c_{elective}.json", "w") as f:
        json.dump(courses_db, f, indent=4)
    with open(f".tmp/s_{elective}.json", "w") as f:
        json.dump(students_json, f, indent=4)
