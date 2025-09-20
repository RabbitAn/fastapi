import datetime
import platform
import psutil
from .logger import system_logger

class SystemMonitor:
    def __init__(self):
        self.mem = psutil.virtual_memory()
        self.net = psutil.net_io_counters()
        system_logger.info("系统监控服务初始化完成")
        self._log_system_info()

    def _log_system_info(self):
        """记录初始系统信息"""
        system_logger.info(f"操作系统: {platform.system()} {platform.release()}")
        system_logger.info(f"CPU型号: {platform.processor()}")
        system_logger.info(f"CPU核心数: {psutil.cpu_count(logical=False)}")
        system_logger.info(f"总内存: {round(self.mem.total / 1024**3, 2)}GB")

    def _update_metrics(self):
        """更新系统指标"""
        self.mem = psutil.virtual_memory()
        self.net = psutil.net_io_counters()

    def get_system_info(self):
        """获取系统信息"""
        try:
            self._update_metrics()
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > 80:  # CPU 使用率超过 80% 记录警告
                system_logger.warning(f"CPU 使用率过高: {cpu_usage}%")

            mem_usage = round(self.mem.percent, 2)
            if mem_usage > 80:  # 内存使用率超过 80% 记录警告
                system_logger.warning(f"内存使用率过高: {mem_usage}%")

            info = {
                "time": f"服务器时间: {now}",
                "message": "欢迎使用 Python+Jinja2！",
                "core_num": f"{psutil.cpu_count(logical=False)}",
                "totalMemory": f"{round(self.mem.total / 1024**3, 2)}GB",
                "usedMemory": f"{round(self.mem.used / 1024**3, 2)}GB",
                "freeMemory": f"{round(self.mem.free / 1024**3, 2)}GB",
                "cpuUsage": f"{cpu_usage}%",
                "os": f"{platform.system()} {platform.release()}",
                "osVersion": f"{platform.version()}",
                "cpuFrequency": f"{psutil.cpu_freq().current}MHz",
                "cpuModel": f"{platform.processor()}",
                "send": f"{round(self.net.bytes_sent / 1024 ** 2, 2)}",
                "receive": f"{round(self.net.bytes_recv / 1024 ** 2, 2)}"
            }
            return info
        except Exception as e:
            system_logger.error(f"获取系统信息时发生错误: {str(e)}")
            raise

system_monitor = SystemMonitor()
