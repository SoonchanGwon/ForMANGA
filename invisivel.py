"""
2021 대건고등학교 2학년 8반 이태영 제작
프로그램 실행후 첫 3초 안에 찍은 사진을 
빨간색을 인식하여 그 부분에 덮어 씌우는 방법
"""
import numpy as np
import cv2
import time

cap=cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))
time.sleep(2)
background=0
for i in range(30):
    ret, background = cap.read();
while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV);
    lower_red=np.array([0,120,70])
    upper_red=np.array([10,255,255])
    mask1=cv2.inRange(hsv, lower_red,upper_red)
    
    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])
    mask2=cv2.inRange(hsv, lower_red,upper_red)
    
    mask1=mask1+mask2
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,
                           np.ones((3,3),np.uint8),iterations=3)
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,
                           np.ones((3,3),np.uint8),iterations=3)
    
    mask2=cv2.bitwise_not(mask1)
    res1=cv2.bitwise_and(background,background,mask=mask1)
    res2=cv2.bitwise_and(img,img,mask=mask2)
    final_output=cv2.addWeighted(res1,1,res2,1,0)
    out.write(final_output) 
    cv2.imshow("Eureka!!!!",final_output)
    k=cv2.waitKey(10)
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()
    
