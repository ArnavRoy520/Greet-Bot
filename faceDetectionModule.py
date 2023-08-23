import cv2
import mediapipe as mp

def detect_faces(frame, img):

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(frameRGB)
    Cx = 0
    Cy = 0
    extracted_faces = []

    if results.detections:

        for id, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = frame.shape

            xmin = int(bboxC.xmin * iw)
            ymin = int(bboxC.ymin * ih)
            xmax = xmin + int(bboxC.width * iw)
            ymax = ymin + int(bboxC.height * ih)

            cx = int((xmin + xmax) / 2)
            cy = int((ymin + ymax) / 2)

            extracted_faces.append(img[ymin-20:ymax+20, xmin-20:xmax+20])

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 255), 2)
            cv2.putText(frame, str(int(detection.score[0] * 100))+"%",
                        (xmin, ymin - 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

            Cx = Cx + cx
            Cy = Cy + cy

        Cx = int(Cx/len(results.detections))
        Cy = int(Cy / len(results.detections))

        return True, Cx, Cy, extracted_faces,len(extracted_faces)

    else:
        return False, Cx, Cy, extracted_faces, 0



mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection(min_detection_confidence=0.7, model_selection=1)





