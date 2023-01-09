CREATE TABLE IF NOT EXISTS "users" (
	"id" serial NOT NULL,
	"user_id" bigint NOT NULL UNIQUE,
	"reg_date" timestamptz NOT NULL,
	CONSTRAINT "users_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE IF NOT EXISTS "devices" (
	"id" serial NOT NULL,
	"name" varchar(50) NOT NULL,
	"ip" varchar(50) NOT NULL,
    "status" varchar(10),
	"do_not_disturb" BOOLEAN NOT NULL,
	"notify" BOOLEAN NOT NULL DEFAULT TRUE,
	"change_date" timestamptz NOT NULL,
	"user_id" bigint NOT NULL,
	CONSTRAINT "devices_pk" PRIMARY KEY ("id"),
    CONSTRAINT "devices_fk0"
    FOREIGN KEY ("user_id")
    REFERENCES "users" ("user_id")
    ON DELETE CASCADE
) WITH (
  OIDS=FALSE
);
