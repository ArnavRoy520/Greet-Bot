import time
import cv2
import audioModule
import faceRecognitionModule
import serial
import faceDetectionModule
import humanPoseDetectionModule
import listeningModule
import platform, multiprocessing as mp
import gui_module


def touch_callback():
    gui_module.main()


def play_videoFile(filePath, mirror=False):
    cap = cv2.VideoCapture(filePath)
    cv2.namedWindow('GreetBot', cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback('GreetBot', touch_callback)
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


def gui_run():
    global flag
    while True:
        if flag == 0:
            play_videoFile('assets/expressions/normal.mp4')
        elif flag == 1:
            play_videoFile('assets/expressions/angry.mp4')


class Greetbot:
    def __init__(self):
        self.face_detected = False
        self.human_detected = False
        self.registering_face = False
        self.Cx = 0
        self.Cy = 0
        self.error_x = 0
        self.error_y = 0
        self.follow_line = 0
        self.extracted_faces = []


    def detectFaces(self, frame, img):
        self.face_detected, self.Cx, self.Cy, self.extracted_faces = faceDetectionModule.detect_faces(frame, img)


    def detectHumans(self, frame):
        self.human_detected, self.Cx, self.Cy = humanPoseDetectionModule.detect_human_pose(frame)


    def calculateError(self, frame):
        h, w, c = frame.shape
        self.error_x = self.Cx - w / 2
        self.error_y = self.Cy - h / 2
        cv2.putText(frame, "Error x: " + str(self.error_x), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                    cv2.LINE_AA)
        cv2.putText(frame, "Error y: " + str(self.error_y), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                    cv2.LINE_AA)


    def send2Arduino(self):
        text1 = str(self.error_x) + "#"
        text2 = str(self.error_y) + "$"
        text3 = str(self.follow_line) + "@"
        # ser.write(text1.encode())
        # ser.write(text2.encode())
        print(text3)
        #ser.write(text3.encode())

    def drawMarkings(self,frame):
        h, w, c = frame.shape

        cv2.circle(frame, (self.Cx, self.Cy), 4, (255, 0, 0), -1, cv2.LINE_AA)
        cv2.line(frame, (self.Cx, self.Cy), (int(w / 2), self.Cy), (0, 255, 0), 2, cv2.LINE_AA)
        cv2.line(frame, (self.Cx, self.Cy), (self.Cx, int(h / 2)), (0, 0, 255), 2, cv2.LINE_AA)

    def registerFace(self,frame):
        pass

    def listen(self):
        listeningModule.listen()


def process_run():
    global flag
    # ser = serial.Serial("/dev/cu.usbmodem14101", 115200, timeout=1)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    greetbot = Greetbot()

    while (True):
        ret, img = cap.read()
        img = cv2.resize(img, (853, 480))
        img = cv2.flip(img, 1)
        frame = img.copy()

        h, w, c = frame.shape

        if (not greetbot.registering_face):

            greetbot.detectFaces(frame, img)

            if (not greetbot.face_detected):
                greetbot.detectHumans(frame)

            if (greetbot.face_detected):

                greetbot.drawMarkings(frame)

                greetbot.calculateError(frame)

                greetbot.follow_line = 0

                if (abs(greetbot.error_x) < 100):
                    greetbot.error_x = 0

                if (abs(greetbot.error_y) < 80):
                    greetbot.error_y = 0

                if (abs(greetbot.error_x) < 100 and abs(greetbot.error_y) < 80):
                    ans = faceRecognitionModule.recogise_person(greetbot.extracted_faces[0])
                    if (ans == None):
                        pass
                    else:
                        # audioModule.speak("Hello" + ans + ",nice to meet you")
                        print(ans)
                    # listeningModule.listen(img)
                    cv2.imshow("img", greetbot.extracted_faces[0])

            elif (greetbot.human_detected):

                greetbot.drawMarkings(frame)

                greetbot.follow_line = 1

                greetbot.calculateError(frame)

                if (abs(greetbot.error_x) < 100):
                    greetbot.error_x = 0

                if (abs(greetbot.error_y) < 80):
                    greetbot.error_y = 0
            else:
                greetbot.error_x = 1000
                greetbot.error_y = 1000
                greetbot.follow_line = 0
        else:
            greetbot.registerFace(frame)
        # greetbot.send2Arduino()
        cv2.imshow("face", frame)

        if (cv2.waitKey(10) == ord('q')):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if platform.system() == "Darwin":
        mp.set_start_method('spawn')
    processing = mp.Process(target=process_run, args=())
    gui = mp.Process(target=gui_run, args=())
    processing.start()
    gui.start()
    processing.join()
    gui.join()


