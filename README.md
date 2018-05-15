# camera-detect-face
Python使用OpenCV从摄像头中识别人脸标注后展示到网页

## Usage

### 安装依赖:

```shell
pip install -r requirements.txt
```

### 启动:

```shell
python camera_detect.py
```

浏览器访问: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

人脸会被绿色边框标注，识别到的人脸被保存在程序执行位置的`facesData`目录下

### 打包:

```shell
pyinstaller -F --add-data=haarcascade_frontalface_alt2.xml;. --add-data=templates;templates camera_detect.py
```

生成的程序在dist目录下，人脸模型文件在`C:\Python27\Lib\site-packages\cv2\data`处获取


