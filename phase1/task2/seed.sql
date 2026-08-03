-- Employees (emp_id is assigned by SERIAL in insertion order: 1-12)
INSERT INTO employees (name, department, salary, hire_date) VALUES
    ('Alice Johnson', 'Engineering', 85000.00, '2021-03-15'),  -- 1
    ('Bob Smith',     'Engineering', 72000.00, '2020-06-01'),  -- 2
    ('Carol Davis',   'Engineering', 95000.00, '2019-11-20'),  -- 3
    ('David Lee',     'Engineering', 68000.00, '2022-01-10'),  -- 4
    ('Eve Martinez',  'Engineering', 78000.00, '2023-04-05'),  -- 5
    ('Frank Wilson',  'Sales',       70000.00, '2020-02-14'),  -- 6
    ('Grace Kim',     'Sales',       78000.00, '2021-07-19'),  -- 7
    ('Henry Brown',   'Sales',       65000.00, '2022-09-01'),  -- 8
    ('Ivy Chen',      'Marketing',   70000.00, '2021-05-30'),  -- 9
    ('Jack Turner',   'Marketing',   66000.00, '2020-12-12'),  -- 10
    ('Karen White',   'HR',          58000.00, '2019-08-08'),  -- 11
    ('Leo Garcia',    'HR',          63000.00, '2022-03-22');  -- 12

-- Projects. Dates are relative to CURRENT_DATE so "active" (future end_date)
-- vs. "completed" (past end_date) stays correct no matter when this is run.
-- David Lee (4), Henry Brown (8), Karen White (11) and Leo Garcia (12)
-- are intentionally left with no projects, for query 4.
INSERT INTO projects (emp_id, project_name, start_date, end_date, budget) VALUES
    (1, 'Platform Migration',      CURRENT_DATE - INTERVAL '18 months', CURRENT_DATE + INTERVAL '4 months',  500000.00), -- Alice, active
    (3, 'AI Research Initiative',  CURRENT_DATE - INTERVAL '26 months', CURRENT_DATE + INTERVAL '10 months', 750000.00), -- Carol, active
    (2, 'Legacy System Upgrade',   CURRENT_DATE - INTERVAL '36 months', CURRENT_DATE - INTERVAL '24 months', 300000.00), -- Bob, completed
    (5, 'Mobile App Redesign',     CURRENT_DATE - INTERVAL '15 months', CURRENT_DATE - INTERVAL '3 months',  220000.00), -- Eve, completed
    (7, 'Sales CRM Rollout',       CURRENT_DATE - INTERVAL '2 months',  CURRENT_DATE + INTERVAL '1 month',   180000.00), -- Grace, active
    (9, 'Brand Refresh Campaign',  CURRENT_DATE - INTERVAL '1 month',   CURRENT_DATE + INTERVAL '4 months',  150000.00), -- Ivy, active
    (1, 'Data Warehouse Build',    CURRENT_DATE - INTERVAL '30 months', CURRENT_DATE - INTERVAL '18 months', 400000.00), -- Alice, completed
    (6, 'Regional Expansion',      CURRENT_DATE - INTERVAL '17 months', CURRENT_DATE - INTERVAL '5 months',  260000.00); -- Frank, completed
