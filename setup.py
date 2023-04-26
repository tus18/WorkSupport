import cv2
import dlib
from imutils import face_utils
from scipy.spatial import distance

#cap = cv2.VideoCapture(0)#カメラの取得


face_detector = dlib.get_frontal_face_detector()
face_parts_detector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")#ポイント位置を出力するツール


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

max_eye=0
min_eye=10
count =0
cap_file = cv2.VideoCapture('./video1.mp4')
while True:
    ret,img = cap_file.read()
    
    eye = face_landmark_find(img)
    if eye > max_eye:
        max_eye = eye
    if eye < min_eye:
        min_eye = eye
    count += 1
    url = './img/im'+str(count)+'.png'
    cv2.putText(img,str(eye),(10,180),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3,1)
    cv2.imshow("frame",img)
    cv2.imwrite(url,img)
    
    if cv2.waitKey(1) == 27:#Escで終了
        break
print("max:",max_eye,"min:",min_eye)
cap_file.release()
cv2.destroyAllWindows()