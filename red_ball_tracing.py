import numpy as np
import cv2

#원주율
PI = 3.14159265359

# 여러 데이터 셋으로 실험
# 1
img_gray = cv2.imread('many_circles.jpg', cv2.IMREAD_GRAYSCALE) # create BGR to grayscale image 
img_color = cv2.imread('many_circles.jpg')
# 2
#img_gray = cv2.imread('donggu.jpeg', cv2.IMREAD_GRAYSCALE) # create BGR to grayscale image 
#img_color = cv2.imread('donggu.jpeg')
# 3
#img_gray = cv2.imread('baby_ball.jpeg', cv2.IMREAD_GRAYSCALE) # create BGR to grayscale image 
#img_color = cv2.imread('baby_ball.jpeg')


img_gray = cv2.medianBlur(img_gray,5) # medianBlur 처리

height, width = img_gray.shape[:2]

#gray image에서 circle 검출
#최적의 param1,2
circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 70, param1=80, param2=30, minRadius=0, maxRadius=0)
circles = np.uint16(np.around(circles))

#사용되는 list 목록
ROI_img_list = []
add_img_list = []
whole_pixel_count_list = []
red_pixel_count_list = []
pixel_ratio = []
filtered_circles = []

#빨간색 검출을 위한 HSV image
hsv_img = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)
lower_red = [ 160, 100, 0]
upper_red = [ 180, 255, 255]
h, s, v =cv2.split(hsv_img)

#threshold
pixel_threshold = 80

# TRACING FUNCTION
def red_ball_tracing(): 
    for i in circles[0, :]:
        count = 0
        count_hsv = 0
        #원본이미지에서 원하는 영역을 위한 circle 그리기
        center_ROI = (int(i[0]), int(i[1]))
        radius_ROI = int(i[2])
        #pixel의 시작 끝 잡아주기 -> ushort_scalar 값이므로 음수가 나오지않는다. < 0 이게 되면 가장 큰 양수 값이 나온다.
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
        for m in range(up, down, 4):
            for n in range(left, right, 4):
                if ROI_img[m][n] == [255]:
                    count = count + 1
                    if h[m][n] > lower_red[0] and h[m][n] < upper_red[0]:
                        if s[m][n] > lower_red[1] and s[m][n] < upper_red[1]:
                            if v[m][n] > lower_red[2] and v[m][n] < upper_red[2]:
                                count_hsv = count_hsv + 1
        whole_pixel_count_list.append(count)
        red_pixel_count_list.append(count_hsv)

        # 전체 pixel 당 빨간색 pixel의 비율 계산
        if count_hsv / count * 100 < pixel_threshold: continue

        # 빨간색 원만 원본이미지에서 ROI 영역 추출
        img_color_sub = img_color
        img_color_sub = cv2.bitwise_and(img_color_sub, img_color_sub, mask = ROI_img)
        add_img_list.append(img_color_sub)
        filtered_circles.append(i)

#TRACKING FUNCTION
def red_ball_tracking():
    #TODO


#전체 circles [x,y, radius] 출력
#print(circles)

red_ball_tracing()

k = 0
for i in range(0,len(add_img_list)):
	cv2.imshow('add_image', add_img_list[k])
	#filtering이 수행된 circles [x, y, radius] 출력
	print(filtered_circles[k])
	k = k+1
	cv2.waitKey(0)

cv2.waitKey(0)
cv2.destroyAllWindows()
