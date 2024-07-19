"""Manually add data to the database using a JSON file."""

import psycopg2

con = psycopg2.connect("postgresql://postgres:sdr@localhost:5432/postgres")
cursor = con.cursor()

with open("students.json") as file:
    data = file.read()

query_sql = """
DO $$ BEGIN
    -- Drop the type if it already exists
    IF EXISTS (SELECT 0 FROM pg_type WHERE typname = 'student_type') THEN
        DROP TYPE student_type;
    END IF;
    -- Create the composite type
    CREATE TYPE student_type AS (
        "email" text,
        "gpa" numeric,
        "priority_1" text,
        "priority_2" text,
        "priority_3" text,
        "priority_4" text,
        "priority_5" text,
        "group" text,
        "completed" text[]
    );
END $$;

-- Drop the table if it already exists
DROP TABLE IF EXISTS students;

-- Create the table
CREATE TABLE students AS SELECT * FROM json_populate_recordset(NULL::student_type, %s);
"""

cursor.execute(query_sql, (data,))
con.commit()
cursor.execute("select * from students")
print(cursor.fetchall())
