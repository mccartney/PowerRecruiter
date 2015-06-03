from power_recruiter.image_comparator.neural_network import network, get_input_image


def is_same_person(path1, path2):
    input_image, pre_results = get_input_image(path1, path2)
    if pre_results:
        return True
    score_one = network.network.activate(input_image)
    #print >> sys.stderr,"SCORE 1"
    #print >> sys.stderr,score_one[0]
    #print >> sys.stderr,score_one[1]
    return score_one[0] > score_one[1]
