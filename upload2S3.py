import boto3
# It is not recommended to hard code you credentials into your code
#session = boto3.Session(aws_access_key_id=None, aws_secret_access_key=None, region='ap-southeast-2')

# Use 'aws configure --profile SLIP_SelfService' to create a profile with your s3 credentials.
session = boto3.Session(profile_name='SLIP_SelfService')

def UploadFile(source_file, bucket, key):
    s3_client = session.client('s3')
    s3_client.upload_file(source_file, bucket, key)
    file_url = '{0}/{1}/{2}'.format(s3_client.meta.endpoint_url, bucket, key)
    return file_url
#UploadFile (<localFile>,<yours3bucket>,<s3key_or_name>)
#print UploadFile(r'D:\selfservice\myData2.zip','lg-slip-selfservice-data-uat','data-load/6/s3_upload.zip')