'''
用途：用于yolov3数据预处理，以增加训练数据量
'''
import os                           # os
from collections import namedtuple  # 集合定义

import matplotlib.pyplot as plt     # 画图
import numpy as np                  # numpy
import glob                         # 读取文件或文件夹的python自带库
from progress.bar import Bar        # 展示进度条的第三方库
import cv2                          # 读取、缩放图片
from xml.dom.minidom import *


curDir = os.path.dirname(__file__)
trainImgName = './data/pictures/IMG_0661.JPG'
trainLabelName = './data/labels/LABEL_0661.xml'

# 随机水平翻转
def horizon_flip(img,lab,p=0.5):
    xmin = []
    ymin = []
    xmax = []
    ymax = []
    if np.random.random() < p:
        img = img[:,::-1,:]
        root = lab.documentElement
        tags = root.getElementsByTagName('width')
        width = int(tags[0].firstChild.data)
        tags = root.getElementsByTagName('height')
        height = int(tags[0].firstChild.data)
        tags = root.getElementsByTagName('xmin')
        for x in tags:
            xmin.append(x)
        tags = root.getElementsByTagName('ymin')
        for x in tags:
            ymin.append(x)
        tags = root.getElementsByTagName('xmax')
        for x in tags:
            xmax.append(x)
        tags = root.getElementsByTagName('ymax')
        for x in tags:
            ymax.append(x)
        for i in range(len(xmin)):
            left = xmin[i].firstChild.data
            right = xmax[i].firstChild.data
            xmin[i].firstChild.data = str(width-int(right))
            xmax[i].firstChild.data = str(width-int(left))

        return img,lab,True
    return [],[],False 


# 随机裁剪
def random_crop(img,label,p=0.5,min=40,max=68): # (min,max)->range of width and height
    if np.random.random()<p:
        width = np.random.randint(min,max)
        height = np.random.randint(min,max)
        point_x = np.random.randint(img.shape[1]/4,(img.shape[1]/4)*3)
        point_y = np.random.randint(img.shape[0]/4,(img.shape[0]/4)*3)
        img_region = img[point_x-width:point_x+width,point_y-height:point_y+height,:]
        label_region = label[point_x-width:point_x+width,point_y-height:point_y+height,:]
        if len(img_region)>0 and len(label_region)>0:
            print(len(img_region),len(label_region))
            img_region = cv2.resize(img_region,(img.shape[1],img.shape[0]))
            label_region = cv2.resize(label_region,(label.shape[1],label.shape[0]))
            return img_region,label_region,True
    return [],[],False




# 处理图片数据，从中获取训练集和验证集
def handle_data():
    # 获取训练集图片
    imgs = glob.glob(os.path.join(curDir, trainImgName))      # 训练集输入图片名列表
    labels = glob.glob(os.path.join(curDir, trainLabelName))  # 训练集标签图片名列表
    ResImg = []
    ResLab = []
    for i in range(len(imgs)):
        # 读取输入图片
        img = cv2.imread(os.path.join(curDir, imgs[i]))
        #img = cv2.resize(img, (img.shape[1]//4, img.shape[0]//4))   # 缩小图片
        # 读取标签文件
        lab = parse(os.path.join(curDir, labels[i]))

        fimg,flab,flag = horizon_flip(img,lab,1)
        if flag == True:
            ResImg.append(fimg)
            ResLab.append(flab)

    for i in range(len(ResImg)):
        cv2.imwrite("./data/fimg/IMG_0"+str(661+i)+".png",ResImg[i])
        f = open("./data/flab/LABEL_0"+str(661+i)+".xml",'w')
        root = ResLab[i].documentElement
        tags = root.getElementsByTagName('folder')
        tags[0].firstChild.data = "flab"
        tags = root.getElementsByTagName('filename')
        tags[0].firstChild.data = "LABEL_0"+str(661+i)+".xml"
        tags = root.getElementsByTagName('path')
        tags[0].firstChild.data = "E:\\yolov3\\data\\flab\\LABEL_0"+str(661+i)+".xml"
        ResLab[i].writexml(f)   

    print("Handle the train data success, length:", len(imgs))


if __name__ == "__main__":
    handle_data()


    # # 显示训练集第一张输入图像
    # print('x:', X_train[0].shape)
    # plt.imshow(X_train[0])
    # plt.show()

    # # 显示训练集第一张标签图像
    # print('y:', Y_train[0])
    # #plt.imshow(temp)
    # #plt.show()
    
