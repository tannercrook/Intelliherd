-- schema.sql
-- This file will create the tables for intelliherd


-- public."system_user" definition
-- Drop table
-- DROP TABLE "system_user";

CREATE TABLE "system_user" (
	user_id int4 generated always as identity,
	email varchar(60) NOT NULL,
	first_name varchar(100) NULL,
	last_name varchar(100) NULL,
	"password" varchar NULL,
	salt varchar NULL,
	date_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by int4 NOT NULL DEFAULT 1,
	date_modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	modified_by int4 NOT NULL DEFAULT 1,
	force_password_change int4 NOT NULL DEFAULT 0,
	login_fail_count int4 NOT NULL DEFAULT 0,
	"admin" int4 NOT NULL DEFAULT 0,
	maint_token varchar NULL,
	CONSTRAINT user_pk PRIMARY KEY (user_id),
	CONSTRAINT system_user_fk FOREIGN KEY (created_by) REFERENCES "system_user"(user_id),
	CONSTRAINT system_user_fk_1 FOREIGN KEY (modified_by) REFERENCES "system_user"(user_id)
);
CREATE UNIQUE INDEX system_user_email_idx ON public.system_user USING btree (email);





-- public.country definition
-- Drop table
-- DROP TABLE country;

CREATE TABLE country (
	country_id int4 generated always as identity,
	"name" varchar(200) NOT NULL,
	abbreviation varchar(6) NULL,
	active int4 NOT NULL DEFAULT 1,
	CONSTRAINT country_pk PRIMARY KEY (country_id)
);




-- public.state definition
-- Drop table
-- DROP TABLE state;

CREATE TABLE state (
	state_id int4 generated always as identity,
	"name" varchar(30) NOT NULL,
	abbreviation varchar(2) NOT NULL,
	active int4 NOT NULL DEFAULT 1,
	country_id int4 NOT NULL,
	CONSTRAINT state_pk PRIMARY KEY (state_id),
	CONSTRAINT state_fk FOREIGN KEY (country_id) REFERENCES country(country_id)
);


-- public."location" definition
-- Drop table
-- DROP TABLE "location";

CREATE TABLE "location" (
	location_id int4 generated always as identity,
	"name" varchar(60) NOT NULL,
	street_address varchar(100) NOT NULL,
	city varchar(60) NOT NULL,
	state_id int4 NOT NULL,
	zip varchar(5) NOT NULL,
	user_id int4 not null,
	CONSTRAINT location_pk PRIMARY KEY (location_id),
	CONSTRAINT location_fk_1 FOREIGN KEY (state_id) REFERENCES state(state_id),
	constraint location_fk_2 foreign key (user_id) references system_user(user_id)
);


-- public.farm definition
-- Drop table
-- DROP TABLE farm;

CREATE TABLE farm (
	farm_id int4 generated always as identity,
	user_id int4 not null,
	"name" varchar(60) NOT NULL,
	location_id int4 NOT NULL,
	start_date date NOT NULL DEFAULT CURRENT_DATE,
	end_date date NULL,
	date_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by int4 NOT NULL DEFAULT 1,
	date_modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	modified_by int4 NOT NULL DEFAULT 1,
	CONSTRAINT farm_pk PRIMARY KEY (farm_id),
	constraint farm_fk_1 foreign key (user_id) references system_user(user_id),
	CONSTRAINT farm_fk_2  FOREIGN KEY (location_id) REFERENCES "location"(location_id),
	CONSTRAINT farm_fk_3 FOREIGN KEY (created_by) REFERENCES "system_user"(user_id),
	CONSTRAINT farm_fk_4 FOREIGN KEY (modified_by) REFERENCES "system_user"(user_id)
);



-- public.animal_type definition
-- Drop table
-- DROP TABLE animal_type;

CREATE TABLE animal_type (
	animal_type_id int4 generated always as identity,
	"name" varchar(60) NOT NULL,
	group_name varchar(60) NOT NULL,
	active int4 NOT NULL DEFAULT 1,
	CONSTRAINT animal_type_pk PRIMARY KEY (animal_type_id)
);




-- public.animal_status definition
-- Drop table
-- DROP TABLE animal_status;

CREATE TABLE animal_status (
	animal_status_id int4 generated always as identity,
	"name" varchar(30) NOT NULL,
	active int4 NOT NULL DEFAULT 1,
	quota_apply int4 NOT NULL DEFAULT 1,
	code varchar(6) NOT NULL,
	date_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by int4 NOT NULL DEFAULT 1,
	date_modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	modified_by int4 NOT NULL DEFAULT 1,
	CONSTRAINT animal_status_pk PRIMARY KEY (animal_status_id)
);





-- public.animal definition
-- Drop table
-- DROP TABLE animal;

CREATE TABLE animal (
	animal_id int4 generated always as identity,
	farm_id int4 NOT NULL,
	animal_type_id int4 NOT NULL DEFAULT 1,
	breed_id int4 NULL,
	gender varchar(1) NOT NULL DEFAULT 'F'::character varying,
	birthdate date NULL,
	"number" varchar(60) NULL,
	"name" varchar(60) NULL,
	scan_number int4 NULL,
	date_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by int4 NOT NULL DEFAULT 1,
	date_modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	modified_by int4 NOT NULL DEFAULT 1,
	animal_status_id int4 NOT NULL DEFAULT 1,
	CONSTRAINT animal_pk PRIMARY KEY (animal_id),
	CONSTRAINT animal_fk FOREIGN KEY (farm_id) REFERENCES farm(farm_id),
	CONSTRAINT animal_fk_1 FOREIGN KEY (animal_type_id) REFERENCES animal_type(animal_type_id),
	CONSTRAINT animal_fk_2 FOREIGN KEY (created_by) REFERENCES "system_user"(user_id),
	CONSTRAINT animal_fk_3 FOREIGN KEY (modified_by) REFERENCES "system_user"(user_id),
	CONSTRAINT animal_fk_4 FOREIGN KEY (animal_status_id) REFERENCES animal_status(animal_status_id)
);



-- public.vaccine definition
-- Drop table
-- DROP TABLE vaccine;

CREATE TABLE vaccine (
	vaccine_id int4 generated always as identity,
	"name" varchar(100) NOT NULL,
	animal_type_id int4 NOT NULL,
	required int4 NOT NULL DEFAULT 0,
	active int4 NOT NULL DEFAULT 1,
	barcode varchar NULL,
	created_by int4 NOT NULL DEFAULT 1,
	date_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	modified_by int4 NOT NULL DEFAULT 1,
	date_modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	code varchar(6) NOT NULL,
	CONSTRAINT newtable_pk PRIMARY KEY (vaccine_id),
	CONSTRAINT newtable_fk FOREIGN KEY (animal_type_id) REFERENCES animal_type(animal_type_id),
	CONSTRAINT newtable_fk_1 FOREIGN KEY (created_by) REFERENCES "system_user"(user_id),
	CONSTRAINT newtable_fk_2 FOREIGN KEY (modified_by) REFERENCES "system_user"(user_id)
);


-- public.vaccine_dose definition
-- Drop table
-- DROP TABLE vaccine_dose;

CREATE TABLE vaccine_dose (
	dose_id int4 generated always as identity,
	animal_id int4 NOT NULL,
	"date" date NOT NULL DEFAULT CURRENT_DATE,
	recorded_by int4 NOT NULL,
	recorded_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	vaccine_id int4 NOT NULL,
	CONSTRAINT vaccine_dose_pk PRIMARY KEY (dose_id),
	CONSTRAINT vaccine_dose_fk FOREIGN KEY (animal_id) REFERENCES animal(animal_id) ON DELETE CASCADE,
	CONSTRAINT vaccine_dose_fk_1 FOREIGN KEY (recorded_by) REFERENCES "system_user"(user_id),
	CONSTRAINT vaccine_dose_fk_2 FOREIGN KEY (vaccine_id) REFERENCES vaccine(vaccine_id)
);


-- public.pen definition
-- Drop table
-- DROP TABLE pen;

CREATE TABLE pen (
	pen_id int4 generated always as identity,
	farm_id int4 NOT NULL,
	"name" varchar(60) NOT NULL,
	location_id int4 NULL,
	active int4 NOT NULL DEFAULT 1,
	created_by int4 NOT NULL DEFAULT 1,
	date_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	modified_by int4 NOT NULL DEFAULT 1,
	date_modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	max_occupancy int4 NULL,
	CONSTRAINT pen_pk PRIMARY KEY (pen_id),
	CONSTRAINT pen_fk FOREIGN KEY (farm_id) REFERENCES farm(farm_id) ON DELETE CASCADE,
	CONSTRAINT pen_fk_1 FOREIGN KEY (location_id) REFERENCES "location"(location_id),
	CONSTRAINT pen_fk_2 FOREIGN KEY (created_by) REFERENCES "system_user"(user_id),
	CONSTRAINT pen_fk_3 FOREIGN KEY (modified_by) REFERENCES "system_user"(user_id)
);



-- public.pen_member definition
-- Drop table
-- DROP TABLE pen_member;

CREATE TABLE pen_member (
	pen_member_id int4 generated always as identity,
	pen_id int4 NOT NULL,
	animal_id int4 NOT NULL,
	start_date date NOT NULL DEFAULT CURRENT_DATE,
	end_date date NULL,
	start_note text NULL,
	end_note text NULL,
	created_by int4 NOT NULL DEFAULT 1,
	date_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	modified_by int4 NOT NULL DEFAULT 1,
	date_modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT pen_member_pk PRIMARY KEY (pen_member_id),
	CONSTRAINT pen_member_fk FOREIGN KEY (pen_id) REFERENCES pen(pen_id) ON DELETE CASCADE,
	CONSTRAINT pen_member_fk_1 FOREIGN KEY (animal_id) REFERENCES animal(animal_id) ON DELETE CASCADE,
	CONSTRAINT pen_member_fk_2 FOREIGN KEY (created_by) REFERENCES "system_user"(user_id),
	CONSTRAINT pen_member_fk_3 FOREIGN KEY (modified_by) REFERENCES "system_user"(user_id)
);


-- public.relationship_type definition
-- Drop table
-- DROP TABLE relationship_type;

CREATE TABLE relationship_type (
	relationship_type_id int4 generated always as identity,
	"name" varchar(20) NOT NULL,
	code varchar(6) NOT NULL,
	active int4 NOT NULL DEFAULT 1,
	CONSTRAINT relationship_type_pk PRIMARY KEY (relationship_type_id)
);


-- public.relationship definition
-- Drop table
-- DROP TABLE relationship;

CREATE TABLE relationship (
	relationship_id int4 generated always as identity,
	animal_id int4 NOT NULL,
	parent_id int4 NOT NULL,
	relationship_type_id int4 NOT NULL,
	artificial int4 NOT NULL DEFAULT 0,
	created_by int4 NOT NULL DEFAULT 1,
	date_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	modified_by int4 NOT NULL DEFAULT 1,
	date_modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT relationship_pk PRIMARY KEY (relationship_id),
	CONSTRAINT relationship_fk FOREIGN KEY (relationship_type_id) REFERENCES relationship_type(relationship_type_id),
	CONSTRAINT relationship_fk_1 FOREIGN KEY (animal_id) REFERENCES animal(animal_id) ON DELETE CASCADE,
	CONSTRAINT relationship_fk_2 FOREIGN KEY (parent_id) REFERENCES animal(animal_id) ON DELETE CASCADE,
	CONSTRAINT relationship_fk_3 FOREIGN KEY (created_by) REFERENCES "system_user"(user_id),
	CONSTRAINT relationship_fk_4 FOREIGN KEY (modified_by) REFERENCES "system_user"(user_id)
);




-- public.transaction_type definition
-- Drop table
-- DROP TABLE transaction_type;

CREATE TABLE transaction_type (
	transaction_type_id int4 generated always as identity,
	"name" varchar(60) NOT NULL,
	active int4 NULL DEFAULT 1,
	"type" varchar(30) NOT NULL DEFAULT 'Expenditure'::character varying,
	CONSTRAINT expense_type_pk PRIMARY KEY (transaction_type_id),
	CONSTRAINT expense_type_uq1 UNIQUE (name)
);


-- public.transaction_log definition
-- Drop table
-- DROP TABLE transaction_log;

CREATE TABLE transaction_log (
	transaction_log_id int4 generated always as identity,
	animal_id int4 NOT NULL,
	transaction_type_id int4 NOT NULL,
	title varchar(30) NOT NULL,
	note text NULL,
	amount numeric(12, 2) NOT NULL DEFAULT 0.00,
	created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by int4 NOT NULL,
	transaction_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT transaction_log_pk PRIMARY KEY (transaction_log_id),
	CONSTRAINT transaction_log_fk1 FOREIGN KEY (animal_id) REFERENCES animal(animal_id),
	CONSTRAINT transaction_log_fk2 FOREIGN KEY (transaction_type_id) REFERENCES transaction_type(transaction_type_id),
	CONSTRAINT transaction_log_fk3 FOREIGN KEY (created_by) REFERENCES "system_user"(user_id)
);


