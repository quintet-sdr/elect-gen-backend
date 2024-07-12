from enum import Enum
from typing import NewType

from pydantic import BaseModel, EmailStr, NonNegativeFloat, NonNegativeInt


class TableExtension(str, Enum):
    CSV = "csv"
    XLSX = "xlsx"


class CourseType(str, Enum):
    HUM = "hum"
    TECH = "tech"


CourseId = NewType("CourseId", str)


class Course(BaseModel):
    id: CourseId
    type: CourseType
    full_name: str
    short_name: str
    description: str
    instructor: str
    quota: NonNegativeInt


class Student(BaseModel):
    email: EmailStr
    gpa: NonNegativeFloat = 0.0
    priority_1: CourseId
    priority_2: CourseId
    priority_3: CourseId
    priority_4: CourseId
    priority_5: CourseId


class Distribution(BaseModel):
    student: EmailStr
    course: CourseId
