class Node:
    def __init__(self, data=None) -> None:
        self.data = data
        self.next = None
    
class LinkedList:
    def __init__(self) -> None:
        self.head = None
    
    def newNode(self, data):
        new = Node(data)
        self.cur.next = new
        