import time
import cv2 as cv2
import audioModule
import faceRecognitionModule
import serial
import faceDetectionModule
import humanPoseDetectionModule
import listeningModule
import platform, multiprocessing as mp
from multiprocessing import Manager
import numpy as np
import hand
import csv
import os

dict={}
face_detected = False
human_detected = False
hand_detected=False
registering_face = False
Cx = 0
Cy = 0
Hx = 0
Hy = 0
error_x = 0
error_y = 0
follow_line = 0
extracted_faces = []
HEIGHT = 900
WIDTH = 1440
wd = (int)(10 / 100 * WIDTH)
close=0
# ser = None
len=0
name=""
flow=0

def panel_callback(event, x, y, flags, param):
    global close
    if (event == cv2.EVENT_LBUTTONDOWN):
        if (x >= 130 and x <= 442 and y >= 356 and y <= 456):
            pass
        elif (x >= 130 and x <= 442 and y >= 556 and y <= 666):
            pass
        elif (x <= WIDTH - 130 and x >= WIDTH - 442 and y >= 356 and y <= 456):
            pass
        elif (x <= WIDTH - 130 and x >= WIDTH - 442 and y >= 556 and y <= 666):
            pass
        elif(x>=((int)(WIDTH/2)-150) and x<=(int)(WIDTH/2)+150 and y>=700 and y<=800):
           pass 
        elif (x >= WIDTH / 2 - wd and x <= WIDTH / 2 + wd and y <= wd):
           pass
        elif (x >= WIDTH - 90 and x <= WIDTH - 40 and y >= 40 and y <= 90):
            cv2.destroyWindow("Panel")
            manager1 = Manager()
            flag1 = manager1.Value('i', 0)
            gui_run(flag1)


def face_callback(event, x, y, flags, param):
    if (event == cv2.EVENT_LBUTTONDOWN):
        img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        cv2.rectangle(img, (0, 0), (WIDTH, HEIGHT), (41, 38, 39), -1)
        cv2.circle(img, ((int)(WIDTH / 2), 0), wd, (255, 255, 255), -1)
        cv2.putText(img, "Map", (680, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.rectangle(img, (130, 356), (442, 456), (0, 255, 0), 3)
        cv2.putText(img, "Button 1", (190, 420), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.rectangle(img, (130, 556), (442, 666), (0, 255, 0), 3)
        cv2.putText(img, "Button 2", (190, 620), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.rectangle(img, (WIDTH - 130, 356), (WIDTH - 442, 456), (0, 255, 0), 3)
        cv2.putText(img, "Button 3", (WIDTH - 380, 420), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2,
                    cv2.LINE_AA)
        cv2.rectangle(img, (WIDTH - 130, 556), (WIDTH - 442, 666), (0, 255, 0), 3)
        cv2.putText(img, "Button 4", (WIDTH - 380, 620), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2,
                    cv2.LINE_AA)
        cv2.rectangle(img, (WIDTH - 90, 40), (WIDTH - 40, 90), (0, 0, 255), -1)
        cv2.line(img, (WIDTH - 80, 50), (WIDTH - 50, 80), (0, 0, 0), 2)
        cv2.line(img, (WIDTH - 50, 50), (WIDTH - 80, 80), (0, 0, 0), 2)

        cv2.rectangle(img, ((int)(WIDTH/2)-150, 800), ((int)(WIDTH/2)+150, 700), (0, 255, 0), 3)
        cv2.putText(img, "Shut Down", ((int)(WIDTH/2)-120, 770), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2,
                    cv2.LINE_AA)
        cv2.namedWindow('Panel', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Panel", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback('Panel', face_callback)
        cv2.imshow("Panel", img)
        cv2.setMouseCallback("Panel", panel_callback)
        cv2.waitKey(0)


def play(filePath, mirror=False):
    cap = cv2.VideoCapture(filePath)
    cv2.namedWindow('GreetBot', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("GreetBot", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback('GreetBot', face_callback)
    while True:
        ret_val, frame = cap.read()
        if not ret_val:
            break
        if mirror:
            frame = cv2.flip(frame, 1)
        cv2.imshow('GreetBot', frame)
        if (cv2.waitKey(30) == ord('q')):
            break
    cap.release()


def gui_run(flag):
    while True:
        if flag.value == 0:
            # print(0)
            play('assets/expressions/normal.mp4')
        elif flag.value == 1:
            # print(1)
            play('assets/expressions/concentration2.mp4')
        elif flag.value == 2:
            # print(2)
            play('assets/expressions/angry.mp4')
        elif flag.value == 3:
            # print(3)
            play('assets/expressions/right.mp4')
        elif flag.value == 4:
            # print(4)
            play('assets/expressions/left.mp4')

def detectFaces(frame, img):
    global face_detected, Cx, Cy, extracted_faces,len
    face_detected, Cx, Cy, extracted_faces,len = faceDetectionModule.detect_faces(frame, img)


def detectHumans(frame):
    global human_detected, Cx, Cy
    human_detected, Cx, Cy = humanPoseDetectionModule.detect_human_pose(frame)


def hand_right(frame):
    global hand_detected, Hx, Hy
    hand_detected, Hx, Hy= hand.detect_hand(frame)


def calculateError(frame):
    global error_x, error_y
    h, w, c = frame.shape
    error_x = Cx - w / 2
    error_y = Cy - h / 2
    cv2.putText(frame, "Error x: " + str(error_x), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                cv2.LINE_AA)
    cv2.putText(frame, "Error y: " + str(error_y), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                cv2.LINE_AA)


def send2Arduino():
    # global ser, error_x, error_y, follow_line
    text1 = str(error_x) + "#"
    text2 = str(error_y) + "$"
    text3 = str(follow_line) + "@"
    # ser.write(text1.encode())
    # ser.write(text2.encode())
    # ser.write(text3.encode())

def drawMarkings(frame):
    h, w, c = frame.shape
    cv2.circle(frame, (Cx, Cy), 4, (255, 0, 0), -1, cv2.LINE_AA)
    cv2.line(frame, (Cx, Cy), (int(w / 2), Cy), (0, 255, 0), 2, cv2.LINE_AA)
    cv2.line(frame, (Cx, Cy), (Cx, int(h / 2)), (0, 0, 255), 2, cv2.LINE_AA)


def registerFace():
    pass


def listen():
    listeningModule.listen()


def processing_run(flag):
    global face_detected, human_detected,close, registering_face,name,flow, Cx, Cy, error_x, error_y , follow_line, extracted_faces, ser
    # ser = serial.Serial('com8',9600)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    print(close)
    while (True):
        
        if close==1:
            break
        ret, img = cap.read()
        if ret == False:
            continue
        img = cv2.resize(img, (853, 480))
        img = cv2.flip(img, 1)
        frame = img.copy()

        h, w, c = frame.shape

        if (not registering_face):
            detectFaces(frame, img)
            if (not face_detected):
                detectHumans(frame)
            if (face_detected):
                drawMarkings(frame)
                calculateError(frame)
                if(error_x>150):
                    flag.value =3
                if(error_x<-150):
                    flag.value =4
                hand_right(frame)
                follow_line = 0
                if (abs(error_x) < 100 and abs(error_y) < 80):
                    
                    #print(faceRecognitionModule.recogise_person(extracted_faces[0]))
                    ans,temp = faceRecognitionModule.recogise_person(extracted_faces[0])
                    #ans = faceRecognitionModule.recogise_person(extracted_faces[0])[0]
                    pair=ans+str(temp)

                    print(ans)
                    # if(t==1 and ans!=None):
                    #     t=0
                    #     name[0]=ans
                    if (ans == None):
                        pass
                    else:
                        if ans == "NO FACE" or ans =="None" :
                            pass
                        else:
                            valid=False
                            if(dict.get(pair,"status")=="status"):
                                valid=True
                                dict[pair]=time.time()
                            else:
                                last_time=dict[pair]
                                if(time.time()-last_time>120):
                                    valid=True
                                    dict[pair]=time.time()
                                else:
                                    valid=False
                                    

                            if(valid and ans==name):
                                audioModule.speak("Hello" + ans + ",nice to meet you")
                                flow=0
                            if(ans!=name and valid):  
                                audioModule.speak("Hello" + ans + ",nice to meet you")
                                name=ans
                                #flow=0
                            # if(flow<30 and ans==name):
                            #     flow=flow+1
                            # print(flow)
                    
                    if ans=="None":
                        if dict.get("freq","status")=="status":
                            dict["freq"]=time.time()
                            audioModule.speak("welcome to tata steel tech ex, hope you have a nice day")

                        else:
                            if time.time()-dict["freq"]>60:
                                dict["freq"]=time.time()
                                audioModule.speak(" welcome to tata steel tech ex, hope you have a nice day")
                                
                    
                    print(ans)  
                    flag.value = 1
                    if (hand_detected and Hx<(425 + 250) and Hx>(425) and Hy>(240 - 110) and Hy < (240 + 110) and ans=="None" ):
                        print("listening..")
                        # cv2.rectangle(frame,(635,130),(315,350),(0,0,255),-1)
                        flag.value = 2
                        cv2.waitKey(1)
                        listeningModule.listen(img)
                    #cv2.imshow("img1", extracted_faces[0])
                else:
                    flag.value = 0

            elif (human_detected):

                drawMarkings(frame)

                follow_line = 1

                calculateError(frame)

                if (abs(error_x) < 100):
                    error_x = 0

                if (abs(error_y) < 80):
                    error_y = 0
            else:
                error_x = 1000
                error_y = 1000
                follow_line = 0
        else:
            registerFace(frame)
        # send2Arduino()
        cv2.imshow("face", frame)
        if ((cv2.waitKey(10) == ord('q'))):
            break

    cap.release()
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    
    if platform.system() == "Darwin":
        mp.set_start_method('spawn')
    manager = Manager()
    flag = manager.Value('i', 0)
    processing = mp.Process(target=processing_run, args=(flag, ))
    gui = mp.Process(target=gui_run, args=(flag, ))
    processing.start()
    gui.start()
    audioModule.speak("Welcome to Tata steel Tech-ex. I am Greet Bot from B I T Mesra.")
    processing.join()
    gui.join()