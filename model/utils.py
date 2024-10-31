import shutil
import logging
import os
from logging.handlers import RotatingFileHandler
import datetime


def setup_logger(log_folder, log_file_name='app.log', max_file_size=10 * 1024 * 1024, backup_count=5):
    """
    设置并返回一个logger，用于将日志记录到指定的文件夹和文件中。
    :param log_folder: 日志文件所在的文件夹路径
    :param log_file_name: 日志文件名，默认为'app.log'
    :param max_file_size: 日志文件的最大大小（字节），默认为10MB
    :param backup_count: 保留的备份文件数量，默认为5
    :return: 配置好的logger对象
    """
    # 确保文件夹存在

    config_path = os.path.join(log_folder, log_file_name)
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    # 创建一个logger
    logger = logging.getLogger(log_file_name)
    logger.setLevel(logging.DEBUG)  # 设置日志级别为DEBUG，可以记录所有级别的日志

    # 创建一个handler，用于写入日志文件
    handler = RotatingFileHandler(os.path.join(log_folder, log_file_name), maxBytes=max_file_size,
                                  backupCount=backup_count, encoding='utf-8', delay=True)
    handler.setLevel(logging.DEBUG)  # 设置handler的日志级别
    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(message)s',"%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(handler)
    return logger



my_logger = setup_logger('logs')
ai_logger = setup_logger('logs/ai_logs', 'ai_logs.log')
auto_publish_logger = setup_logger('logs/auto_publish_logger_', f'auto_publish_logger_{str(datetime.datetime.now().date())}.log')
content_publish_logger = setup_logger('logs/content_publish_logger', 'content_publish_logger.log')
seo_logger = setup_logger('logs/seo_logger', 'seo_logger.log')
word_management_logger = setup_logger('logs/word_management_logger', 'word_management_logger.log')
bt_action_logger = setup_logger('logs/bt_action_logger', f'bt_action_logger_{str(datetime.datetime.now().date())}.log')

