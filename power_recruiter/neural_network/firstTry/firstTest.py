from sklearn.datasets import fetch_lfw_pairs
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import SoftmaxLayer
from pybrain.supervised.trainers import BackpropTrainer

NUM_EPOCHS = 50
NUM_INPUT_UNITS = 250*250
NUM_HIDDEN_UNITS = 25

# Load data set
print "Loading image set"
data_set = fetch_lfw_pairs(subset='train')
print "Images loaded"

print "Building %d x %d x %d neural network..." % (NUM_INPUT_UNITS, NUM_HIDDEN_UNITS, 2)
network = buildNetwork(NUM_INPUT_UNITS, NUM_HIDDEN_UNITS, 2, bias=True, outclass=SoftmaxLayer)
print network

print "preparing trainer"
trainer = BackpropTrainer(network, data_set)
print "runing trainer"