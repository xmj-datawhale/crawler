# import tensorflow as tf
# import numpy as np
#
# print(tf.__version__)
# print(np.__version__)
# x=[[[1, 1,1], [1, 1,1],[1, 1,1]],[[1, 1,1], [1, 1,1],[1, 1,1]]]
# # with tf.Session() as sess:
# #     sess.run(tf.global_variables_initializer())
# #     print(sess.run(tf.reduce_sum(x,0)))
# #     print(sess.run(tf.reduce_sum(x,1)))
# #     print(sess.run(tf.reduce_sum(x,2)))
#     # print(tf.reduce_sum(x,1))
#     # print(tf.reduce_sum(x,2))

import datetime
end_time=int(datetime.datetime.strptime('2019-09-01 00:00:00','%Y-%m-%d %H:%M:%S').timestamp())*1000
now_time = int(datetime.datetime.now().timestamp()*1000)
print(end_time,now_time)
l=[]
l.append('a=2')
l.append('b=3')
print(','.join(l))
print('a=2' in l)
print('a=23' in l)
print('a=23' not in l)

ss=set()
ss.add('a=2')
ss.add('b=3')
print(','.join(ss))
print('a=2' in ss)
print('a=23' in ss)
print('a=23' not in ss)

from pygame import mixer
import pygame
import time
def tip():
    # print(format_time(), '有新的下注码！！！！！')
    pygame.mixer.__init__()
    mixer.init()
    mixer.music.load('D:\\app\\tip.mp3')
    mixer.music.play()
    time.sleep(5)
    # print(format_time(), '休息5秒')


if __name__ == '__main__':
    import pyglet
    sound = pyglet.media.load('D:/app/tip.mp3', streaming=False)
    sound.play()
    pyglet.app.run()