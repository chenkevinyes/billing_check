import os
import numpy as np
import shutil
import time

from PIL import Image

IMAGE_SIZE = (256,256)
 
def resize_image(input_image_path, size):
    with Image.open(input_image_path) as image:
        image = image.convert('RGB')
        resized_image = image.resize(size)
        # resized_image.save(output_image_path)
        return resized_image

def rotated_image(img,angle,orgFileName):
    rotatedImg = img.rotate(angle)
    newFileName = orgFileName.split('.')[-2]+'_'+str(angle)+'.'+orgFileName.split('.')[-1]
    rotatedImg.save(newFileName)
    return newFileName



def split_data(path=None, train_ratio=0.8, new_root=None, pic_split=True, seed=7,newSize=IMAGE_SIZE):
    if path==None or os.path.exists(path)==False:
        raise Exception('数据集路径错误')
    else:
        if os.path.exists(new_root):
          shutil.rmtree(new_root)
        if os.path.exists(new_root):
           raise ValueError('删除目录'+new_root +'失败，请手工删除后重新运行')          
        #创建文件夹
        # 使用os.makedirs()函数递归创建文件夹
        os.makedirs(new_root)#如果没有这个目录，会递归创建
        os.makedirs(new_root+'\\'+'train')#创建train
        os.makedirs(new_root + '\\'+'test')#创建test
        print('文件夹创建成功,分别为',new_root+'\\train'+" "+new_root+'\\test')

    #构建所有文件名的列表，dir为label
    filename = []
    dirs = os.listdir(root)
    print(dirs)
    for index,dir in enumerate(dirs):
        dir_path = root + '\\' + dir
        names = os.listdir(dir_path)
        for name in names:
            filename.append(dir_path + '\\' + name + ' ' + str(index))
    # 设置随机种子
    np.random.seed(seed=seed)#如果随机种子相同，随机的结果也相同
    #打乱文件名列表
    np.random.shuffle(filename)
    #划分训练集、测试集，默认比例4:1
    train = filename[:int(len(filename)*train_ratio)]
    test = filename[int(len(filename)*train_ratio):]

    #分别写入train.txt, test.txt
    with open('train.txt', 'w') as f1, open('test.txt', 'w') as f2,open('train_split.txt','w') as f1_split,open('test_split.txt','w') as f2_split:
        for i in train:
            f1.write(i + '\n')#原始的路径
            i_split=i.split(' ')
            train_img_path=i_split[0]
            train_img_cls=i_split[1]
            train_img_name=train_img_path.split('\\')[-1]
            newSize_image = resize_image(train_img_path, newSize)
            newFileName = new_root+'\\'+'train'+'\\'+train_img_name
            newSize_image.save(newFileName)
            f1_split.write(newFileName+' '+train_img_cls+'\n')
            # 旋转处理
            rotatedFileName = rotated_image(newSize_image,90,newFileName)
            f1_split.write(rotatedFileName+' '+train_img_cls+'\n')
            rotatedFileName = rotated_image(newSize_image,180,newFileName)
            f1_split.write(rotatedFileName+' '+train_img_cls+'\n')
            rotatedFileName = rotated_image(newSize_image,270,newFileName)
            f1_split.write(rotatedFileName+' '+train_img_cls+'\n')            
        for j in test:
            f2.write(j + '\n')#原始的路径
            j_split = j.split(' ')
            test_img_path = j_split[0]
            test_img_cls = j_split[1]
            test_img_name = test_img_path.split('\\')[-1]
            newSize_image = resize_image(test_img_path,  newSize)
            newFileName   =new_root + '\\' + 'test'+'\\'+test_img_name
            newSize_image.save(newFileName)
            # shutil.copy2(test_img_path, new_root + '\\' + 'test'+'\\'+test_img_name)
            f2_split.write(newFileName+' '+test_img_cls+'\n')
            # 旋转处理
            rotatedFileName = rotated_image(newSize_image,90,newFileName)
            f2_split.write(rotatedFileName+' '+train_img_cls+'\n')
            rotatedFileName = rotated_image(newSize_image,180,newFileName)
            f2_split.write(rotatedFileName+' '+train_img_cls+'\n')
            rotatedFileName = rotated_image(newSize_image,270,newFileName)
            f2_split.write(rotatedFileName+' '+train_img_cls+'\n')     

if __name__ == '__main__':
    start=time.time()#开始时间

    root = r"D:\\projects\\imageKaras\\data\\source"#绝对路径，自己的图片数据集路径
    train_ratio=0.8#训练集的占比，自己设定
    root_list=root.split('\\')
    print(root_list)#['D:', 'BaiduNetdiskDownload', 'flower_images']
    new_root=None
    new_root='\\'.join(root_list[:-1])+'\\'+root_list[-1]+"_split"
    print(new_root)#D:\BaiduNetdiskDownload\flower_images_split
    split_data(root, train_ratio,new_root=new_root)

    end=time.time()#结束时间
    print(end-start)# 输出的结果将是以秒为单位的时间间隔