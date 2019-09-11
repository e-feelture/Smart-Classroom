import requests

key = "aJvSkyqo2OUkx2TE7HB6mbZ2ouM-lzdB"
secret = "XysDTHr16_XM8qSOVtQvTMPjbDDnzezV"


url_delete='https://api-cn.faceplusplus.com/facepp/v3/faceset/delete'

url_create='https://api-cn.faceplusplus.com/facepp/v3/faceset/create'

url_addface='https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'

url_getdetail='https://api-cn.faceplusplus.com/facepp/v3/faceset/getdetail'

payload_delete={'api_key':key,
         'api_secret':secret,
         'check_empty':0
         }

payload_create={'api_key':key,
         'api_secret':secret,
         'outer_id':'yfacesy'
         }

payload_addface={'api_key':key,
         'api_secret':secret,
         'outer_id':'yfacesy',
         'face_tokens':''    #可以上传多个，以逗号分隔
         }

payload_getdetail={'api_key':key,
         'api_secret':secret,
         'outer_id':'yfacesy',
         }

payload_getfacesets={'api_key':key,
         'api_secret':secret,
}


def create_set(outer_id):
    global url_create,payload_create
    payload_create['outer_id'] = outer_id
    r=requests.post(url_create,data=payload_create)
    result=r.json()
    return result

    
def add_face(outer_id,face_tokens):
    global url_addface,payload_addface
    payload_addface['outer_id']=outer_id
    payload_addface['face_tokens']=face_tokens
    r = requests.post(url_addface,data=payload_addface)
    result=r.json()
    return result

        
def get_detail(outer_id):
    global url_getdetail,payload_getdetail
    payload_getdetail['outer_id']=outer_id
    r=requests.post(url_getdetail,data=payload_getdetail)
    result=r.json()
    return result


def delete_set(outer_id):
    global url_delete,payload_delete
    payload_delete['outer_id']=outer_id
    r=requests.post(url_delete,data=payload_delete)
    result=r.json()
    return result
