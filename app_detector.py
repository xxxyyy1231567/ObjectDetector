# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app_detector.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import cv2
from ultralytics import YOLOv10

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1114, 712)
        self.model_choose = QtWidgets.QComboBox(Form)
        self.model_choose.setGeometry(QtCore.QRect(920, 30, 171, 22))
        self.model_choose.setObjectName("model_choose")
        self.output = QtWidgets.QLabel(Form)
        self.output.setGeometry(QtCore.QRect(20, 70, 1071, 521))
        self.output.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.output.setAlignment(Qt.AlignCenter)
        self.output.setObjectName("output")
        self.mode_choose = QtWidgets.QComboBox(Form)
        self.mode_choose.setGeometry(QtCore.QRect(40, 30, 141, 22))
        self.mode_choose.setObjectName("mode_choose")
        self.model_choose.addItem("yolov10n")
        self.model_choose.addItem("yolov10s")
        self.mode_b = QtWidgets.QPushButton(Form)
        self.mode_b.setGeometry(QtCore.QRect(210, 30, 91, 21))
        self.mode_b.setObjectName("mode_b")
        self.mode_choose.addItem("vedio")
        self.mode_choose.addItem("picture")
        self.mode_choose.addItem("camera")
        self.file_choose = QtWidgets.QPushButton(Form)
        self.file_choose.setGeometry(QtCore.QRect(370, 30, 111, 23))
        self.file_choose.setObjectName("file_choose")
        self.start = QtWidgets.QPushButton(Form)
        self.start.setGeometry(QtCore.QRect(550, 30, 111, 23))
        self.start.setObjectName("start")
        self.stop = QtWidgets.QPushButton(Form)
        self.stop.setGeometry(QtCore.QRect(750, 30, 111, 23))
        self.stop.setObjectName("stop")
        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(20, 660, 1071, 22))
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.resume = QtWidgets.QPushButton(Form)
        self.resume.setGeometry(QtCore.QRect(20, 600, 161, 31))
        self.resume.setObjectName("resume")
        self.pause = QtWidgets.QPushButton(Form)
        self.pause.setGeometry(QtCore.QRect(210, 600, 161, 31))
        self.pause.setObjectName("pause")
        self.speedx_2 = QtWidgets.QPushButton(Form)
        self.speedx_2.setGeometry(QtCore.QRect(420, 600, 161, 31))
        self.speedx_2.setObjectName("speedx_2")
        self.speedx_5 = QtWidgets.QPushButton(Form)
        self.speedx_5.setGeometry(QtCore.QRect(610, 600, 161, 31))
        self.speedx_5.setObjectName("speedx_5")
        self.file_choose.setEnabled(False)
        self.resume.setEnabled(False)
        self.pause.setEnabled(False)
        self.speedx_5.setEnabled(False)
        self.speedx_2.setEnabled(False)
        self.horizontalSlider.setEnabled(False)
        self.speed=100
        self.frame_position=0
        self.timer = QTimer()
        self.status=1

        # Action
        self.mode_b.clicked.connect(self.mode)
        self.file_choose.clicked.connect(self.file_get)
        self.start.clicked.connect(self.start_det)
        self.stop.clicked.connect(self.stop_det)
        self.horizontalSlider.sliderMoved.connect(self.set_position)
        self.pause.clicked.connect(self.pause1)
        self.resume.clicked.connect(self.resume_vedio)

        self.speedx_2.clicked.connect(self.speed2x)
        self.speedx_5.clicked.connect(self.speed5x)

        self.start.setEnabled(False)
        self.stop.setEnabled(False)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ObjectDetector"))
        self.output.setText(_translate("Form", "output will be here "))
        self.mode_b.setText(_translate("Form", "Mode"))
        self.file_choose.setText(_translate("Form", "File"))
        self.start.setText(_translate("Form", "Start detecting"))
        self.stop.setText(_translate("Form", "Stop detecting"))
        self.resume.setText(_translate("Form", "Resume"))
        self.pause.setText(_translate("Form", "Pause"))
        self.speedx_2.setText(_translate("Form", "Speed 2X"))
        self.speedx_5.setText(_translate("Form", "Speed 0.5X"))
    def speed2x(self):
        self.speed=self.speed/2
        if self.timer.isActive():
            self.timer.start(self.speed)
            self.timer.timeout.connect(self.inference)

    def speed5x(self):
        self.speed = self.speed*2
        if self.timer.isActive():
            self.timer.start(self.speed)
            self.timer.timeout.connect(self.inference)

    def pause1(self):
        if self.status==1:
            self.status=0
            self.timer.stop()
            self.pause.setText("continue")
        else:
            self.status = 1
            self.timer.start(self.speed)
            self.timer.timeout.connect(self.inference)
            self.pause.setText("pause")

    def resume_vedio(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.frame_position = 0

    def file_get(self):
        self.file_choose.setEnabled(False)
        filename = QFileDialog.getOpenFileName()
        self.file_choose.setEnabled(True)
        self.filename = filename[0]
        if self.mode_choose.currentIndex()==0:
            self.cap=cv2.VideoCapture(self.filename)
            self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.horizontalSlider.setRange(0, self.frame_count)
        else:
            self.im=cv2.imread(self.filename)

    def start_det(self):
        self.model_choose.setEnabled(False)
        self.file_choose.setEnabled(False)
        self.start.setEnabled(False)
        self.mode_choose.setEnabled(False)
        # 模型加载
        if self.model_choose.currentIndex() == 0:
            pth_path = 'yolov10n.pt'
            self.detectmodel = YOLOv10(pth_path)
        else:
            pth_path = 'yolov10s.pt'
            self.detectmodel = YOLOv10(pth_path)
        self.timer.start(100)
        self.timer.timeout.connect(self.inference)

    def stop_det(self):
        self.timer.stop()
        self.mode_choose.setEnabled(True)
        self.model_choose.setEnabled(True)
        self.pause.setText("pause")
        self.status=1
        self.pause.setEnabled(False)
        self.mode_b.setEnabled(True)
        self.resume.setEnabled(False)
        self.pause.setEnabled(False)
        self.speedx_5.setEnabled(False)
        self.speedx_2.setEnabled(False)
        self.horizontalSlider.setEnabled(False)
        self.horizontalSlider.setValue(0)
        self.frame_position=0

        if self.cap:
            self.cap.release()

    def set_position(self, position):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
        self.frame_position = position
        #self.horizontalSlider.setValue(self.frame_position)

    def inference(self):
        if self.mode_choose==1:
            results = self.detectmodel.predict(self.im, imgsz=640, conf=0.25)
            annotated_image = results[0].plot()
            image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
            vedio_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            self.output.setPixmap(QPixmap(vedio_img))
            self.output.setScaledContents(True)
        elif self.mode_choose==2:
            ret, frame = self.cap.read()
            if ret:
                results = self.detectmodel.predict(frame, imgsz=640, conf=0.25)
                annotated_image = results[0].plot()
                image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                vedio_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                self.output.setPixmap(QPixmap(vedio_img))
                self.output.setScaledContents(True)
        else:
            ret, frame = self.cap.read()
            if ret:
                self.frame_position+=1
                self.horizontalSlider.setValue(self.frame_position)

                results = self.detectmodel.predict(frame, imgsz=640, conf=0.25)
                annotated_image = results[0].plot()
                image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                vedio_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                self.output.setPixmap(QPixmap(vedio_img))
                self.output.setScaledContents(True)
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.frame_position= 0

    def inference1(self):
        self.start.setEnabled(False)
        if self.mode_choose.currentIndex()==1:
            im = cv2.imread(self.filename)
            results = self.detectmodel.predict(im, imgsz=640, conf=0.25)
            annotated_image = results[0].plot()
            image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
            vedio_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            self.output.setPixmap(QPixmap(vedio_img))
            self.output.setScaledContents(True)
            self.ispic = False
        elif self.mode_choose.currentIndex()==2:
            ret, frame = self.vedio.read()
            if ret:
                results = self.detectmodel.predict(frame, imgsz=640, conf=0.25)
                annotated_image = results[0].plot()
                image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                vedio_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                self.output.setPixmap(QPixmap(vedio_img))
                self.output.setScaledContents(True)
            else:
                print("检测结束")
                self.timer.stop()
                self.vedio.release()
                self.mode_choose.setEnabled(True)
                self.model_choose.setEnabled(True)

    def mode(self):
        self.start.setEnabled(True)
        self.stop.setEnabled(True)
        self.mode_choose.setEnabled(False)
        self.mode_b.setEnabled(False)

        if self.mode_choose.currentIndex() == 0:
            self.file_choose.setEnabled(True)
            self.resume.setEnabled(True)
            self.pause.setEnabled(True)
            self.speedx_5.setEnabled(True)
            self.speedx_2.setEnabled(True)
            self.horizontalSlider.setEnabled(True)
        elif self.mode_choose.currentIndex() == 1:
            self.file_choose.setEnabled(True)
        else:
            self.cap = cv2.VideoCapture(0)

if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    ui=Ui_Form()
    mainwindow=QtWidgets.QMainWindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())