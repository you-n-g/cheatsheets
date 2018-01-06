# coding:utf8


# If we share GPU with others. Use ths to limit the GPU memory usage.
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.3
config.gpu_options.allow_growth = True
set_session(tf.Session(config=config))


from keras.models import Model, Sequential, load_model
from keras.layers import Input, Dense, Activation, Multiply, Lambda, TimeDistributed, Flatten, RepeatVector, Dot, Conv1D
import keras.callbacks
import keras.backend as K


def plot_model(model):
    from keras.utils import plot_model as keras_plot_model
    keras_plot_model(model, show_shapes=True, show_layer_names=True)
    model.summary()
    # Mark down:  ![title](./model.png)

def plot_history(history, keys=['loss', 'acc']):
    '''
    If you want to plot history dynamically. Please use this code
    https://gist.github.com/stared/dfb4dfaf6d9a8501cd1cc8b8cb806d2e
    '''
    print('history.params:\n'), history.params
    print()
    print('history.validation_data[*].shape:\n')
    for val_data in history.validation_data:
        print(val_data.shape)
    for train_key in keys:
        val_key = 'val_' + train_key
        fontsz = 18
        minmax = lambda x: (min(x), max(x))
        fig = plt.figure(figsize=(15, 15))
        plt.plot(history.history[train_key], label='training %s(%f~%f)' % ((train_key,) + minmax(history.history[train_key])))
        if val_key in history.history:
            plt.plot(history.history[val_key], label='validation %s(%f~%f)' % ((train_key,) + minmax(history.history[val_key])))
        plt.xlabel('epoch', fontsize=fontsz)
        plt.ylabel(train_key, fontsize=fontsz)
        plt.xticks(fontsize=fontsz)
        plt.yticks(fontsize=fontsz)
        plt.legend(fontsize=fontsz)
        plt.show()

plot_model(model)

model_name = 'MODEL_NAME'
best_path = 'best_model_%s.hdf5' % model_name
last_path = 'last_model_%s.hdf5' % model_name

verbose = True

earlyStoper = keras.callbacks.EarlyStopping(monitor='val_loss', verbose=verbose, patience=10)
# keras.callbacks.EarlyStopping(monitor='loss', min_delta=1e-6, verbose=verbose, patience=10)  # sometime I train to convergence of training data.
saveBestModel = keras.callbacks.ModelCheckpoint(best_path, monitor='val_loss', verbose=verbose, save_best_only=True)
saveLastModel = keras.callbacks.ModelCheckpoint(last_path, monitor='val_loss', verbose=verbose, save_best_only=False)
callbacks = [earlyStoper, saveBestModel, saveLastModel]

model.compile(optimizer='adadelta', loss='mean_squared_error')
history = model.fit(train_x, train_y, epochs=1000, shuffle=True, validation_data=(test_x, test_y), callbacks=callbacks, verbose=verbose)
plot_history(history)

model.load_weights(best_path)  # load weights will be a little faster than load model



TOTAL_EPOCH = 50
for epoch in range(TOTAL_EPOCH):
    '''
    I think this will be deprecated.
    '''
    model.fit(train_x, train_y,
             epochs=epoch+1, initial_epoch=epoch, shuffle=True,
             validation_data=(test_x, test_y))
# you can use  validation_split=0.2 to split the train_x, train_y
# This will directly use the last 20% data=0.2.
#     from random import shuffle
#     shuffle_idx = range(len(train_x))
#     shuffle(shuffle_idx)
#     train_x[shuffle_idx]
# validation_data will override validation_split



# split data.  You can use the validation_split
from sklearn.model_selection import train_test_split
train_a, test_a, train_b, test_b = train_test_split(train_hist_perf, train_factors_ipt, train_rise_pct, train_best_rise_pct, test_size=0.2, random_state=42))


# If train 作为参数之一！！！！



# How to construct models
# [Building Autoencoders in Keras](https://blog.keras.io/building-autoencoders-in-keras.html)
# 但是我看到的限制是它的input必须是定义的 Input，随便一个layer的 input可能只是一个 Tensor...

# How to get the intermediate result of a model
# [Intermediate](https://keras.io/getting-started/faq/#how-can-i-obtain-the-output-of-an-intermediate-layer)
# 基本的思路是通过 layers找到input和output，然后再用它们拼成model
# 这个可以突破上面的限制


# How to freeze layers.
# https://keras.io/getting-started/faq/#how-can-i-freeze-keras-layers
# BUG unable to freeze some layer: https://github.com/fchollet/keras/issues/7504#issuecomment-321502581
for layer in model.layers:
    if hasattr(layer, 'layer'):
	layer.layer.trainable = False
    layer.trainable = False
# You must recompile to make the trainable attribute to take effect




# keras如何看各个参数的gradient: https://github.com/fchollet/keras/issues/2226#issuecomment-259004640

weights = model.trainable_weights # weight tensors
# weights = [weight for weight in weights if model.get_layer(weight.name[:-2]).trainable] # filter down weights tensors to only ones which are trainable. It raises exception here.
gradients = model.optimizer.get_gradients(model.total_loss, weights) # gradient tensors

input_tensors =  (model.inputs + # input data
                 model.sample_weights + # how much to weight each sample by
                 model.targets + # labels
                 [K.learning_phase()]) # train or test mode

get_gradients = K.function(inputs=input_tensors, outputs=gradients)

sample_n = 32
inputs = [train_hist_perf[:sample_n], train_all_factors[:sample_n], train_next_ex_ret[:sample_n]] + [# X
            np.ones(sample_n), # sample weights
            train_max_ex_ret[:sample_n], # y
            0, # learning phase in TEST mode
]

for w, g in zip(weights, get_gradients(inputs)):
    print w
    print g




# Keras costum the loss function and change regulization during training
# https://github.com/fchollet/keras/issues/4813#issuecomment-339466180
