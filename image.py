import os
import tensorflow as tf
import tensorflow_hub as hub
# Load compressed models from tensorflow_hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# import IPython.display as display

import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['figure.figsize'] = (12,12)
mpl.rcParams['axes.grid'] = False

import numpy as np
import PIL.Image
import time
import functools

def tensor_to_image(tensor):
	tensor = tensor*255
	tensor = np.array(tensor, dtype=np.uint8)
	if np.ndim(tensor)>3:
		assert tensor.shape[0] == 1
		tensor = tensor[0]
	# return tensor
	return PIL.Image.fromarray(tensor)

# content_path = tf.keras.utils.get_file('YellowLabradorLooking_new.jpg', 'https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg')
# style_path = tf.keras.utils.get_file('kandinsky5.jpg','https://storage.googleapis.com/download.tensorflow.org/example_images/Vassily_Kandinsky%2C_1913_-_Composition_7.jpg')


def load_img(path_to_img):
	max_dim = 512
	img = tf.io.read_file(path_to_img)
	img = tf.image.decode_image(img, channels=3)
	img = tf.image.convert_image_dtype(img, tf.float32)

	shape = tf.cast(tf.shape(img)[:-1], tf.float32)
	long_dim = max(shape)
	scale = max_dim / long_dim

	new_shape = tf.cast(shape * scale, tf.int32)

	img = tf.image.resize(img, new_shape)
	img = img[tf.newaxis, :]
	return img

def imshow(image, title=None):
	if len(image.shape) > 3:
		image = tf.squeeze(image, axis=0)
	plt.imshow(image)
	if title:
		plt.title(title)

def showpic(img):
	plt.imshow(img)
	plt.axis('off')
	plt.show()

def Transfer(path1, path2):
	img = plt.imread(path1).astype(np.float32)[np.newaxis, ...] / 255.
	img2 = plt.imread(path2).astype(np.float32)[np.newaxis, ...] / 255.
	img2 = tf.image.resize(img2, (256, 256))
	
	# content_image = load_img(content_path)
	# style_image = load_img(style_path)
	# plt.subplot(1, 3, 1)
	# imshow(content_image, 'Content Image')
	# plt.subplot(1, 3, 2)
	# imshow(style_image, 'Style Image')
	# hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
	# stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
	# plt.subplot(1, 3, 3)
	# plt.imshow(tensor_to_image(stylized_image))
	
	hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
	stylized_image = hub_model(tf.constant(img), tf.constant(img2))[0]
	return tensor_to_image(stylized_image)
	# plt.imshow(tensor_to_image(stylized_image))
	# plt.axis('off')
	# fig = plt.gcf()
	# plt.title('Stylized Image')

	# plt.show()
if __name__ == "__main__":
	img = Transfer(os.path.join("pic", "pic9.jpg"), os.path.join("pic", "pic10.jpg"))
	img.save(os.paht.join("pic", "stylized_image.jpg"))