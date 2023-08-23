import cv2
import mediapipe as mp

def detect_human_pose(frame):

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frameRGB)
    Cx = 0
    Cy = 0

    if (results.pose_landmarks):
        mpDraw.draw_landmarks(frame, results.pose_landmarks, myPose.POSE_CONNECTIONS)
        nose_value = results.pose_landmarks.landmark[myPose.PoseLandmark.NOSE.value]
        ih, iw, ic = frame.shape
        cx, cy = int(nose_value.x * iw), int(nose_value.y * ih)
        Cx = Cx + cx
        Cy = Cy + cy

        return True, Cx, Cy

    else:
        return False, Cx, Cy

mpDraw = mp.solutions.drawing_utils
myPose=mp.solutions.pose
pose=myPose.Pose()