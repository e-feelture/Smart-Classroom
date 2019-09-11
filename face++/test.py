import cv2
import time
from calculate import *
from face import *
from faceset import *
from skeleton_detect import *
from csvfile import *


outer_id = 'yfacesy'
csvfilepath = "./faces/face_token.csv"
create_faceset(outer_id, csvfilepath)
print("初始化人脸数据集\n")
print(get_detail(outer_id))

cap = cv2.VideoCapture("./")
i = 1
testtime = 0
sign = False
while(True):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    ret, frame = cap.read()
    if ret == False:
        break

    if i >= 40:# 40帧=1s 基础用时10s 每个功能平均5s
        time1 = time.time()
        savepath = "./data/cap.jpg"
        cv2.imwrite(savepath, frame)
        testtime += 1
        print('第%d'%testtime + '次检测')
        if sign == False:
            print("\n签到\n")
            print(is_signing(savepath, outer_id))
            sign = True
        print("\n抬头低头\n")
        print(is_pitch(savepath ,outer_id))
        print("\n玩手机\n")
        print(is_playing_phone(savepath ,outer_id))
        print("\n睡觉\n")
        print(is_sleeping(savepath ,outer_id))
        print("\n发言\n")
        print(is_standing(savepath ,outer_id))
        time2 = time.time()
        usetime = time2 - time1
        print('此次测试总共用时为%d' % usetime)
        print('\n####################################################\n')
        i = 0
        os.remove(savepath)
    else :
        i += 1

cap.release()
cv2.destroyAllWindows()

os.remove("./faces/face_token.csv")
os.remove('./faces/body_rect.csv')
result = delete_set(outer_id)
print("\n\n\nfaceset "+result['outer_id']+" 已删除")

