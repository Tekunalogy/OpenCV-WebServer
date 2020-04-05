import cv2 as cv
import numpy as np

class VideoCamera(object):

    centerX = -1;
    centerY = -1;
    hul = 0
    huh = 255
    sal = 0
    sah = 52
    val = 219
    vah = 255
    HSVLOW = np.array([hul, sal, val])
    HSVHIGH = np.array([huh, sah, vah])

    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        #new = self.process(success, image)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv.imencode('.jpg', image)
        return jpeg.tobytes()

    def process(self, ret, frame):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        if ret:
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            mask = cv.inRange(hsv, (self.hul, self.sal, self.val), (self.huh, self.sah, self.vah))
            test = cv.bitwise_and(frame, frame, mask=mask)

            contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

            cv.drawContours(test, contours, -1, (255, 0, 0), 3)

            kernel = np.ones((5, 5), np.uint8)
            mask = cv.erode(mask, kernel, iterations=1)

            if len(contours) >= 1:
                cntr = []
                for cnt in contours:
                    cntr.append(cv.contourArea(cnt))

                cntrSorted = cntr
                cntrSorted.sort()

                i = 0
                if len(contours) > 1:
                    while i <= 1:
                        x1, y1, w1, h1 = cv.boundingRect(contours[cntr.index(cntrSorted[len(cntr) - (i + 1)])])
                        centerx = x1 + int(w1 / 2)
                        centery = y1 + int(h1 / 2)
                        cv.line(test, (centerx - 20, centery), (centerx + 20, centery), (0, 100, 0), 5)
                        cv.line(test, (centerx, centery - 20), (centerx, centery + 20), (0, 100, 0), 5)
                        img2 = cv.rectangle(test, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                        i += 1
                        self.centerX = centerx
                        self.centerY = centery
                        # print(centerx, centery)
                else:
                    x1, y1, w1, h1 = cv.boundingRect(contours[cntr.index(cntrSorted[0])])
                    centerx = x1 + int(w1 / 2)
                    centery = y1 + int(h1 / 2)
                    cv.line(test, (centerx - 20, centery), (centerx + 20, centery), (0, 100, 0), 5)
                    cv.line(test, (centerx, centery - 20), (centerx, centery + 20), (0, 100, 0), 5)
                    img2 = cv.rectangle(test, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                    i += 1
                    self.centerX = centerx
                    self.centerY = centery
                    # print(centerx, centery)

            s1 = cv.resize(test, (320, 240))

        return test
