from power_recruiter.image_comparator.neural_network import network, \
    get_input_image


def is_same_person(path1, path2):
    input_image = get_input_image(path1, path2)
    score = network.activate(input_image)
    return score[0] >= 0.5
