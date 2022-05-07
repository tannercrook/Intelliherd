INSERT INTO animal_status ("name",active,quota_apply,code,date_created,created_by,date_modified,modified_by) VALUES
	 ('Active',1,1,'ACTIVE','2019-11-13 22:12:47.201868',1,'2019-11-13 22:12:47.201868',1),
	 ('Deceased',1,0,'DCSD','2019-11-13 22:12:47.201868',1,'2019-11-13 22:12:47.201868',1),
	 ('Sold',1,0,'SOLD','2019-11-13 22:12:47.201868',1,'2019-11-13 22:12:47.201868',1),
	 ('Inactive',1,0,'INACTV','2019-11-13 22:12:47.201868',1,'2019-11-13 22:12:47.201868',1);
	 
	
insert into country 
( name, abbreviation, active)
values 
('United States of America','USA',1);

insert into state 
(name, abbreviation, active, country_id)
values 
('Wyoming','WY',1,1);

insert into relationship_type 
(name, code, active)
values 
('Mother','MOTHER',1),
('Father','FATHER',1);


INSERT INTO animal_type
( name 
, group_name )
VALUES 
  ( 'Cow', 'Herd' )
, ( 'Dog', 'Pack' )
, ( 'Sheep', 'Flock' )
, ( 'Pig', 'Drove' )
, ( 'Horse', 'Team' )
, ( 'Donkey', 'Herd' )
, ( 'Mule', 'Pack' )
, ( 'Bunny', 'Fluffle' )
, ( 'Chicken', 'Brood' )
, ( 'Goose', 'Gaggle' )
, ( 'Duck', 'Flock' )
, ( 'Goat', 'Tribe' )
, ( 'Fish', 'School' )
, ( 'Deer', 'Herd' )
, ( 'Elk', 'Herd' );



-- Test data 
INSERT INTO system_user 
( email 
, first_name
, last_name)
VALUES 
( 'tannercrook@fakemail.com'
, 'Tanner'
, 'Crook');

INSERT INTO location
( name 
, street_address
, city
, state_id
, zip 
, user_id )
VALUES 
  ('Barnyard', '123 HWY 89', 'Etna', 1, '83110', 1)
, ('Lower Fields', '888 HWY 89', 'Etna', 1, '83110', 1);



insert into transaction_type 
(name, active, type)
values 
('Expenditure',1,'DEBIT'),
('Product Sale',1,'CREDIT'),
('Animal Sale',1,'CREDIT'),
('Loss',1,'DEBIT'),
('Expenditure - Feed',1,'DEBIT'),
('Expenditure - Medical',1,'DEBIT'),
('Expenditure - Habitat',1,'DEBIT');

