Running simulations is easy but it takes some time to prepare the data.

Data Preparation
================
I would recommend using a local copy of Postgres database for the simulation data.

1) Create a schema for the simulation data
    - run data/sql/create_adquality_schema.sql

2) Extract predictors data from the analytics prod and import the predictors into the local database
    - run data/sql/extract_predictors.sql script to dump data to CSV file
    - use pgAdmin or DbVisualizer to load CSV file into "predictors" table (both tools provide such capability)

3) Extract impressions and IAS data and import it into the local database
    - run data/sql/extract_impressions.sql to dump data to CSV file
    - use pgAdmin or DbVisualizer to load CSV file into "impressions" table (both tools provide such capability)

Mini tutorial how to dump table's data from GreenPlum
------------------------------------------------------
psql -h <GreenPlum host> -d vds_prd -U <your username>

vrd_prd => \f ','
vrd_prd => \a
vrd_prd => \o <path to the output csv file name>
vrd_prd => <ENTER SQL>
vrd_prd => \q

Python Environment
==================

To configure the python environment two steps are required:
    (1) Install required python packages
    (2) Create an environment configuration file .env in an user's home directory

Additional Packages
-------------------
Install the following packages
    (1) matplotlib  (graphing & charting)
    (2) unittest    (unit testing)
    (3) psycopg2    (postgres support)

You may get an error while installing any of the above packages because of an old version of pip.
To upgrade pip use the following command:

> python -m pip install --upgrade pip

Configuration
-----------------------
In your home directory create .env file and add the below lines or use a template file conf/example.env:

[database]
login=<username>
password=<password>
host=<database>
database=<password>

[hierarchy]
viewability=ad_format_id,network_id,seller_id,site_id,media_size,ad_position,device,os,browser_name,browser_version
measurability=ad_format_id,device,os,browser_name,browser_version,media_size,network_id,seller_id,site_id,ad_position


Running Simulations
===================
Run python script com.conversant.simulators.ViewabilitySimulator.py


Key Classes
===========
It is expected that you will need to modify some classes to extend simulations to fit specific needs.
The below is a list of key classes with short descriptions. This should be helpful for making modifications:
* com.conversant.simulators.ViewabilitySimulator    - simulates targeting to viewability
* com.conversant.viewability.ViewabilityController  - a simple PID (only P) controller to hit viewability goals
* com.conversant.viewability.MultiKeyPredictor      - multi-key viewability predictors
* com.conversant.viewability.MultiKey               - multi-key
* com.conversant.common.KeyHierarchy                - manages ordered keys and their permutations
* com.conversant.common.Tree                        - a tree structure with support of wildcard matching
* com.conversant.common.DatabaseTree                - a tree structure built from table's data
* com.conversant.common.SQLShell                    - provides access to database



