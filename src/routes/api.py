from fastapi import APIRouter

from src.models import Course, Student, TableExtension

router = APIRouter()


@router.get("/table/")
async def get_table(extension: TableExtension) -> None:
    raise NotImplementedError


@router.post("/courses/")
async def new_course(course: Course) -> None:
    raise NotImplementedError


@router.post("/students/")
async def new_student(student: Student) -> None:
    raise NotImplementedError
