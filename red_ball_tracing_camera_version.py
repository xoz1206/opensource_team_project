from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

#PI
PI = 3.14159265359

#list
ROI_img_list = []
add_img_list = []
whole_pixel_count_list = []
red_pixel_count_list = []
pixel_ratio = []
filtered_circles = []

#HSV
lower_red = [160, 100, 0]
upper_red = [180, 255, 255]

#threshold
pixel_threshold = 80

#using Distance maintain
standard_size = 70 * 70 * PI

#using location x, y, of previous ball, first is center
prev_center_x = 0
prev_center_y = 0

#Tracing Function
def red_ball_tracing(circles, h, s, v, img_color):
    for i in circles[0, :]:
        count = 0
        count_hsv = 0

        center_ROI = (int(i[0]), int(i[1]))
        radius_ROI = int(i[2])

        if center_ROI[0] - radius_ROI >= 0: 
            left = round(center_ROI[0] - radius_ROI)
        elif center_ROI[0] - radius_ROI < 0:
            left = 0

        if center_ROI[0] + radius_ROI <= width: 
            right = round(center_ROI[0] + radius_ROI)
        elif center_ROI[0] + radius_ROI > width: 
            right = width

        if center_ROI[1] - radius_ROI >= 0: 
            up = round(center_ROI[1] - radius_ROI)
        elif center_ROI[1] - radius_ROI < 0:
            up = 0

        if center_ROI[1] + radius_ROI <= height: 
            down = round(center_ROI[1] + radius_ROI)
        elif center_ROI[1] + radius_ROI > height:
            down = height

        ROI_img = np.zeros((height,width,1), np.uint8) # 빈 이미지
        ROI_img = cv2.circle(ROI_img, center_ROI, radius_ROI, (255), -1) # 채워진 원
        ROI_img_list.append(ROI_img)

        #ROI_img에서 원에 해당하는 pixel 수 count
        #전체 pixel을 대상으로 흰색영역을 탐색하면 시간이 매우 오래걸림
        #마찬가지로 빨간색 검출하기에 좋은 위치. 연산량을 줄이기 위해 4의 배수로 pixel 검출
        for m in range(up, down, 20):
            for n in range(left, right, 20):
                if ROI_img[m][n] == [255]:
                    count = count + 1
                    if h[m][n] > lower_red[0] and h[m][n] < upper_red[0]:
                        if s[m][n] > lower_red[1] and s[m][n] < upper_red[1]:
                            if v[m][n] > lower_red[2] and v[m][n] < upper_red[2]:
                                count_hsv = count_hsv + 1
        whole_pixel_count_list.append(count)
        red_pixel_count_list.append(count_hsv)
        # 전체 pixel 당 빨간색 pixel의 비율 계산
        if count != 0 and count_hsv / count * 100 < pixel_threshold: continue

        # 빨간색 원만 원본이미지에서 ROI 영역 추출
        img_color_sub = img_color
        img_color_sub = cv2.bitwise_and(img_color_sub, img_color_sub, mask = ROI_img)
        add_img_list.append(img_color_sub)
        filtered_circles.append(i)

        #print circle
        img_color = cv2.circle(img_color, center_ROI, radius_ROI, (0, 255, 0), 3)

#-----------------main---------------#
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    img_color = image.copy()
    hsv_img = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_img)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.medianBlur(img_gray, 5)
    height, width = img_gray.shape[:2]
    
    #using location x, y, of previous ball, first is center
    prev_center_x = round(width/2)
    prev_center_y = round(height/2)

    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 70, param1=80, param2=30, minRadius=0, maxRadius=0)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        red_ball_tracing(circles, h, s, v, img_color)
    #-----tracking------
    # TODO
    if len(add_img_list) > 0:
        print("detection")
        print(filtered_circles)
    cv2.imshow("Frame", img_color)
    
    ROI_img_list.clear()
    add_img_list.clear()
    whole_pixel_count_list.clear()
    red_pixel_count_list.clear()
    pixel_ratio.clear()
    filtered_circles.clear()

    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    rawCapture.truncate(0)
    if key == ord("q"):
        break;





