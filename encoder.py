# -*- coding: utf-8 -*-

import os
from adain import PROJECT_ROOT
from adain.utils import set_params, get_params

import tensorflow as tf
from AdaIN import image_from_file


decoder_t7 = os.path.join(PROJECT_ROOT, 'decoder.t7')
vgg_t7_file = os.path.join(PROJECT_ROOT, 'vgg_normalised.t7')
content = os.path.join(PROJECT_ROOT, 'input/content/modern.jpg')
style = os.path.join(PROJECT_ROOT, 'input/style/goeritz.jpg')


def vgg_encoder():
    vgg = vgg19(vgg_t7_file, [None,None,3])
    # Todo : hard-coding
    model = tf.keras.models.Model(vgg.input, vgg.layers[-16].output)
    return model


def load_and_preprocess_img(img_fname, img_size=(224,224)):
    from keras.applications.vgg16 import preprocess_input
#     import cv2
#     import numpy as np
#     image = cv2.imread(img_fname)
#     image = cv2.resize(image, img_size)
#     image = preprocess_input(image/256*255)
#     return np.expand_dims(image, axis=0)
    def preprocess_image(image, size=None):
        image = tf.reverse(image, axis=[-1])
        #image = _offset_image(image, -1*_BGR_MEANS)
        image = tf.cast(image, tf.float32) / 256.0
        image = tf.image.resize_images(image, size)
        return image
    filename = tf.placeholder(tf.string)
    image = tf.image.decode_jpeg(tf.read_file(filename))
    image = tf.expand_dims(image, 0)
    image = preprocess_image(image, img_size)
    
    with tf.Session() as sess:
        images = sess.run(image, feed_dict={filename: img_fname})
        images_keras = preprocess_input(images * 255)
        return images_keras

#     with tf.Graph().as_default() as g, tf.Session(graph=g) as sess:
#         c, c_filename = image_from_file(g, 'content_image', size=img_size)
#          
#         # BGR-ordered image [0, 1]-ranged
#         images = sess.run(c, feed_dict = {c_filename: img_fname})
#         print(images.shape)
# 
#     images_keras = preprocess_input(images * 255)
#     return images_keras


class SpatialReflectionPadding(tf.keras.layers.Layer):

    def __init__(self, **kwargs):
        super(SpatialReflectionPadding, self).__init__(**kwargs)

    def call(self, x):
        return tf.pad(x, tf.constant([[0,0], [1,1], [1,1], [0,0]]), "REFLECT")


def vgg19(t7_file, input_shape=[224,224,3]):
    
    def _build_model(input_shape):

        Input = tf.keras.layers.Input
        Conv2D = tf.keras.layers.Conv2D
        MaxPooling2D = tf.keras.layers.MaxPooling2D
        Model = tf.keras.models.Model
        
        img_input = Input(shape=input_shape)
    
        # Block 1
        x = SpatialReflectionPadding()(img_input) # layer 1
        x = Conv2D(64, (3, 3), activation='relu', padding='valid', name='block1_conv1')(x)
        x = SpatialReflectionPadding()(x)
        x = Conv2D(64, (3, 3), activation='relu', padding='valid', name='block1_conv2')(x)
        x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)
        
        # Block 2
        x = SpatialReflectionPadding()(x)
        x = Conv2D(128, (3, 3), activation='relu', padding='valid', name='block2_conv1')(x)
        x = SpatialReflectionPadding()(x)
        x = Conv2D(128, (3, 3), activation='relu', padding='valid', name='block2_conv2')(x)
        x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)
        
        # Block 3
        x = SpatialReflectionPadding()(x)
        x = Conv2D(256, (3, 3), activation='relu', padding='valid', name='block3_conv1')(x)
        x = SpatialReflectionPadding()(x)
        x = Conv2D(256, (3, 3), activation='relu', padding='valid', name='block3_conv2')(x)
        x = SpatialReflectionPadding()(x)
        x = Conv2D(256, (3, 3), activation='relu', padding='valid', name='block3_conv3')(x)
        x = SpatialReflectionPadding()(x)
        x = Conv2D(256, (3, 3), activation='relu', padding='valid', name='block3_conv4')(x)
        x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)
        
        # Block 4
        x = SpatialReflectionPadding()(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='valid', name='block4_conv1')(x)
        x = SpatialReflectionPadding()(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='valid', name='block4_conv2')(x)
        x = SpatialReflectionPadding()(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='valid', name='block4_conv3')(x)
        x = SpatialReflectionPadding()(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='valid', name='block4_conv4')(x)
        x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)
        
        # Block 5
        x = SpatialReflectionPadding()(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='valid', name='block5_conv1')(x)
        x = SpatialReflectionPadding()(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='valid', name='block5_conv2')(x)
        x = SpatialReflectionPadding()(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='valid', name='block5_conv3')(x)
        x = SpatialReflectionPadding()(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='valid', name='block5_conv4')(x)
        model = Model(img_input, x, name='vgg19')
        return model
    
    model = _build_model(input_shape)
    weights, biases = get_params(t7_file)
    set_params(model, weights, biases)
    # model.load_weights("vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5", by_name=True)
    return model


if __name__ == '__main__':
    pass

