import subprocess
from typing import Annotated
from fastapi import APIRouter
from database.crud import get_courses
from fastapi import HTTPException
from utils.db_json_converter import get_json
import os
from dotenv import load_dotenv
import pandas as pd
from fastapi.responses import FileResponse
from utils.excel_converter import (
    get_excel_distribution,
    get_excel_current_tech,
    get_excel_current_hum,
    get_excel_example_tech,
    get_excel_example_hum,
)
from fastapi import File, Depends
from sqlalchemy.orm import Session
from src.database import crud, schemas
from src.database.database import get_db

load_dotenv()

router = APIRouter()


@router.get("/courses-groups/")
async def get_all_courses_groups(
    db: Session = Depends(get_db), elective: str = "hum"
) -> list[str]:
    """Get all courses groups from the database.
    :param db: Database session
    :param elective: Elective type
    :return: List of courses groups
    """
    courses = get_courses(db, elective=elective)
    courses_groups = [course.codename for course in courses]
    return courses_groups


@router.post("/upload-table/")
async def upload_table(
    file: Annotated[bytes, File()], name: str, db: Session = Depends(get_db)
):
    """Upload table and process it.
    :param file: File to upload
    :param name: File name
    :param db: Database session
    :return: Message"""
    type = "." + name.split(".")[-1]
    with open(".tmp/input_table" + type, "wb") as f:
        f.write(file)
    if type == ".xlsx":
        xls = pd.ExcelFile(".tmp/input_table" + type)
    elif type == ".ods":
        xls = pd.read_excel(".tmp/input_table" + type, engine="odf")
    else:
        return {"message": "File format not supported"}

    df_courses = pd.read_excel(xls, "Courses")
    df_students = pd.read_excel(xls, "Students")
    df_constraints = pd.read_excel(xls, "Constraints")
    elective = df_courses["type"][1]
    crud.delete_all_courses(db, elective=elective)
    crud.delete_all_students(db, elective=elective)
    crud.delete_all_constraints(db, elective=elective)

    for i, row in df_courses.iterrows():
        course_dict = row.to_dict()
        course_dict["groups"] = course_dict["groups"].split(";")
        if elective == "hum":
            courseHum = schemas.CourseCreate(**course_dict)
            crud.create_course_hum(db=db, courseHum=courseHum)
        elif elective == "tech":
            courseTech = schemas.CourseCreate(**course_dict)
            crud.create_course_tech(db=db, courseTech=courseTech)

    for _, row in df_constraints.iterrows():
        constraint_dict = row.to_dict()
        if elective == "hum":
            constraintHum = schemas.ConstraintCreate(**constraint_dict)
            crud.create_constraint_hum(db=db, constraintHum=constraintHum)
        elif elective == "tech":
            constraintTech = schemas.ConstraintCreate(**constraint_dict)
            crud.create_constraint_tech(db=db, constraintTech=constraintTech)

    for _, row in df_students.iterrows():
        student_dict = row.to_dict()
        student_dict["group"] = str(student_dict.get("group", "")).split(";")
        student_dict["completed"] = str(student_dict.get("completed", "")).split(";")
        student_dict["available"] = str(student_dict.get("available", "")).split(";")
        if elective == "hum":
            studentHum = schemas.StudentCreate(**student_dict)
            crud.create_student_hum(db=db, studentHum=studentHum)
        elif elective == "tech":
            studentTech = schemas.StudentCreate(**student_dict)
            crud.create_student_tech(db=db, studentTech=studentTech)

    return {"message": "Table uploaded and processed successfully"}


@router.get("/get-current-table/")
def get_table(elective: str = "hum"):
    """Get current table.
    :param elective: Elective type
    :return: File response
    """
    if elective == "hum":
        get_excel_current_hum()
    elif elective == "tech":
        get_excel_current_tech()
    else:
        raise HTTPException(status_code=400, detail="Invalid elective type")

    file_path = f".tmp/table_{elective}.xlsx"
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"table_{elective}.xlsx",
    )


@router.get("/get-example-table/")
def get_example_table(elective: str = "hum"):
    """Get example table.
    :param elective: Elective type
    :return: File response"""
    if elective == "hum":
        get_excel_example_hum()
    elif elective == "tech":
        get_excel_example_tech()
    else:
        raise HTTPException(status_code=400, detail="Invalid elective type")

    file_path = f".tmp/example_{elective}.xlsx"
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f".tmp/example_{elective}.xlsx",
    )


@router.get("/get-student/")
async def get_student_by_email(
    email: str, elective: str, db: Session = Depends(get_db)
):
    """Get student by email.
    :param email: Student email
    :param elective: Elective type
    :param db: Database session
    :return: Student"""

    if elective == "hum":
        student = crud.get_student_by_email(db, email, elective)
    elif elective == "tech":
        student = crud.get_student_by_email(db, email, elective)
    else:
        raise HTTPException(status_code=400, detail="Invalid elective type")
    return student


@router.post("/students/", response_model=schemas.Student)
async def create_student(
    student: schemas.StudentCreate, elective: str, db: Session = Depends(get_db)
):
    """Create student.
    :param student: Student
    :param elective: Elective type
    :param db: Database session
    :return: Student
    """
    if elective == "hum":
        db_student = crud.get_student_by_email(db, email=student.email, elective="hum")
        if db_student:
            crud.delete_student_hum(db, db_student)
        return crud.create_student_hum(db=db, studentHum=student)
    elif elective == "tech":
        db_student = crud.get_student_by_email(db, email=student.email, elective="tech")
        if db_student:
            crud.delete_student_tech(db, db_student)
        return crud.create_student_tech(db=db, studentTech=student)
    else:
        raise HTTPException(status_code=400, detail="Invalid elective type")


@router.get("/students/", response_model=list[schemas.Student])
async def read_students(elective: str, db: Session = Depends(get_db)):
    """Read students.
    :param elective: Elective type
    :param db: Database session
    :return Students
    """
    if elective == "hum":
        students = crud.get_students_hum(db)
    elif elective == "tech":
        students = crud.get_students_tech(db)
    else:
        raise HTTPException(status_code=400, detail="Invalid elective type")
    return students


@router.post("/courses/", response_model=schemas.Course)
async def create_course(
    course: schemas.CourseCreate, elective: str, db: Session = Depends(get_db)
):
    """Create course.
    :param course: Course
    :param elective: Elective type
    :param db: Database session
    :return: Course
    """
    if elective == "hum":
        db_course = crud.get_course_by_codename(
            db, codename=course.codename, elective="hum"
        )
        if db_course:
            crud.delete_course_hum(db, db_course)
        return crud.create_course_hum(db=db, courseHum=course)
    elif elective == "tech":
        db_course = crud.get_course_by_codename(
            db, codename=course.codename, elective="tech"
        )
        if db_course:
            crud.delete_course_tech(db, db_course)
        return crud.create_course_tech(db=db, courseTech=course)
    else:
        raise HTTPException(status_code=400, detail="Invalid elective type")


@router.get("/courses/", response_model=list[schemas.Course])
async def read_courses(elective: str, db: Session = Depends(get_db)):
    """Read courses.
    :param elective: Elective type
    :param db: Database session
    :return: Courses
    """

    if elective == "hum":
        courses = crud.get_courses_hum(db)
    elif elective == "tech":
        courses = crud.get_courses_tech(db)
    else:
        raise HTTPException(status_code=400, detail="Invalid elective type")
    return courses


@router.post("/distributions/")
async def read_distribution(
    file: Annotated[bytes, File()], name: str, db: Session = Depends(get_db)
):
    """Read distribution.
    :param file: File
    :param name: File name
    :param db: Database session
    :return: File response
    """

    type = "." + name.split(".")[-1]
    with open(".tmp/input_table" + type, "wb") as f:
        f.write(file)
    if type == ".xlsx":
        xls = pd.ExcelFile(".tmp/input_table" + type)
    elif type == ".ods":
        xls = pd.read_excel(".tmp/input_table" + type, engine="odf")
    else:
        return {"message": "File format not supported"}

    df_courses = pd.read_excel(xls, "Courses")
    df_students = pd.read_excel(xls, "Students")
    df_constraints = pd.read_excel(xls, "Constraints")
    elective = df_courses["type"][1]
    crud.delete_all_courses(db, elective=elective)
    crud.delete_all_students(db, elective=elective)
    crud.delete_all_constraints(db, elective=elective)
    for i, row in df_courses.iterrows():
        course_dict = row.to_dict()
        course_dict["groups"] = course_dict["groups"].split(";")
        if elective == "hum":
            courseHum = schemas.CourseCreate(**course_dict)
            crud.create_course_hum(db=db, courseHum=courseHum)
        elif elective == "tech":
            courseTech = schemas.CourseCreate(**course_dict)
            crud.create_course_tech(db=db, courseTech=courseTech)
    for _, row in df_constraints.iterrows():
        constraint_dict = row.to_dict()
        if elective == "hum":
            constraintHum = schemas.ConstraintCreate(**constraint_dict)
            crud.create_constraint_hum(db=db, constraintHum=constraintHum)
        elif elective == "tech":
            constraintTech = schemas.ConstraintCreate(**constraint_dict)
            crud.create_constraint_tech(db=db, constraintTech=constraintTech)
    for _, row in df_students.iterrows():
        student_dict = row.to_dict()
        student_dict["group"] = str(student_dict.get("group", "")).split(";")
        student_dict["completed"] = str(student_dict.get("completed", "")).split(";")
        student_dict["available"] = str(student_dict.get("available", "")).split(";")
        if elective == "hum":
            studentHum = schemas.StudentCreate(**student_dict)
            crud.create_student_hum(db=db, studentHum=studentHum)
        elif elective == "tech":
            studentTech = schemas.StudentCreate(**student_dict)
            crud.create_student_tech(db=db, studentTech=studentTech)
    if elective == "hum":
        get_json(db, elective="hum")
        print("Reading distributions for hum")
        core = os.getenv("CORE")
        command = f'python {os.path.join(str(core), "algorithm_cli.py")} --courses .tmp/c_hum.json --students .tmp/s_hum.json --output .tmp/d_hum.json'
    elif elective == "tech":
        get_json(db, elective="tech")
        print("Reading distributions for tech")
        core = os.getenv("CORE")
        command = f'python {os.path.join(str(core), "algorithm_cli.py")} --courses .tmp/c_tech.json --students .tmp/s_tech.json --output .tmp/d_tech.json'
    else:
        raise HTTPException(status_code=400, detail="Invalid elective type")

    print(command)
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, encoding="utf-8"
    )
    print(result.stdout)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr)

    file_path = f".tmp/distributions_{elective}.xlsx"
    get_excel_distribution(elective)
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"distributions_{elective}.xlsx",
    )
