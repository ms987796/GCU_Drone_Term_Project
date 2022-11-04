# 201735812 김민수, 201835834 남승현
import sys

import numpy as np

from utils import *
import time
import cv2
from threading import Thread

keepRecording = True
recorder = 0

def videoRecorder():
    height, width, _ = frame_read.frame.shape

    # Todo: video 이름 변경
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

if __name__ == "__main__":

    myDrone = initTello()
    myDrone.takeoff()
    time.sleep(1)
    myDrone.streamon()
    cv2.namedWindow("drone")
    frame_read = myDrone.get_frame_read()
    time.sleep(1)

    # Todo: 키보드 입력을 제스처로 변경
    while True:
        img = frame_read.frame
        cv2.imshow("drone", img)

        keyboard = cv2.waitKey(1)

        if keyboard & 0xFF == ord('q'):
            myDrone.land()
            frame_read.stop()
            myDrone.streamoff()
            keepRecording = False
            recorder.join()
            exit(0)
            break

        # Class recording
        if keyboard & 0xFF == ord('v'):
            recorder = Thread(target=videoRecorder)
            recorder.start()

            # Todo: 키보드 조작으로 녹화 종료하게

            myDrone.move_up(100)
            myDrone.rotate_counter_clockwise(360)
            myDrone.move_down(50)
            myDrone.rotate_counter_clockwise(360)
            myDrone.move_up(100)
            myDrone.rotate_counter_clockwise(360)
            myDrone.move_down(50)
            myDrone.rotate_counter_clockwise(360)

            keepRecording = False
            recorder.join()

        # Capture student
        if keyboard & 0xFF == ord('c'):
            text = 'panorama'

            myDrone.rotate_clockwise(30)
            image = myDrone.get_frame_read().frame
            image = np.array(image)
            cv2.imwrite('panorama1.jpg', image)
            time.sleep(0.25)

            myDrone.rotate_clockwise(30)
            image = myDrone.get_frame_read().frame
            image = np.array(image)
            cv2.imwrite('panorama2.jpg', image)
            time.sleep(0.25)

            myDrone.rotate_clockwise(30)
            image = myDrone.get_frame_read().frame
            image = np.array(image)
            cv2.imwrite('panorama3.jpg', image)
            time.sleep(0.25)

            myDrone.rotate_clockwise(30)
            image = myDrone.get_frame_read().frame
            image = np.array(image)
            cv2.imwrite('panorama4.jpg', image)
            time.sleep(0.25)

            myDrone.rotate_clockwise(30)
            image = myDrone.get_frame_read().frame
            image = np.array(image)
            cv2.imwrite('panorama5.jpg', image)
            time.sleep(0.25)

            myDrone.rotate_clockwise(-150)
            img_names = ['panorama1.jpg', 'panorama2.jpg', 'panorama3.jpg', 'panorama4.jpg', 'panorama5.jpg']

            imgs = []
            for name in img_names:
                img = cv2.imread(name)

                if img is None:
                    print('Image load failed!')
                    sys.exit()

                imgs.append(img)

            stitcher = cv2.Stitcher_create()
            status, dst = stitcher.stitch(imgs)

            if status != cv2.Stitcher_OK:
                print('Stitch failed!')
                sys.exit()

            # Todo: 이미지 이쁘게 잘라내기
            cv2.imwrite('output.jpg', dst)
