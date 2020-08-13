# -*- coding: utf-8 -*-
"""signalsnet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nEsukJ5MJlnMiBbYjZE1bw5oxFjisWKh
"""


INPUT_PATH = "/cs/ep/514/Snir/"
OUTPUT_PATH = "/cs/ep/514/Snir/"


# from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.layers import Dense, Flatten, Conv2D, Conv1D, MaxPool1D, MaxPool2D, BatchNormalization, Dropout
from tensorflow.keras import Model
tf.enable_eager_execution()

def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels, n_unique_labels))
    one_hot_encode[np.arange(n_labels), labels[:, 0]] = 1
    return one_hot_encode



def get_xy_from_malmag():

    matrix = np.load(INPUT_PATH + "train_set.npy")[:7000]
    # matrix = np.concatenate((np.array(list(matrix[:, 0])), matrix[:, 1].reshape((matrix[:, 1].shape[0], 1)).astype(np.float32)), axis=1)

    matrix = matrix[1:]
    matrix = matrix[np.random.permutation(matrix.shape[0])]
    partition = int(matrix.shape[0] * 0.9)
    numpy_file1 = matrix[:partition]
    numpy_file2 = matrix[partition:]


    print(numpy_file1.shape, numpy_file2.shape)
    pandas_file1 = pd.DataFrame(data=numpy_file1, index=[i for i in range(numpy_file1.shape[0])], columns=['f' + str(i) for i in range(numpy_file1.shape[1])])
    pandas_file2 = pd.DataFrame(data=numpy_file2, index=[i for i in range(numpy_file2.shape[0])], columns=['f' + str(i) for i in range(numpy_file2.shape[1])])
    pandas_file1.dropna(inplace=True)
    pandas_file2.dropna(inplace=True)
    numpy_file1 = pandas_file1.values
    numpy_file2 = pandas_file2.values

    print("gfg", numpy_file1.shape, numpy_file2.shape)


    y1 = numpy_file1[:, -1].reshape(numpy_file1.shape[0], 1).astype(np.int64)
    print("snir1", y1.shape)
    y1 = one_hot_encode(y1-1)
    y2 = numpy_file2[:, -1].reshape(numpy_file2.shape[0], 1).astype(np.int64)
    print("snir2", y2.shape)
    y2 = one_hot_encode(y2 -1)
    X1 = numpy_file1[:, :-1]
    X2 = numpy_file2[:, :-1]
    print((X1.shape, y1.shape), (X2.shape, y2.shape))
    return (X1, np.argmax(y1, axis=1)), (X2, np.argmax(y2, axis=1))



def gen():
    pathes = ['/cs/ep/519/Data/2_vs_1_train.npy']
    for path in pathes:
        file = np.load(path, mmap_mode='r+', allow_pickle=True)
        for i in range(0, file.shape[0], 128):
            if (file.shape[0]-i) < 128:
                chunk_file = file[i:]
            else:
                chunk_file = file[i:i+128]
            for j in range(0, chunk_file.shape[0], 1):
                batch = chunk_file[j]
                batch = batch[..., tf.newaxis]
                batch = batch[..., tf.newaxis]
                # batch = (batch - train_expectation) / train_std
                yield batch[:-1], batch[-1, 0] -1
    return




#if the data is too big, we want to use generator:

# train_ds = tf.data.Dataset.from_generator(gen, (tf.float64, tf.float64),output_shapes=(tf.TensorShape([256000, 1, 1]), tf.TensorShape([1])))#.batch(64).take(64)
# test_ds = tf.data.Dataset.from_generator(gen, (tf.float64, tf.float64), (tf.TensorShape([256000, 1, 1]), tf.TensorShape([1]))).batch(64)


train_set = np.load('/cs/ep/519/Data/penny_train.npy', allow_pickle=True)
test_set = np.load('/cs/ep/519/Data/penny_test.npy', allow_pickle=True)

x_train, y_train = train_set[:, :-1], train_set[:, -1] -1
x_test, y_test = test_set[:, :-1], test_set[:, -1] -1


#normalize the data
train_expectation = np.mean(x_train)
train_std = np.std(x_train)
x_train = (x_train - train_expectation) / train_std
x_test = (x_test - train_expectation) / train_std


x_train = x_train[..., tf.newaxis, tf.newaxis]
x_test = x_test[..., tf.newaxis, tf.newaxis]


# train_ds = tf.data.Dataset.from_generator(gen, (tf.float64, tf.float64), (tf.TensorShape([256000, 1, 1]), tf.TensorShape([1]))).batch(64)

train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(64)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(64)

class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv1 = Conv2D(4, (12, 1), activation='relu')
        self.pool1 = MaxPool2D((4, 1))
        self.conv2 = Conv2D(6, (12, 1), activation='relu')
        self.pool2 = MaxPool2D((4, 1))
        self.conv3 = Conv2D(8, (12, 1), activation='relu')
        self.pool3 = MaxPool2D((4, 1))
        self.conv4 = Conv2D(10, (12, 1), activation='relu')
        self.pool4 = MaxPool2D((4, 1))
        self.conv5 = Conv2D(12, (12, 1), activation='relu')
        self.pool5 = MaxPool2D((4, 1))
        self.conv6 = Conv2D(14, (12, 1), activation='relu')
        self.pool6 = MaxPool2D((4, 1))
        self.conv7 = Conv2D(16, (12, 1), activation='relu')
        self.pool7 = MaxPool2D((4, 1))

        self.flatten = Flatten()
        self.d1 = Dense(8, activation='relu')
        self.d2 = Dense(4, activation='softmax')



    def call(self, x, training=False):
        x = self.conv1(x)
        x = self.pool1(x)

        x = self.conv2(x)
        x = self.pool2(x)

        x = self.conv3(x)
        x = self.pool3(x)

        x = self.conv4(x)
        x = self.pool4(x)

        x = self.conv5(x)
        x = self.pool5(x)

        x = self.conv6(x)
        x = self.pool6(x)

        x = self.conv7(x)
        x = self.pool7(x)

        x = self.flatten(x)
        x = self.d1(x)
        x = self.d2(x)
        return x

# Create an instance of the model
model = MyModel()
_ = model(np.zeros((64, 256000, 1, 1)))

loss_object = tf.keras.losses.SparseCategoricalCrossentropy()

optimizer = tf.keras.optimizers.Adam()

train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')

@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        predictions = model(images, training=True)
        loss = loss_object(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    train_loss(loss)
    train_accuracy(labels, predictions)


@tf.function
def test_step(images, labels):
    predictions = model(images, training=False)
    t_loss = loss_object(labels, predictions)
    test_loss(t_loss)
    test_accuracy(labels, predictions)


EPOCHS = 150
train_loss_lst, test_loss_lst, train_acc_lst, test_acc_lst = [], [], [], []

for epoch in range(EPOCHS):
    # Reset the metrics at the start of the next epoch
    train_loss.reset_states()
    train_accuracy.reset_states()
    test_loss.reset_states()
    test_accuracy.reset_states()
    for images, labels in train_ds:
        train_step(images, labels)

    train_acc_lst.append(train_accuracy.result()*100)
    train_loss_lst.append(train_loss.result())

    for test_images, test_labels in test_ds:
        test_step(test_images, test_labels)

    test_acc_lst.append(test_accuracy.result()*100)
    test_loss_lst.append(test_loss.result())

    template = 'Epoch {}, Loss: {}, Accuracy: {}, Test Loss: {}, Test Accuracy: {}'
    print(template.format(epoch+1, train_loss.result(), train_accuracy.result()*100, test_loss.result(), test_accuracy.result()*100))
    if test_accuracy.result()*100 > 49:
        model.save_weights('/cs/ep/514/Snir/outputs/penny_weights_' + str(test_accuracy.result()*100) + '_acc.h5')


plt.plot(train_loss_lst)
plt.plot(test_loss_lst)
plt.legend(["Train Loss", "Test Loss"])
plt.title('Loss')
plt.show()


plt.plot(train_acc_lst)
plt.plot(test_acc_lst)
plt.legend(["Train Accuracy", "Test Accuracy"])
plt.title('Accuracy')
plt.show()


