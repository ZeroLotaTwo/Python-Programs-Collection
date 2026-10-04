class BST:
    class Node:
        def __init__(self, num, parent = None):
            self.num = num
            self.height = 1
            self.parent = parent
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def getHeight(self, node: Node):
        if(node == None):
            return 0
        return node.height

    def calcNewHeight(self, node: Node):
        left = self.getHeight(node.left)
        right = self.getHeight(node.right)
        if left > right:
            return left + 1
        else: 
            return right + 1  

    def _balanceTree(self, unEvenNode: Node):
        a = unEvenNode
        b = None
        c = None
        avlCase = []
        left = self.getHeight(a.left)
        right = self.getHeight(a.right)
        if(left > right):
            b = a.left
            avlCase.append(0)
        else:
            b = a.right
            avlCase.append(1)
        left = self.getHeight(b.left)
        right = self.getHeight(b.right)
        if(left > right):
            c = b.left
            avlCase.append(0)
        else:
            c = b.right
            avlCase.append(1)
        #LR case first part
        if(avlCase[0] == 0 and avlCase[1] == 1):
            temp = c.left
            c.left = b
            b.right = temp
            if(temp != None):    
                temp.parent = b
            a.left = c
            c.parent = a
            b.parent = c
            # temp2 = b.height
            # b.height = c.height
            # c.height = temp2
            b.height = self.calcNewHeight(b)
            c.height = self.calcNewHeight(c)
            temp = b
            b = c
            c = temp
        #RL case first part
        if(avlCase[0] == 1 and avlCase[1] == 0):
            temp = c.right
            c.right = b
            b.left = temp
            if(temp != None):    
                temp.parent = b
            a.right = c
            c.parent = a
            b.parent = c
            # temp2 = b.height
            # b.height = c.height
            # c.height = temp2
            b.height = self.calcNewHeight(b)
            c.height = self.calcNewHeight(c)
            temp = b
            b = c
            c = temp
        #LL
        if(avlCase[0] == 0):
            b.parent = None
            a.parent = b
            temp = b.right  
            b.right = a
            a.left = temp
            if(temp != None):    
                temp.parent = a
            a.height = self.calcNewHeight(a)
        else:#RR
            b.parent = None
            a.parent = b
            temp = b.left
            b.left = a
            a.right = temp
            if(temp != None):    
                temp.parent = a
            a.height = self.calcNewHeight(a)
        return b


    def _addNum(self, num: int, node: Node):
        if(num == node.num):
            return
        elif(num > node.num):
            if(node.right == None):
                # print("parent", node.num, "child", num)
                node.right = self.Node(num, node)
            else:
                self._addNum(num, node.right)
                node.right.parent = node
        elif(num < node.num):
            if(node.left == None):
                # print("parent", node.num, "child", num)
                node.left = self.Node(num, node)
            else:
                self._addNum(num, node.left)
                node.left.parent = node
        left = self.getHeight(node.left)
        right = self.getHeight(node.right)
        node.height = self.calcNewHeight(node)
        if(abs(left - right) > 1):
            # print("Unbalanced Node", node.num)
            saveParent = node.parent
            # if(saveParent != None):
                # print("saved Parent", saveParent.num)
            ret = self._balanceTree(node)
            # I forgot to show them where their dad was
            ret.parent = saveParent
            if node == self.root:
                self.root = ret
            else:
                if(saveParent.num > ret.num):
                    saveParent.left = ret
                    # print("Went Left")
                else:
                    saveParent.right = ret
                    # print("Went Right")

    def addNum(self, num):
        if(self.root == None):
            self.root = self.Node(num)
            return 
        self._addNum(num, self.root)
    
    def _sortedArray(self, arr: list[int], node: Node) -> None:
        if node == None:
            return
        if(node.left != None):
            self._sortedArray(arr, node.left)
        arr.append(node.num)
        if(node.right != None):
            self._sortedArray(arr, node.right)

    def numInTree(self, num: int) -> None:
        node = self.root
        while(node != None):
            if(num > node.num):
                node = node.right
            elif(num < node.num):
                node = node.left
            else:
                return True
        return False
    
    def bstToList(self) -> list[int]:
        arr = []
        self._sortedArray(arr, self.root)
        return arr

    def clearBST(self) -> None:
        self.root = None
#tests to try and make this thing work
#[2, 5, 10, 11, 13, 15, 25, 29, 36, 38, 39, 41, 46, 50, 56, 58, 63, 66, 70, 71]
#[2, 5, 10, 11, 13, 15, 25, 29, 38, 39, 41, 46, 50, 56, 58, 63, 66, 70, 71]
test = BST()
arr = [1,2,3]
for num in arr:
    test.addNum(num)
print("done")
print(test.bstToList())
print(test.root.right.num)