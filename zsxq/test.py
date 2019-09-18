import tensorflow as tf
import numpy as np

print(tf.__version__)
print(np.__version__)
x=[[[1, 1,1], [1, 1,1],[1, 1,1]],[[1, 1,1], [1, 1,1],[1, 1,1]]]
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(sess.run(tf.reduce_sum(x,0)))
    print(sess.run(tf.reduce_sum(x,1)))
    print(sess.run(tf.reduce_sum(x,2)))
    # print(tf.reduce_sum(x,1))
    # print(tf.reduce_sum(x,2))