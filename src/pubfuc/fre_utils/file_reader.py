import os
import yaml
# import xlwings as xl
import xlrd
# import xlwt


class YamlReader:
    """
    读取yaml数据
    """
    def __init__(self, yaml_file_path):
        if os.path.exists(yaml_file_path):
            self.yaml_file_path = yaml_file_path
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def data(self):

        if not self._data:
            with open(self.yaml_file_path, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))

        return self._data

class ExecelReader:
    """
    读取execel文件
    """
    def __init__(self, excel_file_path):
        if os.path.exists(excel_file_path):
            self.excel_file_path = excel_file_path
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    def data(self, sheet_num):

        if not self._data:
            workbook = xlrd.open_workbook(self.excel_file_path)
            sheet_names = workbook.sheet_names()
            self._data = workbook.sheet_by_name(sheet_names[int('{}'.format(sheet_num))])
        return self._data
