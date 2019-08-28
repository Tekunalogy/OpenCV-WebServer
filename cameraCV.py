import cv2 as cv
import numpy as np

# optional argument for trackbars
def nothing(x):
    pass


# cap = cv.VideoCapture('visionTestVid.avi')
cap = cv.VideoCapture(0)
# cap.set(cv.CAP_PROP_EXPOSURE,-10)

# cap.set(cv.CAP_PROP_EXPOSURE, 5)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)

# named ites for easy reference
barsWindow = 'Bars'
hl = 'H Low'
hh = 'H High'
sl = 'S Low'
sh = 'S High'
vl = 'V Low'
vh = 'V High'
xp = 'exposure'

# create window for the slidebars
cv.namedWindow(barsWindow, flags = cv.WINDOW_NORMAL)

# create the sliders
cv.createTrackbar(hl, barsWindow, 0, 255, nothing)
cv.createTrackbar(hh, barsWindow, 0, 255, nothing)
cv.createTrackbar(sl, barsWindow, 0, 255, nothing)
cv.createTrackbar(sh, barsWindow, 0, 255, nothing)
cv.createTrackbar(vl, barsWindow, 0, 255, nothing)
cv.createTrackbar(vh, barsWindow, 0, 255, nothing)
cv.createTrackbar(xp, barsWindow, 0, 10, nothing)

# set initial values for sliders
cv.setTrackbarPos(hl, barsWindow, 0)
cv.setTrackbarPos(hh, barsWindow, 255)
cv.setTrackbarPos(sl, barsWindow, 0)
cv.setTrackbarPos(sh, barsWindow, 255)
cv.setTrackbarPos(vl, barsWindow, 0)
cv.setTrackbarPos(vh, barsWindow, 255)
cv.setTrackbarPos(xp, barsWindow, 0)

while True:
    # key = cv.waitKey(2)
    ret, frame = cap.read()

    # convert to HSV from BGR
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # read trackbar positions for all
    hul = cv.getTrackbarPos(hl, barsWindow)
    huh = cv.getTrackbarPos(hh, barsWindow)
    sal = cv.getTrackbarPos(sl, barsWindow)
    sah = cv.getTrackbarPos(sh, barsWindow)
    val = cv.getTrackbarPos(vl, barsWindow)
    vah = cv.getTrackbarPos(vh, barsWindow)
    exp = cv.getTrackbarPos(xp, barsWindow)

    # make array for final values
    HSVLOW = np.array([hul, sal, val])
    HSVHIGH = np.array([huh, sah, vah])

    if ret:
        # cap.set(cv.CAP_PROP_EXPOSURE, exp)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # retval, thershold = cv.threshold(cap, 63, 240, cv.THRESH_BINARY)

        # mask = cv.inRange(hsv, (hul, sal, 219), (huh, 52, vah))
        mask = cv.inRange(hsv, (hul, sal, val), (huh, sah, vah))
        test = cv.bitwise_and(frame, frame, mask = mask)

        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        cv.drawContours(test, contours, -1, (255, 0, 0), 3)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv.erode(mask, kernel, iterations=exp)

        if len(contours) >= 1:
            cntr = []
            for cnt in contours:
                # print(cv.contourArea(cnt))
                cntr.append(cv.contourArea(cnt))

            cntrSorted = cntr
            cntrSorted.sort()

            i = 0
            if len(contours) > 1:
                while i <= 1:
                    x1, y1, w1, h1 = cv.boundingRect(contours[cntr.index(cntrSorted[len(cntr) - (i+1)])])
                    centerx = x1 + int(w1/2)
                    centery = y1 + int(h1/2)
                    cv.line(test, (centerx - 20, centery), (centerx + 20, centery), (0, 100, 0), 5)
                    cv.line(test, (centerx , centery - 20), (centerx, centery + 20), (0, 100, 0), 5)
                    img2 = cv.rectangle(test, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                    i += 1
                    print(centerx, centery)
            else:
                x1, y1, w1, h1 = cv.boundingRect(contours[cntr.index(cntrSorted[0])])
                centerx = x1 + int(w1 / 2)
                centery = y1 + int(h1 / 2)
                cv.line(test, (centerx - 20, centery), (centerx + 20, centery), (0, 100, 0), 5)
                cv.line(test, (centerx, centery - 20), (centerx, centery + 20), (0, 100, 0), 5)
                img2 = cv.rectangle(test, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                i += 1
                print(centerx, centery)

        s1 = cv.resize(test, (800, 450))
        cv.imshow(barsWindow, s1)

# # clean up our resources
# cap.release()
# cv.destroyAllWindows()