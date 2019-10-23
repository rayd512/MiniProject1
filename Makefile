refresh:
	rm prj.db
	sqlite3 prj.db < prj-tables.sql
	sqlite3 prj.db < prj-data.sql

compile:
	sqlite3 prj.db < prj-tables.sql
	sqlite3 prj.db < prj-data.sql