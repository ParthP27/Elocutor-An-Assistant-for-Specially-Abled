import cv2
# import numpy as np
import dlib
from math import hypot

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("E:\\Project\\Detection Modules\\shape_predictor_68_face_landmarks.dat")

font = cv2.FONT_HERSHEY_TRIPLEX

def midpoint(p1, p2):
    return (p1.x + p2.x)//2, (p1.y + p2.y)//2
    

def get_blinking_ratio(eye_point, facial_landmarks):
    left_point = (facial_landmarks.part(eye_point[0]).x, facial_landmarks.part(eye_point[0]).y)
    right_point = (facial_landmarks.part(eye_point[3]).x, facial_landmarks.part(eye_point[3]).y)
    
    center_top = midpoint(facial_landmarks.part(eye_point[1]), facial_landmarks.part(eye_point[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_point[5]), facial_landmarks.part(eye_point[4]))
    
    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    
    ratio = hor_line_length / ver_line_length
    return ratio


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    faces = detector(gray)
    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(frame, (x,y), (x1,y1), (0,0,255), 3)
        
        landmarks = predictor(gray,face)
        
        left_point = (landmarks.part(36).x, landmarks.part(36).y)
        right_point = (landmarks.part(39).x, landmarks.part(39).y)
        
        center_top = midpoint(landmarks.part(37), landmarks.part(38))
        center_bottom = midpoint(landmarks.part(41), landmarks.part(40))
        
        hor_line = cv2.line(frame, left_point, right_point, (255,0,0), 2)
        ver_line = cv2.line(frame, center_top, center_bottom, (255,0,0), 2)
        # cv2.circle(frame,(x,y),3,(0,0,255),3)
        
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
        
        if blinking_ratio > 5.7:
            cv2.putText(frame,"Blinking", (50,150), font, 7, (255, 0, 0))
        
    cv2.imshow("Face",frame)
    
    key = cv2.waitKey(1)
    if key == 27: #Press esc to exit
        break


cap.release()
cv2.destroyAllWindows()