__author__ = 'shadowsword'
from pybrain.tools.xml.networkreader import NetworkReader
import pickle
import sys

net = NetworkReader.readFrom(sys.argv[1])
with open(sys.argv[2], 'wb') as f:
    pickle.dump(net, f, pickle.HIGHEST_PROTOCOL)
