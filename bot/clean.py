"""清除 __pycache__ 缓存"""
import os
import shutil
 
 
def purge_cache(path):
    # 遍历目录下所有文件
    for file_name in os.listdir(path):
        abs_path = os.path.join(path, file_name)
        if file_name == "__pycache__":
            print(abs_path)
            # 删除 `__pycache__` 目录及其中的所有文件
            shutil.rmtree(abs_path)
        elif os.path.isdir(abs_path):
            # 递归调用
            purge_cache(abs_path)
 
 
if __name__ == "__main__":
    # 当前文件的绝对路径列表，按当前系统类型路径分隔符分隔
    path_list = os.path.dirname(
        os.path.abspath(__file__)
    ).split(os.sep)
    # 取当前文件的上上级目录，可根据需要修改
    root_dir = os.sep.join(path_list[0:-2:])
    # 开始清除
    purge_cache(root_dir)
 