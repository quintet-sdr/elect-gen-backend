from sqlalchemy import Column, Integer, String, Float

from .database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    codename = Column(String, unique=True, index=True)
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


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    gpa = Column(Float)
    priority_1 = Column(String)
    priority_2 = Column(String)
    priority_3 = Column(String)
    priority_4 = Column(String)
    priority_5 = Column(String)


class Distribution(Base):
    __tablename__ = "distributions"

    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String, index=True)
    course_codename = Column(String, index=True)
