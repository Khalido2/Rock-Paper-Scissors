#Handles preprocessing of rps images before training
import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import tensorflow_datasets as tfds

def makeDataset():
    data_dir = 'Datasets/'
    image_height = 720
    image_width = 720
    batch_size = 10

    #Make dataset from image directory
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        batch_size=batch_size,
        image_size=(image_height,image_width),
        shuffle=True,
        seed=123
    )

    return train_ds

#class_names = train_ds.class_names

#Display Datasset images 
'''
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
  for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    fileName = 'pic'+str(i)+'.png'
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis("off")
    plt.savefig(fileName)
    '''

