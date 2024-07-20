from enum import Enum
from typing import NewType, Optional

from pydantic import BaseModel, EmailStr, NonNegativeFloat, PositiveInt


class TableExtension(str, Enum):
    CSV = "csv"
    XLSX = "xlsx"


class CourseType(str, Enum):
    HUM = "hum"
    TECH = "tech"


CourseCodename = NewType("CourseCodename", str)


class CourseBase(BaseModel):
    id: PositiveInt = 0
    codename: CourseCodename
    type: CourseType
    full_name: str
    short_name: str
    description: str
    instructor: str
    min_overall: int
    max_overall: int
    low_in_group: int
    high_in_group: int
    max_in_group: int
    groups: list[str]


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    class Config:
        orm_mode = True


class StudentBase(BaseModel):
    email: EmailStr
    gpa: NonNegativeFloat = 0.0
    priority_1: CourseCodename
    priority_2: CourseCodename
    priority_3: CourseCodename
    priority_4: CourseCodename
    priority_5: CourseCodename
    group: list[str] = []
    completed: list[CourseCodename] = []
    available: list[CourseCodename] = []


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    class Config:
        orm_mode = True


class DistributionBase(BaseModel):
    student_email: str
    course_codename: CourseCodename


class DistributionCreate(DistributionBase):
    pass


class Distribution(DistributionBase):
    class Config:
        orm_mode = True


class ConstraintBase(BaseModel):
    course_codename: CourseCodename
    student_email: str


class ConstraintCreate(ConstraintBase):
    pass


class Constraint(ConstraintBase):
    class Config:
        orm_mode = True
