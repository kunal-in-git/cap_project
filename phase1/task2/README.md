# Task B — PostgreSQL Query Set

Schema, sample data, and query set for the employees/projects database.

## Files
- `schema.sql` — `employees` and `projects` table definitions
- `seed.sql` — sample data (12 employees across 4 departments, 8 projects)
- `queries.sql` — the 5 required queries

## Schema
```
employees(emp_id, name, department, salary, hire_date)
projects(proj_id, emp_id, project_name, start_date, end_date, budget)
```
`projects.emp_id` references `employees.emp_id` (the employee leading that project).

## Running it
```bash
createdb cap_task2
psql -d cap_task2 -f schema.sql
psql -d cap_task2 -f seed.sql
psql -d cap_task2 -f queries.sql
```

## Queries
1. **Engineering employees earning > 70,000**, ordered by salary descending.
2. **Average salary per department**, only departments where the average exceeds 65,000.
3. **Top 3 most expensive projects** by budget, with the name of the employee leading each one.
4. **Employees not assigned to any project** — implemented with a `LEFT JOIN ... WHERE ... IS NULL`; an equivalent `NOT IN` subquery version is included as a comment in `queries.sql`.
5. **Total budget of active projects** (`end_date` in the future), grouped by department.

Seed data was chosen deliberately to exercise every query: e.g. some Engineering employees sit below the 70,000/65,000 salary thresholds, some employees (David Lee, Henry Brown, Jack Turner, Karen White, Leo Garcia) have no projects, and projects span a mix of past (`end_date` before today) and future end dates so query 5 has a real "active vs. completed" split. Project dates are defined relative to `CURRENT_DATE` (e.g. `CURRENT_DATE + INTERVAL '4 months'`) so the active/completed split stays correct no matter when the seed is run.

## Verified output
All 5 queries were run against a live PostgreSQL 17 instance with the seed data above:

1. Carol Davis (95000), Alice Johnson (85000), Eve Martinez (78000), Bob Smith (72000) — David Lee (68000) correctly excluded.
2. Engineering (79600.00), Sales (71000.00), Marketing (68000.00) — HR (60500.00) correctly excluded.
3. AI Research Initiative / 750000 / Carol Davis, Platform Migration / 500000 / Alice Johnson, Data Warehouse Build / 400000 / Alice Johnson.
4. David Lee, Henry Brown, Jack Turner, Karen White, Leo Garcia.
5. Engineering (1,250,000.00), Sales (180,000.00), Marketing (150,000.00).

## AI-Generated Parts
This schema, seed data, and query set were generated with Claude (Anthropic) and then verified by actually executing them against a local PostgreSQL instance to confirm each result is correct.
