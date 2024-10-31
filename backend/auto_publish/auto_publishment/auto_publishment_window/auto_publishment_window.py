
from frontend.auto_publish.auto_publishment.auto_publishment_window.auto_publishment_window import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
import schedule
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from model.utils import auto_publish_logger as my_logger
import logging


class AutoPublishmentWindow(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self, main_ui):
        super(AutoPublishmentWindow, self).__init__()
        super().setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.main_ui = main_ui
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, False)
        self.create_tray_icon()
        icon = self.main_ui.main_page.get_icon()
        self.setWindowIcon(icon)
        # 设置鼠标按下时的位置，保证无边框时窗口可以用鼠标拖动
        self.drag_position = None
        self.actual_close = False
        self.connect_slot()

    def run(self):
        self.t_schedule_execute_tasks = ScheduleExecuteTasks(self.main_ui, self)
        self.t_schedule_execute_tasks.start()
        self.t_schedule_execute_tasks.msg_trigger.connect(self.return_t_schedule_execute_tasks_msg)
        self.t_schedule_execute_tasks.table_update_trigger.connect(self.main_ui.return_task_l_publish)

    def return_t_schedule_execute_tasks_msg(self, msg):
        self.main_ui.main_page.return_msg_update(msg)

    def connect_slot(self):
        self.pushButton.clicked.connect(self.main_ui.start_stop_task)
        self.tray_icon.activated.connect(self.iconActivated)

    def iconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()  # 双击时显示正常窗口
        else:
            self.hide()  # 其他情况隐藏窗口

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            self.hide()  # 窗口关闭时隐藏而不是退出
            event.ignore()
        # else:
        #     self.tray_icon.show()
        #     event.ignore()
        else:
            self.tray_icon.show()
            if not self.actual_close:
                event.ignore()
            else:
                self.actual_close = False
                # self.hide()
                # event.ignore()
                event.accept()  # 允许正常关闭

    def create_tray_icon(self):
        '''
        创建托盘图标
        :return:
        '''

        # 创建一个QSystemTrayIcon对象
        self.tray_icon = QSystemTrayIcon(self)
        # 设置托盘图标
        icon = icon = self.main_ui.main_page.get_icon()
        icon.addPixmap(icon.pixmap(16, 16))  # 设置图标大小为16x16
        self.tray_icon.setIcon(icon)

        # 创建一个上下文菜单（右击托盘图标显示的菜单栏选项）
        menu = QMenu()
        quit_action = QAction("退出程序", menu)
        quit_action.triggered.connect(self.complete_quit)
        menu.addAction(quit_action)

        # 设置鼠标悬停提示文本
        self.tray_icon.setToolTip('男人秃吧秃吧不是罪')

        # 设置托盘图标的上下文菜单
        self.tray_icon.setContextMenu(menu)

        # 连接激活信号到槽函数
        self.tray_icon.activated.connect(self.icon_activated)

        # # 显示托盘图标
        # self.tray_icon.show()

    def complete_quit(self):
        self.close()
        self.tray_icon.hide()
        self.destroy()
        self.main_ui.start_stop_task()
        # QApplication.quit()
        # sys.exit(0)

    def icon_activated(self, reason):
        '''
        双击托盘图标，恢复窗口
        :param reason:
        :return:
        '''
        if reason == QSystemTrayIcon.DoubleClick:
            self.setWindowState(Qt.WindowActive)
            self.show()
            # 在这里可以添加双击托盘图标时的处理逻辑

    # 窗口拖动实现
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.drag_position = None


class ScheduleExecuteTasks(QThread):
    msg_trigger = pyqtSignal(str)
    finish_trigger = pyqtSignal(str)
    table_update_trigger = pyqtSignal(dict)

    def __init__(self, main_ui, ui):
        super(ScheduleExecuteTasks, self).__init__()
        self.main_ui = main_ui
        self.ui = ui

    def run(self):
        # print("即将开始的task_list: ", self.main_ui.tasks_list)
        for i, task_d in enumerate(self.main_ui.tasks_list):
            task_time = datetime.datetime.fromtimestamp(task_d['settle_time']).time()
            self.place_tasks(task_time, task_d)
        self.main_ui.init_schedule()            # 这是开始任务

    def place_tasks(self, task_time, task_d):  # 非task_list里形式的task, 为dict, {'settle_time': [task_1, task_2, task_3, ...]}
        sec = "0" + str(task_time.second) if task_time.second < 10 else str(task_time.second)
        minute = "0" + str(task_time.minute) if task_time.minute < 10 else str(task_time.minute)
        hr = "0" + str(task_time.hour) if task_time.hour < 10 else str(task_time.hour)
        schedule.every().day.at(f"{hr}:{minute}:{sec}").do(self.task_publish, task_d)

    def task_publish(self, task_info):
        try:
            content_response = self.main_ui.get_random_content(task_info)       # task_l内为同一时间需要推送的数据
            if content_response.get('status'):
                # publish
                content_data = content_response['data']
                # 中间需要经过一段 内容处理
                image_refer_d = self.main_ui.update_images(content_data['content'], task_info)
                print("image_refer_d: ", image_refer_d)
                return
                push_content_response = self.main_ui.content_push(task_info, content_data, image_refer_d)
                if push_content_response.get('status'):
                    self.main_ui.update_published_site(task_info, content_data['id'])
                    self.table_update_trigger.emit(task_info)           # 以信号替代掉thread.Thread中直接调用主程序页面的方法
                    self.msg_trigger.emit(f"站点任务 - 站点ID: {task_info['id']}, 域名: {task_info['web']} 已推送 -> 文章链接: {task_info['web'][:-1] + push_content_response['url']}")
                    my_logger.info(f"站点任务 - 站点ID: {task_info['id']}, 域名: {task_info['web']} 已推送 -> 文章链接: {task_info['web'][:-1] + push_content_response['url']}")
                else:
                    self.msg_trigger.emit(f"站点任务 - 站点ID: {task_info['id']}, 域名: {task_info['web']}推送失败, 错误信息: {push_content_response['msg']}")
                    my_logger.info(f"站点任务 - 站点ID: {task_info['id']}, 域名: {task_info['web']}推送失败, 错误信息: {push_content_response['msg']}")

            else:
                self.msg_trigger.emit(f"站点任务 - 站点ID: {task_info['id']}, 域名: {task_info['web']}推送失败, 错误信息: {content_response['msg']}")
                my_logger.info(f"站点任务 - 站点ID: {task_info['id']}, 域名: {task_info['web']}推送失败, 错误信息: {content_response['msg']}")
        except Exception as e:
            my_logger.error(e)
            logging.error(e, exc_info=True)

