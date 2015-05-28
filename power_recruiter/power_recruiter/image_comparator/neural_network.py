"""Neural network module.

If `SAVE_FILE_NAME` does not exists, running the script will generate it.
"""

import os
import sys
import logging
import gc
from pybrain import LinearLayer, FullConnection
from pybrain import TanhLayer, SigmoidLayer, SoftmaxLayer
import cv2
import time
from pybrain.datasets import SupervisedDataSet
from arac.pybrainbridge import _FeedForwardNetwork
from pybrain.tools.xml.networkwriter import NetworkWriter
import pickle

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from PIL import Image
import numpy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


IMG_WIDTH = 60
IMG_HEIGHT = 60

NUMBER_OF_IMAGES = 2

#Convolutions should be odd numbers
FIRST_CONVOLUTION_FILTER = 5
SECOND_CONVOLUTION_FILTER = 7
MERGE_FILTER = 5
CONVOLUTION_MULTIPLIER = 2

#Allowed number of pair with one person, usefull for huge datasets
SAME_PERSON = 80

# Number of pairs with same person
NUM_PHOTO_PAIRS_SAME = int(sys.argv[1])#100
LEARNING_RATE = float(sys.argv[2])

# Number of pairs with not same person
NUM_PHOTO_PAIRS_NOT_SAME = NUM_PHOTO_PAIRS_SAME

# Number of pairs of photos
NUM_PHOTO_PAIRS = NUM_PHOTO_PAIRS_SAME + NUM_PHOTO_PAIRS_NOT_SAME

# Number of trainings
NUM_EPOCHS = 15

SAVE_FILE_NAME = os.path.join(__location__, 'network.bin')

PHOTOS_ROOT_DIR = "lfw/"

CV_CASCADE = cv2.CascadeClassifier("cascade.xml")

def _convert_to_black_and_white(im):
    return im.convert('L')


def _adjust_size(im):
    width, height = im.size
    if width > height:
        new_height = IMG_HEIGHT
        new_width = new_height * width / height
    else:
        new_width = IMG_WIDTH
        new_height = new_width * height / width
    return im.resize((new_width, new_height), Image.ANTIALIAS)


def _crop_center(im, left=None, top=None, box_side=None):
    width, height = im.size
    if not box_side:
        box_side = min(im.size)
    if not left:
        left = (width - box_side) / 2
    if not top:
        top = (height - box_side) / 2

    crop_box = (left, top, left + box_side, top + box_side)
    return im.crop(crop_box)


def _prepare_image(path):
    image_cv = cv2.imread(path)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    faces = CV_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.4,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    im = Image.open(path)
    if len(faces) > 0:
        x, y, w, h = faces[0]
        im = _crop_center(im, x, y, min(w, h))
    else:
        im = _crop_center(im)

    im = _adjust_size(im)
    im = _convert_to_black_and_white(im)
    #im.show()
    #time.sleep(0.6)
    return im.getdata()


def _save_network_to_file(net):
    logger.info("Saving network...")
    with open(SAVE_FILE_NAME, 'wb') as f:
        #pickle.dump(net, f, pickle.HIGHEST_PROTOCOL)
        NetworkWriter.writeToFile(net, SAVE_FILE_NAME)
    logger.info("Done saving")


def _load_network_from_file():
    logger.info("Loading network...")
    with open(SAVE_FILE_NAME, 'rb') as f:
        net = pickle.load(f)
	logger.info("ConvertingToFastNetwork")
	net = net.convertToFastNetwork()
    gc.collect()
    logger.info("Done loading")
    return net

def _add_convolutional_connection(
        net,
        h1,
        h2,
        filter_size,
        multiplier,
        input_width,
        input_height,
        output_width,
        output_height,
        offset_x,
        offset_y,
        size_x,
        size_y
):
    #print("filter_size: %d, output_width: %d, output_height: %d" % (filter_size, output_width, output_height))
    #print("offset_x: %d, size_x: %d, offset_y: %d, size_y: %d" % (offset_x, size_x, offset_y, size_y))
    for x in xrange(offset_x, offset_x + size_x):
        for y in xrange(offset_y, offset_y + size_y):
            for s in xrange(filter_size):
                for z1 in xrange(multiplier):
                    for z2 in xrange(multiplier):
                        #print("x: %d, y: %d,: s:%d, z1:%d, z2:%d" % (x, y, s, z1, z2))
                        start = x + ((y + s) * input_width)
                        end = start + filter_size
                        target_x = (x + z1 * size_x * NUMBER_OF_IMAGES)
                        target_y = y * output_width + z2 * size_y * output_width
                        target = target_x + target_y
                        #print("adding from %d to %d inside %d" % (start, end, target))
                        net.addConnection(FullConnection(
                            h1,
                            h2,
                            inSliceFrom=start,
                            inSliceTo=end,
                            outSliceFrom=target,
                            outSliceTo=target + 1
                        ))

def _add_pool_connection(
    net,
    h1,
    h2,
    input_width,
    input_height,
):
    for x in xrange(input_width):
        for y in xrange(input_height):
            h1_pos = x + y * input_width
            h2_pos = x/2 + (y/2) * (input_width / 2)
            net.addConnection(FullConnection(
                h1,
                h2,
                inSliceFrom= h1_pos,
                inSliceTo=h1_pos + 1,
                outSliceFrom=h2_pos,
                outSliceTo=h2_pos + 1
            ))

def _merge_connection(
    net,
    h1,
    h2,
    filter_size,
    input_width,
    input_height,
    output_width,
    output_height
):
    #print("input_width: %d, input_height: %d, output_width: %d, ouput_height: %d" % (input_width, input_height, output_width, output_height))
    for x in xrange(output_width):
        for y in xrange(output_height):
            for z1 in xrange(CONVOLUTION_MULTIPLIER * CONVOLUTION_MULTIPLIER * NUMBER_OF_IMAGES):
                for z2 in xrange(CONVOLUTION_MULTIPLIER * CONVOLUTION_MULTIPLIER):
                    for s in xrange(filter_size):
                        h1_pos = x + (y + s) * input_width + z1 * output_width + z2 * input_width * output_height
                        h2_pos = x + y * output_width
                        #print("x: %d, y: %d, h1_pos: %d, h2_pos: %d" % (x, y, h1_pos, h2_pos))
                        net.addConnection(FullConnection(
                            h1,
                            h2,
                            inSliceFrom=h1_pos,
                            inSliceTo=h1_pos + s + 1,
                            outSliceFrom=h2_pos,
                            outSliceTo=h2_pos + 1
                        ))



def _build_network():
    logger.info("Building network...")

    net = _FeedForwardNetwork(bias=True)
    inp = LinearLayer(IMG_WIDTH * IMG_HEIGHT * 2)
    h1_image_width = IMG_WIDTH - FIRST_CONVOLUTION_FILTER + 1
    h1_image_height = IMG_HEIGHT - FIRST_CONVOLUTION_FILTER + 1
    h1_full_width = h1_image_width * CONVOLUTION_MULTIPLIER * NUMBER_OF_IMAGES
    h1_full_height = h1_image_height * CONVOLUTION_MULTIPLIER
    h1 = SigmoidLayer(h1_full_width * h1_full_height)

    h2_width = h1_full_width / 2
    h2_height = h1_full_height / 2
    h2 = LinearLayer(h2_width * h2_height)

    h3_image_width = h2_width / CONVOLUTION_MULTIPLIER / NUMBER_OF_IMAGES - SECOND_CONVOLUTION_FILTER + 1
    h3_image_height = h2_height / CONVOLUTION_MULTIPLIER - SECOND_CONVOLUTION_FILTER + 1
    h3_full_width = h3_image_width * (CONVOLUTION_MULTIPLIER * 2) * NUMBER_OF_IMAGES
    h3_full_height = h3_image_height * (CONVOLUTION_MULTIPLIER * 2)
    h3 = SigmoidLayer(h3_full_width * h3_full_height)

    h4_full_width = h3_image_width - MERGE_FILTER
    h4_full_height = h3_image_height - MERGE_FILTER
    h4 = SigmoidLayer(h4_full_width * h4_full_height)

    logger.info("BASE IMG: %d x %d" % (IMG_WIDTH, IMG_HEIGHT))
    logger.info("First layer IMG: %d x %d" % (h1_image_width, h1_image_height))
    logger.info("First layer FULL: %d x %d" % (h1_full_width, h1_full_height))
    logger.info("Second layer FULL: %d x %d" % (h2_width, h2_height))
    logger.info("Third layer IMG: %d x %d" % (h3_image_width, h3_image_height))
    logger.info("Third layer FULL: %d x %d" % (h3_full_width, h3_full_height))
    logger.info("Forth layer FULL: %d x %d" % (h3_image_width, h3_image_height))
    outp = SoftmaxLayer(2)

    h5 = SigmoidLayer(h4_full_width * h4_full_height)

    # add modules
    net.addOutputModule(outp)
    net.addInputModule(inp)
    net.addModule(h1)
    net.addModule(h2)
    net.addModule(h3)
    net.addModule(h4)
    net.addModule(h5)

    # create connections

    for i in range(NUMBER_OF_IMAGES):
        _add_convolutional_connection(
            net=net,
            h1=inp,
            h2=h1,
            filter_size=FIRST_CONVOLUTION_FILTER,
            multiplier=CONVOLUTION_MULTIPLIER,
            input_width=IMG_WIDTH * 2,
            input_height=IMG_HEIGHT,
            output_width=h1_full_width,
            output_height=h1_full_height,
            offset_x=h1_image_width * i,
            offset_y=0,
            size_x=h1_image_width,
            size_y=h1_image_height
        )

    _add_pool_connection(
        net=net,
        h1=h1,
        h2=h2,
        input_width=h1_full_width,
        input_height=h1_full_height
    )

    for i in range(NUMBER_OF_IMAGES * CONVOLUTION_MULTIPLIER):
        for j in range(CONVOLUTION_MULTIPLIER):
            _add_convolutional_connection(
                net=net,
                h1=h2,
                h2=h3,
                filter_size=SECOND_CONVOLUTION_FILTER,
                multiplier=CONVOLUTION_MULTIPLIER,
                input_width=h2_width,
                input_height=h2_height,
                output_width=h3_full_width,
                output_height=h3_full_height,
                offset_x=h3_image_width * i,
                offset_y=h3_image_height * j,
                size_x=h3_image_width,
                size_y=h3_image_height
            )

    _merge_connection(
        net=net,
        h1=h3,
        h2=h4,
        filter_size=MERGE_FILTER,
        input_width=h3_full_width,
        input_height=h3_full_height,
        output_width=h4_full_width,
        output_height=h4_full_height
    )

    net.addConnection(FullConnection(h4, h5))
    net.addConnection(FullConnection(h5, outp))

    # finish up
    net.sortModules()
    logger.info("Done building network")
    return net


def _run_training(net, data_set):
    logger.info("Running training...")
    data_set_training, data_set_test = data_set.splitWithProportion(0.9)
    rate=LEARNING_RATE
    trainer = BackpropTrainer(net, data_set_training, learningrate=rate)
    for epoch in xrange(NUM_EPOCHS):
        logger.info("Calculating EPOCH %d", epoch)
        logger.info("Result on training set %f", trainer.train())
        if epoch % 10 == 0:
            logger.info("Result on test set %f", trainer.testOnData(data_set_test, verbose=True))
	if epoch % 4 == 3:
	    rate /= 10
	    trainer = BackpropTrainer(net, data_set_training, learningrate=rate)

def _add_images_to_dataset(path1, path2, data_set, value):
    input_image = get_input_image(path1, path2)
    data_set.addSample(input_image, value)


def _add_photos(data_set):
    # pylint: disable=W0612
    first_photos_from_dir = []
    pairs = 0

    # pylint: disable=W0612
    for subdir, dirs, files in os.walk(PHOTOS_ROOT_DIR):
        if files and subdir:
            first_photos_from_dir.append(os.path.join(subdir, files[0]))

    current_dir_num = 0
    for subdir, dirs, files in os.walk(PHOTOS_ROOT_DIR):
        current_dir_num += 1
        if len(files) <= 2:
            if len(files) > 0:
                pairs += 1
	        logger.info("same:" + files[0] + " " + files[0])
                _add_images_to_dataset(
                    os.path.join(subdir, files[0]),
                    os.path.join(subdir, files[0]),
                    data_set,
                    [1,0]
                )
            
                logger.info("other:"+ first_photos_from_dir[current_dir_num + 1] + " " + files[0])
                _add_images_to_dataset(
                    first_photos_from_dir[current_dir_num + 1],
                    os.path.join(subdir, files[0]),
                    data_set,
                    [0,1]
                )

	else:
            num = 0
            for i in xrange(min(len(files), 10) - 1):
                for j in xrange(min(len(files), 10) - 1):
                    if i < j:
                        num = num + 1
                        pairs += 2
                    
       		        logger.info("same:" + files[i] + " " + files[j])
                        _add_images_to_dataset(
                            os.path.join(subdir, files[i]),
                            os.path.join(subdir, files[j]),
                            data_set,
                            [1,0]
                        )


		        logger.info("same:" + files[j] + " " + files[i])
                        _add_images_to_dataset(
                            os.path.join(subdir, files[j]),
                            os.path.join(subdir, files[i]),
                            data_set,
                            [1,0]
                        )

                        logger.info("other:"+ first_photos_from_dir[current_dir_num + i + j + 1] + " " + files[i])
                        _add_images_to_dataset(
                            first_photos_from_dir[current_dir_num + i + j + 1],
                            os.path.join(subdir, files[i]),
                            data_set,
                            [0,1]
                        )

                        logger.info("other:"+files[j] + " " + first_photos_from_dir[current_dir_num + i + j + 2])
                        _add_images_to_dataset(
                            os.path.join(subdir, files[j]),
                            first_photos_from_dir[current_dir_num + i + j + 2],
                            data_set,
                            [0,1]
                        )

            if pairs >= NUM_PHOTO_PAIRS_SAME:
                return
            if num > SAME_PERSON:
                break
        logger.info("NUM: " + str(pairs))

def _create_dataset():
    logger.info("Creating empty dataset...")
    data_set = SupervisedDataSet(IMG_WIDTH * IMG_HEIGHT * 2, 2)
    logger.info("Add photos to dataset...")
    _add_photos(data_set)
    logger.info("Done creating")
    return data_set


def _generate_new_network():
    data_set = _create_dataset()
    net = _build_network()
    _run_training(net, data_set)
    _save_network_to_file(net)
    return net


def _get_network():
    if os.path.isfile(SAVE_FILE_NAME):
        logger.info("Saved file present")
        return _load_network_from_file()
    else:
        logger.info("No saved file present, generating...")
    	return _generate_new_network()


def get_input_image(path1, path2):
    first_image = _prepare_image(path1)
    second_image = _prepare_image(path2)
    return numpy.concatenate((first_image, second_image), axis=0).flat


network = _get_network()
