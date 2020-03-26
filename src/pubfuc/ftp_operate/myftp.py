from ftplib import FTP
import os
import re


class MyFTP(FTP):
    encoding = "utf-8"

    def getdirs(self, dirpath=None):
        """
        输出当前目录下的dirname
        :param args:
        :return:
        """
        if dirpath != None:
            self.cwd(dirpath)
        dir_list = []
        self.dir('.', dir_list.append)
        dir_name_list = [dir_detail_str.split(' ')[-1] for dir_detail_str in dir_list]
        return [file for file in dir_name_list if file != "." and file !=".."]

    def get_modify_time(self, dirpath=None):
        """
        得到指定目录、文件或者当前目录、文件的修改时间
        :param dirname:
        :return:
        """
        if dirpath != None:
            if dirpath[-1] == '/':
                dir_path = os.path.split(dirpath[0: -1])[0]
                current_name = os.path.split(dirpath[0: -1])[1]
            else:
                dir_path = os.path.split(dirpath)[0]
                # .strip()是为了避免出现”/ 2095-8757“这种情况，下面匹配不到
                current_name = os.path.split(dirpath)[1].strip()
            self.cwd(dir_path)
        else:
            dirpath = self.pwd()
            dir_path = os.path.split(dirpath)[0]
            current_name = os.path.split(dirpath)[1]
            self.cwd(dir_path)

        detail_list = []
        self.retrlines('MLSD', detail_list.append)

        current_info = ''
        for detail_info in detail_list:
            # 文件和目录不一样
            # if detail_info.split(';')[2].strip() == current_name:
            if detail_info.split(';')[3].strip() == current_name:
                current_info = detail_info
                break
        # print(current_info)
        # current_info = [detail_info for detail_info in detail_list if detail_info.split(';')[2].strip() == current_name][0]
        modify_time = re.search(r'modify=(.*);', current_info).group(1)

        return modify_time