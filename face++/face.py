# coding=utf-8
import cv2
from faceset import *


def face_detect(filepath):
    key = "aJvSkyqo2OUkx2TE7HB6mbZ2ouM-lzdB"
    secret = "XysDTHr16_XM8qSOVtQvTMPjbDDnzezV"

    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    files = {'image_file': open(filepath, 'rb')}
    payload = {'api_key': key,
               'api_secret': secret,
               'return_attributes': "headpose,eyestatus",
               }
    r = requests.post(url, files=files, data=payload)
    result = r.json()
    return result


def face_getdetail(face_token):
    key = "aJvSkyqo2OUkx2TE7HB6mbZ2ouM-lzdB"
    secret = "XysDTHr16_XM8qSOVtQvTMPjbDDnzezV"

    url = 'https://api-cn.faceplusplus.com/facepp/v3/face/getdetail'
    payload = {'api_key': key,
               'api_secret': secret,
               'face_token': face_token
               }
    r = requests.post(url, data=payload)
    result = r.json()

    return result


def face_search(face_token, outer_id):
    key = "aJvSkyqo2OUkx2TE7HB6mbZ2ouM-lzdB"
    secret = "XysDTHr16_XM8qSOVtQvTMPjbDDnzezV"

    url = 'https://api-cn.faceplusplus.com/facepp/v3/search'
    payload = {'api_key': key,
               'api_secret': secret,
               'face_token': face_token,
               'outer_id': outer_id
               }
    r = requests.post(url, data=payload)
    result = r.json()
    return result


def exist(face_token, outer_id):
    result = get_detail(outer_id)
    face_tokens = result["face_tokens"]

    result = face_search(face_token, outer_id)
    if 'results' not in result:
        return False
    face_token = result["results"][0]["face_token"]
    confidence = result["results"][0]['confidence']
    thresholds = result["thresholds"]["1e-3"]

    if face_token in face_tokens and confidence >= thresholds:
        return True
    else:
        return False


def phone_detect(filepath):
    key = "aJvSkyqo2OUkx2TE7HB6mbZ2ouM-lzdB"
    secret = "XysDTHr16_XM8qSOVtQvTMPjbDDnzezV"

    url = 'https://api-cn.faceplusplus.com/imagepp/beta/detectsceneandobject'
    files = {'image_file': open(filepath, 'rb')}
    payload = {'api_key': key,
               'api_secret': secret,
              }
    r = requests.post(url, files=files, data=payload)
    result = r.json()
    return result


