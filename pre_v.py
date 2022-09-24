import time

import cv2
import numpy as np
from PIL import Image
import os
from tqdm import tqdm
from yolo import YOLO
import torch.backends.cudnn as cudnn
yolo=YOLO()
video_path="./videos/test.mp4"
video_save_path="./static/videos/predict.mp4"
video_fps= 25
def P2():
    capture = cv2.VideoCapture(video_path)
    if video_save_path != "":
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        out = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)

    fps = 0.0
    if os.path.exists("./logs.txt"):
        os.remove("./logs.txt")
    file=open("./logs.txt",'w')
    file.close()
    while (True):
        
        # 读取某一帧
        ref, frame = capture.read()
        if ref==True:
        # 格式转变，BGRtoRGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 转变成Image
            frame = Image.fromarray(np.uint8(frame))
            # 进行检测
            frame = np.array(yolo.detect_image(frame,count=True))
            # RGBtoBGR满足opencv显示格式
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)
            with open("./logs.txt","a",encoding="utf-8") as file1:
                file1.write("\n")
        else:
            break

        
        


    capture.release()
    out.release()
    cv2.destroyAllWindows()

