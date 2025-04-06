select d.dept_name, count(e.dept_id) as emp_number 
from dept d left join emp e on d.dept_id=e.dept_id 
group by d.dept_name 
order by emp_number desc, d.dept_name asc;