-- Q1
-- Simple Query
Select distinct s1.name, d1.faculty ,b.title, s2.name, d2.faculty
from student s1, loan l, book b, department d1,department d2,student s2
where s1.email = l.borrower
and l.book = b.ISBN13
and s1.department = d1.department
and s2.email = l.owner
and s2.department = d2.department;

-- Nested Query
Select distinct s1.name as Borrower , d1.faculty ,b.title, s2.name as Loaner, d2.faculty
FROM student s1,book b, department d1, student s2, department d2
WHERE (s1.email, b.isbn13, s2.email) IN (SELECT l.borrower , l.book , l.owner from loan l) -- can use = ANY
and s1.department = d1.department
and s2.department = d2.department;


-- Q2
-- Get Null value, outer join
-- Or union with NULL





Select distinct s1.name, d1.faculty,s2.name,d2.faculty
FROM student s1, department d1, student s2, department d2, book b1
WHERE (s1.email, b1.isbn13 , s2.email) IN 
(SELECT distinct l.borrower , l.book , l.owner
FROM book b2, loan l
WHERE b2.title like '%Database%'
AND l.book = b2.isbn13)
and s1.department = d1.department
and s2.department = d2.department
UNION ( -- can use union to get NULL
SELECT DISTINCT s1.name, d1.faculty,null,null
FROM student s1, department d1
WHERE d1.department = s1.department
AND s1.email NOT IN ( -- can use <> ALL 
SELECT distinct s2.email
FROM book b2, loan l,student s2
WHERE b2.title like '%Database%'
AND l.book = b2.isbn13
AND s2.email = l.borrower));


-- outer join need to care about on.
SELECT DISTINCT s1.name,d1.faculty,s2.name,d2.faculty
FROM (student s1
INNER JOIN department d1 on s1.department = d1.department)
LEFT OUTER JOIN ( loan l
INNER JOIN book b on l.book = b.ISBN13
INNER JOIN student s2 on s2.email = l.owner
INNER JOIN department d2 on s2.department = d2.department)
on s1.email = l.borrower
and b.title like '%Database%'
Where b.title is NULL; -- never borrow



--- Q3

SELECT DISTINCT s1.email, d1.faculty,null,null
FROM student s1, department d1
WHERE d1.department = s1.department
AND s1.email NOT IN ( -- can use <> ALL 
SELECT distinct s2.email
FROM book b2, loan l,student s2
WHERE b2.title like '%Database%'
AND l.book = b2.isbn13
AND s2.email = l.borrower);

SELECT DISTINCT s1.email, d1.faculty
FROM student s1, department d1
WHERE s1.department = d1.department
AND NOT EXISTS (
SELECT * 
FROM book b2, loan l,student s2
WHERE b2.title like '%Database%'
AND l.book = b2.isbn13
AND s2.email = l.borrower
AND s1.email = s2.email); -- not exists require this options
