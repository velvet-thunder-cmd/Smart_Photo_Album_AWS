import json
import boto3
import requests
# from botocore.vendored import requests
import datetime
def lambda_handler(event, context):
    # TODO implement
    #print(json.dumps(event, indent=4, sort_keys=True))
    s3client = boto3.client('s3')
    s3_info = event['Records'][0]['s3']
    bucket_name = s3_info['bucket']['name']
    key_name = s3_info['object']['key']
    metadata = s3client.head_object(Bucket=bucket_name, Key=key_name)
   #print("metdata", metadata)
    #given_labels = metadata['Metadata']["customlabel"].split(",")
    #given_labels = [x.strip() for x in given_labels]
    #print("given_labels", given_labels)
    #print(bucket_name)
    client = boto3.client('rekognition')
    pass_object = {'S3Object':{'Bucket':bucket_name,'Name':key_name}}
    resp = client.detect_labels(Image=pass_object)
    #print('<---------Now response object---------->')
    #print(json.dumps(resp, indent=4, sort_keys=True))
    timestamp =str(datetime.datetime.now())
    labels = []
    #labels += given_labels
    #temp = resp['Labels'][0]['Name']
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
    #resp_elastic = requests.get(url2,headers={"Content-Type": "application/json"}).json()
    #print('<------------------GET-------------------->')
    print(r.text)
    #print(json.dumps(resp_elastic, indent=4, sort_keys=True))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }