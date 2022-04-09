import cv2
import numpy as np
# import time
cap = cv2.VideoCapture("trafficVideo.mp4")

min_width = 80
min_height = 80

line_position = 550
line_position2 = 700
# Initialize Subtractor Algorithm
algo = cv2.createBackgroundSubtractorMOG2()

def center_handle(x, y, w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx, cy

detect = []
also_detect = []
offset = 6
counter1 = 0
counter2 = 0
while True:
    ret, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)

    if ret == False:
        continue
    # applying on each frame
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
    counterShape, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.imshow('Detecter', dilatada)

    cv2.line(frame, (25, line_position), (600, line_position), (255, 125, 37), 3)
    cv2.line(frame, (5, line_position2), (550, line_position2), (255, 125, 37), 3)
    for (i, c) in enumerate(counterShape):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_counter = (w >= min_width) and (h >= min_height)
        if not validate_counter:
            continue

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # cv2.putText(frame, "Vehicle " + str(counter), (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 254, 0), 2)
        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame, center, 4, (0, 0, 255), -1)

        for (x, y) in detect:
            if y<(line_position+offset) and y>(line_position-offset) and x< 600 and x>25:
                counter1 += 1
            cv2.line(frame, (25, line_position), (600, line_position), (0, 125, 255), 3)
            # cv2.line(frame, (5, line_position2), (550, line_position2), (0, 125, 255), 3)
            detect.remove((x, y))
            print("Vehicle Counter 1: " + str(counter1))


        center1 = center_handle(x, y, w, h)
        also_detect.append(center1)

        for (x, y) in also_detect:
            # if y1< line_position2 and y1 > line_position2 and x1 < 550 and x1 > 5:
            #     counter2 -= 1
            # cv2.line(frame, (5, line_position2), (550, line_position2), (0, 125, 255), 3)
            # also_detect.remove((x1, y1))
            if y<(line_position2+6) and y>(line_position2-6) and x< 600 and x>25:
                counter2 += 1
            cv2.line(frame, (5, line_position2), (550, line_position2), (0, 125, 255), 3)
            # cv2.line(frame, (5, line_position2), (550, line_position2), (0, 125, 255), 3)
            also_detect.remove((x, y))
            print("Vehicle Counter 2: " + str(counter2))



    cv2.putText(frame, "Vehicle Count: " + str(counter1-counter2), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)


    cv2.imshow("Traffic Video",frame)

    key_pressed = cv2.waitKey(5) & 0xFF
    if key_pressed == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()