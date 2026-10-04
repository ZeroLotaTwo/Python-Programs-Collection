from typing import TypeVar
from math import sqrt

#For raising not same dimension error
class lenError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

#used for type hinting the Vector class
Vector = TypeVar('Vector', bound='Vector') 

class Vector:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], list):#if the user passes a list, heavily used inside the class
            args = args[0]
        self.dim = len(args)
        self.vector = [num for num in args]

    def __len__(self) -> int:
        return self.dim
    
    def __getitem__(self, index):
        return self.vector[index]
    
    def __setitem__(self, index, value):
        self.vector[index] = value
    # this can do dot product of vectors then returns a number or makes a new vector with the scaler
    # this is why it does not have a type hint, because it can return two values
    def __mul__(self, other):
        if isinstance(other, Vector):
            if self.dim == other.dim:
                sum = 0
                for i in range(len(self)):
                    sum += self[i] * other[i]
                return sum
            else:
                raise lenError("The vectors are not the same length.")
        elif isinstance(other, (int, float)):
            newVector = []
            for num in self:
                newVector.append(num * other)
            return Vector(newVector)
        else:
            raise TypeError("Unsupported operand type for multiplication")
        
    def __add__(self, other) -> Vector:
        if isinstance(other, Vector):
            if self.dim == other.dim:
                newVector = []
                for i in range(len(self)):
                    newVector.append(self[i] + other[i])
                return Vector(newVector)
            else:
                raise lenError("The vectors are not the same length.")
        else:
            raise TypeError("Unsupported operand type for addition")
        
    def __str__(self):
        return f"{self.vector}"
    
    # def __repr___(self):
    #     return f"Vector({self.vector})"
    
    def norm(self) -> float:
        """returns the length of the vector"""
        sum = 0
        for num in self:
            sum += num * num
        return sqrt(sum)
    


from math import pi, sin, sqrt
from random import uniform, randint

tests = 10000000
distance = 0
print("working")
for _ in range(tests):
    angle = uniform(0, pi/2)
    h = sin(angle)
    b = sqrt(1 - h * h)
    baseVector = Vector(b,h)
    n = randint(1, 100)
    for __ in range(n):
        angle = uniform(0, pi/2)
        h = sin(angle)
        b = sqrt(1 - h * h)
        baseVector += Vector(b, h)
    distance += baseVector.norm() / n

print(distance/tests)
print("done")