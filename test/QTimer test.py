
from PyQt5.QtCore import QTimer, QObject, QThread, pyqtSlot
import sys
from PyQt5.QtWidgets import *



class Slave(QTimer):
    def __init__(self, interval):
        super().__init__()
        self.interval = interval
        self.setInterval(interval)
        self.timeout.connect(self.handle_timeout)
        self.start()

    # @pyqtSlot()
    def handle_timeout(self):
        print("海绵宝宝我们去抓派大星吧！")

# 在你的主程序中
app = QApplication(sys.argv)
worker = Slave(6 * 1000)  # 每隔6s执行一次
sys.exit(app.exec_())




# class Worker(QObject):
#     def __init__(self, interval):
#         super().__init__()
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.handle_timeout)
#         self.timer.setInterval(interval)
#         self.timer.start()
#
#     @pyqtSlot()
#     def handle_timeout(self):
#         print("Task executed")
#         # 这里放置你的任务代码
#
#
# # 在你的主程序中
# app = QApplication(sys.argv)
# worker = Worker(6000)  # 每隔一分钟执行一次
# sys.exit(app.exec_())