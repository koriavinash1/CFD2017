from rest_framework.response import Response
from rest_framework.decorators import api_view
import numpy as np
import tensorflow as tf
from helper import Conv2D, SimilarityMatrix, MaxPooling2D, ConclusionMatrix,\
		BatchNormalization, DiceCriteria2Cls
import cv2

image_array = ['base.jpg', 'base1.jpg', 'base3.jpg', 'case1.jpg', 'case2.jpg', 'check.jpg', 'check1.jpg', 'check2.jpg', 'ck.jpg', 'ck2.jpg']
base_path = "/home/koriavinash/Desktop/cfd2017/img/"

@api_view(['POST'])
def similarity_score(requests):
	(user, inputDict, getParams) = (requests.user,requests.data,requests.GET)
	bool_array = np.array(inputDict['img_array'], dtype=bool)
	base, check = np.where(bool_array)[0][0], np.where(bool_array)[0][1]

	base_image = cv2.imread(base_path+image_array[base], 0)
	check_image = cv2.imread(base_path+image_array[check], 0)
	
	print base_path+image_array[base]
	score = get_score(base=base_image, check= check_image)

	sign_status = "Mis-Match"
	if(score >= 0.55): sign_status = "Matched"

	return Response({'status':True, 'score':score, 'sign_stat': sign_status, 'text': 'Similarity checked'})

def get_score(base, check):
	check_image = check
	base_image = base

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


	# transform_matrix = [tf.cos(theta), tf.sin(theta), 0,\
	# 			-tf.sin(theta), tf.cos(theta), 0,\
	# 			0, 0,1]
	# # network filter simila
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
				if sim_score < 0.55: return sim_score

			step += 1


		print "optimization Done !!"

	return sim_score