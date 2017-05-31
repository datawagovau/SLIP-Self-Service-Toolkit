
rem   Run the FME scripts to extract load log or input log data from PostGIS database for SLIP Future.
rem   
rem   This script calls the FME workbench to read the load log or input log from the PostGIS databases.
rem   The list of agencies and servers are read from a spreadsheet.
rem   The output is written to a spreadsheet which can be emailed.
rem   The workbecn has options to read only the latest load (read from input_log) or the full load log history.
rem   Note that some databases do not have the load_log table, so only the latest load date and time is available.
rem   
rem   User name and password are omitted. They are set in the FME workbench.
rem   In this version the log file name, location and location of the output is set in the FME workbench.
rem   These can be overwritten by including as parameters set in this script.
rem
rem   Written : Robert Chester 02/06/2015
rem   Modified : 
rem




rem    Set location of python executable.
set python_exe="c:\Python27\ArcGIS10.2\python.exe"

rem    Set location of selfsevice python code.
set python_source="C:\selfservice_uploads\end2end_SDE_to_SLIP_Selfservice.py"

rem    Set SDE Connection
set sde=C:\selfservice_uploads\Connection_to_PEAS71-DISS-SDE.sde 

rem    Set SDE FeatureClass to Export
set ifc=GDB.W_IMAGERY_METADATA 

rem    Set path where to store logs and the exported the file geodatabase
set wd=C:\selfservice_uploads

rem    Set the name of the exported FeatureClass Dataset. Note this should be the same name as the dataset already imported into Selfservive.
set ofc=LGATE071

rem    Set the aws profile configured with your upload credentials
set aws=SLIP_SS_uat

rem    Run the python 
%python_exe% %python_source% --sde %sde% --ifc %ifc% --wd %wd% --ofc %ofc% --aws %aws%

pause

EXIT








c:\Python27\ArcGIS10.2\python.exe end2end_SDE_to_SLIP_Selfservice.py --sde 'C:\selfservice_uploads\Connection_to_PEAS71-DISS-SDE.sde' --ifc '