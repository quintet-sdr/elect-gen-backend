import json

import pandas as pd
from openpyxl.reader.excel import load_workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.workbook import Workbook


def get_excel_distribution():
    with open('.tmp/d.json', 'r') as f:
        data = json.load(f)
    with open('.tmp/s.json', 'r') as f:
        students_data = json.load(f)
    students_priorities = {
        student['email']: {student[f'priority_{i}']: i for i in range(1, 6)}
        for student in students_data
    }
    file_path = '.tmp/distributions.xlsx'
    wb = Workbook()
    del wb['Sheet']
    ws_stats = wb.create_sheet('Overall Statistics', 0)
    ws_stats.append(["Distribution", "Priority", "Number of Students"])
    dfs_and_costs = []
    for distribution_name, distribution_data in data.items():
        cost = round(float(distribution_name.split("Cost")[1].split(":")[1]), 2)
        df = pd.DataFrame(distribution_data)
        df['picked priority'] = [students_priorities[row['student']][row['course']] for _, row in df.iterrows()]
        dfs_and_costs.append((cost, distribution_name, df))
    dfs_and_costs.sort()
    for cost, distribution_name, df in dfs_and_costs:
        ws = wb.create_sheet(f'{distribution_name} Cost {cost}'.replace(":", "")[:31])
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)
        priority_counts = df['picked priority'].value_counts().sort_index()
        for priority, count in priority_counts.items():
            ws_stats.append([distribution_name.split(',')[0], priority, count])
        ws_stats.append(["", "", ""])
    wb.save(file_path)
    wb = load_workbook(file_path)

    for sheet in wb:
        ws = wb[sheet.title]
        for row in ws.iter_rows():
            for cell in row:
                cell.font = Font(name='Calibri', size=11)
                cell.alignment = Alignment(horizontal='center', vertical='center')

        for column in ws.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[get_column_letter(column[0].column)].width = adjusted_width

    wb.save(file_path)


def get_excel_template():
    courses = pd.DataFrame({
        "codename": [""],
        "type": [""],
        "full_name": [""],
        "short_name": [""],
        "description": [""],
        "instructor": [""],
        "min_overall": [""],
        "max_overall": [""],
        "low_in_group": [""],
        "high_in_group": [""],
        "max_in_group": [""],
        "groups": [""],
    }, index=[0])
    students = pd.DataFrame({
        "email": [""],
        "gpa": [""],
        "priority_1": [""],
        "priority_2": [""],
        "priority_3": [""],
        "priority_4": [""],
        "priority_5": [""],
        "group": [""],
        "completed": [""],
    }, index=[1])
    constrains = pd.DataFrame({
        "course_codename": [""],
        "group": [""],
    }, index=[2])
    distributions = pd.DataFrame({
        "student_email": [""],
        "course_codename": [""],
    }, index=[3])
    file_path = '.tmp/table.xlsx'
    with pd.ExcelWriter(file_path) as writer:
        courses.to_excel(writer, sheet_name='Courses', index=False)
        students.to_excel(writer, sheet_name='Students', index=False)
        constrains.to_excel(writer, sheet_name='Constrains', index=False)
        distributions.to_excel(writer, sheet_name='Distributions', index=False)
    wb = load_workbook(file_path)

    for sheet in wb:
        ws = wb[sheet.title]
        for row in ws.iter_rows():
            for cell in row:
                cell.font = Font(name='Calibri', size=11)
                cell.alignment = Alignment(horizontal='center', vertical='center')

        for column in ws.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[get_column_letter(column[0].column)].width = adjusted_width

    wb.save(file_path)
