import os
import zipfile


def dfs_get_zip_file(input_path, result):
    """
    得到指定目录下所有的文件路径
    Get all the files path in the specified directory
    :param input_path:
    :param result:
    :return:
    """
    files = os.listdir(input_path)

    for file in files:
        dir_path = os.path.join(input_path, file)
        if os.path.isdir(dir_path):
            dfs_get_zip_file(dir_path, result)
        else:
            result.append(dir_path)


def path_split_list(path, result):
    """
    将路径分割开后的列表，例:/opt/net/udd,得到列表['opt', 'net', 'udd'],同样也适用于windows下的路径
    split path list, example: /opt/net/udd, get list ['opt', 'net', 'udd'], it also applies to
    the path under Windows.
    :param path:
    :param result:
    :return:
    """
    dir_path = os.path.split(path)[0]
    dir_name = os.path.split(path)[1]
    # print(dir_name)
    if dir_name:
        result.append(dir_name)
        path_split_list(dir_path, result)
    else:
        pass


def zip_path(input_path, output_path, output_name):
    """
    压缩整个目录，并指定输出路径及输出的名称
    :param input_path:
    :param output_path:
    :param output_name:
    :return:
    """
    # 开始输入的路径分割的列表，用于比较去掉查询出来后重复的路径
    input_file_list = []
    path_split_list(input_path, input_file_list)

    ret = {}
    filelists = []
    dfs_get_zip_file(input_path, filelists)
    for file in filelists:

        # 执行出的路径
        file_list = []
        path_split_list(file, file_list)
        in_path_list = [x for x in file_list[::-1] if x not in input_file_list]

        # 要进入压缩包的路径
        arcname = ''
        for fil in in_path_list:
            arcname = os.path.join(arcname, fil)

        # 这样放在一个字典后再去压缩是为了不会把本来的压缩包带进去
        ret[file] = arcname

    f = zipfile.ZipFile(os.path.join(output_path, output_name), 'w', zipfile.ZIP_DEFLATED)
    for key, value in ret.items():
        f.write(filename=key, arcname=value)
    f.close()