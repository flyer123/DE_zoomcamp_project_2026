-- create the datatase
CREATE DATABASE flight_analytics;


-- create a role to the terraform user with minimal privileges
CREATE ROLE TERRAFORM_MANAGER;

-- allow the role to create schema
GRANT CREATE SCHEMA ON DATABASE FLIGHT_ANALYTICS TO ROLE TERRAFORM_MANAGER;

-- allow the role to access to the database
GRANT USAGE ON DATABASE FLIGHT_ANALYTICS TO ROLE TERRAFORM_MANAGER;

-- allow the role to access all schemas in the database
GRANT ALL ON ALL SCHEMAS IN DATABASE FLIGHT_ANALYTICS TO ROLE TERRAFORM_MANAGER;

-- allow the role to create a warehouse
GRANT CREATE WAREHOUSE ON ACCOUNT TO ROLE TERRAFORM_MANAGER;

-- create terraform user
USE ROLE ACCOUNTADMIN;

CREATE USER TERRAFORM_SVC
    TYPE = SERVICE
    COMMENT = "Service user for Terraforming Snowflake"
    RSA_PUBLIC_KEY = "<RSA_PUBLIC_KEY_HERE>";
    
-- grant the role to the user
GRANT ROLE TERRAFORM_MANAGER TO USER TERRAFORM_SVC

