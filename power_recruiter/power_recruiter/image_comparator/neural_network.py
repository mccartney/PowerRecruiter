"""Neural network module.

If `SAVE_FILE_NAME` does not exists, running the script will generate it.
"""

import os
import pickle
import logging

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


# 250px x 250px
IMG_WIDTH = 250
IMG_HEIGHT = 250

# We compare two faces
IMG_NUM = 2

# Number of input values
NUM_INPUT_UNITS = IMG_WIDTH * IMG_HEIGHT * IMG_NUM

# Hidden units of network
NUM_HIDDEN_UNITS_1 = 90

# Hidden units of network
NUM_HIDDEN_UNITS_2 = 45

# Hidden units of network
NUM_HIDDEN_UNITS_3 = 30

# Number of pairs with same person
NUM_PHOTO_PAIRS_SAME = 500

# Number of pairs with not same person
NUM_PHOTO_PAIRS_NOT_SAME = 500

# Number of pairs of photos
NUM_PHOTO_PAIRS = NUM_PHOTO_PAIRS_SAME + NUM_PHOTO_PAIRS_NOT_SAME

# Number of trainings
NUM_EPOCHS = 200

SAVE_FILE_NAME = os.path.join(__location__, 'network.bin')

PHOTOS_ROOT_DIR = "lfw/"


def _open_image_as_bw(path):
    return Image.open(path).convert('L').getdata()


def _save_network_to_file(net):
    logger.info("Saving network...")
    with open(SAVE_FILE_NAME, 'wb') as f:
        pickle.dump(net, f, pickle.HIGHEST_PROTOCOL)
    logger.info("Done saving")


def _load_network_from_file():
    logger.info("Loading network...")
    with open(SAVE_FILE_NAME, 'rb') as f:
        net = pickle.load(f)
    # Hack to make pickling work with PyBrain
    # see: http://stackoverflow.com/a/4336001
    net.sorted = False
    net.sortModules()
    logger.info("Done loading")
    return net


def _build_network():
    logger.info("Building network...")
    net = buildNetwork(
        NUM_INPUT_UNITS,
        NUM_HIDDEN_UNITS_1,
        NUM_HIDDEN_UNITS_2,
        NUM_HIDDEN_UNITS_3,
        1
    )
    logger.info("Done building network")
    return net


def _run_training(net, data_set):
    logger.info("Running training...")
    # Should we train on 0.1 of the data only?
    data_set_training, _ = data_set.splitWithProportion(0.1)
    trainer = BackpropTrainer(net, data_set_training)
    for epoch in xrange(NUM_EPOCHS):
        logger.info("Calculating EPOCH %d", epoch)
        logger.info("Result on training set %f", trainer.train())


def _add_images_to_dataset(path1, path2, data_set, value):
    input_image = get_input_image(path1, path2)
    data_set.addSample(input_image, value)


def _add_same_photos(data_set):
    pairs = 0
    # pylint: disable=W0612
    for subdir, dirs, files in os.walk(PHOTOS_ROOT_DIR):
        if len(files) <= 2:
            continue
        for i in xrange(len(files)/2):
            _add_images_to_dataset(
                os.path.join(subdir, files[i]),
                os.path.join(subdir, files[i + 1]),
                data_set,
                1
            )
            pairs += 1
            if pairs >= NUM_PHOTO_PAIRS_SAME:
                return


def _add_not_same_photos(data_set):
    first_photos_from_dir = []

    # pylint: disable=W0612
    for subdir, dirs, files in os.walk(PHOTOS_ROOT_DIR):
        if files:
            first_photos_from_dir.append(os.path.join(subdir, files[0]))

    for i in xrange(NUM_PHOTO_PAIRS_NOT_SAME):
        _add_images_to_dataset(
            first_photos_from_dir[i],
            first_photos_from_dir[i + 1],
            data_set,
            0
        )


def _create_dataset():
    logger.info("Creating empty dataset...")
    data_set = SupervisedDataSet(NUM_INPUT_UNITS, 1)
    _add_same_photos(data_set)
    _add_not_same_photos(data_set)
    logger.info("Done creating")
    return data_set


def _generate_new_network():
    data_set = _create_dataset()
    net = _build_network()
    _run_training(net, data_set)
    _save_network_to_file(net)
    return network


def _get_network():
    if os.path.isfile(SAVE_FILE_NAME):
        logger.info("Saved file present")
        return _load_network_from_file()
    else:
        logger.info("No saved file present, generating...")
        return _generate_new_network()


def get_input_image(path1, path2):
    first_image = _open_image_as_bw(path1)
    second_image = _open_image_as_bw(path2)
    return numpy.concatenate((first_image, second_image), axis=0).flat


network = _get_network()
