from tensorflow.keras import layers
from tensorflow.keras.models import Model
from ..blocks import add_common_layers_1D, conv_layer_1D, residual_block_1D, wavenet_residual_block_1D
import numpy as np
from tensorflow.keras.regularizers import l2

def unet_model(input_shape,
               number_of_classes,
               num_outputs,
               kernel_size,
               num_layers_encoder,
               num_layers_decoder,
               init_filter_num=32,
               filter_increase_factor=2,
               max_pool_size=2,
               dropout_rate=0,
               layer_depth=1,
               cardinality=1,
               bottle_neck=False,
               dilation_rate=1,
               BN_momentum=0.95,
               output_layer='sigmoid',
               block_type='conv_1D',
               weight_regularization=0,
               input_dropout_rate=0,
               output_dropout_rate=0):

    assert (filter_increase_factor == 1 or filter_increase_factor == 2)  # fixed or double.

    x_input = layers.Input(shape=tuple(input_shape))
    x = x_input
    x = layers.Dropout(input_dropout_rate)(x)

    # model
    x = unet(x,
             init_filter_num=init_filter_num,
             filter_increase_factor=filter_increase_factor,
             kernel_size=kernel_size,
             max_pool_size=max_pool_size,
             cardinality=cardinality,
             bottle_neck=bottle_neck,
             dropout_rate=dropout_rate,
             layer_depth=layer_depth,
             dilation_rate=dilation_rate,
             BN_momentum=BN_momentum,
             num_layers_encoder=num_layers_encoder,
             num_layers_decoder=num_layers_decoder,
             block_type=block_type,
             weight_regularization=weight_regularization)

    x = layers.Dropout(output_dropout_rate)(x)
    x = layers.Dense(units=number_of_classes,
                     activation=output_layer,
                     kernel_initializer='he_normal')(x)
    return Model(inputs=x_input, outputs=x)


def unet(x, block_type, init_filter_num=8, filter_increase_factor=1, kernel_size=3, cardinality=1, dropout_rate=0,
         layer_depth=1, num_layers_encoder=4, num_layers_decoder=4, dilation_rate=1, BN_momentum=0.95,
         bottle_neck=False, weight_regularization=0, max_pool_size=2):

    d = {}

    if num_layers_encoder > 0:
        x = layers.Conv1D(init_filter_num,
                          kernel_size=kernel_size,
                          strides=1,
                          padding='same',
                          dilation_rate=dilation_rate,
                          kernel_initializer='he_normal',
                          kernel_regularizer=l2(weight_regularization),
                          bias_regularizer=l2(weight_regularization))(x)

        d['conv0'] = add_common_layers_1D(x, dropout_rate=dropout_rate, BN_momentum=BN_momentum)
    layer_counter = 1

    # ENCODER
    for n in range(num_layers_encoder):
        kernel_size_ = min(x.shape[1], kernel_size)
        x = layers.MaxPooling1D(pool_size=max_pool_size)(d['conv{0}'.format(layer_counter - 1)])
        for m in range(layer_depth):
            if block_type == 'resnet':
                project_shortcut = True if m == 0 else False
                x = residual_block_1D(y=x,
                                      num_channels_in=x.shape[-1],
                                      num_channels=init_filter_num * filter_increase_factor ** layer_counter,
                                      kernel_size=kernel_size_,
                                      strides=1,
                                      _project_shortcut=project_shortcut,
                                      bottle_neck=bottle_neck,
                                      cardinality=cardinality,
                                      weight_regularization=weight_regularization)
            elif block_type == 'wavenet':
                wavenet_residual_block_1D(y=x,
                                          num_channels=init_filter_num * filter_increase_factor ** layer_counter,
                                          kernel_size=kernel_size_,
                                          dilation_rate=dilation_rate,
                                          weight_regularization=weight_regularization)
            else:
                x = conv_layer_1D(y=x,
                                  dilation_rate=dilation_rate,
                                  num_channels=init_filter_num * filter_increase_factor ** layer_counter,
                                  kernel_size=kernel_size_,
                                  weight_regularization=weight_regularization)
            x = add_common_layers_1D(x, dropout_rate=dropout_rate, BN_momentum=BN_momentum)
        d['conv{0}'.format(layer_counter)] = x
        layer_counter += 1

    # DECODER
    for n in range(num_layers_decoder):
        x = layers.UpSampling1D(size=max_pool_size)(d['conv{0}'.format(layer_counter - 1)])
        x = conv_layer_1D(y=x, num_channels=x.shape[-1] // 2 , kernel_size=2)
        x = layers.concatenate([d['conv{0}'.format(num_layers_encoder - (n + 1))], x], axis=2)
        kernel_size_ = min(x.shape[1], kernel_size)

        for m in range(layer_depth):
            if block_type == 'resnet':
                project_shortcut = True if m == 0 else False
                x = residual_block_1D(y=x,
                                      num_channels_in=x.shape[-1],
                                      num_channels=init_filter_num * filter_increase_factor ** (num_layers_encoder - (n + 1)),
                                      kernel_size=kernel_size_,
                                      strides=1,
                                      _project_shortcut=project_shortcut,
                                      bottle_neck=bottle_neck,
                                      cardinality=cardinality,
                                      weight_regularization=weight_regularization)
            elif block_type == 'wavenet':
                wavenet_residual_block_1D(y=x,
                                          num_channels=init_filter_num * filter_increase_factor ** (num_layers_encoder - (n + 1)),
                                          kernel_size=kernel_size_,
                                          dilation_rate=dilation_rate,
                                          weight_regularization=weight_regularization)
            else:
                x = conv_layer_1D(y=x,
                                  dilation_rate=dilation_rate,
                                  num_channels=init_filter_num * filter_increase_factor ** (num_layers_encoder - (n + 1)),
                                  kernel_size=kernel_size_,
                                  weight_regularization=weight_regularization)
            x = add_common_layers_1D(x, dropout_rate=dropout_rate, BN_momentum=BN_momentum)
        d['conv{0}'.format(layer_counter)] = x
        layer_counter += 1
    return x
