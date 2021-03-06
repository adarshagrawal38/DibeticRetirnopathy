# -*- coding: utf-8 -*-
"""DiabeticRetinopathy_gray_alexnet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Uu9QqGSPYls6DEp6cKlYpi3LPNJblycN
"""

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
import numpy as np
#IMG_SIZE = 50
IMG_SIZE = 200
#input_shape = (IMG_SIZE, IMG_SIZE, 1)
input_shape = (IMG_SIZE, IMG_SIZE, 3)

train = np.load('rgb_200X200_100_images.npy',  allow_pickle=True)

test = train[1:50]


#tr_img_data = np.array([i[0] for i in train]).reshape(-1,IMG_SIZE,IMG_SIZE,1)
#tr_lbl_data = np.array([i[1] for i in train])

#tst_img_data = np.array([i[0] for i in test]).reshape(-1,IMG_SIZE,IMG_SIZE,1)
#tst_lbl_data = np.array([i[1] for i in test])



tr_img_data = np.array([i[0] for i in train]).reshape(-1,IMG_SIZE,IMG_SIZE,3)
tr_lbl_data = np.array([i[1] for i in train])

tst_img_data = np.array([i[0] for i in test]).reshape(-1,IMG_SIZE,IMG_SIZE,3)
tst_lbl_data = np.array([i[1] for i in test])


model = Sequential()
#number of filter, shape of filter, (ImageSIze, IMage_size, 3)
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
#normalize by column
#increases the learning rate
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))

model.add(Conv2D(32, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))

model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())

# Fully connected layer
model.add(Dense(512))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(2))
model.add(Activation('softmax'))


#optimiaer -> reduces loss

model.compile(loss=keras.losses.categorical_crossentropy,
optimizer=keras.optimizers.Adam(),
metrics=['accuracy'])

model.fit(tr_img_data, tr_lbl_data,batch_size=10,epochs=5,verbose=1,
 validation_data=(tst_img_data, tst_lbl_data))
model.save("keras_car.h5")
score = model.evaluate(tst_img_data, tst_lbl_data, verbose=1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

import matplotlib.pyplot as plt
from keras.models import load_model
import numpy as np
# if you need to create the data:
#test_data = process_test_data()
# if you already have some saved:
test_data = np.load('rgb_200X200_100_images.npy', allow_pickle=True)
model = load_model('keras_car.h5')

fig=plt.figure()

for num,data in enumerate(test_data[:12]):
    # cat: [1,0]
    # dog: [0,1]
    
    img_num = data[1]
    img_data = data[0]
    
    y = fig.add_subplot(3,4,num+1)
    orig = img_data
    data = img_data.reshape(1,IMG_SIZE,IMG_SIZE,3)
    #model_out = model.predict([data])[0]
    
    
    con_data= np.expand_dims(data, axis=0)
    
    model_out = model.predict(con_data)[0]
    #model_out = model.predict([data])[0]
    
    if np.argmax(model_out) == 1: str_label='Infected'
    else: str_label='Normal'
    
    model_out = np.squeeze(model_out, axis=0)
    model_out = model_out.reshape(con.shape[:2])
    
    y.imshow(model_out)
    plt.title(str_label)
    y.axes.get_xaxis().set_visible(False)
    y.axes.get_yaxis().set_visible(False)
plt.show()