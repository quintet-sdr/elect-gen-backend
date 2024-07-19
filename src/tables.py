from pandas import DataFrame  # pyright: ignore[reportMissingTypeStubs]
from pydantic import BaseModel

from db.schemas import Course, Student


def courses_to_df(courses: list[Course]) -> DataFrame:
    COLUMNS = {"id": "Course ID", "quota": "Quota"}

    df = DataFrame(map(BaseModel.model_dump, courses))[COLUMNS.keys()]  # pyright: ignore[reportUnknownVariableType]
    df = df.rename(columns=COLUMNS)  # pyright: ignore[reportCallIssue, reportUnknownMemberType, reportUnknownVariableType]

    assert isinstance(df, DataFrame)
    return df


def parse_students(df: DataFrame) -> list[Student]:
    df = df.rename(
        columns={
            "Email": "email",
            "GPA": "gpa",
            "Priority 1": "priority_1",
            "Priority 2": "priority_2",
            "Priority 3": "priority_3",
            "Priority 4": "priority_4",
            "Priority 5": "priority_5",
        }
    )

    return list(map(Student.model_validate, df.to_dict("records")))  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]


def dump_courses_df(df: DataFrame) -> list[Course]:
    # TODO: type validation.

    df = df.rename(
        columns={
            "Code Name": "id",
            "Quota": "quota",
            "Type": "type",
        }
    )

    return df.to_dict("records")  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]


def dump_students(students: list[Student]) -> list[dict[str, str | float]]:
    return list(map(BaseModel.model_dump, students))


def dump_courses(courses: list[Course]) -> list[dict[str, str | int]]:
    return [it.model_dump(include={"id": True, "quota": True}) for it in courses]
