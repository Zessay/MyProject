#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# author@zhushuai

'''
神经网络的训练过程
'''
import os
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# 加载mnist_inference.py中定义的常量和前向传播的函数
import mnist_inference

# 为了防止之前定义的变量占用了命名空间，重启图
tf.reset_default_graph()
# 配置神经网络的参数
BATCH_SIZE = 100
LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99
REGULARAZTION_RATE = 0.0001
TRAINING_STEPS = 30000
MOVING_AVERAGE_DECAY = 0.99

# 模型保存的路径和文件名
MODEL_SAVE_PATH =  r"D:\Project\mnist\model\ "
MODEL_NAME = "mnist_model.ckpt"

def train(mnist):
    # 定义输入输出placeholder
    x = tf.placeholder(tf.float32, [BATCH_SIZE, mnist_inference.IMAGE_SIZE,
                                    mnist_inference.IMAGE_SIZE, 
                                    mnist_inference.NUM_CHANNELS], name="x-input")
    y_ = tf.placeholder(tf.float32, [None, mnist_inference.OUTPUT_NODE], name="y-input")

    regularizer = tf.contrib.layers.l2_regularizer(REGULARAZTION_RATE)
    # 直接使用mnist_inference.py中定义的前向传播过程
    y = mnist_inference.inference(x, True, regularizer)
    global_step = tf.Variable(0, trainable=False)

    # 定义损失函数、学习率、滑动平均和训练过程
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)  # 定义滑动平均类的实例
    variable_averages_op = variable_averages.apply(tf.trainable_variables())
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step,
                                               mnist.train.num_examples / BATCH_SIZE, LEARNING_RATE_DECAY)
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    # 同时迭代多个变量时
    with tf.control_dependencies([train_step, variable_averages_op]):
        train_op = tf.no_op(name='train')

    # 初始化Tensorflow持久化类
    saver = tf.train.Saver(max_to_keep=2)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        # 在训练过程中不再测试模型在验证数据上的表现，验证和测试由独立的程序完成
        for i in range(TRAINING_STEPS):
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            reshaped_xs = np.reshape(xs, (BATCH_SIZE, mnist_inference.IMAGE_SIZE,
                                          mnist_inference.IMAGE_SIZE,
                                          mnist_inference.NUM_CHANNELS))
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x:reshaped_xs, y_:ys})

            # 每1000轮保存一次模型
            if i % 1000 == 0:
                # 输出当前训练情况，即损失函数大小
                print("After %d training step(s), loss on training batch is %g ." % (step, loss_value))
                # 保存当前模型
                saver.save(sess, r'D:\Project\mnist_lenet5\model\mnist_model.ckpt', global_step=global_step)

def main(argv=None):
    mnist = input_data.read_data_sets("D:\Dataset\mnist", one_hot=True)
    train(mnist)

if __name__ == "__main__":
    tf.app.run()