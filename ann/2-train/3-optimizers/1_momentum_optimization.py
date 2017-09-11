"""
Training a very deep neural network can be painfully slow. Using a faster optimizer than the Gradient Descent
optimizer can speed up the training process quite a bit.

Common optimization techniques are: Momentum, Nesterov Accelerated Gradient, AdaGrad, RMSProp, and Adam.

Momentum Optimization
---------------------
Ref: https://distill.pub/2017/momentum/

Gradient Descent takes small regular steps down the slope, so it'll take a lot of time to reach the minumum.
Gradient Descent updates the weights θ by subtracting the gradient of the cost function J(θ) with respect to
the weights multiplied by the learning rate. Note that Gradient Descent pays no attention to the previous
graidents. If the local graident is small, Gradient Descent goes very slowly.

Momentum optimization, on the other hand, pays a great attention to previous gradients. At each iteration,
it maintains a momentum vector (m) by adding local gradient to this vector, multiplied by the learning rate.
It then updates the weights by subtracting that vector.

Momentum algorithm:
m <- βm + η∇θJ(θ)
θ <- θ - m

In Momentum optimization, the gradient is used as an acceleration not a speed?

To prevent the momentum from growing too large, we use a hyperparameter β (called momentum)
which receives a value between 0 and 1 (generally β is set to 0.9)

If the gradient remains constant, the terminal velocity (!?) is equal to that gradient
multiplied by the learning rate, multiplied by 1 / (1 - β). If β = 0.9, the terminal
velocity is equal to 10 X the gradient x the learning rate, Momentum optimization
would go 10 times faster than Gradient Descent !? (1000 times if β = 0.999). This characteristic
allows Momentum optimization to escape from plateaus much fater than GD.

In DNN which doesn't use Batch Normalization, the upper layers often end up having inputs with
very different scales, using Momentum can be a solution for this problem.

Momentum optimization may overshoot through its steps (like pendulum oscillation) before stabilizing
at the minimum.

A drawback of  Momentum optimization is that it introduces a new hyperparameter for tuning - the momentum.
However, in real-life problems this value is usually set to 0.9, and it works well in lots of problems.
Generally, Momentum optimization is faster in reaching to minimum than Gradient Descent.
"""
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

z = np.linspace(-5, 5, 200)
tf.reset_default_graph()
n_inputs = 784
n_hidden1 = 300
n_hidden2 = 100
n_outputs = 10
learning_rate = 0.01

X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
y = tf.placeholder(tf.int64, shape=(None), name="y")

with tf.name_scope("dnn"):
    hidden1 = tf.layers.dense(X, n_hidden1, activation=tf.nn.elu, name="hidden1")
    hidden2 = tf.layers.dense(hidden1, n_hidden2, activation=tf.nn.elu, name="hidden2")
    logits = tf.layers.dense(hidden2, n_outputs, name="outputs")

with tf.name_scope("loss"):
    xen = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
    loss = tf.reduce_mean(xen, name="loss")

with tf.name_scope("train"):
    # Using Momentum optimizer rather than Gradient Descent optimizer
    optimizer = tf.train.MomentumOptimizer(learning_rate=learning_rate, momentum=0.9)
    training_op = optimizer.minimize(loss)

with tf.name_scope("eval"):
    correct = tf.nn.in_top_k(logits, y, 1)
    accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

init = tf.global_variables_initializer()


n_epochs = 100
batch_size = 100
mnist = input_data.read_data_sets("/tmp/data/")

with tf.Session() as sess:
    init.run()
    for epoch in range(n_epochs):
        for iteration in range(len(mnist.test.labels) // batch_size):
            X_batch, y_batch = mnist.train.next_batch(batch_size)
            sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
        acc_train = accuracy.eval(feed_dict={X: X_batch, y: y_batch})
        acc_test = accuracy.eval(feed_dict={X: mnist.test.images, y: mnist.test.labels})
        print(epoch, "Train accuracy:", acc_train, "Test accuracy:", acc_test)