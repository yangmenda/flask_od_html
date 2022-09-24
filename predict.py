
#coding=utf-8 

import time

import cv2
import numpy as np
from PIL import Image
import os
from tqdm import tqdm
from yolo import YOLO
import torch.backends.cudnn as cudnn
def P1():
    cudnn.benchmark = True
    yolo=YOLO()
    
    
    
    dir_origin_path = "./images/"
    dir_save_path   = "./static/"
    if os.path.exists("./logs.txt"):
        os.remove("./logs.txt")
    file=open("./logs.txt",'w')
    file.close()
    addr1="test.bmp"
    img = os.path.join(dir_origin_path,addr1)
    image = Image.open(img)
    r_image = yolo.detect_image(image,count=True)
    addr2="predict.bmp"
    r_image.save(os.path.join(dir_save_path, addr2))

        
   
            
            

    

    
	

