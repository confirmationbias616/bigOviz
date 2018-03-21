
def itertools_algo10(list1):
    import itertools
    return [seq for i in range(len(list1), 0, -1) for
            seq in itertools.combinations(list1, i) if sum(seq) == 10]


def itertools_algo1000(list1):
    import itertools
    return [seq for i in range(len(list1), 0, -1) for
            seq in itertools.combinations(list1, i) if sum(seq) == 1000]


def subset_sum10(list1):
    target = 10
    partial = []

    def subset_sum(list1, target, partial=[]):
        s = sum(partial)
        if s >= target:
            return  # if we reach the number why bother to continue

    for i in range(len(list1)):
            n = list1[i]
            remaining = list1[i + 1:]
            subset_sum(remaining, target, partial + [n])


def subset_sum1000(list1):
    target = 1000
    partial = []

    def subset_sum(list1, target, partial=[]):
        s = sum(partial)
        if s >= target:
            return  # if we reach the number why bother to continue

    for i in range(len(list1)):
            n = list1[i]
            remaining = list1[i + 1:]
            subset_sum(remaining, target, partial + [n])
