PRAGMA foreign_keys = ON;

insert into persons values('Trayvon','Fox','1892-07-17','PeaceRiver,AB','133 Street PR','443-449-9999');
insert into persons values ('Lillian', 'Bounds', '1899-02-15', 'Spalding, Idaho', 'Los Angeles, US', '213-555-5556');
insert into persons values ('Adam','Rafiei',"1900-01-02","Shiraz,Iran","Tehran,Iran","916-331-3311");
insert into persons values('James','Smith','1900-08-08','Calgary,AB','43,43Ave','720-000-0001');
insert into persons values ('Walt', 'Disney', '1901-12-05', 'Chicago, US', 'Los Angeles, US', '213-555-5555');
insert into persons values('Mary','Brown','1905-11-15','Nordegg,AB','22,67Ave','776-655-9955');
insert into persons values ('John', 'Truyens', '1907-05-15', 'Flanders, Belgium', 'Beverly Hills, Los Angeles, US', '213-555-5558');
insert into persons values('Linda','Smith','1908-02-26','Ohaton,AB','43,43Ave','680-099-9943');
insert into persons values ('Minnie', 'Mouse', '1928-01-05', 'Disneyland', 'Anaheim, US', '714-555-5552');
insert into persons values ('Mickey', 'Mouse', '1928-01-05', 'Disneyland', 'Anaheim, US', '714-555-5551');
insert into persons values ("Mary","Smith","1950-11-08","Calgary,AB","11Ave,1st","604-555-2244");
insert into persons values ("Aunt","Smith","1951-12-08","Calgary,AB","11Ave,1st","888-555-2244");
insert into persons values ("Dave","Fox","1950-03-29","Calgary,AB","11Ave,1st","664-110-8763");
insert into persons values ("Uncle","Fox","1951-03-29","Calgary,AB","11Ave,1st","780-110-8743");
insert into persons values ('Michael','Fox','1981-06-09','Edmonton, AB','Manhattan, New York, US', '212-111-1111');
insert into persons values ('Cousin1','Fox','1981-06-09','Edmonton, AB','Manhattan, New York, US', '666-111-1111');
insert into persons values ('Cousin2','Fox','1991-02-06','Edmonton, AB','Manhattan, New York, US', '666-111-1111');
insert into persons values ("Megan","Fox","1982-06-09","Calgary,AB","12Ave,101st","780-460-1134");
insert into persons values ("Fatima","Fox","1992-06-09","Calgary,AB","12Ave,101st","444-470-7734");
insert into persons values ("Lisa","Bounds","1999-04-10","Spalding,Idaho","Moscow,101st","604-420-1234");
insert into persons values('Diane','Wong','1973-04-04','England','London,Hackney','766-664-6678');
insert into persons values ('Davood','Rafiei',date('now','-21 years'),'Iran','100 Lovely Street,Edmonton,AB', '780-111-2222');
insert into persons values('Linda','Fox','1991-02-04','England','London','344-447-7755');
insert into persons values('Tammy','Fox','1991-02-04','England','Manchester','344-111-2345');
insert into persons values('Henry','Wong','1993-04-04','Canada','Alert','566-664-6678');
insert into persons values('Michael','Parenti','1991-02-04','England','London','344-447-7755');
--insert into persons values('','','','','','');

insert into births values (1,'Mary','Smith','1920-04-04','Ohaton,AB','F','James','Smith','Linda','Smith');
insert into births values (2,'Aunt','Smith','1922-06-04','Ohaton,AB','F','James','Smith','Linda','Smith');
insert into births values (3,'Dave','Fox','1922-03-06','Calgary,AB','M','Trayvon','Fox','Mary','Brown');
insert into births values (5,'Uncle','Fox','1925-11-06','Calgary,AB','M','Trayvon','Fox','Mary','Brown');
insert into births values (6,'Cousin1', 'Fox', '1982-06-10', 'Edmonton,AB', 'F', 'Walt', 'Disney', 'Aunt', 'Smith');
insert into births values (7,'Cousin2', 'Fox', '1991-02-06', 'Edmonton,AB', 'F', 'Uncle', 'Fox', 'Lillian', 'Bounds');
insert into births values (100,'Mickey', 'Mouse', '1928-02-05', 'Anaheim, US', 'M', 'Walt', 'Disney', 'Lillian', 'Bounds');
insert into births values (200,'Minnie', 'Mouse', '1928-02-04', 'Anaheim, US', 'M', 'Walt', 'Disney', 'Lillian', 'Bounds');
insert into births values (300,'Michael', 'Fox', '1981-06-10', 'Edmonton,AB', 'M', 'Dave', 'Fox', 'Mary', 'Smith');
insert into births values (310,'Megan', 'Fox', '1982-06-10', 'Edmonton,AB', 'F', 'Dave', 'Fox', 'Mary', 'Smith');
insert into births values (320,'Fatima', 'Fox', '1992-06-10', 'Edmonton,AB', 'F', 'Dave', 'Fox', 'Lillian', 'Bounds');
insert into births values (330,'Adam', 'Rafiei', '1960-02-10', 'Iran', 'M', 'Walt', 'Disney', 'Mary', 'Brown');
insert into births values (400,'Lisa', 'Bounds', '1999-04-16', 'Spalding,Idaho', 'F', 'John', 'Truyens', 'Lillian', 'Bounds');
insert into births values (600,'Davood', 'Rafiei', date('now','-21 years'), 'Iran', 'M', 'Adam', 'Rafiei', 'Mary', 'Smith');
insert into births values(700,'Linda','Fox','1991-02-06','England','F',"Michael","Fox","Lisa","Bounds");
insert into births values(750,'Tammy','Fox','1991-02-04','England','F',"Michael","Fox","Lisa","Bounds");
insert into births values(775,'Henry','Wong','1993-04-05','Canada','M',"Michael","Fox","Diane","Wong");

insert into marriages values (200, '1925-07-13', 'Idaho, US', 'Walt', 'Disney', 'Lillian', 'Bounds');
insert into marriages values (201, '1969-05-03', 'Los Angeles, US', 'Lillian', 'Bounds', 'John', 'Truyens');
insert into marriages values (300, '1990-04-13', 'Idaho, US', 'Michael', 'Fox', 'Lisa', 'Bounds');
insert into marriages values (301, '1992-09-12', 'Idaho, US', 'Diane', 'Wong','Michael', 'Fox');
insert into marriages values (305, '1945-09-11', 'Idaho, US', 'Mickey', 'Mouse', 'Lisa', 'Bounds');

insert into vehicles values (200, 'Chevrolet', 'Camaro', 1969, 'red');
insert into vehicles values (100, 'Doge', 'Challenger', 1969, 'red');
insert into vehicles values (101, 'Doge', 'Challenger', 1969, 'red'); 
insert into vehicles values (300, 'Mercedes', 'SL 230', 1969, 'black');
insert into vehicles values (400, 'Mercedes', 'Benz', 1980, 'white');
insert into vehicles values (500, 'Ferrari', 'F1', 1999, 'red');
insert into vehicles values (600, 'Toyota', 'Camry', 2005, 'black');
insert into vehicles values (700, 'Nissan', 'Altima', 2005, 'black');
insert into vehicles values (801, 'Honda', 'Accord', 2005, 'white');
insert into vehicles values (800, 'Maza', '3', 2005, 'white');
insert into vehicles values (900, 'Nissan', 'Altima', 2010, 'red');
insert into vehicles values (1000, 'Nissan', 'Altima', 2010, 'blue');
insert into vehicles values (1001, 'Toyota', 'Camry', 2010, 'green');

insert into registrations values (300, '1964-05-06','1965-05-06', 'Plate1',100, 'Walt', 'Disney');
insert into registrations values (302, '2019-01-06','2020-01-06', 'Plate2',100, 'Lillian', 'Bounds');
insert into registrations values (801, '2019-01-06','2020-08-25', 'Plate3',101, 'Michael', 'Fox');
insert into registrations values (802, '2018-12-08','2019-12-08', 'Plate4',300, "Diane","Wong");
insert into registrations values (803, '2018-01-08','2020-01-08', 'Plate5',200, "Diane","Wong");
insert into registrations values (804, '2018-12-25','2019-12-25', 'Plate6',500, "Diane","Wong");
insert into registrations values (805, '2018-12-16','2020-12-16', 'Plate7',600, 'John', 'Truyens');
insert into registrations values (901, '2018-11-16','2019-11-16', 'Plate9',801, 'John', 'Truyens');
insert into registrations values (902, '2016-10-11','2017-10-11', 'PlateA',800, 'Lisa', 'Bounds');
insert into registrations values (806, '1999-01-11','2001-01-11', 'Plate8',900, 'John', 'Truyens');
insert into registrations values (903, '2016-02-29','2018-02-28', 'PlateB', 1000, 'Lisa', 'Bounds');
insert into registrations values (905, '2017-06-26','2019-06-26', 'PlateC', 1001, 'Davood', 'Rafiei');
insert into registrations values (1001, '2019-01-16','2021-01-16', 'PlateD',200, 'John', 'Truyens');
insert into registrations values (1002, '2018-11-11','2020-11-11', 'PlateE',100, 'Lisa', 'Bounds');
insert into registrations values (1003, '2018-01-11','2019-09-30', 'PlateF',101, 'John', 'Truyens');
insert into registrations values (1004, '2019-02-29','2020-02-28', 'PlateG', 700, 'Lisa', 'Bounds');
insert into registrations values (1005, '2019-06-26','2020-06-26', 'PlateH', 1000, 'Davood', 'Rafiei');

insert into tickets values (100,300,40,'red light violation','1964-08-20');
insert into tickets values (101,805,40,'red light violation','2018-12-20');
insert into tickets values (107,905,40,'red violation','2019-01-20');
insert into tickets values (109,902,150,'yellow light violation','2018-01-21');
insert into tickets values (108,803,150,'Stunting','2019-02-29');
insert into tickets values (102,901,220,'DUI','2019-02-18');
insert into tickets values (103,806,70,'illegal parking','2016-08-30');
insert into tickets values (104,805,40,'speeding','2019-02-29');
insert into tickets values (105,905,10,'yellow light violation','2019-02-28');
insert into tickets values (106,905,220,'red violation','2018-12-30');
insert into tickets values (111,805,220,'DUI','2019-06-12');
insert into tickets values (112,801,220,'red light violation','2019-06-30');
insert into tickets values (113,801,221,'grand theft auto','2020-12-30');
insert into tickets values (114,801,222,'grand theft auto','2020-12-30');
insert into tickets values (115,801,222,'grand theft auto','2020-12-30');

insert into demeritNotices values ('1991-03-29', 'Lisa', 'Bounds', 10, 'DUI');
insert into demeritNotices values ('2018-07-20', 'Michael', 'Fox', 4, 'Speeding');
insert into demeritNotices values ('1993-04-25', 'Diane', 'Wong', 2, 'Speeding');
insert into demeritNotices values ('2018-03-20', 'Michael', 'Fox', 12, 'DWI');
insert into demeritNotices values ('2019-10-31', 'Diane', 'Wong', 2, 'Speeding');
insert into demeritNotices values ('1964-08-20', 'Walt', 'Disney', 4, 'Speeding');
insert into demeritNotices values ('1991-03-30', 'Lisa', 'Bounds', 4, 'Speeding');
insert into demeritNotices values ('2019-09-28', 'Mickey', 'Mouse', 12, 'DUI');
insert into demeritNotices values ('2018-08-20', 'Walt', 'Disney', 20, 'Vehicular Manslaughter');
insert into demeritNotices values ('1994-03-30', 'Lisa', 'Bounds', 4, 'Speeding');
insert into demeritNotices values ('2019-03-22', 'Mickey', 'Mouse', 12, 'DUI');

-- Some additional data test test Q1
insert into persons values('Diane','Lee','1973-04-04','England','London,Hackney','434-596-234');

insert into vehicles values (201,'Chevrolet','Cruze','1969','gold');
insert into vehicles values (202,'Abc','Camaro','1969',	'pink');
insert into vehicles values (203,'Chevrolet','Camaro','1999','pink');
insert into vehicles values (204,'Chevrolet','Camaro','1969','gold');

insert into registrations values (201,'2013-02-11','2015-02-14','plate100','201','Diane','Lee');
insert into registrations values (202,'2013-02-11','2015-02-14','plate100','202','Diane','Lee');
insert into registrations values (203,'2013-02-11','2015-02-14','plate100','203','Diane','Lee');
insert into registrations values (204,'2013-02-11','2015-02-14','plate100','204','Diane','Wong');

-- Some additional data to test Q2
insert into persons values('Robert','Conner','1850-11-02','United States','Mississippi','443-449-9999');
insert into persons values('Fox','Conner','1874-11-02','United States','Mississippi','443-449-9999');
insert into persons values('Michael','Clarke','1981-04-02','Australia','Liverpool','344-447-7755');

insert into births values (800,'Fox','Conner','1874-11-02','United States','M','Robert','Conner','Mary','Smith');
insert into births values (850,'Michael','Clarke','1981-04-02','Australia','M',null,null,'Mary','Smith');

-- Some additional data to test Q5
INSERT INTO registrations (regno, regdate, expiry, plate, vin, fname, lname) VALUES (404, '2017-01-10', '2018-01-10', 'PlateN', '400', 'Mary', 'Brown');
INSERT INTO registrations (regno, regdate, expiry, plate, vin, fname, lname) VALUES (405, '2018-02-10', '2018-08-10', 'PlateM', '400', 'Mary', 'Smith');

INSERT INTO demeritNotices (ddate, fname, lname, points, desc) VALUES ('2019-10-11', 'Lisa', 'Bounds', 2, 'Speeding');
INSERT INTO demeritNotices (ddate, fname, lname, points, desc) VALUES ('2019-10-10', 'Lillian', 'Bounds', 14, 'Unknown');
INSERT INTO demeritNotices (ddate, fname, lname, points, desc) VALUES ('2017-11-11', 'Mary', 'Brown', 10, 'Unknown');
INSERT INTO demeritNotices (ddate, fname, lname, points, desc) VALUES ('2018-04-10', 'Mary', 'Smith', 6, 'Unknown');
INSERT INTO demeritNotices (ddate, fname, lname, points, desc) VALUES ('2017-10-13', 'Lisa', 'Bounds', 16, 'Unknown');
INSERT INTO demeritNotices (ddate, fname, lname, points, desc) VALUES ('1994-01-05', 'Davood', 'Rafiei', 14, 'Unknown');
INSERT INTO demeritNotices (ddate, fname, lname, points, desc) VALUES ('2019-01-02', 'Davood', 'Rafiei', 2, 'Unknown');

insert into persons values("Daniel", "Florendo", "1999-08-18", "Philippines", "123 Rainbow Road", "780-707-7690");
insert into persons values("Ibrahim", "Aly", "1998-08-04", "Cairo, Egypt", "Southside", "780-707-7691");
insert into persons values("Raynard", "Dizon", "1999-05-12", "St. Albert, Alberta", "35 Lafleur Dr.", "587-988-182");
insert into persons values("Hugh", "Janus", "1999-04-06", "St. Albert, Alberta", "35 Mountainview Pt.", "780-909-8863");


insert into users values("florendo", "FLORENDO", "a", "Daniel", "Florendo", "Sherwood Park");
insert into users values("ialy", "IALY", "a", "Ibrahim", "Aly", "Edmonton");
insert into users values("rdizon", "RDIZON", "a", "Raynard", "Dizon", "St. Albert");
insert into users values("hjanus", "hjanus1", "o", "Hugh", "Janus", "Edmonton");