from ftplib import FTP, error_perm
import os
import re


class MyFTP(FTP):
    encoding = "utf-8"

    def getdirs(self, dirpath=None):
        """
        获取当前路径或者指定路径下的文件、目录
        :param args:
        :return:
        """
        if dirpath != None:
            self.cwd(dirpath)
        dir_list = []
        self.dir('.', dir_list.append)
        dir_name_list = [dir_detail_str.split(' ')[-1] for dir_detail_str in dir_list]
        return [file for file in dir_name_list if file != "." and file !=".."]

    def checkFileDir(self, dirpath):
        """
        检查指定路径是目录还是文件
        :param dirpath: 文件路径或目录路径
        :return:返回字符串“File”为文件，“Dir”问文件夹，“Unknow”为无法识别
        """
        rec = ""
        try:
            rec = self.cwd(dirpath)  # 需要判断的元素
            self.cwd("..")  # 如果能通过路劲打开必为文件夹，在此返回上一级
        except error_perm as fe:
            rec = fe  # 不能通过路劲打开必为文件，抓取其错误信息
        finally:
            if "Not a directory" in str(rec):
                return "File"
            elif "Current directory is" in str(rec):
                return "Dir"
            else:
                return "Unknow"

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
            # 文件从字符串获取名称
            if detail_info.split(';')[3].strip() == current_name:
                current_info = detail_info
                break
        if not current_info:
            for detail_info in detail_list:
                # 目录从字符串获取名称
                if detail_info.split(';')[2].strip() == current_name:
                    current_info = detail_info
        modify_time = re.search(r'modify=(.*);', current_info).group(1)

        return modify_time