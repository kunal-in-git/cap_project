-- =====================================================================
-- Query 1: List all employees in the 'Engineering' department with
-- salary > 70,000, ordered by salary descending.
-- =====================================================================
SELECT emp_id, name, department, salary, hire_date
FROM employees
WHERE department = 'Engineering'
  AND salary > 70000
ORDER BY salary DESC;


-- =====================================================================
-- Query 2: Find the average salary per department, showing only
-- departments where the average salary exceeds 65,000.
-- =====================================================================
SELECT department, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 65000
ORDER BY avg_salary DESC;


-- =====================================================================
-- Query 3: Return the top 3 most expensive projects (by budget) along
-- with the employee name leading them.
-- =====================================================================
SELECT p.project_name, p.budget, e.name AS lead_employee
FROM projects p
JOIN employees e ON e.emp_id = p.emp_id
ORDER BY p.budget DESC
LIMIT 3;


-- =====================================================================
-- Query 4: Find all employees who have NOT been assigned to any
-- project (LEFT JOIN version).
-- =====================================================================
SELECT e.emp_id, e.name, e.department
FROM employees e
LEFT JOIN projects p ON p.emp_id = e.emp_id
WHERE p.proj_id IS NULL
ORDER BY e.emp_id;

-- Equivalent subquery version:
-- SELECT emp_id, name, department
-- FROM employees
-- WHERE emp_id NOT IN (SELECT emp_id FROM projects WHERE emp_id IS NOT NULL)
-- ORDER BY emp_id;


-- =====================================================================
-- Query 5: Calculate the total budget of all active projects (where
-- end_date is in the future) grouped by department.
-- =====================================================================
SELECT e.department, SUM(p.budget) AS total_active_budget
FROM projects p
JOIN employees e ON e.emp_id = p.emp_id
WHERE p.end_date > CURRENT_DATE
GROUP BY e.department
ORDER BY total_active_budget DESC;
