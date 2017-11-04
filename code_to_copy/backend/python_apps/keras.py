# coding:utf8

from keras.models import Model, Sequential
from keras.layers import Input, Dense, Activation, Multiply, Lambda, TimeDistributed, Flatten, RepeatVector, Dot, Conv1D
import keras.backend as K

model.compile(optimizer='adadelta', loss='mean_squared_error')
# model.compile(optimizer='adadelta', loss='mean_absolute_error')

def plot_model(model):
    from keras.utils import plot_model
    plot_model(model, show_shapes=True, show_layer_names=True)
    model.summary()
    # Mark down:  ![title](./model.png)

TOTAL_EPOCH = 50
for epoch in range(TOTAL_EPOCH):
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

history = model.fit(train_x, train_y, epochs=TOTAL_EPOCH, shuffle=True, validation_data=(test_x, test_y))


def plot_history(history):
    print 'parameters:\n', history.params
    print 
    print 'validation_size:\n', history.validation_data[0].shape
    fontsz = 18
    minmax = lambda loss: (min(loss), max(loss))
    fig = plt.figure(figsize=(15, 15))
    plt.plot(history.history['loss'], label='training loss(%f~%f)' % minmax(history.history['loss']))
    plt.plot(history.history['val_loss'], label='validation loss(%f~%f)' % minmax(history.history['val_loss']))
    plt.xlabel('epoch', fontsize=fontsz)
    plt.ylabel('loss', fontsize=fontsz)
    plt.xticks(fontsize=fontsz)
    plt.yticks(fontsize=fontsz)
    plt.legend(fontsize=fontsz)
    plt.show()


# TODO: summary the result
# goto http://10.150.144.96:8121/notebooks/playground/calibration.ipynb


# split data.  You can use the validation_split
from sklearn.model_selection import train_test_split
train_a, test_a, train_b, test_b = train_test_split(train_hist_perf, train_factors_ipt, train_rise_pct, train_best_rise_pct, test_size=0.2, random_state=42))
