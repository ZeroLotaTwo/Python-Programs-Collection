from random import randint
from time import time
from typing import Iterable, Any
from sys import maxsize
# class List:
#     def __init__(self):
#         self.heap = []
#     def __getitem__(self, index):
#         return self.heap[index]
#     def __setitem__(self, index, value):
#         self.heap[index] = value
#     def __repr__(self):
#         string = "["
#         for index in range(len(self.heap) - 1):
#             string += f"{self.heap[index]}, "
#         if len(self.heap) > 0:
#             string += f"{self.heap[len(self.heap) - 1]}]"
#         else:
#             string += "]"
#         return string
#     def __str__(self):
#         string = "["
#         for index in range(len(self.heap) - 1):
#             string += f"{self.heap[index]}, "
#         if len(self.heap) > 0:
#             string += f"{self.heap[len(self.heap) - 1]}]"
#         else:
#             string += "]"
#         return string
#     def __delitem__(self, index: int):
#         del self.heap[index]
#     def append(self, item: Any):
#         return self.heap.append(item)
#     def sort(self):
#         return self.heap.sort()
#     def clear(self):
#         return self.heap.clear()
#     def pop(self, index:  int = -1):
#         return self.heap.pop(index)
#     def reverse(self):
#         return self.heap.reverse()
#     def extend(self, iterable: Iterable):
#         return self.heap.extend(iterable)
#     def copy(self):
#         '''Returns a shallow copy of the list.
#         meaning it will not copy a list that is inside of this.
#         '''
#         return self.heap.copy()
#     def count(self, value: Any):
#         return self.heap.count(value)
#     def set(self, lst: list):
#         self.heap = lst
#     def index(self, value: Any, start: int, stop: int = maxsize):
#         return self.heap(value, start, stop)
#     def count(self, value: Any):

def swap(idx1, idx2, arr):
    temp = arr[idx1]
    arr[idx1] = arr[idx2]
    arr[idx2] = temp

def comparision(item1, item2):
    """Right now this will max it a max heap"""
    if item1 < item2:
        return True
    else:
        return False

def giveCompIdx(idx1, idx2, arr):
    if comparision(arr[idx1], arr[idx2]):
        return idx1
    elif arr[idx1] == arr[idx2]:
        return idx1
    else: 
        return idx2
    
class Heap:
    def __init__(self, lst = None):
        self.heap = []
        if lst:
            self.heap = lst[:]
            self.__heapify(lst)

    def __len__(self):
        return len(self.heap)

    # I should not allow you to do this, because you can easily break the structure
    # def __getitem__(self, index):
    #     return self.heap[index]
    
    # def __setitem__(self, index):
    #     return self.heap[index]
    
    def __repr__(self):
        """Returns a string of the raw heap."""
        string = "["
        for index in range(len(self.heap) - 1):
            string += f"{self.heap[index]}, "
        if len(self.heap) > 0:
            string += f"{self.heap[len(self.heap) - 1]}]"
        else:
            string += "]"
        return string
    
    def __str__(self):
        """Returns a string of the raw heap."""
        string = "["
        for index in range(len(self.heap) - 1):
            string += f"{self.heap[index]}, "
        if len(self.heap) > 0:
            string += f"{self.heap[len(self.heap) - 1]}]"
        else:
            string += "]"
        return string
    # Same reason as above was commented
    # def __delitem__(self, index: int):
    #     del self.heap[index]

    def __heapify(self, lst) -> None:
        """(Changes the given list) Makes a list into a heap structure. If I remember correctly O(N), but actaully not sure."""
        self.heap = lst
        for i in range(len(self.heap) - 1, -1, -1):
            self.__bubbleDown(i)

    def __bubbleUp(self, index) -> None:
        """Takes a node and index. Then it bubbles up in the heap to be the either greater than prev elements or less than."""
        parent = (index - 1) // 2
        if index >= len(self.heap) or parent < 0:
            return
        while parent >= 0:
            if comparision(self.heap[index], self.heap[parent]):
                swap(index, parent, self.heap)
            index = parent
            parent = (index - 1) // 2

    def __bubbleDown(self, index = 0):
        """ This will is mostly used on the root to pop the min or max of the heap, but I think it will work on other indexes as well.
            This bubbles stuff from said index till either all elements above are either greater than or smaller than.
            Which one is decided on what type of heap your using.
        """
        leftChild = index * 2 + 1
        while leftChild < len(self.heap):
            compIdx = leftChild
            if leftChild + 1 < len(self.heap):
                compIdx = giveCompIdx(leftChild, leftChild + 1, self.heap)
            if comparision(self.heap[compIdx], self.heap[index]):
                swap(compIdx, index, self.heap)
            else:
                break
            index = compIdx
            leftChild = index * 2 + 1

    def add(self, item: Any) -> None:
        """Adds any item to the heap."""
        self.heap.append(item)
        self.__bubbleUp(len(self.heap) - 1)

    def getSortedList(self):
        """returns a shallow copy of the array sorted"""
        return sorted(self.heap)
    
    def clear(self):
        return self.heap.clear()
    
    def pop(self):
        """Pops the Max or Min from the heap then returns it."""
        ret = self.lookAtMax()
        if len(self.heap) == 0:
            return ret
        temp = self.heap.pop()
        if len(self.heap) > 1:
            self.heap[0] = temp
            self.__bubbleDown()
        return ret

    def extend(self, iterable: Iterable) -> None:
        """
        Adds items from and iterable structure to the heap.
        You can use this for heapifying a list but this does take O(N Lg(N)) time.
        """
        for item in iterable:
            self.add(item)
        return None
    
    def copy(self):
        '''Returns a shallow copy of the list.
        meaning it will not copy a list that is inside of this.
        '''
        return self.heap.copy()
    
    def set(self, lst: list):
        """Makes a copy of your list, then sets it to the heap then heapifys it."""
        self.__heapify(lst)

    def index(self, value: Any, start: int = 0, stop: int = maxsize):
        """Looks to see if an item is in the heap. Lower indexed items not guarenteed to show up before higher indexed items."""
        return self.heap(value, start, stop)
    
    def count(self, value: Any):
        """Counts how many times the any item/value appears in the heap"""
        return self.heap.count(value)
    
    def lookAtTop(self):
        """Returns the max/min of the heap."""
        if len(self.heap) == 0:
            return None
        else:
            return self.heap[0]

lst = []        
maxNum = 10000
for i in range(maxNum):
    lst.append(randint(1,maxNum * 10))
test = Heap(lst)
print(test.getSortedList())
print(test.lookAtMax())