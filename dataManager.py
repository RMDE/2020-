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
def random_crop(img,lab,p=0.5,min=40,max=68): # (min,max)->range of width and height
    if np.random.random()<p:
        xmin = []
        ymin = []
        xmax = []
        ymax = []
        new_width = np.random.randint(min,max)
        new_height = np.random.randint(min,max)
        point_x = np.random.randint(0,(img.shape[1]/2))
        point_y = np.random.randint(0,(img.shape[0]/2))
        if new_width+point_x > img.shape[1]:
            new_width = img.shape[1]-point_x
        if new_height+point_y > img.shape[0]:
            new_height = img.shape[0]-point_y
        print(new_width,new_height)
        print(point_x,point_y)
        img_region = img[point_y:point_y+new_height,point_x:point_x+new_width,:]
        print(img.shape[1],img.shape[0],img_region.shape[1],img_region.shape[0])
        root = lab.documentElement
        tags = root.getElementsByTagName('width')
        tags[0].firstChild.data = str(new_width)
        tags = root.getElementsByTagName('height')
        tags[0].firstChild.data = str(new_height)
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
            left = int(xmin[i].firstChild.data)
            right = int(xmax[i].firstChild.data)
            top = int(ymin[i].firstChild.data)
            bottom = int(ymax[i].firstChild.data)
            print("lrtb:",left,right,top,bottom)
            a = []
            a.append(left-point_x)
            a.append(right-point_x)
            b = []
            b.append(top-point_y)
            b.append(bottom-point_y)
            print("rse:",a,b)
            for x in range(len(a)):
                if a[x] < 0:
                    a[x] = 0
                elif a[x] > new_width:
                    a[x] = new_width

            for x in range(len(b)):
                if b[x] < 0:
                    b[x] = 0
                elif b[x] > new_height:
                    b[x] = new_height
            xmin[i].firstChild.data = str(a[0])
            xmax[i].firstChild.data = str(a[1])
            ymin[i].firstChild.data = str(b[0])
            ymax[i].firstChild.data = str(b[1])
        nodes = root.getElementsByTagName('object')
        for i in range(len(nodes)):
            if xmin[i].firstChild.data == xmax[i].firstChild.data or ymin[i].firstChild.data == ymax[i].firstChild.data:
                root.removeChild(nodes[i])
        return img_region,lab,True
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
        for num in range(4):
            lab = parse(os.path.join(curDir, labels[i]))
            fimg,flab,flag = random_crop(img,lab,1,min=2000,max=3000)
            if flag == True:
                ResImg.append(fimg)
                ResLab.append(flab)

    for i in range(len(ResImg)):
        cv2.imwrite("./data/fimg/IMG_0"+str(761+i)+".png",ResImg[i])
        f = open("./data/flab/LABEL_0"+str(761+i)+".xml",'w')
        root = ResLab[i].documentElement
        tags = root.getElementsByTagName('folder')
        tags[0].firstChild.data = "flab"
        tags = root.getElementsByTagName('filename')
        tags[0].firstChild.data = "LABEL_0"+str(661+i)+".xml"
        tags = root.getElementsByTagName('path')
        tags[0].firstChild.data = "E:\\yolov3\\data\\flab\\LABEL_0"+str(761+i)+".xml"
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
    
