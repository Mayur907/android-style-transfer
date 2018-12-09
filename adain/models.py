
import os
from adain import PROJECT_ROOT
import tensorflow as tf

Input = tf.keras.layers.Input
Conv2D = tf.keras.layers.Conv2D
Model = tf.keras.models.Model
UpSampling2D = tf.keras.layers.UpSampling2D

decode_t7_file = os.path.join(PROJECT_ROOT, 'decoder.t7')


def adain_style_transfer(alpha):
    from adain.adain_layer import adain_combine_model
    from adain.decoder import decoder

    model = adain_combine_model(alpha)
    decoder_model = decoder()
    
    content_input_tensor = tf.keras.layers.Input((None, None, 3))
    style_input_tensor = tf.keras.layers.Input((None, None, 3))
    
    x = model([content_input_tensor, style_input_tensor])
    x = decoder_model(x)
    model = Model([content_input_tensor, style_input_tensor], x, name='style_transfer')
    return model


    


    
    
    


