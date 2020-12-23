import cv2 #0이면 노트북 내장 웹캠 숫자를 올리면 추가된 웹캠을 이용할 수 있다.
import threading
import time
import numpy as np
import pandas as pd
from point_degree import degree_class as dc

class threadprologue :
    def __init__(self, num):
        self.num = num
        #BODY_25 모델의 프로토파일과 가중치 파일, 그리고 이어진 관절
        self.protoFile = "C:/Users/SMJeong/PycharmProjects/JustFit/venv/models/pose_deploy.prototxt"
        self.weightsFile = "C:/Users/SMJeong/PycharmProjects/JustFit/venv/models/pose_iter_584000.caffemodel"
        self.nPoints = 15
        self.POSE_PAIRS = [[0, 1], [1, 2], [2, 3], [3, 4], [1, 5],[1, 8], [5, 6], [6, 7],  [8, 9], [8, 12], [9, 10], [12, 13], [13,14], [10, 11]]
        #모델을 넷에 입력
        self.net = cv2.dnn.readNetFromCaffe(self.protoFile, self.weightsFile)
        self.cap = None
        self.hitpoints = []

        self.video = None
        self.data = None
        self.camera_setting()
        self.video_setting(3)
        self.degree_class = dc()
        self.running_program = True

        self.skeltal_pool()

    def skeltal_pool(self):
        th1 = threading.Thread(target=self.camera_thread, args=())
        th1.start()
        self.skeletal_detect()

    def camera_setting(self):
        self.cap = cv2.VideoCapture(0)  # 3은 가로 4는 세로 길이
        self.cap.set(3, 480)
        self.cap.set(4, 720)

    def video_setting(self, num):
        directory = "C:\\Users\SMJeong\PycharmProjects\JustFit/venv\csv\\"
        if num == 1 :
            filename = "warrior_position"
        elif num == 2 :
            filename = "neck_and_arm_stretch"
        elif num == 3 :
            filename = "neck_and_shoulder"
        elif num == 4 :
            filename = "leg_stretch"
        elif num == 5 :
            filename = "lower_body"

        print(directory + filename+".csv")

        self.data = pd.read_csv(directory + filename+".csv")
        self.video = cv2.VideoCapture(directory + filename + ".mp4")  # 3은 가로 4는 세로 길이
        self.video.set(3, 480)
        self.video.set(4, 720)

    def csv_to_point(self, index):
        noneNum = 0
        points = []
        list = self.data.iloc[index+1].tolist()
        #print(index)
        #print(list)
        for i in range(15):
            if list[i * 2 + 2] < 0:
                points.append(None)
                noneNum = noneNum+1
                continue
            else:
                points.append((list[i * 2 + 2], list[i * 2 + 3]))

        if noneNum>7 :
            points = []
            for i in range(15) :
                points.append(None)

        #print(points)

        return points

    def camera_thread(self):
        for i in range(15):
            self.hitpoints.append(None)

        points = self.csv_to_point(1)
        count = 0
        while True:
            ret, frame = self.cap.read()
            rets, videoframe = self.video.read()

            if count%5 == 0 :
                points = self.csv_to_point(int(count/5))
                print("count : "+str(count))

            # Draw Skeleton
            for pair in self.POSE_PAIRS:
                partA = pair[0]
                partB = pair[1]
                #print(partA, partB)


                if points[partA] and points[partB]:
                    cv2.line(videoframe, points[partA], points[partB], (0, 255, 255), 3, lineType=cv2.LINE_AA)
                    cv2.circle(videoframe, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
                    cv2.circle(videoframe, points[partB], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
                    #cv2.putText(videoframe, "{}".format(partA), points[partA], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2,lineType=cv2.LINE_AA)
                    #cv2.putText(videoframe, "{}".format(partB), points[partB], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2,lineType=cv2.LINE_AA)


            frame = cv2.flip(frame, 1)

            for pair in self.POSE_PAIRS:
                partA = pair[0]
                partB = pair[1]

                degree1 = self.degree_class.get_degree(self.hitpoints[partA], self.hitpoints[partB])
                degree2 = self.degree_class.get_degree(points[partA], points[partB])

                #print("degree1 = " +str(degree1) + ", degree2 = " + str(degree2))
                if pair[0] == 1 and pair[1] == 2  or pair[0] == 1 and pair[1] == 5:
                    color = (0, 255, 255)
                else :
                    color = self.degree_class.degree_compare(degree1, degree2)

                if self.hitpoints[partA] and self.hitpoints[partB]:
                    #cv2.line(frame, self.hitpoints[partA], self.hitpoints[partB], (0, 255, 255), 3, lineType=cv2.LINE_AA)
                    cv2.line(frame, self.hitpoints[partA], self.hitpoints[partB], color, 3, lineType=cv2.LINE_AA)
                    cv2.circle(frame, self.hitpoints[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
                    cv2.circle(frame, self.hitpoints[partB], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)


            concatframe = cv2.hconcat([videoframe,frame])
            concatframe = cv2.resize(concatframe, (2100, 900))
            cv2.imshow('test', concatframe)


            k = cv2.waitKey(1)
            if k == 27:
                self.running_program = False
                break
            elif count>len(self.data)*5-10 :
                self.running_program = False
                break


            count += 1

    def skeletal_detect(self):
        while cv2.waitKey(1) < 0 and self.running_program == True:
            inWidth = 200
            inHeight = 150
            threshold = 0.1

            t = time.time()
            hasFrame, frame = self.cap.read()
            frame = cv2.flip(frame, 1)

            inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)
            self.net.setInput(inpBlob)
            output = self.net.forward()

            H = output.shape[2]
            W = output.shape[3]

            frameWidth = frame.shape[1]
            frameHeight = frame.shape[0]
            # Empty list to store the detected keypoints
            points = []

            #포착된 관절 리스트에 추가
            for i in range(self.nPoints):
                # confidence map of corresponding body's part.
                probMap = output[0, i, :, :]

                # Find global maxima of the probMap.
                minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

                # Scale the point to fit on the original image
                x = (frameWidth * point[0]) / W
                y = (frameHeight * point[1]) / H

                if prob > threshold:
                    # Add the point to the list if the probability is greater than the threshold
                    points.append((int(x), int(y)))
                else:
                    points.append(None)

            self.hitpoints = points

if __name__ == "__main__":
    cameras = threadprologue()
    cameras.skeltal_pool()