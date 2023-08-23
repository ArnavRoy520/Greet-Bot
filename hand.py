import mediapipe as mp
import cv2

def detect_hand(frame):
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frameRGB)
    Cx = 0
    Cy = 0


    if (results.pose_landmarks):
        # mpDraw.draw_landmarks(frame, results.pose_landmarks, myPose.POSE_CONNECTIONS)
        hand_value = results.pose_landmarks.landmark[myPose.PoseLandmark.LEFT_INDEX.value]
        ih, iw, ic = frame.shape
        cx, cy = int(hand_value.x * iw), int(hand_value.y * ih)
        cv2.circle(frame, (cx,cy),8,(255,155,255),-1)
        # print(cx,cy)
        Cx = Cx + cx
        Cy = Cy + cy

        return True, Cx, Cy

    else:
        return False, Cx, Cy 



mpDraw = mp.solutions.drawing_utils
myPose=mp.solutions.pose
pose = myPose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)