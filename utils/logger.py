import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class Logger:
    def __init__(self, name="system", log_dir="logs"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 创建日志目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # 日志文件路径
        log_file = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m')}.log")
        
        # 创建 RotatingFileHandler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        self.logger.info(message)
        
    def error(self, message):
        self.logger.error(message)
        
    def warning(self, message):
        self.logger.warning(message)
        
    def debug(self, message):
        self.logger.debug(message)

# 创建全局日志实例
system_logger = Logger()
