# coding=utf-8
from face import *
from skeleton_detect import *
from csvfile import *
import cv2
import os
import csv


def is_signing(filepath ,outer_id):
    result = face_detect(filepath)
    if 'faces' not in result:
        return
    faces = result["faces"]

    sign = {}
    for fa in faces:
        face_token = fa["face_token"]
        if (exist(face_token, outer_id)):
            result = face_search(face_token, outer_id)
            face_token = result['results'][0]['face_token']
            csvfilepath = './faces/face_token.csv'
            sign[find_faceID(face_token,csvfilepath)] = 1
    return sign


############################################################


def is_pitch(filepath ,outer_id):
    result = face_detect(filepath)
    if 'faces' not in result:
        return
    faces = result["faces"]

    pos = {}
    for fa in faces:
        face_token = fa["face_token"]

        if exist(face_token, outer_id):
            if 'attributes' in fa:
                attr = fa["attributes"]
                headp = attr["headpose"]
                pitch_angle = headp["pitch_angle"]

                result_search = face_search(face_token, outer_id)
                face_token = result_search['results'][0]['face_token']

                csvfilepath = './faces/face_token.csv'
                faceID = find_faceID(face_token, csvfilepath)
                if pitch_angle < 0:
                    pos[faceID] = 1
                else:
                    pos[faceID] = 0

    return pos


##############################################################


def is_playing_phone(filepath ,outer_id):
    result = skeleton_detect(filepath)
    if 'skeletons' not in result:
        return
    skeletons = result['skeletons']
    ipp = {}

    for sk in skeletons:
        lm = sk['landmark']
        hhlen = abs(lm['left_hand']['x'] - lm['left_hand']['x'])
        eelen = abs(lm['left_elbow']['x'] - lm['left_elbow']['x'])

        if hhlen < eelen / 2:
            top0 = (result['left_shoulder']['y'] + result['right_shoulder']['y']) / 2
            bottom0 = (result['left_buttocks']['y'] + result['right_buttocks']['y']) / 2
            left0 = (result['left_buttocks']['x'] + result['left_shoulder']['x']) / 2
            right0 = (result['right_buttocks']['x'] + result['right_shoulder']['x']) / 2
            top = (3 * top0 + 2 * bottom0) / 4
            bottom = (3 * bottom0 + 2 * top0) / 4
            left = (3 * left0 + 2 * right0) / 4
            right = (3 * right0 + 2 * left0) / 4
            cropped = img[top:bottom, left:right]
            savepath = "./data/sit.jpg"
            cv2.imwrite(savepath, cropped)
            result = phone_detect(savepath)
            os.remove(savepath)
            objects = result['objects']
            for item in objects:
                if item['value'] == 'Cell phone':
                    rect = sk["body_rectangle"]
                    width = rect["width"]
                    top = rect["top"]
                    left = rect["left"]
                    height = rect["height"]

                    img = cv2.imread(filepath)
                    savepath = "./face/data/sit.jpg"
                    cropped = img[top:top + height, left:left + width]
                    cv2.imwrite(savepath, cropped)
                    result = face_detect(savepath)
                    os.remove(savepath)
                    face_num = result['face_num']
                    if face_num == 1:
                        if (exist(face_token, outer_id)):
                            result = face_search(face_token, outer_id)
                            face_token = result['results'][0]['face_token']
                            csvfilepath = './faces/face_token.csv'
                            ipp[find_faceID(face_token,csvfilepath)] = 1
    return ipp


##############################################################


def is_sleeping(filepath ,outer_id):
    result = skeleton_detect(filepath)
    if 'skeletons' not in result:
        return
    skeletons = result['skeletons']
    sleep = {}
    img = cv2.imread(filepath)

    for sk in skeletons:
        rect = sk["body_rectangle"]
        width = rect["width"]
        top = rect["top"]
        left = rect["left"]
        height = rect["height"]

        lm = sk['landmark']
        cropped = img[top:top + height, left:left + width]
        savepath = "./data/sit.jpg"
        cv2.imwrite(savepath, cropped)
        result = face_detect(savepath)
        os.remove(savepath)
        face_num = result['face_num']
        outer_id = 'yfacesy'
        if face_num == 1:
            left_eye_status = result['faces'][0]['attributes']['eyestatus']['left_eye_status']
            right_eye_status = result['faces'][0]['attributes']['eyestatus']['right_eye_status']
            if (left_eye_status['no_glass_eye_close'] >= 70 and right_eye_status['no_glass_eye_close'] >= 70) or (
                    left_eye_status['normal_glass_eye_close'] >= 70 and left_eye_status['normal_glass_eye_close'] >= 70):
                face_token = result['faces'][0]["face_token"]
                if (exist(face_token, outer_id)):
                    result = face_search(face_token, outer_id)
                    face_token = result['results'][0]['face_token']
                    csvfilepath = './faces/face_token.csv'
                    faceID = find_faceID(face_token, csvfilepath)
                    sleep[faceID] = 1

        elif face_num == 0:
            hslen = (lm['left_shoulder']['y'] + lm['right_shoulder']['y'] - lm['head']['y'] * 2) / 2
            nslen = (lm['left_shoulder']['y'] + lm['right_shoulder']['y'] - lm['neck']['y'] * 2) / 2
            if hslen > nslen:
                if lm['left_hand']['y'] > lm['head']['y'] or lm['right_hand']['y'] > lm['head']['y']:
                    csvfile = open("./faces/body_rect.csv", 'a', newline='')
                    fwriter = csv.writer(csvfile)
                    fwriter.writerow([top, top + height, left, left + width])
                    csvfile.close()

    csvfilepath = './faces/body_rect.csv'
    if os.path.exists(csvfilepath) and os.path.getsize(csvfilepath):
        csvfile = open(csvfilepath, 'r')
        freader = csv.reader(csvfile)
        for item in freader:
            top = int(item[0])
            bottom = int(item[1])
            left = int(item[2])
            right = int(item[3])
            cropped = img[top:bottom, left:right]
            savepath = "./data/judge.jpg"
            cv2.imwrite(savepath, cropped)
            result = face_detect(savepath)
            os.remove(savepath)
            face_num = result['face_num']
            outer_id = 'yfacesy'
            if face_num == 1:
                face_token = result['faces'][0]["face_token"]
                if (exist(face_token, outer_id)):
                    result = face_search(face_token, outer_id)
                    face_token = result['results'][0]['face_token']
                    csvfilepath = './faces/face_token.csv'
                    faceID = find_faceID(face_token, csvfilepath)
                    sleep[faceID] = 1
                    csvfilepath = './faces/body_rect.csv'
                    string = ",".join(item)
                    delete_row(string, csvfilepath)

    return sleep



##############################################################


def is_standing(filepath ,outer_id):
    result = skeleton_detect(filepath)
    if 'skeletons' not in result:
        return
    skeletons = result["skeletons"]

    stand = {}
    img = cv2.imread(filepath)

    for sk in skeletons:
        lm = sk["landmark"]

        rect = sk["body_rectangle"]
        width = rect["width"]
        top = rect["top"]
        left = rect["left"]
        height = rect["height"]

        if 'left_knee' in lm or 'right_knee' in lm:
            bodylen = lm['left_knee']['y'] - lm['head']['y']
            headlen = lm['neck']['y'] - lm['head']['y']

            if bodylen > 3 * headlen:
                savepath = "D:\\face\\data\\stand.jpg"
                cropped = img[top:top + height, left:left + width]
                cv2.imwrite(savepath, cropped)
                result = face_detect(savepath)
                os.remove(savepath)
                face_num = result['face_num']
                if face_num == 1:
                    face_token = result['faces'][0]['face_token']
                    if (exist(face_token, outer_id)):
                        result = face_search(face_token, outer_id)
                        face_token = result['results'][0]['face_token']
                        csvfilepath = './faces/face_token.csv'
                        faceID = find_faceID(face_token, csvfilepath)
                        stand[faceID] = 1

    return stand


############################################################
