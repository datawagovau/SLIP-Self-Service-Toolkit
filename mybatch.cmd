rem    Set location to the python executable.
set python_exe="c:\Python27\ArcGIS10.2\python.exe"

rem    Set location to selfsevice python code.
set python_source="C:\selfservice_uploads\end2end_SDE_to_SLIP_Selfservice.py"

rem    Set the SDE Connection
set sde=C:\selfservice_uploads\Connection_to_PEAS71-DISS-SDE.sde 

rem    Set SDE FeatureClass to Export
set ifc=GDB.W_IMAGERY_METADATA 

rem    Set path where to store logs and the exported the file geodatabase. This will be dat
set wd=C:\selfservice_uploads

rem    Set the name of the exported FeatureClass Dataset. Note this needs to be the same name as the dataset have already imported into Selfservive.
set ofc=LGATE071

rem    Set the aws profile configured with your upload credentials. Note you must first install the aws cli tools.https://aws.amazon.com/cli/
rem    after CLI is istalled use the following command to configure your AWS id
set aws=SLIP_SS_uat

rem    Run the python 
%python_exe% %python_source% --sde %sde% --ifc %ifc% --wd %wd% --ofc %ofc% --aws %aws%

pause

EXIT
