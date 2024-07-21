from sqlalchemy.orm import Session
from sqlalchemy import cast, ARRAY, String

from . import models, schemas


def get_student_by_email(db: Session, email: str, elective: str):
    if elective == 'hum':
        return db.query(models.StudentHum).filter(models.StudentHum.email == email).first()
    elif elective == 'tech':
        return db.query(models.StudentTech).filter(models.StudentTech.email == email).first()
    else:
        raise ValueError("Invalid elective type")


def get_students(db: Session, elective: str):
    if elective == 'hum':
        return db.query(models.StudentHum).all()
    elif elective == 'tech':
        return db.query(models.StudentTech).all()
    else:
        raise ValueError("Invalid elective type")


def create_student_hum(db: Session, studentHum: schemas.StudentCreate):
    db_student = models.StudentHum(
        email=studentHum.email,
        gpa=studentHum.gpa,
        priority_1=studentHum.priority_1,
        priority_2=studentHum.priority_2,
        priority_3=studentHum.priority_3,
        priority_4=studentHum.priority_4,
        priority_5=studentHum.priority_5,
        group=studentHum.group,
        completed=studentHum.completed,
        available=studentHum.available,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def create_student_tech(db: Session, studentTech: schemas.StudentCreate):
    db_student = models.StudentTech(
        email=studentTech.email,
        gpa=studentTech.gpa,
        priority_1=studentTech.priority_1,
        priority_2=studentTech.priority_2,
        priority_3=studentTech.priority_3,
        priority_4=studentTech.priority_4,
        priority_5=studentTech.priority_5,
        group=studentTech.group,
        completed=studentTech.completed,
        available=studentTech.available,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student_hum(db: Session, studentHum: models.StudentHum):
    db.delete(studentHum)
    db.commit()
    return studentHum


def delete_student_tech(db: Session, studentTech: models.StudentTech):
    db.delete(studentTech)
    db.commit()
    return studentTech


def get_students_hum(db: Session):
    return db.query(models.StudentHum).all()


def get_students_tech(db: Session):
    return db.query(models.StudentTech).all()


def get_courses_hum(db: Session):
    return db.query(models.CourseHum).all()


def get_courses_tech(db: Session):
    return db.query(models.CourseTech).all()


def get_course_by_codename(db: Session, codename: str, elective: str):
    if elective == 'hum':
        return db.query(models.CourseHum).filter(models.CourseHum.codename == codename).first()
    elif elective == 'tech':
        return db.query(models.CourseTech).filter(models.CourseTech.codename == codename).first()
    else:
        raise ValueError("Invalid elective type")


def get_courses(db: Session, elective: str):
    if elective == 'hum':
        return db.query(models.CourseHum).all()
    elif elective == 'tech':
        return db.query(models.CourseTech).all()
    else:
        raise ValueError("Invalid elective type")


def get_courses_by_group(db: Session, group: str, elective: str):
    if elective == 'hum':
        return db.query(models.CourseHum).filter(models.CourseHum.groups.op('@>')(cast([group], ARRAY(String)))).all()
    elif elective == 'tech':
        return db.query(models.CourseTech).filter(models.CourseTech.groups.op('@>')(cast([group], ARRAY(String)))).all()
    else:
        raise ValueError("Invalid elective type")


def create_course_hum(db: Session, courseHum: schemas.CourseCreate):
    db_course = models.CourseHum(
        codename=courseHum.codename,
        type=courseHum.type,
        full_name=courseHum.full_name,
        short_name=courseHum.short_name,
        description=courseHum.description,
        instructor=courseHum.instructor,
        min_overall=courseHum.min_overall,
        max_overall=courseHum.max_overall,
        low_in_group=courseHum.low_in_group,
        high_in_group=courseHum.high_in_group,
        max_in_group=courseHum.max_in_group,
        groups=courseHum.groups,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def create_course_tech(db: Session, courseTech: schemas.CourseCreate):
    db_course = models.CourseTech(
        codename=courseTech.codename,
        type=courseTech.type,
        full_name=courseTech.full_name,
        short_name=courseTech.short_name,
        description=courseTech.description,
        instructor=courseTech.instructor,
        min_overall=courseTech.min_overall,
        max_overall=courseTech.max_overall,
        low_in_group=courseTech.low_in_group,
        high_in_group=courseTech.high_in_group,
        max_in_group=courseTech.max_in_group,
        groups=courseTech.groups,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course_hum(db: Session, courseHum: models.CourseHum):
    db.delete(courseHum)
    db.commit()


def delete_course_tech(db: Session, courseTech: models.CourseTech):
    db.delete(courseTech)
    db.commit()


def delete_all_courses(db, elective):
    if elective == 'hum':
        if db.query(models.CourseHum).count() == 0:
            return
        db.query(models.CourseHum).delete()
        db.commit()
    elif elective == 'tech':
        if db.query(models.CourseTech).count() == 0:
            return
        db.query(models.CourseTech).delete()
        db.commit()
    else:
        raise ValueError("Invalid elective type")


def delete_all_students(db, elective):
    if elective == 'hum':
        if db.query(models.StudentHum).count() == 0:
            return
        db.query(models.StudentHum).delete()
        db.commit()
    elif elective == 'tech':
        if db.query(models.StudentTech).count() == 0:
            return
        db.query(models.StudentTech).delete()
        db.commit()
    else:
        raise ValueError("Invalid elective type")


def delete_all_constraints(db, elective):
    if elective == 'hum':
        if db.query(models.ConstraintHum).count() == 0:
            return
        db.query(models.ConstraintHum).delete()
        db.commit()
    elif elective == 'tech':
        if db.query(models.ConstraintTech).count() == 0:
            return
        db.query(models.ConstraintTech).delete()
        db.commit()
    else:
        raise ValueError("Invalid elective type")


def create_constraint_hum(db: Session, constraintHum: schemas.ConstraintCreate):
    db_constraint = models.ConstraintHum(
        course_codename=constraintHum.course_codename,
        student_email=constraintHum.student_email,
    )
    db.add(db_constraint)
    db.commit()
    db.refresh(db_constraint)
    return db_constraint


def create_constraint_tech(db: Session, constraintTech: schemas.ConstraintCreate):
    db_constraint = models.ConstraintTech(
        course_codename=constraintTech.course_codename,
        student_email=constraintTech.student_email,
    )
    db.add(db_constraint)
    db.commit()
    db.refresh(db_constraint)
    return db_constraint


def get_constraints(db: Session, elective: str):
    if elective == 'hum':
        return db.query(models.ConstraintHum).all()
    elif elective == 'tech':
        return db.query(models.ConstraintTech).all()
    else:
        raise ValueError("Invalid elective type")


def delete_constraint_hum(db: Session, constraintHum: models.ConstraintHum):
    db.delete(constraintHum)
    db.commit()
    return constraintHum


def delete_constraint_tech(db: Session, constraintTech: models.ConstraintTech):
    db.delete(constraintTech)
    db.commit()
    return constraintTech
