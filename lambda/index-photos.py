import json
import boto3
import requests
import datetime
def lambda_handler(event, context):
    s3client = boto3.client('s3')
    s3_info = event['Records'][0]['s3']
    bucket_name = s3_info['bucket']['name']
    key_name = s3_info['object']['key']
    metadata = s3client.head_object(Bucket=bucket_name, Key=key_name)
    client = boto3.client('rekognition')
    pass_object = {'S3Object':{'Bucket':bucket_name,'Name':key_name}}
    resp = client.detect_labels(Image=pass_object)
    timestamp =str(datetime.datetime.now())
    labels = []
  
    for i in range(len(resp['Labels'])):
        labels.append(resp['Labels'][i]['Name'])
    print('<------------Now label list----------------->')
    print(labels)
    format = {'objectKey':key_name,'bucket':bucket_name,'createdTimestamp':timestamp,'labels':labels}
    required_json = json.dumps(format)
    print(required_json)
    url = "https://search-photoboot-53tyon3nsbikh7e7qkyc26ivzm.us-west-2.es.amazonaws.com/photos/_doc"
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(format).encode("utf-8"), headers=headers,auth=('admin', 'Admin@123'))
    print(r.text)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
