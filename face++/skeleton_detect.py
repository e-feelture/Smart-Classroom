import requests
import json


def skeleton_detect(filepath):
    key = "aJvSkyqo2OUkx2TE7HB6mbZ2ouM-lzdB"
    secret = "XysDTHr16_XM8qSOVtQvTMPjbDDnzezV"

    url = 'https://api-cn.faceplusplus.com/humanbodypp/v1/skeleton'
    files = {'image_file': open(filepath, 'rb')}
    payload = {'api_key': key,
               'api_secret': secret,
               }
    r = requests.post(url, files=files, data=payload)
    result = r.json()
    return result