from power_recruiter.image_comparator.neural_network import network, \
    get_input_image


def is_same_person(path1, path2):
    input_image = get_input_image(path1, path2)
    score_one = network.activate(input_image)
    input_image = get_input_image(path2, path1)
    score_two = network.activate(input_image)
    return score_one[0] >= 0.55 and score_two[0] >= 0.55
