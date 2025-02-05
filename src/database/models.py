from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import ARRAY

from .database import Base


class CourseHum(Base):
    __tablename__ = "courses_hum"

    codename = Column(String, primary_key=True, index=True)
    type = Column(String)
    full_name = Column(String)
    short_name = Column(String)
    description = Column(String)
    instructor = Column(String)
    min_overall = Column(Integer)
    max_overall = Column(Integer)
    low_in_group = Column(Integer)
    high_in_group = Column(Integer)
    max_in_group = Column(Integer)
    groups = Column(ARRAY(String))

    def to_dict(self):
        return {
            "codename": self.codename,
            "type": self.type,
            "full_name": self.full_name,
            "short_name": self.short_name,
            "description": self.description,
            "instructor": self.instructor,
            "min_overall": int(self.min_overall),
            "max_overall": int(self.max_overall),
            "low_in_group": int(self.low_in_group),
            "high_in_group": int(self.high_in_group),
            "max_in_group": int(self.max_in_group),
            "groups": self.groups,
        }


class StudentHum(Base):
    __tablename__ = "students_hum"

    # id = Column(Integer, primary_key=True, index=True)
    email = Column(String, primary_key=True, index=True)
    gpa = Column(Float)
    priority_1 = Column(String)
    priority_2 = Column(String)
    priority_3 = Column(String)
    priority_4 = Column(String)
    priority_5 = Column(String)
    group = Column(ARRAY(String))
    completed = Column(ARRAY(String))
    available = Column(ARRAY(String))

    def to_dict(self):
        return {
            "email": self.email,
            "gpa": float(self.gpa),
            "priority_1": self.priority_1,
            "priority_2": self.priority_2,
            "priority_3": self.priority_3,
            "priority_4": self.priority_4,
            "priority_5": self.priority_5,
            "group": self.group,
            "completed": self.completed,
            "available": self.available,
        }


class DistributionHum(Base):
    __tablename__ = "distributions_hum"

    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String, index=True)
    course_codename = Column(String, index=True)

    def to_dict(self):
        return {
            "student_email": self.student_email,
            "course_codename": self.course_codename,
        }


class ConstraintHum(Base):
    __tablename__ = "constraints_hum"

    id = Column(Integer, primary_key=True, index=True)
    course_codename = Column(String, index=True)
    student_email = Column(String)

    def to_dict(self):
        return {
            "course_codename": self.course_codename,
            "student_email": self.student_email,
        }


class CourseTech(Base):
    __tablename__ = "courses_tech"

    codename = Column(String, primary_key=True, index=True)
    type = Column(String)
    full_name = Column(String)
    short_name = Column(String)
    description = Column(String)
    instructor = Column(String)
    min_overall = Column(Integer)
    max_overall = Column(Integer)
    low_in_group = Column(Integer)
    high_in_group = Column(Integer)
    max_in_group = Column(Integer)
    groups = Column(ARRAY(String))

    def to_dict(self):
        return {
            "codename": self.codename,
            "type": self.type,
            "full_name": self.full_name,
            "short_name": self.short_name,
            "description": self.description,
            "instructor": self.instructor,
            "min_overall": int(self.min_overall),
            "max_overall": int(self.max_overall),
            "low_in_group": int(self.low_in_group),
            "high_in_group": int(self.high_in_group),
            "max_in_group": int(self.max_in_group),
            "groups": self.groups,
        }


class StudentTech(Base):
    __tablename__ = "students_tech"

    # id = Column(Integer, primary_key=True, index=True)
    email = Column(String, primary_key=True, index=True)
    gpa = Column(Float)
    priority_1 = Column(String)
    priority_2 = Column(String)
    priority_3 = Column(String)
    priority_4 = Column(String)
    priority_5 = Column(String)
    group = Column(ARRAY(String))
    completed = Column(ARRAY(String))
    available = Column(ARRAY(String))

    def to_dict(self):
        return {
            "email": self.email,
            "gpa": float(self.gpa),
            "priority_1": self.priority_1,
            "priority_2": self.priority_2,
            "priority_3": self.priority_3,
            "priority_4": self.priority_4,
            "priority_5": self.priority_5,
            "group": self.group,
            "completed": self.completed,
            "available": self.available,
        }


class DistributionTech(Base):
    __tablename__ = "distributions_tech"

    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String, index=True)
    course_codename = Column(String, index=True)

    def to_dict(self):
        return {
            "student_email": self.student_email,
            "course_codename": self.course_codename,
        }


class ConstraintTech(Base):
    __tablename__ = "constraints_tech"

    id = Column(Integer, primary_key=True, index=True)
    course_codename = Column(String, index=True)
    student_email = Column(String)

    def to_dict(self):
        return {
            "course_codename": self.course_codename,
            "student_email": self.student_email,
        }
