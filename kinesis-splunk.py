from __future__ import print_function

import json
import base64
import requests

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True

def lambda_handler(event, context):
  
  # The splunk endpoint address
  endpoint = "https://splunk.amazonaws.com:8088/services/collector"
  
  # The http event collector token
  token = "Splunk AAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"

  # Create the custom header
  headers = {'Authorization': token, 'content-type': 'application/json'}

  # Create an empty string to append to
  data = ""
  count = 0
  for record in event['Records']:
    # Kinesis record is base 64 encoded.
    payload=base64.b64decode(record["kinesis"]["data"])
    
    # Create a dict with an event object 
    if is_json(payload):
      json_payload = json.loads(payload)
      data = data + json.dumps({'event': json_payload})
    else:
      data = data + json.dumps({'event': payload})
    count = count+1
  r = requests.post(url=endpoint, data=data, headers=headers, verify=False)
  print("decoded_event_count=" + str(count))
  print("event_collector_return_code=" + str(r.status_code))
