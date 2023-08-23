import cv2
import numpy as np
import math

blank=np.zeros((500,900,3),np.uint8)
cv2.namedWindow("screen",cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("screen",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
k=0
tim=1
co=255

eye_co_left=[250,150]
eye_co_right=[650,150]

def eye(b):
    blank=np.zeros((500,900,3),np.uint8)
    cv2.ellipse(blank,(eye_co_left[0],eye_co_left[1]),(95,b),0,0,360,(255,255,255),-1)
    cv2.ellipse(blank,(eye_co_right[0],eye_co_right[1]),(95,b),0,0,360,(255,255,255),-1)
    cv2.circle(blank,(eye_co_left[0],eye_co_left[1]),35,(0,0,0),-1)
    cv2.circle(blank,(eye_co_right[0],eye_co_right[1]),35,(0,0,0),-1)
    cv2.circle(blank,(eye_co_left[0]+25,eye_co_left[1]),9,(co,co,co),-1)
    cv2.circle(blank,(eye_co_right[0]-25,eye_co_right[1]),9,(co,co,co),-1)
    cv2.imshow("screen",blank)

def search(left,top):
    blank=np.zeros((500,900,3),np.uint8)
    cv2.ellipse(blank,(eye_co_left[0],eye_co_left[1]),(95,70),0,0,360,(255,255,255),-1)
    cv2.ellipse(blank,(eye_co_right[0],eye_co_right[1]),(95,70),0,0,360,(255,255,255),-1)
    cv2.circle(blank,(eye_co_left[0]-top,eye_co_left[1]-left),35,(0,0,0),-1)
    cv2.circle(blank,(eye_co_right[0]-top,eye_co_right[1]-left),35,(0,0,0),-1)
    cv2.circle(blank,(eye_co_left[0]-top,eye_co_left[1]-left-25),9,(co,co,co),-1)
    cv2.circle(blank,(eye_co_right[0]-top,eye_co_right[1]-left-25),9,(co,co,co),-1)
    cv2.imshow("screen",blank)

def path():
    flag=True
    left=0
    top=0
    while flag:
        a=cv2.waitKey(15)
        if(left<20 and top<20):
            left=left+1
            top=top+1
            search(left,top)
        if(left==20 and top==20):
            flag=False
    flag=True
    left=0
    while flag:
        a=cv2.waitKey(15)
        if(left<40):
            left=left+1
            search(20,-left+20)
        if(left==40):
            flag=False
    flag=True
    left=0
    while flag:
        a=cv2.waitKey(15)
        if(left<20):
            left=left+1
            search(-left+20,left-20)
        if(left==20):
            flag=False
  
def blink():
    flag=True
    b=-70
    while flag:
        a=cv2.waitKey(2)
        if(b>=-70 and b<=0):
            eye(-b)
            b=b+1
            
        if(b>0 and b<70):
            eye(b)
            b=b+1
            
        if(b==70):
            flag=False


def still():
    eye(70)
    path()
    blink()
    cv2.waitKey(2000)
    

while True:
    still()
    if (cv2.waitKey(10) == ord('q')):
        break
cv2.destroyAllWindows()


