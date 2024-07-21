import base64
import json
import subprocess
from typing import Annotated

from fastapi import APIRouter, Form
from matplotlib import pyplot as plt
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows
from sqlalchemy import text

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
from utils.excel_converter import get_excel_distribution, get_excel_example, get_excel_current
from fastapi import UploadFile, File
from fastapi import UploadFile, File, Depends
from sqlalchemy.orm import Session
from src.database import crud, schemas
from src.database.database import get_db

load_dotenv()

router = APIRouter()


# @router.post("/upload")
# def upload(file: Annotated[bytes, File()], name: str):
#     type = '.' + name.split('.')[-1]
#     with open('.tmp/input_table1' + type, 'wb') as f:
#         f.write(file)
#     xls = pd.ExcelFile('.tmp/input_table' + type)
#     df_courses = pd.read_excel(xls, 'Courses')
#     df_students = pd.read_excel(xls, 'Students')
#     df_constraints = pd.read_excel(xls, 'Constraints')
#     return {"message": f"Successfully uploaded {'.tmp/input_table' + type} to .tmp directory"}
@router.get("/courses-groups/")
async def get_all_courses_groups(db: Session = Depends(get_db)):
    courses = crud.get_courses(db)
    groups = []
    for course in courses:
        for group in course.groups:
            groups.append(group)
    return list(set(groups))


@router.post("/upload-table/")
async def upload_table(file: Annotated[bytes, File()], name: str, db: Session = Depends(get_db)):
    type = '.' + name.split('.')[-1]
    print(type)
    with open('.tmp/input_table' + type, 'wb') as f:
        f.write(file)
    if type == '.xlsx':
        xls = pd.ExcelFile('.tmp/input_table' + type)
    elif type == '.ods':
        xls = pd.read_excel('.tmp/input_table' + type, engine='odf')
    else:
        return {"message": "File format not supported"}
    df_courses = pd.read_excel(xls, 'Courses')
    df_students = pd.read_excel(xls, 'Students')
    df_constraints = pd.read_excel(xls, 'Constraints')

    crud.delete_all_courses(db)
    for i, row in df_courses.iterrows():
        course_dict = row.to_dict()
        course_dict['groups'] = course_dict['groups'].split(';')
        course = schemas.CourseCreate(**course_dict)
        db_course = crud.get_course_by_codename(db, codename=course.codename)
        if db_course:
            crud.delete_course(db, db_course)
        crud.create_course(db=db, course=course)

    crud.delete_all_constraints(db)
    for _, row in df_constraints.iterrows():
        constraint = row.to_dict()
        constraint = schemas.ConstraintCreate(**constraint)
        crud.create_constraint(db=db, constraint=constraint)

    crud.delete_all_students(db)
    for _, row in df_students.iterrows():
        student_dict = row.to_dict()
        if student_dict['group']:
            student_dict['group'] = str(student_dict['group']).split(';')
        else:
            student_dict['group'] = []
        if student_dict['completed']:
            student_dict['completed'] = str(student_dict['completed']).split(';')
        else:
            student_dict['completed'] = []
        if student_dict['available']:
            student_dict['available'] = str(student_dict['available']).split(';')
        else:
            student_dict['available'] = []
        print(student_dict['group'])
        for group in student_dict['group']:
            for course in crud.get_courses_by_group(db, group):
                student_dict['available'] += [course.codename]
        for constraint in crud.get_constraints(db):
            if constraint.student_email == student_dict['email'] and constraint.course_codename not in student_dict[
                'completed']:
                student_dict['completed'] += [constraint.course_codename]
        student_dict['available'] = list(set(student_dict['available']) - set(student_dict['completed']))
        student = schemas.StudentCreate(**student_dict)
        db_student = crud.get_student_by_email(db, email=student.email)
        if db_student:
            crud.delete_student(db, db_student)
        crud.create_student(db=db, student=student)

    return {"message": "Table uploaded and cells updated successfully"}


@router.get("/get-current-table/")
def get_table():
    get_excel_current()
    file_path = '.tmp/table.xlsx'
    return FileResponse(file_path, media_type='application/octet-stream', filename='table.xlsx')


@router.get("/get-example-table/")
def get_example_table():
    get_excel_example()
    file_path = '.tmp/example.xlsx'
    return FileResponse(file_path, media_type='application/octet-stream', filename='example.xlsx')


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
    db_course = crud.get_course_by_codename(db, codename=course.codename)
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
