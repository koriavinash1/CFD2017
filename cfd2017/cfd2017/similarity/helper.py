import tensorflow as tf
import numpy as np

def Conv2D(data,filters,kernel_size,name=None,strides=(1,1), activation=tf.nn.elu, train=True):
	initializer = tf.contrib.layers.variance_scaling_initializer(factor=2.0, 
		mode='FAN_IN', uniform=False, seed=None, dtype=tf.float32)
	output = tf.layers.conv2d(data,
			filters,
			kernel_size,
			strides=strides,
			padding='same',
			data_format='channels_last',
			activation=activation,
			kernel_initializer=initializer,
			trainable=train,
			name=name)
	return output

def SimilarityMatrix(base_tensor, case_tensor, name=None):
	similarity_score = tf.contrib.losses.mean_squared_error(
			    case_tensor,
			    labels=base_tensor,
				    weights=1.0,
			    scope=name
			)
	return similarity_score

def MaxPooling2D(data, name=None, pool_size=(2,2), strides=(2,2)):
	output = tf.layers.max_pooling2d(data,
			pool_size,
			strides,
			padding='valid',
			data_format='channels_last',
			name=name)
	return output

def BatchNormalization(data,name,training=False,activation=tf.nn.elu):
	output = tf.contrib.layers.batch_norm(data,
			decay=0.99,
			epsilon=0.001,
			is_training=training,
			activation_fn =activation,
			scope=name)
	return output

def ConclusionMatrix(similarity_array):
	thresh = 0.5
	if np.sum(similarity_array) > thresh*similarity_array.shape[0]: 
		return True
	else:
		return False

def DiceCriteria2Cls(base_tensor, case_tensor, chief_class = 1, smooth = 1.0):
	last_dim_idx = base_tensor.get_shape().ndims - 1
	# print last_dim_idx
	# num_class = tf.shape(base_tensor)[last_dim_idx]
	# print num_class
	# # predictions = tf.one_hot(tf.argmax(logits,last_dim_idx),num_class)
	# case_unrolled = tf.reshape(case_tensor,[-1,num_class])[:,chief_class]
	# base_unrolled = tf.reshape(base_tensor,[-1,num_class])[:,chief_class]
	intersection = tf.reduce_sum(case_tensor*base_tensor)
	ret_val = (2.0*intersection)/(tf.reduce_sum(case_tensor) + tf.reduce_sum(base_tensor) + smooth)
	return ret_val