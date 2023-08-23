import multiprocessing
import speech_recognition as sr
import faceRecognitionModule
import cv2
import audioModule


def takeCommand1():
    r = sr.Recognizer()
    with sr.Microphone(1) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=6)
        print("Audio")
    try:
        query = r.recognize_google(audio, language='en-in')
    except Exception as e:
        print(e)
        return ""
    return query



# def takeCommand():

#     ct=0
#     query=""

#     # while not('thank you' in query or len(query)>12):
#     while(True):
#         if('thank you' in query or len(query)>12):
#             return query

#         else:
#             print("zccvb")
#             r = sr.Recognizer()

#             with sr.Microphone(1) as source:
#                 r.adjust_for_ambient_noise(source)
#                 audio = r.listen(source)
#                 print("Audio")

#             try:
#                 query = r.recognize_google(audio, language='en-in')
#                 # if query!="":
#                 #     print("NOT NULL query")
#                 #     return query
#                 # else:
#                 #     audioModule.speak("Try Again")
#                 #     continue  
                
                    
#             except Exception as e:
#                 print(e)
#                 return "None"
    


def listen(frame):
    isRegistering = False
    # cv2.waitKey(1)
    count = 0
    audioModule.speak("Please tell me your name")

    query=""
    while(count<2):
        
        query = takeCommand1().lower()

        if 'thank you' in query:
            audioModule.speak("ok")
            break

        elif 'my name is ' in query and len(query)>12:
            name = query.replace("my name is ", '')
            faceRecognitionModule.register_person(frame, name)
            print(name + " is registered")
            break
            
        elif(count==1):
            audioModule.speak("Sorry for the inconvenience")
            break

        else:
            audioModule.speak("please try again")
    
        count= count+1        




def play_videoFile(location, mirror=False):
    filePath = 'assets/' + location + '.mp4'
    cap = cv2.VideoCapture(filePath)
    cv2.namedWindow(location,cv2.WINDOW_AUTOSIZE)
    while True:
        ret_val, frame = cap.read()
        if mirror:
            frame = cv2.flip(frame, 1)
        cv2.imshow(location, frame)
        if (cv2.waitKey(5) == ord('q')):
            break
    cv2.release()
    cv2.destroyAllWindows()