# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response
from gevent.wsgi import WSGIServer
import time
import cv2
import sys
import os

currPath = sys.path[0]  

# face_cascade = cv2.CascadeClassifier(currPath+'\\haarcascade_frontalface_default.xml') # 默认模型
# face_cascade = cv2.CascadeClassifier(currPath+'\\haarcascade_profileface.xml')         # 侧脸模型
face_cascade = cv2.CascadeClassifier(currPath+'\\haarcascade_frontalface_alt2.xml')      # 正脸模型

app = Flask(__name__, template_folder=currPath+'\\templates')

if not os.path.exists('facesData'):
    os.makedirs('facesData')

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0) 
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()

        # try:
        faces = face_cascade.detectMultiScale(image, 1.3, 5)
        for (x,y,w,h) in faces:

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # cv2.imwrite("facesData/"+str(time.time())[:10]+ ".jpg", image[y-40:y+h+40, x-20:x+w+20])
            cv2.imwrite("facesData/"+str(time.time())[:10]+ ".jpg", gray[y-40:y+h+40, x-20:x+w+20])

            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

            cv2.waitKey(100)

        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()



@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')   

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=5000)
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    print("* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)")
    http_server.serve_forever()



