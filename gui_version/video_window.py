import cv2
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, Qt
from PyQt5 import QtWidgets


class Video_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Video_Window, self).__init__()
        loadUi("video_window.ui", self)
        self.image = None
        self.start_video_button.clicked.connect(self.start_video)
        self.stop_video_button.clicked.connect(lambda: self.update_video)
        self.predict_button.clicked.connect(self.start_predict)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    @pyqtSlot()
    def start_video(self):
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video)
        self.timer.start(40)

    @pyqtSlot()
    def update_video(self):
        ret, self.image = self.capture.read()
        self.display_video(self.image)

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
