def merge_lists_scan(list1, list2):
    merged_list = []
    a = 0  # current index for list1
    b = 0  # current index for list2

    while a < len(list1) or b < len(list2):
        if b >= len(list2):
            while a < len(list1):
                merged_list.append(list1[a])
                a += 1
        elif a >= len(list1):
            while b < len(list2):
                merged_list.append(list2[b])
                b += 1
        elif list1[a] <= list2[b]:
            merged_list.append(list1[a])
            a += 1
        elif list1[a] > list2[b]:
            merged_list.append(list2[b])
            b += 1

    return merged_list

'''
def merge_lists_pop(list1, list2):
    merged_list = []
    listA = list1.copy()
    listB = list2.copy()

    while len(listA) > 0 or len(listB) > 0:
        if len(listB) == 0:
            while len(listA) > 0:
                merged_list.append(listA.pop(0))
        elif len(listA) == 0:
            while len(listB) > 0:
                merged_list.append(listB.pop(0))
        elif listA[0] <= listB[0]:
            merged_list.append(listA.pop(0))
        elif listA[0] > listB[0]:
            merged_list.append(listB.pop(0))

    return merged_list
'''

def merge_lists_py(list1, list2):
    merged_list = sorted(list1 + list2)

    return merged_list


def merge_lists_cake(my_list, alices_list):

    # set up our merged_list
    merged_list_size = len(my_list) + len(alices_list)
    merged_list = [None] * merged_list_size

    current_index_alices = 0
    current_index_mine = 0
    current_index_merged = 0

    while current_index_merged < merged_list_size:

        is_my_list_exhausted = current_index_mine >= len(my_list)
        is_alices_list_exhausted = current_index_alices >= len(alices_list)

        # case: next comes from my list
        # my list must not be exhausted, and EITHER:
        # 1) Alice's list IS exhausted, or
        # 2) the current element in my list is less
        #    than the current element in Alice's list
        if not is_my_list_exhausted and \
            (is_alices_list_exhausted or
             (my_list[current_index_mine] <
              alices_list[current_index_alices])):

            merged_list[current_index_merged] = my_list[current_index_mine]
            current_index_mine += 1

        # case: next comes from Alice's list
        else:
            merged_list[current_index_merged] = \
                alices_list[current_index_alices]
            current_index_alices += 1

        current_index_merged += 1

    return merged_list