import os
import sys
sys.path.append(os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[0])

from src.utils.file_reader import YamlReader

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config.yml')
DATA_PATH = os.path.join(BASE_PATH, 'test_data')

LOG_PATH = os.path.join(os.path.dirname(BASE_PATH), 'info_logs')


class Config:
    """
    用于加载配置文件
    """
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlReader(config).data

    def get(self, element, index=0):
        return self.config[index].get(element)