insert into persons values("Daniel", "Florendo", "1999-08-18", "Philippines", "123 Rainbow Road", "780-707-7690");
insert into persons values("Ibrahim", "Aly", "1998-08-04", "Cairo, Egypt", "Southside", "780-707-7691");
insert into persons values("Raynard", "Dizon", "1999-05-12", "St. Albert, Alberta", "35 Lafleur Dr.", "587-988-182");
insert into persons values("Hugh", "Janus", "1999-04-06", "St. Albert, Alberta", "35 Mountainview Pt.", "780-909-8863");


insert into users values("florendo", "FLORENDO", "a", "Daniel", "Florendo", "Sherwood Park");
insert into users values("ialy", "IALY", "a", "Ibrahim", "Aly", "Edmonton");
insert into users values("rdizon", "RDIZON", "a", "Raynard", "Dizon", "St. Albert");
insert into users values("hjanus", "hjanus1", "o", "Hugh", "Janus", "Edmonton");

insert into vehicles values("099174", "Mitsubishi", "Lancer", 2009, "Silver");
insert into vehicles values("275215", "Accura", "Civic", 2008, "Blue");
insert into vehicles values("418611", "Ford", "Shelby", 1986, "Champagne");
insert into vehicles values("123456", "Toyota", "LandCruiser", 2001, "White");

insert into registrations values(1, "2018-10-15", "2020-10-15", "CBB9961", "099174", "Daniel", "Florendo");
insert into registrations values(2, "2018-10-14", "2020-10-14", "HTQ4028", "275215", "Raynard", "Dizon");
insert into registrations values(3, "2018-10-16", "2020-10-16", "DZF5598", "418611", "Ibrahim", "Aly");
insert into registrations values(4, "2018-10-17", "2020-10-17", "ABC1234", "123456", "Ibrahim", "Aly");

insert into tickets values(100, 1, 200, "DUI", "1999-05-03");
insert into tickets values(101, 1, 300, "Speeding", "2018-02-04");
insert into tickets values(102, 1, 450, "Reckless Driving", "2019-01-03");
insert into tickets values(103, 1, 100, "Redlight Infraction", "2019-01-04");
insert into tickets values(104, 1, 150, "Assaulting a Peace Officer", "2019-01-05");
insert into tickets values(105, 1, 300, "Jail Time son", "2019-01-06");

insert into demeritNotices values("1995-03-08", "Daniel", "Florendo", 3, "DanNotice 1");
insert into demeritNotices values("2018-09-02", "Daniel", "Florendo", 4, "DanNotice 2");
insert into demeritNotices values("2018-09-04", "Daniel", "Florendo", 5, "DanNotice 4");
insert into demeritNotices values("2018-09-03", "Daniel", "Florendo", 4, "DanNotice 3");

insert into tickets values(201, 2, 300, "Speeding", "2010-02-04");
insert into tickets values(202, 2, 450, "Reckless Driving", "2010-01-03");

insert into demeritNotices values("1995-03-08", "Raynard", "Dizon", 1, "RayNotice 1");
insert into demeritNotices values("2010-09-02", "Raynard", "Dizon", 10, "RayNotice 2");
insert into demeritNotices values("2010-09-04", "Raynard", "Dizon", 5, "RayNotice 4");
insert into demeritNotices values("2010-09-03", "Raynard", "Dizon", 4, "RayNotice 3");

insert into tickets values(300, 3, 200, "DUI", "1999-05-03");
insert into tickets values(301, 3, 300, "Speeding", "2018-02-04");
insert into tickets values(302, 3, 450, "Reckless Driving", "2019-01-03");
insert into tickets values(303, 3, 100, "Redlight Infraction", "2019-01-04");
insert into tickets values(304, 3, 150, "Assaulting a Peace Officer", "2019-01-05");
insert into tickets values(305, 3, 300, "Jail Time son", "2019-01-06");
insert into tickets values(306, 3, 200, "DUI", "1998-05-03");
insert into tickets values(307, 4, 300, "Speeding", "2017-02-04");
insert into tickets values(308, 4, 450, "Reckless Driving", "2019-01-11");
insert into tickets values(309, 4, 100, "Redlight Infraction", "2015-01-04");
insert into tickets values(310, 4, 150, "Assaulting a Peace Officer", "2019-01-13");
insert into tickets values(311, 4, 300, "Jail Time son", "2019-01-26");