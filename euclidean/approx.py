from sortedcontainers import SortedSet
from collections.abc import Iterable, Set


def approx(a, b, atol=1e-6):
    try:
        return abs(a - b) <= atol
    except TypeError:
        return False


class ApproxSet(Set):
    def __init__(self, values, approx_fcn=approx):
        self.__impl = SortedSet(values)
        self.__approx = approx_fcn

    def __len__(self):
        return len(self.__impl)

    def __iter__(self):
        return iter(self.__impl)

    def __eq__(self, other):
        if isinstance(other, ApproxSet):
            return self.__equals(other.__impl)
        if isinstance(other, Set):
            return self.__equals(other)
        if isinstance(other, Iterable):
            return self.__equals(SortedSet(other))
        return NotImplemented

    def __equals(self, sequence):
        if len(self) != len(sequence):
            return False
        sequence = sequence if isinstance(sequence, SortedSet) else SortedSet(sequence)
        return all(self.__approx(a, b) for a, b in zip(self.__impl, sequence))

    def __contains__(self, item):
        """Does the set contain an item that is approximately equal to ``item``.

        Args:
            item:

        Returns:

        """
        idx = self.__impl.bisect_right(item)
        return self.__test_index(idx, item) or self.__test_index(idx - 1, item)

    def __test_index(self, index, item):
        try:
            return self.__approx(self.__impl[index], item)
        except IndexError:
            return False
