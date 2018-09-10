-- Q1
SELECT FACULTY, DEPARTMENT
FROM STUDENT
GROUP BY FACULTY,DEPARTMENT
ORDER BY FACULTY,DEPARTMENT;
-- OR 
SELECT DISTINCT s.FACULTY,s.DEPARTMENT
FROM STUDENT s;

-- Q2
SELECT DEPARTMENT,count(DISTINCT faculty)
FROM STUDENT  s
GROUP BY s.DEPARTMENT;

-- Q3
-- Cannot get exactly 2
SELECT s.DEPARTMENT 
FROM STUDENT s,STUDENT st
WHERE s.DEPARTMENT = st.DEPARTMENT
  AND s.FACULTY > st.FACULTY; -- if use <> will have double count because of symmetric 

-- Q4
-- EMPTY SET
SELECT DEPARTMENT,count(DISTINCT faculty)
FROM STUDENT  s
GROUP BY s.DEPARTMENT
HAVING COUNT(DISTINCT faculty) = 2; -- ??? some people use >1


-- Create DEPARTMENT
CREATE TABLE DEPARTMENT (
DEPARTMENT VARCHAR(64) PRIMARY KEY  ,
FACULTY VARCHAR(64) NOT NULL
);
  
INSERT INTO DEPARTMENT (SELECT DISTINCT DEPARTMENT,FACULTY FROM STUDENT);

SELECT * FROM DEPARTMENT;

ALTER TABLE STUDENT DROP COLUMN FACULTY; 

ALTER TABLE STUDENT ADD CONSTRAINT DEPARTMENT_FK
FOREIGN KEY (DEPARTMENT) REFERENCES DEPARTMENT(DEPARTMENT);

SELECT * FROM STUDENT;

SELECT DISTINCT DEPARTMENT FROM DEPARTMENT;

-- Q6 
SELECT s.department,d.faculty,count(*)
FROM STUDENT s,DEPARTMENT d
WHERE s.department = d.department
GROUP BY d.faculty,s.department
HAVING count(*) > 4
ORDER BY s.department,d.faculty asc;

-- Test
SELECT count(*)
FROM STUDENT s
WHERE s.DEPARTMENT = 'CS' ;


SELECT count(*)
FROM STUDENT s
GROUP BY s.department;

-- Q7
SELECT s.department, count(*)
FROM STUDENT s
GROUP BY s.department
HAVING count(*) >= ALL (
SELECT count(*)
FROM STUDENT s
GROUP BY s.department);

-- Faculty with largest number of student

SELECT d.faculty
FROM student s,DEPARTMENT d
where s.department = d.department
GROUP BY d.faculty
HAVING count(*) >= ALL (
SELECT count(*)
FROM student s1,DEPARTMENT d1
where s1.department = d1.department
GROUP BY d1.faculty
);


-- Q8 
SELECT * FROM BOOK;
SELECT * FROM LOAN;

SELECT distinct d.faculty
FROM BOOK b, LOAN l,STUDENT s,DEPARTMENT d
WHERE s.email = l.borrower
AND s.department = d.department
AND b.title LIKE '%Calculus%';

-- Get all calculus book?
SELECT d.faculty
FROM LOAN l, STUDENT s, DEPARTMENT d
WHERE l.book = ALL (
SELECT DISTINCT b.ISBN13
FROM BOOK b
WHERE b.title like '%Calculus%')
AND s.email = l.borrower
AND s.department = d.department;

-- Correct
SELECT d.faculty, count (DISTINCT b1.ISBN13)
FROM LOAN l,STUDENT s,DEPARTMENT d,BOOK b1
WHERE l.borrower = s.email
AND b1.ISBN13 = l.book
AND s.department = d.department
AND b1.title LIKE '%Calculus%'
GROUP BY d.faculty
HAVING COUNT(DISTINCT b1.ISBN13) = (
SELECT DISTINCT count(*) 
FROM BOOK b
WHERE b.title LIKE '%Calculus%'
);

SELECT DISTINCT count(*) 
FROM BOOK b
WHERE b.title LIKE '%Calculus%';
