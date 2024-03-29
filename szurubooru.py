"""
Script that automatically uploads images to a Szurubooru server when saving in Grabber.
"""

from urllib.parse import quote
import base64
import configparser
import json
import sys
import requests

# Reading config file for user details
config = configparser.ConfigParser()
config.read('config.ini')

username    = config.get('API', 'username')
login_token = config.get('API', 'token')
api_url     = config.get('API', 'api_url')

# Szurubooru uses different safety categories so we map them to the usual ones
ratingsMap = {
    "safe": "safe",
    "questionable": "sketchy",
    "explicit": "unsafe",
}

# Headers required by the API to process requests
headers = {
    'Authorization': 'Token ' + base64.b64encode(
        f'{username}:{login_token}'.encode('ascii')
    ).decode('ascii'),
    'Accept': 'application/json'
}

# This is the command Grabber will run:
# python szurubooru.py
# "%all:includenamespace,unsafe,underscores%" "%rating%" "%source:unsafe%" "%path:nobackslash%"

# Split the tags to seperate the tag from the category
original_tags = sys.argv[1].split()
tag_category_map = {}
for tag_and_category in original_tags:
    cat, *tag = tag_and_category.split(":")
    if isinstance(tag, list):
        TAG = ':'.join(tag)
    tag_category_map[TAG] = cat

# Checks if the tag category exist/create it
for tag_category in tag_category_map.values():
    req = requests.get(f'{api_url}/tag-category/{quote(tag_category)}', headers=headers, timeout=10)
    try:
        if req.json()['name'] == 'TagCategoryNotFoundError':
            request_input = {
                "name": tag_category,
                "color": "#00ffff",
                "order": 1
            }
            json_input = json.dumps(request_input)
            req = requests.post(f'{api_url}/tag-categories', headers=headers, data=json_input, \
                timeout=10)
    except KeyError:
        ...

# Checks if the tag exists and if not creates it so it has the correct category
for tag_name, cat in tag_category_map.items():
    req = requests.get(f'{api_url}/tag/{quote(tag_name)}', headers=headers, timeout=10)
    try:
        if req.json()['name'] == 'TagNotFoundError':
            request_input = {
                "names": tag_name,
                "category": cat
            }
            json_input = json.dumps(request_input)
            req = requests.post(f'{api_url}/tags', headers=headers, data=json_input, timeout=10)
    except KeyError:
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

if __name__ == '__main__':
    r = requests.post(f'{api_url}/posts/', headers=headers, files=multipart_form_data, timeout=10)
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(r.text)
