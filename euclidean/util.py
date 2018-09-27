from itertools import chain


def rolled(sequence, offset):
    return chain(sequence[offset:], sequence[:offset])
