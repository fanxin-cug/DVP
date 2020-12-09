import cv2
import numpy as np
import os

#获取图像路径列表
img_path=os.listdir("30frame")
for i in range(len(img_path)):
    img_path[i]="30frame/"+img_path[i]

#前10帧均值滤波
sum_img=np.zeros((360,640,3))
for i in range(10):
    img=cv2.imread(img_path[i])
    sum_img+=img

mean_img = np.uint8(sum_img/10)
#cv2.imwrite("mean.jpg", mean_img)

#前10帧中值滤波
img_lst=[]
for i in range(10):
    img=cv2.imread(img_path[i])
    img_lst.append(img)

img_batch=np.array(img_lst)
median_img=np.median(img_batch,axis=0)
#cv2.imwrite("median.jpg", median_img)

#确定阈值T=180，通过当前帧减去均值或中值滤波模型帧检测运动对象，并保存差值帧
model_mean=cv2.imread("mean.jpg")
model_median=cv2.imread("median.jpg")
for i in range(10,30,2):
    img=cv2.imread(img_path[i])
    #分别计算并保存当前帧与均值滤波模型帧和中值滤波模型帧的差值
    mean_diff=cv2.subtract(img,model_mean)
    median_diff=cv2.subtract(img,model_median)
    cv2.imwrite("FD_mean/"+str(i)+".jpg", mean_diff)
    cv2.imwrite("FD_median/"+str(i)+".jpg", median_diff)

    #均值滤波检测运动对象
    img_mean = cv2.imread("FD_mean/"+str(i)+".jpg")
    mean_gray = cv2.cvtColor(img_mean, cv2.COLOR_BGR2GRAY)
    (T, thresh_mean) = cv2.threshold(mean_gray, 180, 255, cv2.THRESH_BINARY)
    cv2.imwrite("T_mean/"+str(i)+".jpg", thresh_mean)

    #中值滤波检测运动对象
    img_median = cv2.imread("FD_median/"+str(i)+".jpg")
    median_gray = cv2.cvtColor(img_median, cv2.COLOR_BGR2GRAY)
    (T, thresh_median) = cv2.threshold(median_gray, 180, 255, cv2.THRESH_BINARY)
    cv2.imwrite("T_median/"+str(i)+".jpg", thresh_median)