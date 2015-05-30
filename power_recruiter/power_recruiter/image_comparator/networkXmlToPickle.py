__author__ = 'shadowsword'
from pybrain.tools.xml.networkreader import NetworkReader
from pybrain.tools.xml.networkwriter import NetworkWriter
import pickle
import sys

# Version for modified Reader which loads data partially
#net = NetworkReader.readFrom(sys.argv[1], None, network=None)
#net = NetworkReader.readFrom(sys.argv[2], None, network=net)
net = NetworkReader.readFrom(sys.argv[1])
with open(sys.argv[2], 'wb') as f:
    pickle.dump(net, f, pickle.HIGHEST_PROTOCOL)
