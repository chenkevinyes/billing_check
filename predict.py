from PIL import Image
import cv2
import numpy as np
import os
from keras.models import Sequential,load_model
import fitz
import shutil
import uuid
IMAGE_SIZE = (256,256)
def color_print(text: str, mode: str = '', fore: str = '', back: str = '',end="") -> None:
    dict_mode = {'d': '0', 'h': '1', 'nb': '22', 'u': '4', 'nu': '24',
                 't': '5', 'nt': '25', 'r': '7', 'nr': '27', '': ''}
    dict_fore = {'k': '30', 'r': '31', 'g': '32', 'y': '33', 'b': '34',
                 'm': '35', 'c': '36', 'w': '37', '': ''}
    dict_back = {'k': '40', 'r': '41', 'g': '42', 'y': '43', 'b': '44',
                 'm': '45', 'c': '46', 'w': '47', '': ''}
    formats = ';'.join([each for each in [
        dict_mode[mode], dict_fore[fore], dict_back[back]] if each])
    print(f'\033[{formats}m{text}\033[0m')

def get_filename_without_extension(filepath):
    filename_with_extension = os.path.basename(filepath)
    return os.path.splitext(filename_with_extension)[0]

def resize_image(name ,size=IMAGE_SIZE):
    output_image_path = './temp/test.jpg' 
    with Image.open(name) as image:
        image = image.convert('RGB')
        resized_image = image.resize(size)
        resized_image.save(output_image_path)    
    img = cv2.imread(output_image_path)
    img = np.array(img) / 255
    img = img.astype(np.float64)
    img = img.reshape(-1, size[0], size[1], 3)    
    return img


def read_pdf(fileName,outfolder= './temp'):
    pdfName = get_filename_without_extension(fileName)
    uuid1 = uuid.uuid1()    
    # print("UUID1:", uuid1)
    newFolder = outfolder +'//'+pdfName
    if os.path.exists(newFolder):
        shutil.rmtree(newFolder)
    if os.path.exists(newFolder):
        raise ValueError('删除目录'+newFolder +'失败，请手工删除后重新运行')          
    if not os.path.exists(newFolder):                    
        os.mkdir(newFolder)
    if not os.path.exists(newFolder):
        raise ValueError('创建目录'+newFolder +'失败')          
    # 打开PDF文件
    doc = fitz.open(fileName)
    # 遍历PDF中的每一页
    for page_index in range(doc.page_count):
        page = doc[page_index]
        
        for image_index, img in enumerate(page.get_images(), start=1): 
            # 获取图像的XREF编号和图像数据
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            # 保存图像
            if str(fitz.csRGB) == str(pix.colorspace):                
                img_path =newFolder +'//'+str(uuid1)+'_'+ f'{page_index+1}_{xref}.png'
                pix.save(img_path)
    # 关闭PDF文件
    doc.close()
    return newFolder




def predict(model,imgFile):
    img = resize_image(imgFile)
    predict_y = model.predict(img)
    pred_y = int(np.round(predict_y))
    # print(pred_y)
    return pred_y

def predict_folder(dirs):
    names = os.listdir(dirs)
    findList = []
    for name in names:                    
        testFile = dirs +'\\'+name                    
        file_extension = (os.path.splitext(testFile)[1]).lower()
        if file_extension in ['.jpg','.png']:                   
            predict_y=  predict(model,testFile)
            if predict_y == 1:
                findList.append(name)
        else:
            print('不支持的文件:'+testFile)
            # color_print( name +' 是',fore='g',back='b')                
        # else:
        #     color_print(name + ' 不是',fore='r')                       
    color_print('从'+str(len(names))+'图片中，识别出'+str(len(findList))+'张发票',fore='g',back='b')
    if len(findList)>0:
        color_print(','.join(findList)) 

# read_pdf('D:\\projects\\imageKaras\\temp\\pdf\\海油发展亚氨基二琥珀酸四钠采购通用协议应答文件商务部分.pdf')

model = load_model('增值税发票识别.h5')

while True:
    q = input('请输入包含发票图片(jpg,png)的文件路径或文件名：')
    if q != '':
        try:
            # testFile = 'd:\\temp\crhqhq1y.png'
            testFile = q
            if not os.path.exists(testFile):
                print('文件或路径不存在，请重新输入')
                continue
            if os.path.isfile(testFile):
                file_extension = (os.path.splitext(testFile)[1]).lower()
                if file_extension in ['.jpg','.png']:
                    predict_y=  predict(model,testFile)
                    if predict_y == 1:
                        color_print('是增值税发票',fore='g',back='b')                
                    else:
                        color_print('不是',fore='r')    
                elif file_extension == '.pdf':
                    pdfFolder = read_pdf(testFile)
                    predict_folder(pdfFolder)
                else:
                    raise ValueError('不支持胡文件类型：'+testFile) 
            else:
                dirs = q
                predict_folder(dirs)
        except Exception as e:
            print(e)


