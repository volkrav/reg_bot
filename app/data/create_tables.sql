CREATE TABLE users (
	id integer PRIMARY KEY AUTOINCREMENT,
	user_id integer,
	reg_date datetime
);

CREATE TABLE devices (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar,
	ip varchar,
	do_not_disturb integer,
	notify integer,
	user_id integer
);
