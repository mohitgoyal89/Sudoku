###########################################
# you need to implement five funcitons here
###########################################
from SudokuGameSolver import SudokuSolver

def backtracking(filename):
    ###
    # use backtracking to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    solver = SudokuSolver()
    solver.readGameState(filename)
    solver.initializeDomainCellList()
    solver.backtrack()
    return (solver.sudoku, solver.consistencyChecks)
    #return ([[],[]], 0)

def backtrackingMRV(filename):
    ###
    # use backtracking + MRV to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    solver = SudokuSolver()
    solver.readGameState(filename)
    solver.initializeDomainCellList()
    solver.backTrackMRV()
    return (solver.sudoku, solver.consistencyChecks)
    #return ([[],[]], 0)
def backtrackingMRVfwd(filename):
    ###
    # use backtracking +MRV + forward propogation
    # to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    solver = SudokuSolver()
    solver.readGameState(filename)
    solver.initializeDomainCellList()
    solver.backtrackMRVFwd()
    return (solver.sudoku, solver.consistencyChecks)
    # return ([[],[]], 0)

def backtrackingMRVcp(filename):
    ###
    # use backtracking + MRV + cp to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    solver = SudokuSolver()
    solver.readGameState(filename)
    solver.initializeDomainCellList()
    solver.backtrackMRVFwdCp()
    return (solver.sudoku, solver.consistencyChecks)
    #return ([[],[]], 0)

def minConflict(filename):
    ###
    # use minConflict to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    solver = SudokuSolver()
    solver.readGameState(filename)
    solver.initializeDomainCellList()
    solver.minConflict()
    return (solver.sudoku, solver.consistencyChecks)
    # return ([[],[]], 0)