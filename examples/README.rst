Test data for QRACLib
=============================================================
This directory contains test data. 

::
├── example.json
├── netdiligence_2019_data.json
├── test_data_18.csv
├── test_data_600.csv
└── test_data_60.csv 
::


QRACLib accepts 2 kinds of files; csv and nested JSON. 

The example data contains one or more version of each risk. The risk types are based on the various distributions and their usage:
============ ========= ======
Distribution Frequency Impact
============ ========= ======
Uniform      X         
Lognormal              X
Beta         X         
PERT         X         X
============ ========= ======

The risk types are: 

-  Uniform-Lognormal
-  Uniform-PERT
-  Beta-Lognormal
-  Beta-PERT
-  PERT-Lognormal
-  PERT-PERT


example.json
~~~~~~~
Test data in JSON format. Use as template for nested JSON. Contains one risk of each kind.

netdiligence_2019_data.json
~~~~~~~

Contains the data from Table 5 - Breach Costs by Business Sector, SMEs – 2014-2018 from the `NetDiligence Cyber Claims Study 2019 Report <https://netdiligence.com/wp-content/uploads/2020/05/2019_NetD_Claims_Study_Report_1.2.pdf>`__

This data set has frequency in beta distribution and impact in PERT distribution. 

test_data_18.csv
~~~~~~~
Contains 18 risks, three versions of each risk. Random test data. Useful for quick tests. 

test_data_60.csv
~~~~~~~
Contains 60 risks, ten versions of each risk. Random test data. Useful for standard usage tests. 

test_data_600.csv
~~~~~~~
Contains 600 risks, 100 versions of each risk. Random test data. Useful for performance tests. 
