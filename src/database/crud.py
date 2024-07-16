from sqlalchemy.orm import Session

from . import models, schemas


def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        email=student.email,
        gpa=student.gpa,
        priority_1=student.priority_1,
        priority_2=student.priority_2,
        priority_3=student.priority_3,
        priority_4=student.priority_4,
        priority_5=student.priority_5,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_course_by_codename(db: Session, codename: str):
    return db.query(models.Course).filter(models.Course.codename == codename).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()


def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(
        codename=course.codename,
        type=course.type,
        full_name=course.full_name,
        short_name=course.short_name,
        description=course.description,
        instructor=course.instructor,
        min_overall=course.min_overall,
        max_overall=course.max_overall,
        low_in_group=course.low_in_group,
        high_in_group=course.high_in_group,
        max_in_group=course.max_in_group,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course
