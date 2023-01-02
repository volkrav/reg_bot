CREATE TABLE "public.users" (
	"id" serial NOT NULL,
	"user_id" bigint NOT NULL,
	"reg_date" TIMESTAMP NOT NULL,
	CONSTRAINT "users_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.devices" (
	"id" serial NOT NULL,
	"name" character varying(50) NOT NULL,
	"ip" character varying(50) NOT NULL,
	"do_not_disturb" BOOLEAN NOT NULL,
	"notify" BOOLEAN NOT NULL,
	"user_id" bigint NOT NULL,
	CONSTRAINT "devices_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);




ALTER TABLE "devices" ADD CONSTRAINT "devices_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("user_id");


