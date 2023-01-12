from collections import deque
import copy
import signal

#Eric Chen
#This Python code works best if run on Apple/Mac
#This code should output a file called "output.txt"

def signal_handler(signum, frame): #timeout function for if searching takes too long
    raise Exception("Timed out!")

def heurestic(state, g1, g2): #heurestic funtion
    return abs(state.jugone - g1) + abs(state.jugtwo - g2)

def getG(state): #get cost from inital state to current node
    cost = 0
    curr = state
    while (curr != None):
        if (curr.getAction() != ""):
            cost += 1
        curr = curr.parent
    return cost

class State: #node
    def __init__(self, jugone, jugtwo ):
        self.jugone = jugone
        self.jugtwo = jugtwo
        self.sucessor = None #node's child
        self.parent = None #node's parent
        self.action = "" #action that resulted in this node
        self.h = None #heurestic
        self.g = None #node's cost from inital state to itself

    def getPair(self):
        pair = (self.jugone, self.jugtwo)
        return pair

    def getAction(self):
        return self.action

    def getH(self):
        return self.h

def goalTest(state, g1, g2): #test state to see it is goal node
    if state.jugone == g1 and state.jugtwo == g2:
        return True
    else:
        return False

def getF(state): #get f(n) = g(n) + h(n)
    cost = getG(state)
    #curr = state
    #while (curr != None):
        #if (curr.getAction() != ""):
            #cost += 1
        #curr = curr.parent
    return cost + state.h

def getNode(state, queue): #search list to see if node exist in that list. Return it if found, else return "0"
    for i in queue:
        if state.jugone == i.jugone and state.jugtwo == i.jugtwo and state.action == i.action:
            return i
    return "0"

def reorderList(queue): #Reorder the list based on f(n)
    newqueue = []
    while queue:
        minimum = queue[0]
        for x in queue:
            if getF(x) < getF(minimum):
                minimum = x
        newqueue.append(minimum)
        queue.remove(minimum)
    return newqueue

def pourOneToTwo(state, g1, g2): #pours jug 1 to jug 2
    if state.jugone > 0 and state.jugtwo < 2:
        dump = min(state.jugone, 2-state.jugtwo)
        state.jugone -= dump
        state.jugtwo += dump
        state.action = "Pour1"
        state.h = heurestic(state, g1, g2)
        return state
    else: #if jug 2 is full or jug 1 has no water
        return "0"


def pourTwoToOne(state, g1, g2): #pours jug 2 to jug 1
    if state.jugone < 5 and state.jugtwo > 0:
        dump = min(state.jugtwo, 5-state.jugone)
        state.jugone += dump
        state.jugtwo -= dump
        state.action = "Pour2"
        state.h = heurestic(state, g1, g2)
        return state
    else: #if jug 1 is full or jug 2 has no water
        return "0"

def dumpOne(state, g1, g2): #dump jug 1
    if state.jugone > 0:
        state.jugone = 0
        state.action = "Dump1"
        state.h = heurestic(state, g1, g2)
        return state
    else: #if jug 1 has no water
        return "0"

def dumpTwo(state, g1, g2): #dump jug 2
    if state.jugtwo > 0:
        state.jugtwo = 0
        state.action = "Dump2"
        state.h = heurestic(state, g1, g2)
        return state
    else: #if jug 2 has no water
        return "0"


def BFS(j1, j2, g1, g2): #Breath First Search
    f.write("Inital State: (%d , %d)\n" % (j1, j2))
    f.write("Goal State: (%d , %d)\n" % (g1, g2))
    f.write("Seaching strategy: BFS\n")
    head = State(j1,j2)
    queue = []
    visited = [] #track visited nodes
    queue.append(head) #take out inital node
    while(len(queue) != 0):
        if len(queue) == 0:
            f.write("BFS Failed\n")
            return 0
        node = queue.pop(0) #take out node from front of list to possibly expand
        if goalTest(node, g1, g2) == True: #check if current node is a goal node, f.write results
            nodes = []
            actions = []
            cost = 0
            curr = node
            while(curr != None):
                nodes.insert(0, curr.getPair())
                if(curr.getAction() != ""):
                    actions.insert(0, curr.getAction())
                    cost += 1
                curr = curr.parent
            f.write("Path:")
            for i in nodes:
                f.write("(%d, %d)" % (i[0], i[1]))
            f.write("\n")
            f.write("Action:")
            for i in actions:
                f.write("%s " % i)
            f.write("\n")
            f.write("Cost: %d" % cost)
            f.write("\n")
            return node
        if getNode(node, visited) == "0": #expand node if it is not visted. Check each action if it is possible and add resulting state to queue and tree if so.
            node1 = dumpOne(copy.deepcopy(node), g1, g2) #check if dump jug 1 is possible
            if node1 != "0":
                queue.append(node1)
                node.sucessor = node1 #set node's child
                node1.parent = node #set child node's parent
            node2 = dumpTwo(copy.deepcopy(node), g1, g2) #check if dump jug 2 is possible
            if node2 != "0":
                queue.append(node2)
                node.sucessor = node2
                node2.parent = node
            node3 = pourOneToTwo(copy.deepcopy(node), g1, g2) #check if pour 1 to 2 is possible
            if node3 != "0":
                queue.append(node3)
                node.sucessor = node3
                node3.parent = node
            node4 = pourTwoToOne(copy.deepcopy(node), g1, g2) #check if pour 2 to 1 is possible
            if node4 != "0":
                queue.append(node4)
                node.sucessor = node4
                node4.parent = node
        visited.append(node) #add node to list of already visited nodes
    f.write("BFS Failed\n") #if all possible nodes are search and queue is empty


def DFS(j1, j2, g1, g2): #Depth First Search
    f.write("Inital State: (%d , %d)\n" % (j1, j2))
    f.write("Goal State: (%d , %d)\n" % (g1, g2))
    f.write("Seaching strategy: DFS\n")
    head = State(j1,j2)
    stack = []
    stack.append(head)
    while(len(stack) != 0):
        if len(stack) == 0:
            f.write("DFS Failed\n")
            return 0
        node = stack.pop() #take out node from top of stack to possibly expand
        if goalTest(node, g1, g2) == True: #check if current node is a goal node, f.write results
            nodes = []
            actions = []
            cost = 0
            curr = node
            while (curr != None):
                nodes.insert(0, curr.getPair())
                if (curr.getAction() != ""):
                    actions.insert(0, curr.getAction())
                    cost += 1
                curr = curr.parent
            f.write("Path:")
            for i in nodes:
                f.write("(%d, %d)" % (i[0], i[1]))
            f.write("\n")
            f.write("Action:")
            for i in actions:
                f.write("%s " % i)
            f.write("\n")
            f.write("Cost: %d" % cost)
            f.write("\n")
            return node
        node1 = pourOneToTwo(copy.deepcopy(node), g1, g2) #check if pour 1 to 2 is possible
        if node1 != "0":
            stack.append(node1)
            node.sucessor = node1
            node1.parent = node
        node2 = pourTwoToOne(copy.deepcopy(node), g1, g2) #check if pour 2 to 1 is possible
        if node2 != "0":
            stack.append(node2)
            node.sucessor = node2
            node2.parent = node
        node3 = dumpOne(copy.deepcopy(node), g1, g2) #check if dump jug 1 is possible
        if node3 != "0":
            stack.append(node3)
            node.sucessor = node3
            node3.parent = node
        node4 = dumpTwo(copy.deepcopy(node), g1, g2) #check if dump jug 2 is possible
        if node4 != "0":
            stack.append(node4)
            node.sucessor = node4
            node4.parent = node
    f.write("DFS Failed\n") #if all possible nodes are search and queue is empty


def AStar(j1, j2, g1, g2): #A Star Search
    f.write("Inital State: (%d , %d)\n" % (j1, j2))
    f.write("Goal State: (%d , %d)\n" % (g1, g2))
    f.write("Seaching strategy: A *\n")
    head = State(j1, j2)
    head.h = heurestic(head, g1, g2) #calcuate heurestic
    queue = []
    visited = []
    queue.append(head)
    while (len(queue) != 0):
        if len(queue) == 0:
            f.write("A Star Search Failed\n")
            return 0
        node = queue.pop(0) #take out node from front of list to possibly expand
        if goalTest(node, g1, g2) == True:
            nodes = []
            actions = []
            cost = 0
            curr = node
            while (curr != None):
                nodes.insert(0, curr.getPair())
                if (curr.getAction() != ""):
                    actions.insert(0, curr.getAction())
                    cost += 1
                curr = curr.parent
            f.write("Path:")
            for i in nodes:
                f.write("(%d, %d)" % (i[0], i[1]))
            f.write("\n")
            f.write("Action:")
            for i in actions:
                f.write("%s " % i)
            f.write("\n")
            f.write("Cost: %d" % cost)
            f.write("\n")
            return node
        if getNode(node, visited) == "0":
            node1 = dumpOne(copy.deepcopy(node), g1, g2)
            if node1 != "0":
                node1.parent = node
                if getNode(node1, queue) == "0": #if node doesn't already exists on the tree or queue
                    queue.append(node1) # add new node to queue and reorder queue based on f(n)
                    queue = reorderList(queue)
                    node.sucessor = node1
                    node1.parent = node
                    node1.g = getG(node1)
                else: #if new node already exists on tree or queue, update's pointers, g(n), and reorder the list
                    # f.write("We have ", getG(node1), getNode(node1, queue).g, "for", node1.getPair())
                    if getG(node1) < getNode(node1, queue).g:
                        getNode(node1, queue).g = getG(node1)
                        getNode(node1, queue).parent = node
                        node.sucessor = getNode(node1, queue)
                        queue = reorderList(queue)
            node2 = dumpTwo(copy.deepcopy(node), g1, g2)
            if node2 != "0":
                node2.parent = node
                if getNode(node2, queue) == "0":
                    queue.append(node2) # add new node to queue and reorder queue based on f(n)
                    queue = reorderList(queue)
                    node.sucessor = node2
                    node2.parent = node
                    node2.g = getG(node2)
                else:
                    # f.write("We have ", getG(node2), getNode(node2, queue).g, "for", node2.getPair())
                    if getG(node2) < getNode(node2, queue).g:
                        getNode(node2, queue).g = getG(node2)
                        getNode(node2, queue).parent = node
                        node.sucessor = getNode(node2, queue)
                        queue = reorderList(queue)
            node3 = pourOneToTwo(copy.deepcopy(node), g1, g2)
            if node3 != "0":
                node3.parent = node
                if getNode(node3, queue) == "0":
                    queue.append(node3)  # add new node to queue and reorder queue based on f(n)
                    queue = reorderList(queue)
                    node.sucessor = node3
                    node3.parent = node
                    node3.g = getG(node3)
                else:
                    # f.write("We have ", getG(node3), getNode(node3, queue).g, "for", node3.getPair())
                    if getG(node3) < getNode(node3, queue).g:
                        getNode(node3, queue).g = getG(node3)
                        getNode(node3, queue).parent = node
                        node.sucessor = getNode(node3, queue)
                        queue = reorderList(queue)
            node4 = pourTwoToOne(copy.deepcopy(node), g1, g2)
            if node4 != "0":
                node4.parent = node
                if getNode(node4, queue) == "0":
                    queue.append(node4)  # add new node to queue and reorder queue based on f(n)
                    queue = reorderList(queue)
                    node.sucessor = node4
                    node4.parent = node
                    node4.g = getG(node4)
                else:
                    # f.write("We have", getG(node4), getNode(node4, queue).g, "for", node4.getPair())
                    if getG(node4) < getNode(node4, queue).g:
                        getNode(node4, queue).g = getG(node4)
                        getNode(node4, queue).parent = node
                        node.sucessor = getNode(node4, queue)
                        queue = reorderList(queue)
        visited.append(node)
    f.write("A Star Search Failed\n")






if __name__ == "__main__":
    with open('output.txt', 'w') as f:
        BFS(4, 1, 0, 1)
        f.write("\n")
        BFS(4, 1, 4, 0)
        f.write("\n")
        BFS(4, 1, 5, 0)
        f.write("\n")
        BFS(4, 1, 3, 2)
        f.write("\n")
        BFS(4, 1, 1, 2)
        f.write("\n")
        signal.signal(signal.SIGALRM, signal_handler) #timeout function if DFS ends up going into the wrong branch
        signal.alarm(2)
        try:
            DFS(4, 1, 0, 1)
            f.write("\n")
        except Exception as msg:
            f.write("DFS taking too long to find to find (0, 1)\n")
            f.write("\n")
        signal.alarm(1)
        try:
            DFS(4, 1, 4, 0)
            f.write("\n")
        except Exception as msg:
            f.write("DFS taking too long to find (4, 0)\n")
            f.write("\n")
        signal.alarm(2)
        try:
            DFS(4, 1, 5, 0)
            f.write("\n")
        except Exception as msg:
            f.write("DFS taking too long to find (5, 0)\n")
            f.write("\n")
        signal.alarm(2)
        try:
            DFS(4, 1, 3, 2)
            f.write("\n")
        except Exception as msg:
            f.write("DFS taking too long to find (3, 2)\n")
            f.write("\n")
        signal.alarm(2)
        try:
            DFS(4, 1, 1, 2)
            f.write("\n")
        except Exception as msg:
            f.write("DFS taking too long to find (1, 2)\n")
            f.write("\n")
        signal.alarm(2)
        AStar(4, 1, 0, 1)
        f.write("\n")
        AStar(4, 1, 4, 0)
        f.write("\n")
        AStar(4, 1, 5, 0)
        f.write("\n")
        AStar(4, 1, 3, 2)
        f.write("\n")
        AStar(4, 1, 1, 2)
        f.write("\n")
    f.close()
