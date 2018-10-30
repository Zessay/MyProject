#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# author@zhushuai
'''
定义前向传播的过程以及神经网络中的参数
'''
import tensorflow as tf

# 定义神经网络结构相关的参数
INPUT_NODE = 784
OUTPUT_NODE = 10

IMAGE_SIZE = 28
NUM_CHANNELS = 1
NUM_LABELS = 10

# 第一层卷积层的尺寸和深度
CONV1_DEEP = 32
CONV1_SIZE = 5
# 第二层卷积层的尺寸和深度
CONV2_DEEP = 64
CONV2_SIZE = 5
# 全连接层的节点个数
FC_SIZE = 512



# 定义卷积神经网络前向传播的过程。添加一个新参数train，用于区分训练过程和测试过程。
# 程序中将用到dropout方法，防止过拟合
def inference(input_tensor, train, regularizer):
    # 声明第一层卷积层的变量并实现前向传播过程，输出矩阵28x28x32
    with tf.variable_scope('layer1-conv1'):
        conv1_weights = tf.get_variable('weight', [CONV1_SIZE, CONV1_SIZE, NUM_CHANNELS, CONV1_DEEP],
                                        initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv1_biases = tf.get_variable('bias', [CONV1_DEEP], initializer=tf.constant_initializer(0.0))
        
        # 使用变长为5，深度为32的过滤器，过滤器移动的步长为1，且使用全0填充
        conv1 = tf.nn.conv2d(input_tensor, conv1_weights, strides=[1,1,1,1],padding='SAME')
        relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_biases))
    
    # 实现第二层池化层的前向传播过程，输出矩阵14x14x32
    with tf.variable_scope('layer2-pool1'):
        pool1 = tf.nn.max_pool(relu1, ksize=[1,2,2,1],strides=[1,2,2,1], padding='SAME')
        
    # 声明第三层卷积层变量并实现前向传播过程，输出为14x14x64
    with tf.variable_scope('layer3-conv2'):
        conv2_weights = tf.get_variable("weight", [CONV2_SIZE, CONV2_SIZE, CONV1_DEEP, CONV2_DEEP],
                                        initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv2_biases = tf.get_variable("bias", [CONV2_DEEP], initializer=tf.constant_initializer(0.0))
        
        # 使用变长为5，深度为64的过滤器，过滤器移动的步长为1，且使用全0填充
        conv2 = tf.nn.conv2d(pool1, conv2_weights, strides=[1,1,1,1], padding='SAME')
        relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_biases))
        
    # 实现第四层池化层的前向传播过程。输出为7x7x64
    with tf.variable_scope('layer4-poo12'):
        pool2 = tf.nn.max_pool(relu2, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
        
    # 将第四层池化层输出转化为第五层全连接层的输入格式
    pool_shape = pool2.get_shape().as_list()
    # 计算将矩阵拉直称直向量之后的长度，就是矩阵长宽和深度的乘积
    # 这里的pool_shape[0]是一个batch中数据的个数
    nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]
    
    # 通过tf.reshape函数将第四层的输出编程一个batch的向量
    reshaped = tf.reshape(pool2, [pool_shape[0], nodes])
    
    # 声明第五层全连接层的变量并实现前向传播。输入是拉直之后的向量，长度为3136，输出是长度为512的向量
    # dropout一般只在全连接层，而不在卷积层或池化层使用
    with tf.variable_scope('layer5-fc1'):
        fc1_weights = tf.get_variable("weight", [nodes, FC_SIZE], initializer=tf.truncated_normal_initializer(stddev=0.1))
        # 只有全连接层的权重需要加入正则化
        if regularizer != None:
            tf.add_to_collection("losses", regularizer(fc1_weights))
        fc1_biases = tf.get_variable('bias', [FC_SIZE], initializer=tf.constant_initializer(0.1))
        fc1 = tf.nn.relu(tf.matmul(reshaped, fc1_weights) + fc1_biases)
        if train:
            fc1 = tf.nn.dropout(fc1, 0.5)
    
    # 声明第六层全连接层的变量并实现前向传播。该层输入为一组长度为512的向量，输出是一组长度为10的向量
    with tf.variable_scope('layer6-fc2'):
        fc2_weights = tf.get_variable("weight", [FC_SIZE, NUM_LABELS], initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer != None:
            tf.add_to_collection('losses',regularizer(fc2_weights))
        fc2_biases = tf.get_variable('bias', [NUM_LABELS], initializer=tf.constant_initializer(0.1))
        logit = tf.matmul(fc1, fc2_weights) + fc2_biases
    
    # 返回第六层的输出
    return logit