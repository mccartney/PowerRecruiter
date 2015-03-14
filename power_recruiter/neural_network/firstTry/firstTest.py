from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from PIL import Image
import numpy
import os

#250px x 250px
IMG_WIDTH = 250
IMG_HEIGHT = 250

#We compare two faces
IMG_NUM = 2

#Number of input values
NUM_INPUT_UNITS = IMG_WIDTH * IMG_HEIGHT * IMG_NUM

#Hidden units of network
NUM_HIDDEN_UNITS_1 = 90

#Hidden units of network
NUM_HIDDEN_UNITS_2 = 45

#Hidden units of network
NUM_HIDDEN_UNITS_3 = 30

#Number of pairs with same person
NUM_PHOTO_PAIRS_SAME = 500

#Number of pairs with not same person
NUM_PHOTO_PAIRS_NOT_SAME = 500

#Number of pairs of photos
NUM_PHOTO_PAIRS = NUM_PHOTO_PAIRS_SAME + NUM_PHOTO_PAIRS_NOT_SAME

#Number of trainings
NUM_EPOCHS = 200

#Notes:
#EPOCH takes 40s with HIDDEN_UNITS=75, NUM_PHOTO_PAIRS=550

def add_images_to_dataset(path1, path2, data_set, value):
    first_image = Image.open(path1).convert('L').getdata()
    second_image = Image.open(path2).convert('L').getdata()
    input_image = numpy.concatenate((first_image,second_image), axis=0).flat
    data_set.addSample(input_image, value)


def create_dataset():
    #Creating empty dataset
    data_set = SupervisedDataSet(NUM_INPUT_UNITS, 1)
    root_dir = "../lfw/";
    pairs = 0

    for subdir, dirs, files in os.walk(root_dir):
        if len(files) > 2:
            for i in xrange(len(files)/2):
                add_images_to_dataset(os.path.join(subdir, files[i]), os.path.join(subdir, files[i + 1]), data_set, 1)
                pairs += 1
                if pairs >= NUM_PHOTO_PAIRS_SAME:
                    break

        if pairs >= NUM_PHOTO_PAIRS_SAME:
                    break

    first_photos_from_dir = []

    for subdir, dirs, files in os.walk(root_dir):
        if len(files) > 0:
            first_photos_from_dir.append(os.path.join(subdir, files[0]))

    pairs = 0
    for i in xrange(NUM_PHOTO_PAIRS_NOT_SAME):
        add_images_to_dataset(first_photos_from_dir[i], first_photos_from_dir[i + 1], data_set, 0)
        if pairs >= NUM_PHOTO_PAIRS_NOT_SAME:
            break

    return data_set

def build_network():
    network = buildNetwork(NUM_INPUT_UNITS, NUM_HIDDEN_UNITS_1, NUM_HIDDEN_UNITS_2, NUM_HIDDEN_UNITS_3, 1)
    return network

def run_training():
    #Creating trainer
    data_set_training, data_set_test = data_set.splitWithProportion(0.1)
    trainer = BackpropTrainer(network, data_set_training)
    for epoch in xrange(NUM_EPOCHS):
        print "Calculating EPOCH %d" % epoch
        print "Result on training set %f" % trainer.train()
        if epoch % 10 == 9:
            print "Result on real set %f" % trainer.testOnData(data_set_test)

#THE FUN STARTS HERE

print "Creating dataset"
data_set = create_dataset()

print "Creating network"
network = build_network()

print "Running training"
run_training()

print "[Success]"