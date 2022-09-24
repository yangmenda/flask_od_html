
#coding=utf-8 

import time

import cv2
import numpy as np
from PIL import Image
import os
from tqdm import tqdm
from yolo import YOLO
import torch.backends.cudnn as cudnn
def detect():
    yolo=YOLO()
    cudnn.benchmark = True
    
    capture=cv2.VideoCapture(0)
        
  
          
        

    fps = 0.0
    while(True):
        t1 = time.time()
            # 读取某一帧
        ref,frame=capture.read()
            # 格式转变，BGRtoRGB
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            # 转变成Image
        frame = Image.fromarray(np.uint8(frame))
            # 进行检测
        frame = np.array(yolo.detect_image(frame))
            # RGBtoBGR满足opencv显示格式
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            
        fps  = ( fps + (1./(time.time()-t1)) ) / 2
        print("fps= %.2f"%(fps))
        frame = cv2.putText(frame, "fps= %.2f"%(fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        cv2.imshow("video",frame)
        c= cv2.waitKey(1) & 0xff 
            

        if c==27:           #按esc退出
            capture.release()
                
            cv2.destroyAllWindows()
            break
    capture.release()
        

   