rem    Set location to the python executable.
set python_exe="c:\Python27\ArcGIS10.2\python.exe"

rem    Set location to selfsevice python code.
set python_source="C:\selfservice_uploads\end2end_SDE_to_SLIP_Selfservice.py"

rem    Set the SDE Connection
set sde_Connection="C:\selfservice_uploads\Connection_to_PEAS71-DISS-SDE.sde" 

rem    Set SDE FeatureClass to Export
set inputFeatureClass="GDB.W_IMAGERY_METADATA" 

rem    Set path where to store logs and the exported file geodatabase. 
set workingDir="C:\selfservice_uploads"

rem    Set the name of the exported FeatureClass Dataset. Note this needs to be the same name as the dataset you have already loaded into Selfservive.
set outputFeatureClass="LGATE071"

rem    Set the aws profile configured with your upload credentials. Note you must either first install the aws cli tools.https://aws.amazon.com/cli/
rem    and run aws configure --profile <profile_name (ie uat_ss)> to configure the user profile. The other option is to manually create the credential file see. http://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html
set aws_profile="uat_ss"

rem    Set the AWS S3 Bucket Name. You can get this information from the selfservice upload panel
set S3_Bucket="lg-slip-selfservice-data-uat"

rem    Set the AWS S3 folder(Known as the s3 key minus the bucket name)
set S3_FolderKey="data-load/6/"

rem    Run the python script
%python_exe% %python_source% --sde_Connection %sde_Connection% --inputFeatureClass %inputFeatureClass% --workingDir %workingDir% --outputFeatureClass %outputFeatureClass% --aws_profile %aws_profile% --S3_Bucket %S3_Bucket% --S3_FolderKey %S3_FolderKey%

