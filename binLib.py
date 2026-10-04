# This works with lists. No strings allowed >:(
from Queue import Queue
def removeLeadingZeros(num: list[int]) -> bool:
    """There has to be at least one zero, because this returns a two's compliment number."""
    i = 0
    for i in range(len(num)):
        if num[i] == 1:
            break
    return num[i - 1:]

def isZero(num: list[int]) -> bool:
    for bit in num:
        if bit == 1:
            return False
    return True

def bitAbs(num: list[int]) -> bool:
    """Returns True if it flipped it to a positive number, but abs the bit in place"""
    if num[0] == 1:
        compliment(num)
        return True
    return False

def padOutNum(num: list[int], numBits: int) -> None:
    if numBits < len(num):
        return
    neg = int(num[0] == 1)
    oldLen = len(num)
    num.extend([neg for _ in range(numBits - len(num))])
    j = len(num) - 1
    for i in range(oldLen):
        num[j] = num[i]
        num[i] = neg
        j -= 1

def add(num1: list[int], num2: list[int]) -> list[int]:
    """Adds two binary numbers with two's compliment. So the binary number has to be in the form of two's compliment."""
    newNum = []
    if len(num2) > len(num1):
        temp = num1
        num1 = num2
        num2 = temp
    carry = 0
    num1Offset = len(num1) - 1
    for i in range(len(num2) - 1, -1, -1):
        num1Offset = len(num1) - len(num2) + i
        newNum.append((carry + num1[num1Offset] + num2[i]) & 1)
        carry = num1[num1Offset] & num2[i] or (num1[num1Offset] | num2[i]) & carry
        # print(num1[num1Offset])
    while(num1Offset > 0):
        num1Offset -= 1
        newNum.append((carry + num1[num1Offset] + num2[0]) & 1)
        carry = num1[num1Offset] & num2[0] or (num1[num1Offset] | num2[0]) & carry
    # if the number overflows
    if (num1[0] == num2[0]) & (newNum[len(newNum) - 1] != num1[0]):
        newNum.append(num1[0])
    return newNum[::-1]

def sub(num1: list[int], num2: list[int]) -> list[int]:
    """Returns num1 - num2. All this is just a sub interface, it compliments num2 then adds."""
    num2 = num2[:]
    compliment(num2)
    return add(num1, num2)

def compliment(num: list[int], start = 0, end = None) -> None:
    """Does the 2's compliment of the binary number in place. Keeps the same magnitude"""
    if end == None:
        end = len(num) - 1
    for i in range(start, end + 1):
        num[i] ^= 1
    carry = 1
    i = end
    while carry:
        temp = num[i]
        num[i] = (num[i] + carry) & 1
        carry = temp & carry
        i -= 1

def mul(num1: list[int], num2: list[int]) -> list[int]:
    """Only use with two's compliment numbers"""
    # Below is not needed, but I think it might make it run a little faster
    if len(num2) > len(num1):
        temp = num1
        num1 = num2
        num2 = temp
    if isZero(num1) or isZero(num2):
        return [0,0]
    neg = 0
    neg ^= bitAbs(num1)
    neg ^= bitAbs(num2)
    # Starts working of the multiplicatoin
    newNum = [0 for _ in range(2 * len(num1) + len(num2))]
    startDigitIdx = 1
    carry = 0
    for i in range(len(num2) - 1, -1, -1):
        # This is the offset for where the multiplication and summation will be placed
        mulIdx = len(newNum) - startDigitIdx
        for j in range(len(num1) - 1, -1, -1):
            temp = newNum[mulIdx]
            # print(temp)
            newNum[mulIdx] = (num1[j] * num2[i] + newNum[mulIdx] + carry) & 1
            carry = ((num1[j] * num2[i]) and temp) or ((num1[j] * num2[i] | temp) and carry)
            tempIdx = mulIdx
            mulIdx -= 1
            while carry and tempIdx > 0 :
                tempIdx -= 1
                # print("MULIDX: ",tempIdx)
                temp = newNum[tempIdx]
                newNum[tempIdx] = (newNum[tempIdx] + carry) & 1
                carry = temp & carry
        # print(newNum)
        startDigitIdx += 1

    newNum = removeLeadingZeros(newNum)
    if neg:
        compliment(newNum)
    return newNum


def gte(num1: list[int], num2: list[int]) -> bool:
    """Greater than or equal to. Does exactly num1 >= num2"""
    for i in range(len(num1)):
        if num1[i] == 1:
            break
    num1 = num1[i:]
    if len(num1) > len(num2):
        return True
    elif len(num1) < len(num2):
        return False

    length = min(len(num1), len(num2))
    for i in range(length):
        if num1[i] > num2[i]:
            return True
        elif num1[i] < num2[i]:
            return False
    return True


def div(num1: list[int], num2: list[int]) -> list[int]:
    """This uses integer division"""
    newNum = []
    neg = 0
    neg ^= bitAbs(num1)
    neg ^= bitAbs(num2)
    num1 = num1[1:]
    num2 = num2[1:]
    start = 0
    if isZero(num2):
        raise ZeroDivisionError("YOU CAN'T DIVIDE BY 0 DUMMY!!!")
    if isZero(num1):
        return [0]

    #Starts to acctually divide here
    for i in range(len(num1)):
        bit = 0
        if i - start + 1 >= len(num2):
            if gte(num1[start: i + 1], num2):
                bit = 1
                num2SubIdx =  len(num2) - 1
                num1SubIdx = i
                carry = 0
                while 0 <= num2SubIdx:
                    temp = num1[num1SubIdx]
                    num1[num1SubIdx] = (num1[num1SubIdx] - num2[num2SubIdx]) & 1
                    carry = int(temp < num2[num2SubIdx])
                    carryIdx = num1SubIdx - 1
                    while carry:
                        temp = num1[carryIdx]
                        num1[carryIdx] = (num1[carryIdx] - carry) & 1
                        carry = carry ^ temp
                        carryIdx -= 1
                    num1SubIdx -= 1
                    num2SubIdx -= 1
        newNum.append(bit)
    newNum = removeLeadingZeros(newNum)
    #If the number should be negative, flips it to a negative number.
    if neg:
        compliment(newNum)
    return newNum

def numToSignedBi(num: int):
    """Converts a python int into a two's compliment number"""
    newNum = []
    negBool = num < 0
    num = abs(num)
    while num > 0:
        newNum.append(num & 1)
        num >>= 1
    newNum.append(0)
    newNum = newNum[::-1]
    if negBool:
        compliment(newNum)
    return newNum

def printDecimal(num: list[int]) -> None:
    num = num[:]
    numToPrint = 0
    neg = bitAbs(num)
    mult = 1
    for bit in num[::-1]:
        numToPrint += bit * mult
        mult *= 2
    if neg:
        print(numToPrint * -1)
    else:
        print(numToPrint)

def rotateRight(num: list[int], shiftAmt: int):
    savedNums = shiftAmt % len(num)
    if savedNums == 0:
        return
    pastNums = Queue(len(num))
    for i in range(len(num) - savedNums,  len(num)):
        pastNums.enqueue(num[i])
    for i in range(len(num)):
        if i <= len(num) - savedNums - 1:
            pastNums.enqueue(num[i])
        num[i] = pastNums.dequeue()

def rotateLeft(num: list[int], shiftAmt: int):
    savedNums = shiftAmt % len(num)
    if savedNums == 0:
        return
    pastNums = Queue(len(num))
    for i in range(savedNums,  len(num)):
        pastNums.enqueue(num[i])
    for i in range(len(num)):
        if i <= savedNums - 1:
            pastNums.enqueue(num[i])
        num[i] = pastNums.dequeue()

def bitShiftRight(num: list[int], shiftAmt: int):
    if shiftAmt > len(num):
        shiftAmt = len(num)
    swapIdx = len(num) - 1 - shiftAmt
    for i in range(len(num) - 1, shiftAmt - 1, -1):
        temp = num[swapIdx]
        num[swapIdx] = num[i]
        num[i] = temp
        swapIdx -= 1
    for i in range(shiftAmt):
        num[i] = 0

def bitShiftLeft(num: list[int], shiftAmt: int):
    if shiftAmt > len(num):
        shiftAmt = len(num)
    swapIdx = shiftAmt
    for i in range(len(num) - shiftAmt):
        print(i, swapIdx)
        temp = num[swapIdx]
        num[swapIdx] = num[i]
        num[i] = temp
        swapIdx += 1
    for i in range(len(num) - shiftAmt, len(num)):
        num[i] = 0

# def unSignedadd(num1: list[int], num2: list[int]) -> list[int]:
#     """Adds two binary numbers with two's compliment. So the binary number has to be in the form of two's compliment."""
#     newNum = []
#     if len(num2) > len(num1):
#         temp = num1
#         num1 = num2
#         num2 = temp
#     carry = 0
#     num1Offset = len(num1) - 1
#     for i in range(len(num2) - 1, -1, -1):
#         num1Offset = len(num1) - len(num2) + i
#         newNum.append((carry + num1[num1Offset] + num2[i]) & 1)
#         carry = num1[num1Offset] & num2[i] or (num1[num1Offset] | num2[i]) & carry
#         # print(num1[num1Offset])
#     while(num1Offset > 0):
#         num1Offset -= 1
#         newNum.append((carry + num1[num1Offset]) & 1)
#         carry = num1[num1Offset] & carry
#     if carry:
#         newNum.append(1)
#     return newNum[::-1]

# Test if multiplication actually works
# for i in range(1001):
#     for j in range(1001):
#         num1 = numToSignedBi(i)
#         num2 = numToSignedBi(j)
#         multi = mul(num1,num2)
#         if isZero(multi):
#             multi = [0]
#         if multi != numToSignedBi(i * j):
#             print(i,"*",j)
#             print(num1)
#             print(num2)
#             print(multi)
#             print(numToSignedBi(i*j))
#             print("broken")
#             break
print("done")
num1 = [0,1,0,1,0]
printDecimal(num1)
num2 = [0,1,1,1,1,1]
printDecimal(num2)
mult = mul(num1, num2)
print(mult)
printDecimal(mult)
