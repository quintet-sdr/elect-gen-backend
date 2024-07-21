from sqlalchemy.orm import Session

from . import models, schemas


def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()


def get_students(db: Session):
    return db.query(models.Student).all()


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        email=student.email,
        gpa=student.gpa,
        priority_1=student.priority_1,
        priority_2=student.priority_2,
        priority_3=student.priority_3,
        priority_4=student.priority_4,
        priority_5=student.priority_5,
        group=student.group,
        completed=student.completed,
        available=student.available,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student: models.Student):
    db.delete(student)
    db.commit()
    return student


def get_course_by_id(db: Session, id: int):
    return db.query(models.Course).filter(models.Course.id == id).first()


def get_course_by_codename(db: Session, codename: str):
    return db.query(models.Course).filter(models.Course.codename == codename).first()


def get_courses(db: Session):
    return db.query(models.Course).all()


from sqlalchemy import cast, ARRAY, String

def get_courses_by_group(db: Session, group: str):
    return db.query(models.Course).filter(models.Course.groups.op('@>')(cast([group], ARRAY(String)))).all()

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(
        id=course.id,
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
        groups=course.groups,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course: models.Course):
    db.delete(course)
    db.commit()


def get_distributions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Distribution).offset(skip).limit(limit).all()


def create_distribution(db: Session, distribution: schemas.DistributionCreate):
    db_distribution = models.Distribution(
        student_email=distribution.student_email,
        course_codename=distribution.course_codename,
    )
    db.add(db_distribution)
    db.commit()
    db.refresh(db_distribution)
    return db_distribution


def delete_all_courses(db):
    db.query(models.Course).delete()
    db.commit()


def delete_all_students(db):
    db.query(models.Student).delete()
    db.commit()


def delete_all_constraints(db):
    db.query(models.Constraint).delete()
    db.commit()


def delete_all_distributions(db):
    db.query(models.Distribution).delete()
    db.commit()


def create_constraint(db: Session, constraint: schemas.ConstraintCreate):
    db_constraint = models.Constraint(
        course_codename=constraint.course_codename,
        student_email=constraint.student_email,
    )
    db.add(db_constraint)
    db.commit()
    db.refresh(db_constraint)
    return db_constraint


def get_constraints(db: Session):
    return db.query(models.Constraint).all()


def delete_constraint(db: Session, constraint: models.Constraint):
    db.delete(constraint)
    db.commit()
    return constraint
