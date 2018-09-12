import os
# 获得一个文件夹下的所有子文件夹的绝对路径
def dir_list(pathname):
    dir_name=[]
    for root,dirname,filename in os.walk(pathname):
        for name in dirname:
            dir_name.append(os.path.join(root,name))
    return dir_name

# 获得一个文件夹下的所有文件的绝对路径
def file_list(dir_name):
    file_name=[]
    for dirname in dir_name:
        for root,dirs,files in os.walk(dirname):
            for subfile in files:
                file_name.append(os.path.join(root,subfile))
    return file_name


