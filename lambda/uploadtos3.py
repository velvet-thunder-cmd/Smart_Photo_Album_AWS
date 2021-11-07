import json
import base64
import boto3
def lambda_handler(event, context):
    # TODO implement
    print(event)
    img_data = event['img']
    print(img_data)
    image_name = event['name']
    img = base64.b64decode(img_data, validate=True)
    # our S# Bucket
    s3 = boto3.client('s3')
    bucket = 'b1phtos'
    img_path = '/tmp/'+image_name
    handler = open(img_path, "wb+")
    handler.write(img)
    handler.close()
    # upload the temp image to s3
    s3.upload_file(img_path, bucket, image_name)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }