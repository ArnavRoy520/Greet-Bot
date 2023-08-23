import os
import face_recognition
import cv2
import csv
import numpy as np
import audioModule
from csv import writer
import time

index=-1

def encode_img_list():
    with open('Data_base.csv', 'r') as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            res = [float(j) for j in line]
            res = list(res)
            Encode.append(res)
        f.close()


# extracting img name from csv file
# should be call at the begin
def img_name():
    with open('Name.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            name.append(line[0])
            prev_time.append(line[1])
        f.close()


# Best match index searching
def compare_img(img_encoding):
    face_distances = []
    for y in Encode:
        x = np.array(y)
        face_distances.append(
            face_recognition.face_distance([img_encoding], x))
        face_distances_narray = np.array(face_distances)
        #print(face_distances_narray)
    best_match_index = np.argmin(face_distances_narray)
    if face_distances_narray[best_match_index] < 0.45:
        return best_match_index
    else:
        return -1


# encoding received img
def img_frame(img):
    if img.all()==None:
        return ["",-1]
    global count_no_match,index
    #cv2.imshow("rgb",img)
    
    if(len(img)<=0):
        count_no_match = 0
        # print("kjlaslfhaskhflkashflkashflashflashflashflashfl")
        return ["NO FACE",-1]
        #print("NO FACE")
    if(len(img)>0):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encoding = face_recognition.face_encodings(rgb_img)
        index = -2
        if(len(img_encoding)!=0):
            index = compare_img(img_encoding[0])
        if index == -2:
            count_no_match = 0
            return ["NO FACE",-1]
            #print("NO FACE")
            
        elif index >= 0:
            # curr_time = time.localtime().tm_min * 60 + time.localtime().tm_
            # print(time.localtime().tm_min)
            # if(abs(curr_time-int(prev_time[index]))>5):
            #     # print(curr_time, prev_x.writelines(text)time[index])
            #     text = open("Name.csv", "r")
            #     text = ''.join([i for i in text]).replace(name[index]+','+prev_time[index],name[index]+','+str(curr_time))
            #     x = open("Name.csv", "w")
            #     
            #     x.close()
            #     return (name[index])
            return ([name[index],index])
        else:
            return ["None",-1]
    else:
        return ["None",-1]

def recogise_person(img):
    encode_img_list()
    img_name()
    return img_frame(img)

def register_person(img, name):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encoding = face_recognition.face_encodings(rgb_img)
    if(len(img_encoding)>0):
        cv2.waitKey(1)
        print(name + "is registered")
        curr_time = time.localtime().tm_hour * 60 + time.localtime().tm_min - 6
        with open('Data_base.csv', 'a', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(img_encoding[0])
            f_object.close()
        with open('Name.csv', 'a', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow([name, curr_time])
            f_object.close()
        audioModule.speak("Your name is registered")
    else:
        audioModule.speak("Face not clear, Please retry...")


Encode = []
name = []
prev_time = []
print("Started", os.getpid())
# extracting img encode from csv file
# should be call at the begin