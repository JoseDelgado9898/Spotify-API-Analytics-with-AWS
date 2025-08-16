import boto3
from dotenv import load_dotenv
import json
import os
from botocore.exceptions import (
    ClientError, NoCredentialsError
)
class S3_Client:
    def __init__(self):
        load_dotenv()
        self.s3 = boto3.client('s3')
    
    def upload_object(self,obj,bucket_name,key):
        try:
            body=json.dumps(obj).encode('utf-8')
            self.s3.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=body,
                ContentType="application/json"
            )
        except NoCredentialsError:
            print('Credentials error, please validate .env file')
        except ClientError as e:
            print(f'Client error: {e}')
        except Exception as e:
            print(f'An error has ocurred...\n{e}')

