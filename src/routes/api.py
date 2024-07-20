import json
import subprocess

from fastapi import APIRouter
from matplotlib import pyplot as plt
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows

from src.database.schemas import TableExtension

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import crud, schemas
from src.database.database import get_db
from src.database.models import Distribution
from utils.db_json_converter import get_json
import os
from os import path
from src.cli import Args
from dotenv import load_dotenv
from fastapi import File, UploadFile
import pandas as pd
from fastapi.responses import FileResponse
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from io import BytesIO
from openpyxl.utils.dataframe import dataframe_to_rows
import json
from utils.excel_converter import get_excel_distribution, get_excel_template
load_dotenv()

router = APIRouter()


@router.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        file_location = os.path.join('.tmp', file.filename)
        with open(file_location, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to upload file")
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename} to .tmp directory"}


@router.get("/example_table/")
def get_table():
    get_excel_template()
    file_path = '.tmp/table.xlsx'
    return FileResponse(file_path, media_type='application/octet-stream', filename='table.xlsx')


# @router.get("/tables/")
# async def get_table(extension: TableExtension) -> None:
#     raise NotImplementedError


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
        crud.delete_student(db, db_student)
    return crud.create_student(db=db, student=student)


@router.get("/students/", response_model=list[schemas.Student])
async def read_students(db: Session = Depends(get_db)):
    students = crud.get_students(db)
    return students


@router.post("/courses/", response_model=schemas.Course)
async def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_id(db, id=course.id)
    if db_course:
        crud.delete_course(db, db_course)
    new_course = crud.create_course(db=db, course=course)
    return new_course


@router.get("/courses/", response_model=list[schemas.Course])
async def read_courses(db: Session = Depends(get_db)):
    courses = crud.get_courses(db)
    return courses


@router.get("/distributions/")
async def read_distribution(db: Session = Depends(get_db)):
    get_json(db)
    print("Reading distributions")
    core = os.getenv("CORE")
    print("Got core", core)
    command = f'python {os.path.join(str(core), "algorithm_cli.py")} --courses .tmp/c.json --students .tmp/s.json --output .tmp/d.json'
    print(command)
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, encoding="utf-8"
    )
    print(result.stdout)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr)
    get_excel_distribution()
    file_path = '.tmp/distributions.xlsx'
    return FileResponse(file_path, media_type='application/octet-stream', filename='distributions.xlsx')
