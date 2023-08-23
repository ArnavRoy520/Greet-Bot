import cv2
import numpy as np


def face_callback(event, x, y, flag, param):
    if(event==cv2.EVENT_LBUTTONDOWN):
        main()


def face(filePath, mirror=False):
    cap = cv2.VideoCapture(filePath)
    cv2.namedWindow('GreetBot', cv2.WINDOW_AUTOSIZE)
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
    cv2.destroyAllWindows()


def fn(event, x, y, flags, param):
    if(event == cv2.EVENT_LBUTTONDOWN):
        if (x>=130 and x<=442 and y>=356 and y<=456):
            print("Button1")
        elif (x>=130 and x<=442 and y>=556 and y<=666):
            print("Button2")
        elif (x <= WIDTH-130 and x >= WIDTH-442 and y >= 356 and y <= 456):
            print("Button3")
        elif(x<=WIDTH-130 and x>=WIDTH-442 and y>=556 and y<=666):
            print("Button4")
        elif(x>=WIDTH/2-wd and x<=WIDTH/2+wd and y<=wd):
            print("Map")
        elif (x>=WIDTH-90 and x<=WIDTH-40 and y>=40 and y<=90):
            print("Back")
            cv2.destroyAllWindows()

HEIGHT = 900
WIDTH = 1440
wd = (int)(10 / 100 * WIDTH)


def main():
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    cv2.rectangle(img, (0, 0), (WIDTH, HEIGHT), (41, 38, 39), -1)
    cv2.circle(img, ((int)(WIDTH / 2), 0), wd, (255, 255, 255), -1)
    cv2.putText(img, "Map", (680, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.rectangle(img, (130, 356), (442, 456), (0, 255, 0), 3)
    cv2.putText(img, "Button 1", (190, 420), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.rectangle(img, (130, 556), (442, 666), (0, 255, 0), 3)
    cv2.putText(img, "Buton 2", (190, 620), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.rectangle(img, (WIDTH - 130, 356), (WIDTH - 442, 456), (0, 255, 0), 3)
    cv2.putText(img, "Button 3", (WIDTH - 380, 420), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.rectangle(img, (WIDTH - 130, 556), (WIDTH - 442, 666), (0, 255, 0), 3)
    cv2.putText(img, "Buton 4", (WIDTH - 380, 620), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.rectangle(img, (WIDTH - 90, 40), (WIDTH - 40, 90), (0, 0, 255), -1)
    cv2.line(img, (WIDTH - 80, 50), (WIDTH - 50, 80), (0, 0, 0), 2)
    cv2.line(img, (WIDTH - 50, 50), (WIDTH - 80, 80), (0, 0, 0), 2)
    cv2.imshow("WIN", img)
    cv2.setMouseCallback("WIN", fn)
    cv2.waitKey(0)
    cv2.destroyAllWindows()