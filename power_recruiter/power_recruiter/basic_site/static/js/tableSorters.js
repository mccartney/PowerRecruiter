function nameSorter(a, b) {
    if (a.candidateName > b.candidateName) return 1;
    if (a.candidateName < b.candidateName) return -1;
    return 0;
}

function stateSorter(a, b) {
    if (a.stateName > b.candidateName) return 1;
    if (a.candidateName < b.candidateName) return -1;
    return 0;
}