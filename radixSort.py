test = [5,3,6,7,1]

def radixSort(arr: list) -> None:
    mask = 1
    bucket = [0 for i in range(len(test))]
    for _ in range(5):
        left = 0
        right = len(bucket) - 1
        for num in test:
            if num & mask:
                bucket[right] = num
                right = right - 1
            else:
                bucket[left] = num
                left = left + 1
        print(left, right)
        # At this point, left and right will be at the same index, at the pivit point
        for i in range(left):
            test[i] = bucket[i]
        for i in range(len(bucket) - 1, right, -1):
            testIdx = left + (len(bucket) - 1 - i)
            test[testIdx] = bucket[i]
        mask <<= 1
        print(test, bucket)
radixSort(test)
print(test)
