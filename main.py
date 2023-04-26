import cv2
import dlib
from imutils import face_utils
from scipy.spatial import distance
import subprocess
import time

cap = cv2.VideoCapture(0)#カメラの取得
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 30)#フレーム数の指定

face_detector = dlib.get_frontal_face_detector()
face_parts_detector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")#ポイント位置を出力するツール


name='out'#音楽ファイル名
cmd = "python sub.py "+str(name)#サブプロセスの呼び出しコマンド

EYE_AR_THRESH = 0.17
EYE_AR_OPENING = 0.20
flag = False
time_start = time.time()
count = 0
minutes = 0
l = []
l_count = []
up_count = 0
down_count =0
stock = 0


def calc_ear(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    eye_ear = (A + B) / (2.0 * C)
    return eye_ear


def face_landmark_find(img):
    eye = 10
    # 顔検出
    img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector(img_gry, 1)

    for face in faces:
        # 顔のランドマーク検出
        landmark = face_parts_detector(img_gry, face)
        # 処理高速化のためランドマーク群をNumPy配列に変換(必須)
        landmark = face_utils.shape_to_np(landmark)

        left_eye_ear = calc_ear(landmark[42:48])
        right_eye_ear = calc_ear(landmark[36:42])
        eye = (left_eye_ear + right_eye_ear) / 2.0

    return eye

def tired_time_function(l):
    with open('blink.txt','w') as f:
        for lis in l:
            f.writelines("%s\n" % lis)

def end_time_function(l,l_count):
    with open('finel.txt','w') as f:
        for lis in l:
            f.writelines("%s\n" % lis)
    with open('count.txt','w') as f:
        for lis in l_count:
            f.writelines("%s\n" % lis)



while True:
    tired = False
    ret,img = cap.read()
    eye = face_landmark_find(img)

    if eye > EYE_AR_OPENING:
        flag = True
    elif eye < EYE_AR_THRESH and flag == True:
        count = count + 1
        flag = False
        
    time_end = time.time()
    tim = time_end - time_start

    if tim >= 60:
        time_start = time_end
        minutes += 1 
        l_count.append(count)#確認用
        if minutes == 30:
            a = count/30
            a = int(a)
        if minutes >= 30:
            l.append(count-a*minutes)
            print(l)
            if minutes == 30:
                peak = count-a*minutes
            if minutes > 31:#最大値最小値の検出
                
                if l[len(l)-3] < l[len(l)-2] and l[len(l)-1] < l[len(l)-2] and len(l)-1-stock >= 2:
                    if peak < l[len(l)-2]:
                        up_count += 1
                        if down_count < 2:
                            down_count = 0
                    elif peak > l[len(l)-2]:
                        down_count += 1
                        if up_count < 2:
                            up_count = 0
                    peak = l[len(l)-2]
                    stock = len(l)-1

                elif l[len(l)-3] < l[len(l)-2] and l[len(l)-2] < l[len(l)-1] and len(l)-1-stock >= 2:
                    up_count += 1
                    stock = len(l)-1
                    peak = l[len(l)-1]
                    if down_count < 2:
                        down_count = 0
                elif l[len(l)-3] > l[len(l)-2] and l[len(l)-2] > l[len(l)-1] and len(l)-stock >= 2:
                    down_count += 1
                    stock = len(l)-1
                    peak = l[len(l)-1]
                    if up_count < 2:
                        up_count = 0
                
                if down_count > 1 and up_count > 1:
                    down_count = up_count = 0
                    tired = True

            if tired == True:
                if 'pro' in globals():
                    if not pro.poll() is None:
                        pro = subprocess.Popen(cmd)
                else:
                    pro = subprocess.Popen(cmd)
        
    if flag:#確認用
        cv2.putText(img,"true",(100,180),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3,1)
    else:
        cv2.putText(img,"false",(100,180),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3,1)
    cv2.putText(img,str(count),(10,180),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3,1)
    cv2.imshow("frame",img)

    
    if cv2.waitKey(1) == 27:#Escで終了
        break
#終了
if 'pro' in globals():  #proが宣言されている時の処理
    if pro.poll() is None:
        pro.terminate()

cap.release()
cv2.destroyAllWindows()

print(l)
end_time_function(l,l_count)