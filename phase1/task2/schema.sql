DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    emp_id      SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    department  VARCHAR(50) NOT NULL,
    salary      NUMERIC(10, 2) NOT NULL,
    hire_date   DATE NOT NULL
);

CREATE TABLE projects (
    proj_id       SERIAL PRIMARY KEY,
    emp_id        INTEGER REFERENCES employees(emp_id),
    project_name  VARCHAR(100) NOT NULL,
    start_date    DATE NOT NULL,
    end_date      DATE,
    budget        NUMERIC(12, 2) NOT NULL
);
