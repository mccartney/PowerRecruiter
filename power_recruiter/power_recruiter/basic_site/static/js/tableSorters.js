function idSorter(a, b) {
    if (a.id > b.id) return 1;
    if (a.id < b.id) return -1;
    return 0;
}

function nameSorter(a, b) {
    if (a.candidate_name > b.candidate_name) return 1;
    if (a.candidate_name < b.candidate_name) return -1;
    return 0;
}

function stateSorter(a, b) {
    if (a.state_name > b.state_name) return 1;
    if (a.state_name < b.state_name) return -1;
    return 0;
}