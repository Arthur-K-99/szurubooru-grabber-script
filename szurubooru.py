import sys
import requests
import json
from urllib.parse import quote
import base64

# Required User Input
username = ''
token = ''
api_url = 'http://localhost:8080/api'

# Authentication Headers
auth_message = f'{username}:{token}'
auth_message_ascii = auth_message.encode('ascii')
auth_message_base64 = base64.b64encode(auth_message_ascii)
auth_message_decoded = auth_message_base64.decode('ascii')
headers = {
    'Authorization': 'Token ' + auth_message_decoded,
    'Accept': 'application/json'
}

# Szurubooru uses different safety categories so we map them to the usual ones
ratingsMap = {
    "safe": "safe",
    "questionable": "sketchy",
    "explicit": "unsafe",
}

# Split the tags to seperate the name from the category
# The join/split in tag_name handles tag names which have ':' in them, like Re:Zero etc. 
tag_name = [':'.join(i.split(':')[1:]) for i in sys.argv[1].split()]
tag_category = [i.split(':')[0] for i in sys.argv[1].split()]

# Checks if the tag exists and if not creates it so it has the correct category
for tag_name, tag_category in zip(tag_name, tag_category):
    req = requests.get(f'{api_url}/tag/{quote(tag_name)}', headers=headers)
    try:
        if req.json()['name'] == 'TagNotFoundError':
            request_input = {
                "names": tag_name,
                "category": tag_category
            }
            json_input = json.dumps(request_input)
            req = requests.post(f'{api_url}/tags', headers=headers, data=json_input)
    except:
        ...

# The data to be sent alongside the file
metadata = {
    "tags": [':'.join(i.split(':')[1:]) for i in sys.argv[1].split()],
    "safety": ratingsMap[sys.argv[2]],
    "source": sys.argv[3]
}

# The whole data
multipart_form_data = {
    'content': ('test.jpg', open(sys.argv[4], 'rb')),
    'metadata': json.dumps(metadata),
}

r = requests.post('http://localhost:8080/api/posts/', headers=headers, files=multipart_form_data)

with open('output.txt', 'w') as f:
    f.write(r.text)
