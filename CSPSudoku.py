#Eric Chen
#CMSC 471 Assigment 2
#implementation of AC3 inspired by http://aima.cs.berkeley.edu/python/csp.html
#implementation of backtracking inspired by https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/

# How to run this code
# 1.) Begin running the code
# 2.) You will asked to enter an 81 char string
# 3.) Enter that string
# 4.) Code will convert the string into a 9x9 puzzle and try to solve it
# 5.) Code will tell you if it can be solve and output a solved puzzle if so

class Sudoku:
    def __init__(self, puzzle):
        self.puzzle = [] #create a 9x9 array
        j = 0
        row = [] #row for the 9x9 array
        r = 0 #row
        c = 0 #column
        for i in range(81): #convert string into 9x9 array by adding each char
            if puzzle[i].isnumeric(): #insert number
                row.append([int(puzzle[i]), [1,2,3,4,5,6,7,8,9], [r, c]]) #each element in 9x9 array is the vaule, the domain, and the row/column postion.
                c += 1 #track colum
            else: #insert 0 if char is is "."
                row.append([0, [1,2,3,4,5,6,7,8,9], [r, c]])
                c += 1
            j += 1 #track number of elements in row
            if j == 9: #if row has 9 element, put it into puzzle
                self.puzzle.append(row)
                j = 0 #reset number of elements in row
                c = 0 #reset column
                r += 1 #track row
                row = [] #reset row


    def printPuzzle(self): #print out the assigned vaules of the puzzle
        print("Current Sudoku")
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                print(self.puzzle[i][j][0], end=" ")
            print()
        print("_________________________________")

#Backtracking Search

def get_empty(puzzle): #find the next empty cell in puzzle starting from the top left
    for i in range(0, 9):
        for j in range(0, 9):
            if puzzle[i][j][0] == 0: #0 indicates empty or unassinged cell
                return i, j
    return False


def backtrackingsolve(puzzle):
    if get_empty(puzzle) == False:  # end search if puzzle has no empty cells
        return True
    else:
        row, col = get_empty(puzzle)  # get next empty cell
        for i in puzzle[row][col][1]:  # check each vaule in the cell's domain to see if it is or is not allowed
            if backtrackingvalid(puzzle, i, (row, col)):
                puzzle[row][col][0] = i  # if vaule is allowed, assigned it

                if backtrackingsolve(puzzle): #recursive call
                    return True

                puzzle[row][col][0] = 0  # if assigned vaule does not solve the puzzle, set it back to 0 or empty
        return False


def backtrackingvalid(puzzle, num, positon): #checks every connected cell to see if possible vaule that is num is allowed
    for j in range(0, 9): #check every cell in col
        if puzzle[positon[0]][j][0] == num:
            return False

    for i in range(0, 9): #check every cell in row
        if puzzle[i][positon[1]][0] == num:
            return False

    startrow = positon[1] // 3
    startcol = positon[0] // 3

    for i in range(startcol * 3, startcol * 3 + 3): #check every cell in 3x3 section
        for j in range(startrow * 3, startrow * 3 + 3):
            if puzzle[i][j][0] == num and (i,j) != positon:
                return False
    return True


#AC3 alogrithim

def AC3(puzzle):
    queue = []
    for i in range(len(puzzle)): #put all cells' coordinates into a stack
        for j in range(len(puzzle[i])):
            queue.append(puzzle[i][j][2])
    while len(queue) != 0:
        index = queue.pop() #pop cell's coordinates
        for i in range(0, 9): #check every cell in col
            if remove_arc_inconsistent(puzzle, index, (index[0], i)): #check for arc consistenty
                if len(puzzle[index[0]][i][1]) != 0: #if connected cell's domain is not empty, put it into the stack
                    queue.append((index[0], i))
                else:
                    return False

        for j in range(0, 9): #check every cell in row
            if remove_arc_inconsistent(puzzle, index, (j, index[1])):
                if len(puzzle[j][index[1]][1]) != 0:
                    queue.append((j, index[1]))
                else:
                    return False

        startrow = index[1] // 3
        startcol = index[0] // 3

        for i in range(startcol * 3, startcol * 3 + 3): #check every cell in 3x3 section
            for j in range(startrow * 3, startrow * 3 + 3):
                if remove_arc_inconsistent(puzzle, index, (i, j)):
                    if len(puzzle[i][j][1]) != 0:
                        queue.append((i, j))
                    else:
                        return False

    if backtrackingsolve(puzzle): #after removing all disallowed vaules, try to solve the puzzle
        return True
    else:
        return False



def remove_arc_inconsistent(puzzle, x_index, y_index):
    removed = False #indicated if a vaule in a domain is removed
    if puzzle[x_index[0]][x_index[1]][0] == 0 and puzzle[y_index[0]][y_index[1]][0] == 0: #can't check two cells with no assigned numbers
        return False
    for i in puzzle[x_index[0]][x_index[1]][1]: #check every vaule is domain of x_index cell
        if i == puzzle[y_index[0]][y_index[1]][0]:
            if i in puzzle[x_index[0]][x_index[1]][1]:
                puzzle[x_index[0]][x_index[1]][1].remove(i) #if vaule in domain is assigned in cell y_index, remove it if not already
                removed = True
    for i in puzzle[y_index[0]][y_index[1]][1]: #check every vaule is domain of y_index cell
        if i == puzzle[x_index[0]][x_index[1]][0]:
            if i in puzzle[y_index[0]][y_index[1]][1]:
                puzzle[y_index[0]][y_index[1]][1].remove(i) #if vaule in domain is assigned in cell x_index, remove it if not already
                removed = True
    return removed





if __name__ == "__main__":
    puzzle = input("Enter your unsolved puzzle here: ")
    sudkou = Sudoku(puzzle)
    print("Unsolved puzzle")
    sudkou.printPuzzle()
    if AC3(sudkou.puzzle):
        print("Puzzle Solved!")
        sudkou.printPuzzle()
    else:
        print("Puzzle cannot be solved")

