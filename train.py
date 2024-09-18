import os
import cv2
import numpy as np

# os.environ['KERAS_BACKEND'] = 'torch'
# os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
# os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense,Dropout

IMAGE_SIZE = (256,256)
def build_train(trainFile):
    x_train =[]
    y_train =[]
    with open(trainFile, 'r') as f:
        for line in f:
            imageFile = line.split(' ')[0]
            imageLabel = int(line.split(' ')[1].split('\n')[0])
            try:
                imData =cv2.imread(imageFile)
                x_train.append((imData))
                y_train.append(imageLabel)
            except Exception as e:
                print(e)
                
    x = np.array(x_train)
    x = x/255
    x = x.astype(dtype=np.float64)
    return x,np.array(y_train)         

model = Sequential()
model.add(Conv2D(64, (3, 3), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.1))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.1))
model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
 
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

x_train,y_train = build_train('./train_split.txt')
model.fit(x_train, y_train, epochs=30, batch_size=128)
model.save('增值税发票识别.keras')
print('训练结束')
