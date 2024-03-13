from random import shuffle


def selection_sort(array):
    n = len(array)
    for x in range(n):
        min_index = x
        for y in range(x, n):
            if min_index:
                if array[y] < array[min_index]:
                    min_index = y
            else:
                min_index = y
        hold = array[x]
        array[x] = array[min_index]
        array[min_index] = hold
    return array


def sort_check(array):
    for x in range(len(array) - 1):
        if array[x] > array[x+1]:
            return False
    return True


def insertion_sort(array):
    n = len(array)
    for x in range(n-1, 0, -1):
        for y in range(x, 0, -1):
            if array[y-1] > array[y]:
                hold = array[y]
                array[y] = array[y-1]
                array[y-1] = hold
    return array


def shell_sort(array, mode='s'):
    n = len(array)
    h = 0

    # uses knuth's increment
    while h < n//3 and mode == 'k':
        h = 3*h + 1

    # uses sedgewick's increment
    while h < n//3 and mode == 's':
        h = (pow(4, n+1)+3*pow(2, n)+1)
    while h >= 1:
        for x in range(h, n):
            y = x
            while y >= h:
                if array[y] < array[y-h]:
                    temp = array[y-h]
                    array[y-h] = array[y]
                    array[y] = temp
                y -= h
        h = h//3
    return array


def merge_sort(array):
    length = len(array)
    if length <= 1:
        return
    midpoint = length//2
    left_side = array[:midpoint]
    right_side = array[midpoint:]
    merge_sort(left_side)
    merge_sort(right_side)
    left_length, right_length = len(left_side), len(right_side)
    i = j = k = 0
    while True:
        if i < left_length and j < right_length:
            if left_side[i] < right_side[j]:
                array[k] = left_side[i]
                i += 1
            elif left_side[i] > right_side[j]:
                array[k] = right_side[j]
                j += 1
            else:
                array[k] = right_side[j]
                j += 1
            k += 1
        elif i < left_length:
            array[k] = left_side[i]
            i += 1
            k += 1
        elif j < right_length:
            array[k] = right_side[j]
            j += 1
            k += 1
        else:
            break
    return array


def qsort(array, lo=0, hi=0, call=False):
    def sort(work, low, high):
        i = low + 1
        j = high
        while True:
            while work[i] <= work[low]:
                if i == high:
                    break
                else:
                    i += 1
            while work[j] >= work[low]:
                if j == low:
                    break
                else:
                    j -= 1
            if i >= j:
                break
            hold = work[j]
            work[j] = work[i]
            work[i] = hold
        hold = work[low]
        work[low] = work[j]
        work[j] = hold
        return j
    if not call:
        call = True
        shuffle(array)
        hi = len(array) - 1
    if hi <= lo:
        return
    j = sort(array, lo, hi)
    qsort(array, lo, j-1, True)
    qsort(array, j+1, hi, True)
    return array


def quick_sort(array, low=0, high=0, call=False):
    if not call:
        high = len(array) - 1
        shuffle(array)
    if high <= low:
        return
    lt, gt = low, high
    i = low
    key = array[low]
    while i <= gt:
        if array[i] < key:
            array[lt], array[i] = array[i], array[lt]
            lt += 1
            i += 1
        elif array[i] > key:
            array[i], array[gt] = array[gt], array[i]
            gt -= 1
        else:
            i += 1
    quick_sort(array, low, lt-1, True)
    quick_sort(array, gt+1, high, True)
    return array


def topological_sort(graph, mode=False):
    marked = [False for _ in range(graph.v)]
    reverse_post = []

    def dfs(v):
        marked[v] = True
        for w in graph.adj_to(v):
            if mode:
                try:
                    w = w.other(v)
                except AttributeError:
                    w = w.end()
            if not marked[w]:
                dfs(w)
        reverse_post.append(v)

    for vertix in range(graph.v):
        if not marked[vertix]:
            dfs(vertix)

    reverse_post.reverse()
    return reverse_post

