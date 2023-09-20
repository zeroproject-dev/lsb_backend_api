import os
import boto3
import uuid


def upload_video(file):
    bucket = os.getenv('S3_BUCKET')
    region = os.getenv('S3_REGION')

    new_filename = uuid.uuid4().hex + '.' + \
        file.filename.rsplit('.', 1)[1].lower()

    s3 = boto3.resource('s3', endpoint_url='http://localhost:9000',
                        aws_access_key_id='BBBG2O2xdE9XaX71OrTe',
                        aws_secret_access_key='tJAlewg4pGxKC9HIIdGsulrIdWu1OrSS0KkEfx6b',
                        aws_session_token=None,
                        config=boto3.session.Config(signature_version='s3v4'),
                        verify=False)
    s3.Bucket(bucket).upload_fileobj(file, new_filename)

    return region
