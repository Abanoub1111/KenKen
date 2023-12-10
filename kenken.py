import random
from collections import deque


class Kenken:
    def __init__(self):
        self.grid = [[0 for i in range(6)] for j in range(6)]
        self.cages = self.get_user_input_for_cages()  # Call the method here
        self.cellToCageMap = self.mapCellsToCages()


    def get_user_input_for_cages(self):
        cages = {}
        num_cages = int(input("Enter the number of cages: "))

        for i in range(1, num_cages + 1):
            op = input(f"Enter the operation for cage {i} (+, -, *, /, or none): ")
            value = int(input(f"Enter the target value for cage {i}: "))
            cells_input = input(f"Enter cell positions for cage {i} (e.g., 0,0 0,1 1,0): ")

            print(f"Entered cells_input for cage {i}: {cells_input}")

            cells = [tuple(map(int, cell.split(','))) for cell in cells_input.split()]

            print(f"Processed cells for cage {i}: {cells}")

            cages[i] = {'value': value, 'op': op, 'cells': cells}

        return cages


    def mapCellsToCages(self):

        gameSize = len(self.grid)
        cellToCageMap = [ [0]*gameSize for i in range(gameSize)] # --- number of all cells in the game ---
        for cage in self.cages:
            cellsOfCageTupleList = self.cages[cage]['cells']  # --- cellsOfCage is list of tuples ---
            for cellTuple in cellsOfCageTupleList:
                row = cellTuple[0]
                col = cellTuple[1]
                cellToCageMap[row][col] = cage

        return cellToCageMap


    def Bounding(self, row, col, value):

        isAllConstraintsApplied = False
        conditionsList = [self.check_row(row= row, value= value), # --- check row constraint ---
                          self.check_column(col= col, value= value), # --- check column constraint ---
                          self.check_cage(row= row, col= col, value= value)] # --- check cage operation constraint ---
        if all(conditionsList):
            isAllConstraintsApplied = True

        return isAllConstraintsApplied

    def check_row(self, row, value):
 
        # --- Default: Row constraint is applied ---
        isConstraintApplied = True
        # --- self.grid[row] is a 1-D list ---
        for columnItem in self.grid[row]:
            # --- check if there is a repeated value ---
            if columnItem == value:
                isConstraintApplied = False

        return isConstraintApplied

    def check_column(self, col, value):

        # --- Default: Column constraint is applied ---
        isConstraintApplied = True
        # --- Iterate over each row ---
        for row in range(len(self.grid)):
            # --- check if there is a repeated value ---
            if self.grid[row][col] == value:
                isConstraintApplied = False

        return isConstraintApplied

    
    def check_cage(self, row, col, value):

        isConstraintApplied =False
        # search with the row and col (cell position in cellToCageMap 2D array to get cage number
        cageNumber = self.cellToCageMap[row][col]
        cageNeededToBeChecked = self.cages.get(cageNumber)
        # get cellsList of the cage
        cellsList = cageNeededToBeChecked['cells']
        # get cage operation
        cageOperation = cageNeededToBeChecked['op']

        # FreeBie
        if cageOperation == "none": # freeBie
            # index of [0] is used because cellsList of this cage contains only ONE cell(freeBie)
            if int(value) == int(cageNeededToBeChecked['value']):
                isConstraintApplied = True

        # ADDITION
        elif cageOperation == "+" : # cellsList > = 2
            summationResult = 0
            zerosCount = 0
            for cell in cellsList: # cell is tuple (1,2)
                if (row,col) != cell: # sum all cells except the one Iam checking
                    zerosCount += (self.grid[cell[0]][cell[1]] == 0)
                    summationResult += int(self.grid[cell[0]][cell[1]])
            if zerosCount and summationResult + int(value) < int(cageNeededToBeChecked['value']):
                isConstraintApplied = True
            elif not zerosCount and summationResult + int(value) == int(cageNeededToBeChecked['value']):
                isConstraintApplied = True

        # SUBTRACTION
        elif cageOperation == "-": # cellsList has only 2 cells according to game Rules
            subtractionResult = 0
            for cell in cellsList:
                if (row,col) != cell : # I have this cell value passed to my function
                    if self.grid[cell[0]][cell[1]] == 0:
                        isConstraintApplied = True
                        break
                    subtractionResult = int(value) - int(self.grid[cell[0]][cell[1]])
            # check if constraint is applied
            if abs(subtractionResult) == cageNeededToBeChecked['value']:
                isConstraintApplied = True

        # MULTIPLICATION
        elif cageOperation == "*": # cellsList > = 2
            multiplicationResult = 1
            zerosCount = 0
            for cell in cellsList:
                if (row,col) != cell:
                    if self.grid[cell[0]][cell[1]] == 0:
                        zerosCount += 1
                    else:
                        multiplicationResult *= self.grid[cell[0]][cell[1]]

            if zerosCount and multiplicationResult * value <= cageNeededToBeChecked['value']:
                isConstraintApplied = True
            elif not zerosCount and multiplicationResult * value == cageNeededToBeChecked['value']:
                isConstraintApplied = True

        # DIVISION
        elif cageOperation == "/": # cellsList = 2
            divisionResult = 1
            for cell in cellsList:
                if (row,col) != cell : # I have this cell value passed to my function
                    if self.grid[cell[0]][cell[1]] == 0:
                        isConstraintApplied = True
                        break
                    elif value > self.grid[cell[0]][cell[1]]:
                        # divide greater/smaller
                        divisionResult = value / self.grid[cell[0]][cell[1]]
                    else:
                        # divide greater/smaller
                        divisionResult = self.grid[cell[0]][cell[1]] / value
            # check if constraint is applied
            if divisionResult == cageNeededToBeChecked['value']:
                isConstraintApplied = True

        return isConstraintApplied
    



    def solve(self):

        if self.backtracking():
            print("Puzzle solved:")
            self.print_solution()
        else:
            print("Puzzle unsolvable.")


    def print_solution(self):

        for row in self.grid:
            print(row)


    def backtracking(self):

        row, col = self.find_empty()
        # Base case
        if row is None:
            return True

        # iterate over all possible values to test them
        for i in range(1, len(self.grid) + 1):
            # check if the current value will obey all constraints
            if self.Bounding(row, col, i):
                self.grid[row][col] = i
                if self.backtracking():
                    return True

        # backtrack the value
        self.grid[row][col] = 0
        return False


    def getKenkenGrid(self):
        return self.grid

    def getKenkenCagesDict(self):
        return self.cages


    def find_empty(self):

        # --- Loop over each cell position and check its value ---
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                # --- if cellValue is "0" means empty cell ---
                cellValue = self.grid[row][col]
                # --- typeCasting "int()" to ensure that if condition is valid in case the self.grid 2-D list
                #     is initialized by "0" value as a string ---
                if int(cellValue) == 0:
                    # --- return first empty position to work on it next ---
                    return (row,col)
        return (None,None)