from fastapi import APIRouter
from database.schemas import TableExtension

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud, schemas
from database.database import get_db

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
