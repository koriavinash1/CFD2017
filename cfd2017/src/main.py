# import lib...
import cv2
import sklearn
import keras
import tensorflow as tf
import keras
import numpy as np
from helper import Conv2D, SimilarityMatrix, MaxPooling2D, ConclusionMatrix,\
		BatchNormalization, DiceCriteria2Cls

# for image uploading option with ui
# from tkinter.filedialog import askopenfilename // later...

train = []
test = []

check_image = cv2.imread("../img/case.jpg", 0)
base_image = cv2.imread("../img/base.jpg", 0)

# hyperparams
image_height = 100 
image_width = 200

learning_rate = 1e-1
iterations = 800
angle_step = 2
similarity = 100

# image pre-processing
# check_image_g = cv2.cvtColor(check_image, cv2.COLOR_RGB2GRAY) # gray scaled image
check_image_r = cv2.resize(check_image, (image_width, image_height), \
				 interpolation = cv2.INTER_CUBIC).reshape(1, image_height, image_width, 1) # resized image for network

# base_image_g = cv2.cvtColor(base_image, cv2.COLOR_RGB2GRAY) # gray scaled image
base_image_r = cv2.resize(base_image, (image_width, image_height), \
				interpolation = cv2.INTER_CUBIC).reshape(1, image_height, image_width, 1) # resized image for network

# init transform parameters
transform_matrix = [0, 0, 0, 0, 0, 0]

# def f(w): return -np.sum((w - transform_matrix)**2)

npop = 500      # population size
sigma = 0.1    # noise standard deviation


# network filter simila
base_input = tf.placeholder(shape=(1, image_height, image_width, 1), \
                    name='baseInput', dtype=tf.float32)

check_input = tf.placeholder(shape=(1, image_height, image_width, 1), \
                    name='caseInput', dtype=tf.float32)

base_conv1 = Conv2D(data=base_input, filters=32, kernel_size=(5,5), train=False)
base_pool1 = MaxPooling2D(data=base_conv1)

base_conv2 = Conv2D(data=base_pool1, filters=64, kernel_size=(5,5), train=False) 
base_pool2 = MaxPooling2D(data=base_conv2)

# base_conv3 = Conv2D(data=base_pool2, filters=64, kernel_size=(5,5), train=False) 
# base_pool3 = MaxPooling2D(data=base_conv3)

# case input transformation
check_conv1 = Conv2D(data=check_input, filters=32, kernel_size=(5,5))
check_pool1 = MaxPooling2D(data=check_conv1)

check_conv2 = Conv2D(data=check_pool1, filters=64, kernel_size=(5,5)) 
check_pool2 = MaxPooling2D(data=check_conv2)


saver = tf.train.Saver()
# pred, conv1, conv2 = main_network(x, weights, biases, keep_prob, phase_train)
    
# sim = SimilarityMatrix(base_conv1, check_conv1) + \
# 	SimilarityMatrix(base_conv2, check_conv2)+ \
# 	SimilarityMatrix(base_input, check_input)

sim = DiceCriteria2Cls(base_conv1, check_conv1)+\
	DiceCriteria2Cls(base_conv2, check_conv2)+\
	DiceCriteria2Cls(base_input, check_input) 
sim = (sim-140)*0.1

optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(sim)
tf.summary.scalar("similarity", sim)

merged = tf.summary.merge_all()
init = tf.global_variables_initializer()
w = tf.random_normal([6])
with tf.Session() as sess:
	sess.run(init)
	step = 1
	train_writer = tf.summary.FileWriter('./logs', sess.graph)
	while step <= iterations:
 		_, sim_score, summary = sess.run([optimizer, sim, merged], feed_dict={base_input: base_image_r, check_input: check_image_r})
 		train_writer.add_summary(summary, step)

		"""
		if sim_score > similarity:
			N = tf.random_normal((npop,6), stddev = sigma)
		R = tf.zeros(npop)
		for j in range(npop):
		w_try = w + sigma*N[j]
		R[j] = f(w_try)
		A = (R - np.mean(R)) / np.std(R)
		w = w + learning_rate/(npop*sigma) * np.dot(N.T, A)
		"""

		if step % 100 == 0:
			print "Iteration= {:.1f}".format(step)+", similarity Score= {:.6f}".format(sim_score)

		step += 1


	print "optimization Done !!"