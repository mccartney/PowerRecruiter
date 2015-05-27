import sys

#from power_recruiter.image_comparator.neural_network import network, \
#    get_input_image

from neural_network_FAST import network, \
    get_input_image


def is_same_person(path1, path2):
    input_image = get_input_image(path1, path2)
    score_one = network.activate(input_image)
    print >> sys.stderr,"SCORE 1"
    print >> sys.stderr,score_one[0]
    print >> sys.stderr,score_one[1]
    input_image = get_input_image(path2, path1)
    score_two = network.activate(input_image)
    print >> sys.stderr,"SCORE 2"
    print >> sys.stderr,score_two[0]
    print >> sys.stderr,score_two[1]
    return max(score_one[0], score_two[0]) > max(score_two[1], score_two[1]) #and score_two[0] > score_two[1]
