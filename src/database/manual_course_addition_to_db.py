"""Manually add data to the database using a JSON file."""

import psycopg2

con = psycopg2.connect("postgresql://postgres:sdr@localhost:5432/postgres")
cursor = con.cursor()

with open('courses.json') as file:
    data = file.read()

query_sql = """
DO $$ BEGIN
    -- Drop the type if it already exists
    IF EXISTS (SELECT 0 FROM pg_type WHERE typname = 'course_type') THEN
        DROP TYPE course_type;
    END IF;
    -- Create the composite type
    CREATE TYPE course_type AS (
        "codename" text,
        "type" text,
        "full_name" text,
        "short_name" text,
        "description" text,
        "instructor" text,
        "min_overall" numeric,
        "max_overall" numeric,
        "low_in_group" numeric,
        "high_in_group" numeric,
        "max_in_group" numeric
    );
END $$;

-- Drop the table if it already exists
DROP TABLE IF EXISTS courses;

-- Create the table
CREATE TABLE courses AS SELECT * FROM json_populate_recordset(NULL::course_type, %s);
"""

cursor.execute(query_sql, (data,))
con.commit()
cursor.execute('select * from courses')
print(cursor.fetchall())
