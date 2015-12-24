from random import random, sample, choice, shuffle
import copy


class SudokuSolver():
    def __init__(self):
        self.sudoku = [[], []]  # sudoku[i][j] contains assigned value for each cell or -1 if unassigned
        self.n = 0  # size of sudoku puzzle
        self.m = 0  # row size of each square
        self.k = 0  # column size of each square
        self.consistencyChecks = 0  # no. of consistency checks done
        self.constPos = set()
        self.varPos = set()
        self.allPos = set()


# read the initial game state from the input file
    def readGameState(self, filePath):
        # Reading file
        fileHandle = open(filePath, 'r')
        gridVal = fileHandle.readline().rstrip(';\n').split(',')

        # Read n, m, k
        self.n = int(gridVal[0])
        self.m = int(gridVal[1])
        self.k = int(gridVal[2])

        self.allPos = [(i, j) for i in range(self.n) for j in range(self.n)]

        sudokuRawState = [line.rstrip(';\n').split(',') for line in open(filePath)]
        sudokuRawState.remove(sudokuRawState[0])
        # print sudokuRawState
        self.sudoku = [[0 for x in range(self.n)] for x in range(self.n)]

        # check for dimension of given board
        if len(sudokuRawState) != self.n:
            print "Wrong gameState given, check txt file"
            exit(0)
        else:
            for i in range(self.n):
                if len(sudokuRawState[i]) != self.n:
                    print "Wrong gameState given, check txt file"
                    exit(0)

        # update peg and corner positions
        for i in range(self.n):
            for j in range(self.n):
                if sudokuRawState[i][j] == '-':
                    self.sudoku[i][j] = -1
                else:
                    self.sudoku[i][j] = int(sudokuRawState[i][j])
                    pos = (i, j)
                    self.constPos.add(pos)
                    # else:
                    #     print "Invalid Character in game state, check txt file"
                    #     exit(0)
        # Initialize domain of each variable in nxn sudoku puzzle
        self.domainValList = list()
        for x in range(1, self.n + 1):
            self.domainValList.append(x)
        # Initial domain = [1,2,..n] for each uninitialized variable

        # self.domain[i][j] represents domain value list for each (i,j) cell
        self.domain = []
        for p in range(self.n):
            self.domain.append([])
            for q in range(self.n):
                self.domain[p].append([])


    # Update the domain of (i,j) cell variable in the sudoku based on its row, col and mxk square items
    def setDomainOfCell(self, i, j):
        rStart = i - i % self.m  # starting row index for square to which this variable belongs
        cStart = j - j % self.k  # starting col index for square to which this variable belongs

        # Update domain based on row items
        for col in xrange(0, self.n):
            val = self.sudoku[i][col]
            if val != -1 and val in self.domain[i][j]:
                self.domain[i][j].remove(val)

        # Update domain based on col items
        for row in xrange(0, self.n):
            val = self.sudoku[row][j]
            if val != -1 and val in self.domain[i][j]:
                self.domain[i][j].remove(val)

        # Update domain based on square
        for row in xrange(0, self.m):
            for col in xrange(0, self.k):
                val = self.sudoku[row + rStart][col + cStart]
                if val != -1 and val in self.domain[i][j]:
                    self.domain[i][j].remove(val)


    # Initialize the domain list for each cell in sudoku
    def initializeDomainCellList(self):
        # If variable is uninitialized, domain is [1,2...n]
        for i in range(self.n):
            for j in range(self.n):
                if self.sudoku[i][j] == -1:
                    self.domain[i][j] = copy.deepcopy(self.domainValList)
                else:
                    self.domain[i][j] = [self.sudoku[i][j]]
        # IF variable is initialized then domain = [its_val]
        for p in range(self.n):
            for q in range(self.n):
                if self.sudoku[p][q] == -1:
                    self.setDomainOfCell(p, q)


                # Check for consistency of selected value for a variable


    def isValConsistent(self, val, i, j):
        rStart = i - i % self.m
        cStart = j - j % self.k
        # Row consistency
        for col in xrange(0, self.n):
            if self.sudoku[i][col] == val:
                return False
        # Column consistency
        for row in xrange(0, self.n):
            if self.sudoku[row][j] == val:
                return False

        # Square consistency
        for row in xrange(0, self.m):
            for col in xrange(0, self.k):
                if self.sudoku[row + rStart][col + cStart] == val:
                    return False
        return True


    # Remove val from constrained variable with AllDiff constraint in row, col and square of given cell
    def removeValFromAffectedCellsDomain(self, val, cell):
        i = cell[0]
        j = cell[1]
        constrainedCells = list()  # Modified cells list, used if assignment is inconsistent
        rStart = i - i % self.m
        cStart = j - j % self.k

        # Remove val from domains of constrained variables in row
        for col in xrange(0, self.n):
            if self.sudoku[i][col] == -1 and val in self.domain[i][col]:
                self.domain[i][col].remove(val)
                constrainedCells.append((i, col))
        # Remove val from domains of constrained variables in col
        for row in xrange(0, self.n):
            if self.sudoku[row][j] == -1 and val in self.domain[row][j]:
                self.domain[row][j].remove(val)
                constrainedCells.append((row, j))
        # Remove val from domains of constrained variables in square
        for row in xrange(0, self.m):
            for col in xrange(0, self.k):
                if self.sudoku[row + rStart][col + cStart] == -1 \
                        and val in self.domain[row + rStart][col + cStart]:
                    self.domain[row + rStart][col + cStart].remove(val)
                    constrainedCells.append((row + rStart, col + cStart))
        return constrainedCells

    #Forward checking using AllDiff constraint check for each row, col and sqaure
    def fwdCheckCellsDomain(self, val, cell):
        i = cell[0]
        j = cell[1]
        constrainedCells = list()
        rStart = i - i % self.m
        cStart = j - j % self.k
        for col in xrange(0, self.n):
            if self.sudoku[i][col] == -1 and col != j and val in self.domain[i][col]:
                self.domain[i][col].remove(val)
                constrainedCells.append((i, col))
                if len(self.domain[i][col]) == 0:
                    self.addValToAffectedCellsDomain(val, constrainedCells)
                    return None

        for row in xrange(0, self.n):
            if self.sudoku[row][j] == -1 and row != i and val in self.domain[row][j]:
                self.domain[row][j].remove(val)
                constrainedCells.append((row, j))
                if len(self.domain[row][j]) == 0:
                    self.addValToAffectedCellsDomain(val, constrainedCells)
                    return None

        for row in xrange(0, self.m):
            for col in xrange(0, self.k):
                if self.sudoku[row + rStart][col + cStart] == -1 \
                        and row + rStart != i and col + cStart != j \
                        and val in self.domain[row + rStart][col + cStart]:
                    self.domain[row + rStart][col + cStart].remove(val)
                    constrainedCells.append((row + rStart, col + cStart))
                    if len(self.domain[row + rStart][col + cStart]) == 0:
                        self.addValToAffectedCellsDomain(val, constrainedCells)
                        return None

        # self.domain[i][j].append(val) # Add val back to domain of (i,j) cell
        return constrainedCells


    # Select first uninitialized var(-1) in row by row scan
    def selectFirstUnassignedVar(self):
        self.consistencyChecks += 1
        for i in xrange(self.n):
            for j in xrange(self.n):
                if self.sudoku[i][j] == -1:
                    return (i, j)  # Iterate row by row, return first unassigned var
        return (-1, -1)  # Sudoku assignment complete


    # Select next variable using MRV heuristic
    def selectMRVVar(self):
        min = 12
        min_cell = (-1, -1)  # Sudoku complete
        # Select item with minimum domain size
        for i in xrange(self.n):
            for j in xrange(self.n):
                if self.sudoku[i][j] == -1 and min > len(self.domain[i][j]):
                    min = len(self.domain[i][j])
                    min_cell = (i, j)
        return min_cell

    # Constraint propagation after applying AllDiff constraint
    def propagateArcConsistency(self, val, cell):
        i = cell[0]
        j = cell[1]
        constrainedCells = list()
        rStart = i - i % self.m
        cStart = j - j % self.k
        for col in xrange(0, self.n):
            if self.sudoku[i][col] == -1 and col != j and val in self.domain[i][col]:
                self.domain[i][col].remove(val)
                constrainedCells.append((i, col))
                if len(self.domain[i][col]) == 0:
                    self.addValToAffectedCellsDomain(val, constrainedCells)
                    return None

        for row in xrange(0, self.n):
            if self.sudoku[row][j] == -1 and row != i and val in self.domain[row][j]:
                self.domain[row][j].remove(val)
                constrainedCells.append((row, j))
                if len(self.domain[row][j]) == 0:
                    self.addValToAffectedCellsDomain(val, constrainedCells)
                    return None

        for row in xrange(0, self.m):
            for col in xrange(0, self.k):
                if self.sudoku[row + rStart][col + cStart] == -1 \
                        and row + rStart != i and col + cStart != j \
                        and val in self.domain[row + rStart][col + cStart]:
                    self.domain[row + rStart][col + cStart].remove(val)
                    constrainedCells.append((row + rStart, col + cStart))
                    if len(self.domain[row + rStart][col + cStart]) == 0:
                        self.addValToAffectedCellsDomain(val, constrainedCells)
                        return None
        return constrainedCells


    # Add values back to constrained variables as val was inconsistent
    def addValToAffectedCellsDomain(self, val, constrainedCells):
        for cell in constrainedCells:
            if cell:
                self.domain[cell[0]][cell[1]].append(val)


    # Implements simple backtracking technique for sudoku
    def backtrack(self):
        pos = self.selectFirstUnassignedVar()
        i = pos[0]
        j = pos[1]
        if pos == (-1, -1):
            return True  # Success, sudoku game complete
        for val in self.domain[i][j]:
            isConsistent = self.isValConsistent(val, i, j)
            if isConsistent == True:  # Value consistent, use it and recursively call gameSolver()
                self.sudoku[i][j] = val
                if (self.backtrack()):
                    return True  # assignment correct for this pos (i,j)
                self.sudoku[i][j] = -1

        return False


    def backTrackMRV(self):
        pos = self.selectMRVVar()
        i = pos[0]
        j = pos[1]
        self.consistencyChecks += 1
        if pos == (-1, -1):
            return True  # Success, sudoku game complete

        # MRV heuristic doesn't check for empty domain of constrained variable ,
        # This problem will be solved in Forward checking
        if (len(self.domain[i][j]) == 0):
            return False
        for val in self.domain[i][j]:
            isConsistent = self.isValConsistent(val, i, j)
            if isConsistent == True:  # Value consistent, use it and recursively call gameSolver()
                self.sudoku[i][j] = val
                constrainedCells = self.removeValFromAffectedCellsDomain(val, pos)
                if (self.backTrackMRV()):
                    return True  # assignment correct for this pos (i,j)
                self.sudoku[i][j] = -1
                self.addValToAffectedCellsDomain(val, constrainedCells)
        return False


    # Implements Backtracking + MRV + Forward check
    def backtrackMRVFwd(self):
        self.consistencyChecks += 1
        pos = self.selectMRVVar()
        i = pos[0]
        j = pos[1]
        if pos == (-1, -1):
            return True  # Success, sudoku game complete
        for val in self.domain[i][j]:
            constrainedCells = self.fwdCheckCellsDomain(val, pos)
            if constrainedCells != None:
                self.sudoku[i][j] = val
                if (self.backtrackMRVFwd()):
                    return True  # assignment correct for this pos (i,j)
                self.sudoku[i][j] = -1
                self.addValToAffectedCellsDomain(val, constrainedCells)
        return False


    # Implements Backtracking + MRV + Forward check + Constraint propagation
    def backtrackMRVFwdCp(self):
        pos = self.selectMRVVar()
        i = pos[0]
        j = pos[1]
        if pos == (-1, -1):
            return True  # Success, sudoku game complete
        for val in self.domain[i][j]:
            constrainedCells = self.propagateArcConsistency(val, pos)
            if constrainedCells != None:
                self.sudoku[i][j] = val
                if (self.backtrackMRVFwdCp()):
                    return True  # assignment correct for this pos (i,j)
                self.sudoku[i][j] = -1
                self.consistencyChecks += 1
                self.addValToAffectedCellsDomain(val, constrainedCells)
        return False
        # MIN CONFLICT


    def conflictChecker(self, pos):
        i, j = pos
        domain = self.domain[i][j]

        rStart = i - i % self.m
        cStart = j - j % self.k

        for constRow, constCol in self.constPos:
            if constRow == i or constCol == j or (constRow == rStart and constCol == cStart):
                val = self.sudoku[constRow][constCol]
                try:
                    domain.remove(val)
                except ValueError:  # 'remove' throws 'ValueError' if element not found
                    pass
        return domain


    """Returns the number of conflicts in given state with respect to given Position"""


    def totalConflict(self, gameState, pos):
        res = 0
        row, col = pos
        rStart = row - row % self.m
        cStart = col - col % self.k
        val = gameState[row][col]

        # same row
        for i in range(self.n):
            if (i != col and gameState[row][i] == val):
                res += 1

        # same column
        for i in range(self.n):
            if (i != row and gameState[i][col] == val):
                res += 1

        beg = rStart, cStart
        end = beg[0] + self.m, beg[1] + self.k

        for i in xrange(beg[0], end[0]):
            for j in xrange(beg[1], end[1]):
                if (i, j) != pos and gameState[i][j] == val:
                    res += 1

        return res

    #Check if a given position is conflicted or not
    def isConflict(self, gameState, pos):
        return self.totalConflict(gameState, pos) > 0

    # getPos returns next randomly selected conflicted variable from the sudoku
    def getPos(self, gameState):
        while self.allPos:
            pos = choice(self.allPos)
            if pos in self.constPos:
                self.allPos.remove(pos)
                continue
            if self.isConflict(gameState, pos):
                return pos
            else:
                self.allPos.remove(pos)
        return -1

    # Return the conflicted variable with the minimum value
    def minConflictVal(self, gameState, pos):
        conflictVal = {}
        i, j = pos
        for val in self.domain[i][j]:
            newState = self.updateSudoku(gameState, pos, val)
            conflictVal[val] = self.totalConflict(newState, pos)
        minConflictVal = conflictVal[min(conflictVal, key=conflictVal.get)]
        allMinVal = [val for val, totalConflict in conflictVal.items() if totalConflict == minConflictVal]
        minVal = choice(allMinVal)
        return minVal

    def updateSudoku(self, gameState, pos, val):
        gameState[pos[0]][pos[1]] = val
        return gameState

    # Initialize the domain and sudoku cells value
    def initialState(self):
        for i in range(self.n):
            for j in range(self.n):
                pos = (i, j)
                if pos not in self.constPos:
                    self.domain[i][j] = self.conflictChecker(pos)
                    self.sudoku[i][j] = choice(self.domain[i][j])
        return self.sudoku

    # minConflict algorithm
    def minConflict(self):
        self.sudoku = self.initialState()
        for i in range(100000):
            pos = self.getPos(self.sudoku)
            self.consistencyChecks+=1
            if pos == -1:
                return True # Sudoku solved
            # select the next min conflict value
            val = self.minConflictVal(self.sudoku, pos)
            self.sudoku = self.updateSudoku(self.sudoku, pos, val)
        return False
