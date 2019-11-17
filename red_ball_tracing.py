import numpy as np
import cv2

#원주율
PI = 3.14159265359


# 여러 데이터 셋으로 실험
img_gray = cv2.imread('many_circles.jpg', cv2.IMREAD_GRAYSCALE) # create BGR to grayscale image 
img_color = cv2.imread('many_circles.jpg')
img_gray = cv2.medianBlur(img_gray,5) # medianBlur 처리
height, width = img_gray.shape[:2]

#gray image에서 circle 검출
#최적의 param1,2
circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 70, param1=80, param2=30, minRadius=0, maxRadius=0)
circles = np.uint16(np.around(circles))

#사용되는 list 목록
ROI_img_list = []

for i in circles[0, :]:
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

#전체 circles [x,y, radius] 출력
print(circles)


#only red_ball_image imshow()
for i in range(0,len(ROI_img_list)):
	cv2.imshow('add_image', ROI_img_list[i])
	cv2.waitKey(0)

cv2.waitKey(0)
cv2.destroyAllWindows()
