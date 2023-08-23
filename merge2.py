from asyncio import sleep
import time
import cv2
import audioModule
import faceRecognitionModule
# import serial
import faceDetectionModule
import humanPoseDetectionModule
import listeningModule
import threading
import platform, multiprocessing as mp
from multiprocessing import Manager
import numpy as np
import hand
import csv

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
Encode = []
name = []
prev_time = []
delay=0


def panel_callback(event, x, y, flags, param):
    if (event == cv2.EVENT_LBUTTONDOWN):
        if (x >= 130 and x <= 442 and y >= 356 and y <= 456):
            print("Button1")
        elif (x >= 130 and x <= 442 and y >= 556 and y <= 666):
            print("Button2")
        elif (x <= WIDTH - 130 and x >= WIDTH - 442 and y >= 356 and y <= 456):
            print("Button3")
        elif (x <= WIDTH - 130 and x >= WIDTH - 442 and y >= 556 and y <= 666):
            print("Button4")
        elif (x >= WIDTH / 2 - wd and x <= WIDTH / 2 + wd and y <= wd):
            print("Map")
        elif (x >= WIDTH - 90 and x <= WIDTH - 40 and y >= 40 and y <= 90):
            print("Back")
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
        cv2.putText(img, "Buton 2", (190, 620), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.rectangle(img, (WIDTH - 130, 356), (WIDTH - 442, 456), (0, 255, 0), 3)
        cv2.putText(img, "Button 3", (WIDTH - 380, 420), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2,
                    cv2.LINE_AA)
        cv2.rectangle(img, (WIDTH - 130, 556), (WIDTH - 442, 666), (0, 255, 0), 3)
        cv2.putText(img, "Buton 4", (WIDTH - 380, 620), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2,
                    cv2.LINE_AA)
        cv2.rectangle(img, (WIDTH - 90, 40), (WIDTH - 40, 90), (0, 0, 255), -1)
        cv2.line(img, (WIDTH - 80, 50), (WIDTH - 50, 80), (0, 0, 0), 2)
        cv2.line(img, (WIDTH - 50, 50), (WIDTH - 80, 80), (0, 0, 0), 2)
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
        if (cv2.waitKey(10) == ord('q')):
            break
    cap.release()
    


def gui_run(flag):
    while True:
        if flag.value == 0:
            print(0)
            play('assets/expressions/normal.mp4')
        elif flag.value == 1:
            print(1)
            play('assets/expressions/concentration-2.mp4')
        elif flag.value == 2:
            print(2)
            play('assets/expressions/angry.mp4')

def detectFaces(frame, img):
    global face_detected, Cx, Cy, extracted_faces
    face_detected, Cx, Cy, extracted_faces = faceDetectionModule.detect_faces(frame, img)


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
    text1 = str(error_x) + "#"
    text2 = str(error_y) + "$"
    text3 = str(follow_line) + "@"
    # ser.write(text1.encode())
    # ser.write(text2.encode())
    print(text3)
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


# ser = serial.Serial("com9", 9600, timeout=1)
# t1 = threading.Thread(target=greetbot.listen, )
# t1.start()
def processing_run(flag):
    global face_detected, human_detected, registering_face, Cx, Cy, error_x, error_y , follow_line, extracted_faces
    # ser = serial.Serial("/dev/cu.usbmodem14101", 115200, timeout=1)

    with open('Data_base.csv', 'r') as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            res = [float(j) for j in line]
            res = list(res)
            Encode.append(res)
        f.close()


    # extracting img name from csv file
    # should be call at the begin
    with open('Name.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            name.append(line[0])
            # print(name)
            prev_time.append(line[1])
        f.close()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    while (True):
        ret, img = cap.read()
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
                hand_right(frame)
                follow_line = 0
                if (abs(error_x) < 100 and abs(error_y) < 80):
                    ans = faceRecognitionModule.recogise_person(img,Encode, name, prev_time)
                    if (ans == None):
                        pass
                    else:
                        print(ans)
                    flag.value = 1
                    if (hand_detected and Hx<(425 + 200) and Hx>(425 - 100) and Hy>(240 - 100) and Hy < (240 + 100)):
                        if (delay >= 4): #skipping 2 frames for clearer image as the servo stops.
                            print("listening..")
                            delay=0
                            cv2.waitKey(1)
                            flag.value = 2
                            listeningModule.listen(img)
                            cv2.imshow("img1", extracted_faces[0])
                                

                        else:
                            print("ELSE")
                            delay= delay+1
                            continue
                    
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
        # greetbot.send2Arduino()
        cv2.imshow("face", frame)
        if (cv2.waitKey(10) == ord('q')):
            break
    cap.release()
    cv2.destroyAllWindows()

if _name_ == '_main_':
    if platform.system() == "Darwin":
        mp.set_start_method('spawn')
    manager = Manager()
    flag = manager.Value('i', 0)
    processing = mp.Process(target=processing_run, args=(flag, ))
    gui = mp.Process(target=gui_run, args=(flag, ))
    processing.start()
    gui.start()
    processing.join()
    gui.join()