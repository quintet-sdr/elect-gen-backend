import subprocess

from fastapi import APIRouter
from src.database.schemas import TableExtension

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import crud, schemas
from src.database.database import get_db
from src.database.models import Distribution
from src.database import algorithm
from utils.db_json_converter import get_json
import os
from os import path
from src.cli import Args
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


@router.get("/tables/")
async def get_table(extension: TableExtension) -> None:
    raise NotImplementedError


# @router.post("/courses/")
# async def new_course(course: Course) -> None:
#     raise NotImplementedError
#
#
# @router.post("/students/")
# async def new_student(student: Student) -> None:
#     raise NotImplementedError


@router.post("/students/", response_model=schemas.Student)
async def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db=db, student=student)


@router.get("/students/", response_model=list[schemas.Student])
async def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students


@router.post("/courses/", response_model=schemas.Course)
async def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_codename(db, codename=course.codename)
    if db_course:
        raise HTTPException(status_code=400, detail="Course already registered")
    return crud.create_course(db=db, course=course)


@router.get("/courses/", response_model=list[schemas.Course])
async def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses


@router.get("/distributions/")
async def read_distribution(db: Session = Depends(get_db)):
    get_json(db)
    print('Reading distributions')
    core = os.getenv('CORE')
    print('Got core', core)
    command = f'python {os.path.join(str(core), "algorithm_cli.py")} --courses .tmp/c.json --students .tmp/s.json --output .tmp/d.json'
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
    print(result.stdout)
    return {"message": "Success"}
