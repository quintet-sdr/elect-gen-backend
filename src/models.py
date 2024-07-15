from enum import Enum
from typing import NewType

from pydantic import BaseModel, EmailStr, NonNegativeFloat, NonNegativeInt


class TableExtension(str, Enum):
    CSV = "csv"
    XLSX = "xlsx"


class CourseType(str, Enum):
    HUM = "hum"
    TECH = "tech"


CourseCodename = NewType("CourseCodename", str)


class Course(BaseModel):
    id: NonNegativeInt
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


class Student(BaseModel):
    email: EmailStr
    gpa: NonNegativeFloat = 0.0
    priority_1: CourseCodename
    priority_2: CourseCodename
    priority_3: CourseCodename
    priority_4: CourseCodename
    priority_5: CourseCodename


class Distribution(BaseModel):
    student: EmailStr
    course: CourseCodename
