function nameSorter(a, b) {
    if (a.candidateName > b.candidateName) return 1;
    if (a.candidateName < b.candidateName) return -1;
    return 0;
}