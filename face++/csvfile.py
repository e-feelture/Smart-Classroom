import csv
import os
from faceset import *
from face import *


def store_facetoken(filepath):
    faceID = filepath[8:18]
    csvfilepath = "./faces/face_token.csv"
    csvfile = open(csvfilepath, 'a', newline='')
    result = face_detect(filepath)
    if result['face_num'] != 0:
        face_token = result['faces'][0]['face_token']
        fwriter = csv.writer(csvfile)
        fwriter.writerow([faceID, face_token])
        csvfile.close()

def traverse_folder(folderpath):
    name1 = 'jpg'
    name2 = 'jpeg'
    name3 = 'png'
    for file in os.listdir(folderpath):
        if file.endswith(name1) or file.endswith(name2) or file.endswith(name3):
            store_facetoken("./faces/"+file)


def create_faceset(outer_id, csvfilepath):
    create_set(outer_id)
    folderpath = ('./faces')
    traverse_folder(folderpath)
    face_tokens_str = ''
    csvfile = open(csvfilepath,'r')
    freader = csv.reader(csvfile)
    face_tokens = []
    i = 0
    for item in freader:
        i += 1
        face_tokens_str += item[1]+','
        if i%5 == 0:
            face_tokens_str = face_tokens_str[:-1]
            face_tokens.append(face_tokens_str)
            add_face(outer_id,face_tokens)
            face_tokens_str = ''
            face_tokens = []
    face_tokens_str = face_tokens_str[:-1]
    face_tokens.append(face_tokens_str)
    add_face(outer_id, face_tokens)
    csvfile.close()


def find_faceID(face_token,csvfilepath):
    csvfile = open(csvfilepath, 'r')
    reader = csv.reader(csvfile)
    for row in reader:
        if row[1] == face_token:
            return row[0]


def delete_row(item, csvfilepath):
    with open(csvfilepath, 'r') as r:
        lines = r.readlines()
    with open(csvfilepath, 'w') as w:
        for l in lines:
            if item not in l:
                w.write(l)

delete_row('f77d039639e1ed66816d34c411800ba4', './faces/face_token.csv')