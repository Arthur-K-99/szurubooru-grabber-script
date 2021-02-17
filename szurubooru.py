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
original_tags = sys.argv[1].split()
tag_category_map = {}
for tag_and_category in original_tags:
    cat, *tag = tag_and_category.split(":")
    if isinstance(tag, list):
        tag = ':'.join(tag)
    tag_category_map[tag] = cat

# Checks if the tag category exist/create it
for tag_category in tag_category_map.values():
    req = requests.get(f'{api_url}/tag-category/{quote(tag_category)}', headers=headers)
    try:
        if req.json()['name'] == 'TagCategoryNotFoundError':
            request_input = {
                "name": tag_category,
                "color": "#00ffff",
                "order": 1
            }
            json_input = json.dumps(request_input)
            req = requests.post(f'{api_url}/tag-categories', headers=headers, data=json_input)
    except:
        ...

# Checks if the tag exists and if not creates it so it has the correct category
for tag_name in tag_category_map.keys():
    req = requests.get(f'{api_url}/tag/{quote(tag_name)}', headers=headers)
    try:
        if req.json()['name'] == 'TagNotFoundError':
            request_input = {
                "names": tag_name,
                "category": tag_and_category[tag_name]
            }
            json_input = json.dumps(request_input)
            req = requests.post(f'{api_url}/tags', headers=headers, data=json_input)
    except:
        ...

# The data to be sent alongside the file
metadata = {
    "tags": list(tag_category_map.keys()),
    "safety": ratingsMap[sys.argv[2]],
    "source": sys.argv[3]
}

# The whole data
multipart_form_data = {
    'content': ('test.jpg', open(sys.argv[4], 'rb')),
    'metadata': json.dumps(metadata),
}

r = requests.post(f'{api_url}/posts/', headers=headers, files=multipart_form_data)

# with open('output.txt', 'w') as f:
#     f.write(r.text)
