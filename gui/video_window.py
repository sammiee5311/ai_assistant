import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5 import QtWidgets


class Video_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Video_Window, self).__init__()
        loadUi("video_window.ui", self)
        self.image = None
        self.start_video_button.clicked.connect(self.start_video)
        self.stop_video_button.clicked.connect(lambda : self.update_video(is_capturing=0))
        self.predict_button.clicked.connect(self.start_predict)

    @pyqtSlot()
    def start_video(self):
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video)
        self.timer.start(40)

    @pyqtSlot()
    def update_video(self, is_capturing=1):
        if is_capturing:
            ret, self.image = self.capture.read()
            self.display_video(self.image)
        else:
            self.image = None
            
    @pyqtSlot()
    def start_predict(self):
        self.predict_result_label.setText('Happy')


    def display_video(self, image):
        image = cv2.resize(image, (640, 480))
        image_format = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                image_format = QImage.Format_RGBA8888
            else:
                image_format = QImage.Format_RGB888
        image = QImage(image, image.shape[1], image.shape[0], image.strides[0], image_format)
        image = image.rgbSwapped()

        self.video_label.setPixmap(QPixmap.fromImage(image))
        self.video_label.setScaledContents(True)
