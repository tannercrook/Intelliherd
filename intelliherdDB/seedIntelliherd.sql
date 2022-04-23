/* 

seedIntelliherd.sql
================================================
(c) 2019 CrookTec LLC
Author: Tanner Crook
-----------------------------------------------
This script will seed the data for the intelliherd
database. 

*/


-- Insert the base user for the system
INSERT INTO system_user 
( email 
, first_name
, last_name)
VALUES 
( 'systems@crooktec.com'
, 'SYSTEM'
, 'CROOKTEC');


-- Insert the other users for the testbed data
INSERT INTO system_user 
( email 
, first_name
, last_name)
VALUES 
( 'tanner@crooktec.com'
, 'Tanner'
, 'Crook');

INSERT INTO system_user 
( email 
, first_name
, last_name)
VALUES 
( 'aleecrook@gmail.com'
, 'Alee'
, 'Crook');





-- System-wide Data
-- ----------------------------------------
INSERT INTO subscription
( name 
, max_farms 
, max_users 
, max_animals 
, start_date
, price_monthly
, price_annual
, created_by
, modified_by)
VALUES 
( 'Personal'
, 1
, 1
, 10
, CURRENT_DATE 
, 5.00
, 50.00
, 2
, 2 );

INSERT INTO subscription
( name 
, max_farms 
, max_users 
, max_animals 
, start_date
, price_monthly
, price_annual
, created_by
, modified_by)
VALUES 
( 'Business'
, 1
, 4
, 200
, CURRENT_DATE 
, 30.00
, 300.00
, 2
, 2 );

INSERT INTO subscription
( name 
, max_farms 
, max_users 
, max_animals 
, start_date
, price_monthly
, price_annual
, created_by
, modified_by)
VALUES 
( 'Business Gold'
, 2
, 10
, 500
, CURRENT_DATE 
, 50.00
, 500.00
, 2
, 2 );

INSERT INTO subscription
( name 
, max_farms 
, max_users 
, max_animals 
, start_date
, price_monthly
, price_annual
, created_by
, modified_by)
VALUES 
( 'Enterprise'
, 5
, 50
, 10000
, CURRENT_DATE 
, 500.00
, 5000.00
, 2
, 2 );

INSERT INTO subscription
( name 
, max_farms 
, max_users 
, max_animals 
, start_date
, price_monthly
, price_annual
, created_by
, modified_by)
VALUES 
( 'Enterprise Gold'
, 5
, 100
, 50000
, CURRENT_DATE 
, 1000.00
, 10000.00
, 2
, 2 );

INSERT INTO subscription
( name 
, max_farms 
, max_users 
, max_animals 
, start_date
, price_monthly
, price_annual
, created_by
, modified_by)
VALUES 
( '4-H'
, 1
, 25
, 50
, CURRENT_DATE 
, 0.00
, 0.00
, 2
, 2 );


INSERT INTO payment_type
( name 
, code 
, web_enabled )
VALUES 
  ( 'VISA', 'VISA', 1 )
, ( 'American Express', 'AMEX', 1 )
, ( 'MasterCard', 'MASTER', 1 )
, ( 'E-Check', 'ECHECK', 0 )
, ( 'Check', 'CHECK', 0 )
, ( 'Coupon', 'COUPON', 0 );


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










-- Insert into organization
-- -----------------------------------------------------

INSERT INTO organization 
( name )
VALUES 
( 'Crook Family Farms' );

INSERT INTO purchase_order
( organization_id 
, user_id
, processed_by
, payment_type_id
, subscription_id
, total_amount )
VALUES 
( 1
, 2
, 2
, 6
, (SELECT subscription_id FROM "subscription" WHERE name = 'Business Gold')
, 0.00 );

INSERT INTO org_subscription
( organization_id
, subscription_id
, end_date
, months_duration
, order_id )
VALUES 
( 1
, (SELECT subscription_id FROM "subscription" WHERE name = 'Business Gold')
, CURRENT_DATE+INTERVAL '1 year'
, 12
, 2 );

INSERT INTO organization 
( name )
VALUES 
( 'Salt River Ranch' );

INSERT INTO purchase_order
( organization_id 
, user_id
, processed_by
, payment_type_id
, subscription_id
, total_amount )
VALUES 
( 2
, 3
, 2
, 6
, (SELECT subscription_id FROM "subscription" WHERE name = 'Business Gold')
, 0.00 );

INSERT INTO org_subscription
( organization_id
, subscription_id
, end_date
, months_duration
, order_id )
VALUES 
( 2
, (SELECT subscription_id FROM "subscription" WHERE name = 'Business Gold')
, CURRENT_DATE+INTERVAL '1 year'
, 12
, 2 );



-- Default roles (will be made with each new org)
-- --------------------------------------------------------------------------------
INSERT INTO role 
( name 
, organization_id
, organization_mask
, farm_mask
, user_mask
, animal_mask )
VALUES 
  ('Organization Admin', 1, 777, 777, 777, 777 )
, ('Farm Admin', 1, 555, 777, 777, 777)
, ('Farm Worker', 1, 000, 555, 000, 777)
, ('Read Only', 1, 000, 555, 555, 555)
, ('Organization Read', 1, 555, 555, 555, 555);

INSERT INTO role 
( name 
, organization_id
, organization_mask
, farm_mask
, user_mask
, animal_mask )
VALUES 
  ('Organization Admin', 2, 777, 777, 777, 777 )
, ('Farm Admin', 2, 555, 777, 777, 777)
, ('Farm Worker', 2, 000, 555, 000, 777)
, ('Read Only', 2, 000, 555, 555, 555)
, ('Organization Read', 2, 555, 555, 555, 555);


-- Locations
INSERT INTO location
( name 
, street_address
, city
, state
, zip 
, organization_id )
VALUES 
  ('Barnyard', '110511 HWY 89', 'Etna', 'WY', '83110', 1)
, ('Lower Fields', '111617 HWY 89', 'Etna', 'WY', '83110', 1)
, ('Ranch', '1130 County Rd', 'Etna', 'WY', '83110', 2);



-- Farms
INSERT INTO farm
( name 
, organization_id
, location_id )
VALUES 
  ( 'Crook Farms', 1, 1 )
, ( 'Salt River Ranch', 2, 3 )
, ( 'Crook Puppers', 1, 1 );


-- User Relations and Permissions
INSERT INTO org_user
( organization_id
, user_id
, role_id )
VALUES 
( 1
, 2
, (SELECT role_id FROM role WHERE name = 'Organization Admin' AND organization_id = 1));

INSERT INTO org_user
( organization_id
, user_id
, role_id )
VALUES 
( 2
, 3
, (SELECT role_id FROM role WHERE name = 'Organization Admin' AND organization_id = 2));