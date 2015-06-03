from pybrain.tools.xml.networkreader import NetworkReader
import pickle
import sys

# Version for modified Reader which loads data partially
#net = NetworkReader.readFrom(sys.argv[1], None, netwowrk=None)
#net = NetworkReader.readFrom(sys.argv[2], None, network=net)
net = NetworkReader.readFrom(sys.argv[1])
with open(sys.argv[2], 'wb') as f:
    pickle.dump(net, f, pickle.HIGHEST_PROTOCOL)
