var ConflictModalContent = function (data) {
    this.name = data[0][0]['candidate_name']['candidate_name'];
    this.images = new ConflictingPair(
        data[0][0]['photo']['photo'] || GHOST_PIC,
        data[0][1]['photo']['photo'] || GHOST_PIC);
    this.states = new ConflictingPair(
        data[0][0]['state']['raw_state_name'],
        data[0][1]['state']['raw_state_name']);
    this.ids = new ConflictingPair(
        data[0][0]['id']['id'],
        data[0][1]['id']['id']);
    this.linkedin = new ConflictingPair(
        data[0][0]['contact']['linkedin'],
        data[0][1]['contact']['linkedin']);
    this.goldenline = new ConflictingPair(
        data[0][0]['contact']['goldenline'],
        data[0][1]['contact']['goldenline']);
    this.email = new ConflictingPair(
        data[0][0]['contact']['email'],
        data[0][1]['contact']['email']);
};