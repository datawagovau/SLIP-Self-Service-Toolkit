import boto3

# Function Name: UploadFile()
# Purpose:
#   This fuction can be used to upload files to aws s3
#       The function will return the  S3 file url . 
#          
# usage:
#      UploadFile (<localFile>,<yours3bucket>,<s3key_or_name><AWS_profile>)
#           ie UploadFile(r'D:\selfservice\myData2.zip','lg-slip-selfservice-data-uat','data-load/6/s3_upload.zip',SLIP_SelfService)
#
# Author: Aaron Thorn        
# Version : 0.1 26/5/2017   

def UploadFile(source_file, bucket, key, profile):    
    # It is not recommended to hard code your credentials into code such as 
    # session = boto3.Session(aws_access_key_id=None, aws_secret_access_key=None, region='ap-southeast-2')
    # see http://boto3.readthedocs.io/en/latest/guide/configuration.html how to set your credentials or 
    # Download the aws cli tool and run 'aws configure --profile SLIP_SelfService' to create a user profile 
    session = boto3.Session(profile_name=profile)
    s3_client = session.client('s3')
    s3_client.upload_file(source_file, bucket, key)
    file_url = '{0}/{1}/{2}'.format(s3_client.meta.endpoint_url, bucket, key)
    return file_url

# test 
#UploadFile (<localFile>,<yours3bucket>,<s3key_or_name><AWS_profile>)
#print UploadFile(r'D:\selfservice\myData2.zip','lg-slip-selfservice-data-uat','data-load/6/s3_upload.zip',SLIP_SelfService)