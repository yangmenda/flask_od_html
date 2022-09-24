# coding:utf-8
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify,flash,Response
from werkzeug.utils import secure_filename
import os
import cv2
import time
from predict import P1
from pre_v import P2
from datetime import timedelta
from predict_video import detect
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
ALLOWED_EXTENSIONS_v = set(['mp4'])
dir_origin_path = "./images/"
video_origin_path = "./videos/"
def allowed_file_v(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
@app.route('/upload_v', methods=['POST', 'GET'])  # 添加路由
def upload_v():
    if request.method == 'POST':
        f = request.files['file']
        if not (f):
            return render_template('index.html')
 

        
        
 
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        upload_path = os.path.join(basepath, 'videos', secure_filename(f.filename))
        
        f.save(upload_path)

        cap = cv2.VideoCapture(os.path.join(basepath, 'videos', secure_filename(f.filename)))

        # 2. 获取图像的属性（宽和高，）,并将其转换为整数
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        # 3. 创建保存视频的对象，设置编码格式，帧率，图像的宽高等
        out = cv2.VideoWriter(os.path.join(basepath, 'videos', "test.mp4"), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
                             (frame_width, frame_height))  # 保存视频
        while (True):

            # 4.获取视频中的每一帧图像
            ret, frame = cap.read()
            if ret == True:

                # 5.将每一帧图像写入到输出文件中
                out.write(frame)  # 视频写入
            else:
                break

        # 6.释放资源
        cap.release()
        out.release()  # 资源释放
        cv2.destroyAllWindows()

        os.remove(os.path.join(basepath, 'videos', secure_filename(f.filename)))

        
 
        
 
    return render_template('upload_v.html')


@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if not (f):
            return render_template('index.html')

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'images', secure_filename(f.filename))

        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'images', 'test.bmp'), img)
        os.remove(os.path.join(basepath, 'images', secure_filename(f.filename)))

    return render_template('upload.html')

@app.route('/predict', methods=['POST', 'GET'])
def p(): 
        if os.path.exists(os.path.join(dir_origin_path,"test.bmp")):
            P1()
            return render_template('predict.html')
        else:

            return redirect(url_for("upload"))


@app.route('/predict_v', methods=['POST', 'GET'])
def p_v():
    if os.path.exists(os.path.join(video_origin_path, "test.mp4")):
        P2()
        return render_template('predict_v.html')
    else:

        return redirect(url_for("upload_v"))


@app.route('/remove', methods=['POST', 'GET'])

def del_file():
    ls = os.listdir("images/")
    for i in ls:
        c_path = os.path.join("images", i)
       
        os.remove(c_path)
    return render_template('remove.html')
@app.route('/realtime', methods=['POST', 'GET'])  
def realtime():
    detect()
    return render_template('video.html')    

if __name__ == '__main__':
    # app.debug = True
   
    app.run(host='0.0.0.0', port=5000, debug=True)
    

