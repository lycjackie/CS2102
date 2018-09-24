elect *
from likes natural left outer join (sells natural join restaurants);

select s.pizza, count(DISTINCT r.rname ) as numRes , count(DISTINCT r.area) as numArea
from sells s , restaurants r
where s.rname = r.rname
group by s.pizza;

with PizzaStat as  (select s.pizza, count(DISTINCT s.rname) as numRes , count(DISTINCT r.area) as numArea
from sells s , restaurants r
where s.rname = r.rname
group by s.pizza)
Select distinct l.cname,st.numRes
from likes l, Pizzastat st
where l.pizza = st.pizza
AND (st.numRes < 10 OR st.numArea < 5);


with PizzaStat as  (select s.pizza, count(DISTINCT s.rname) as numRes , count(DISTINCT r.area) as numArea
from sells s , restaurants r
where s.rname = r.rname
group by s.pizza)
Select Distinct c.cname
from customers c
Minus (
Select distinct l.cname
from likes l, Pizzastat st
where l.pizza = st.pizza
AND (st.numRes < 10 OR st.numArea < 5)
);


Select distinct c.cname
from customers c, likes l
where l.pizza not in (
select s.pizza
from sells s , restaurants r
where s.rname = r.rname
group by s.pizza
having count(r.rname) < 10
OR count(r.area) < 5)
and c.cname = l.cname;
