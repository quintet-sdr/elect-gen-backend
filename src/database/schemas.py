from enum import Enum
from typing import NewType

from pydantic import BaseModel, EmailStr, NonNegativeFloat


class TableExtension(str, Enum):
    CSV = "csv"
    XLSX = "xlsx"


class CourseType(str, Enum):
    HUM = "hum"
    TECH = "tech"


CourseCodename = NewType("CourseCodename", str)


class CourseBase(BaseModel):
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

