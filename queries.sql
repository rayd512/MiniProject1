-- THIS FILE IS FOR TESTING PURPOSES ONLY
-- number of tickets, 
-- the number of demerit notices, 
-- the total number of demerit points received both within the past two years 
-- and within the lifetime

select rt.fname, rt.lname, tcount, dcount, sum(d1.points) 
from(select r.fname, r.lname, COUNT(distinct tno) as tcount, COUNT(distinct ddate) as dcount
		from ( 
			(registrations r left join tickets t  on (r.regno = t.regno and vdate >= date('now', '-2 years'))) 
			left join demeritNotices d on (r.fname = d.fname and r.lname = d.lname and ddate >= date('now', '-2 years')) 
			)
		group by r.fname, r.lname) rt 
		left join demeritNotices d1 on (rt.fname = d1.fname and rt.lname = d1.lname and ddate >= date('now', '-2 years'))
group by rt.fname, rt.lname
;

select rt.fname, rt.lname, tcount, dcount, sum(d1.points) 
from(select r.fname, r.lname, COUNT(distinct tno) as tcount, COUNT(distinct ddate) as dcount
		from ( 
			(registrations r left join tickets t  on (r.regno = t.regno)) 
			left join demeritNotices d on (r.fname = d.fname and r.lname = d.lname) 
			)
		group by r.fname, r.lname) rt 
		left join demeritNotices d1 on (rt.fname = d1.fname and rt.lname = d1.lname)
group by rt.fname, rt.lname
;
-- The user should be given the option to see the tickets ordered from the latest to the oldest. For each ticket, you will report 
-- the ticket number, 
-- the violation date, 
-- the violation description, 
-- the fine, 
-- the registration number 
-- and the make 
-- and model of the car for which the ticket is issued. 
-- If there are more than 5 tickets, 
-- at most 5 tickets will be shown at a time, 
-- and the user can select to see more.

-- SELECT tno, vdate, violation, fine, r.regno, make, model
-- FROM tickets t, registrations r, vehicles v
-- WHERE t.regno = r.regno
-- AND r.fname = "Raynard" AND r.lname = "Dizon"
-- AND r.vin = v.vin
-- ORDER BY vdate DESC
-- ;