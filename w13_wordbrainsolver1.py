#Howard Zeng

import json
import sys
import numpy as np

POSITION = None
FILE = None
DIC = None
PRE_DIC = None
all_puzzles = []

class Trie:

    def __init__(self):
        self.root = []
        self.isWord = False
        for l in range(26):
            self.root.append(None)
        
    def addKey(self, iWord):
        if len(iWord) == 0:
            self.isWord = True
        else:
            # 65 is ord('A')
            let = ord(iWord[0]) - 97
            if self.root[let] == None:
                newTree = Trie()
                newTree.addKey(iWord[1:])
                self.root[let] = newTree
            else:
                self.root[let].addKey(iWord[1:])

    def pre(self, iLetter):
        return self.root[ord(iLetter) - 97]

def createTrie(iDictionaryFile):
    global FILE
    global DIC
    global PRE_DIC
    global POSITION

    FILE = iDictionaryFile
    DIC = []
    PRE_DIC = Trie()
    POSITION = '-'

    with open(FILE) as f:
        lines = f.readlines()

    for line in lines:
        DIC.append(line.strip('\n'))
        
    for word in DIC:
        PRE_DIC.addKey(word)

def applyGravity(g, rows, cols):
    global POSITION
    
    for r in range(rows-1):
        for c in range(cols):
            if g[r+1][c] == POSITION:
                for hold in reversed(range(r+1)):
                    g[hold+1][c] = g[hold][c]
                g[0][c] = POSITION

def solAppend(s, ans):
    if s:
        ans.append(s)

# Traverses grid in all of the 8 directions on a 2d grid
def traverse(solution, grid, x, y, remain, row, col, wrd, stp, branch):
    global POSITION
    global DIC
    
    if (x >= col) or (y >= row) or (x < 0) or (y < 0) or (grid[x][y] == POSITION):
        return False
        
    if [x, y] in stp:
        return False
    
    newSteps = list(stp)
    newSteps.append([x, y])
    wrd += grid[x][y]
    remain -= 1
    letter = wrd[-1]
    branch = branch.pre(letter)
    
    if branch == None:
        return False
    
    if remain == 0:
        if branch.isWord == True:
            return [grid, wrd, newSteps]
        else:
            return False
        

    checkSol = traverse(solution, grid, x + 1, y, remain, row, col, wrd, newSteps, branch)
    solAppend(checkSol, solution)
    
    checkSol = traverse(solution, grid, x, y + 1, remain, row, col, wrd, newSteps, branch)
    solAppend(checkSol, solution)
    
    checkSol = traverse(solution, grid, x - 1, y, remain, row, col, wrd, newSteps, branch)
    solAppend(checkSol, solution)
  
    checkSol = traverse(solution, grid, x, y - 1, remain, row, col, wrd, newSteps, branch)
    solAppend(checkSol, solution)

    checkSol = traverse(solution, grid, x + 1, y + 1, remain, row, col, wrd, newSteps, branch)
    solAppend(checkSol, solution)

    checkSol = traverse(solution, grid, x - 1, y - 1, remain, row, col, wrd, newSteps, branch)
    solAppend(checkSol, solution)
        
    checkSol = traverse(solution, grid, x + 1, y - 1, remain, row, col, wrd, newSteps, branch)
    solAppend(checkSol, solution)
        
    checkSol = traverse(solution, grid, x - 1, y + 1, remain, row, col, wrd, newSteps, branch)
    solAppend(checkSol, solution)

if __name__ == "__main__":
    

    # For enumeration
    xCounter = 0
    yCounter = 1
    gridCounter = 0
    wordCounter = 1
    stepCounter = 2

    inputFile = sys.argv[2]
    
    # Extract the dictionary file (first line of the input file)
    createTrie(inputFile)

    while True:
        inline = input("")    
        try:
            #makes line a dictionary        
            puzzline = json.loads(inline)
            all_puzzles.append(puzzline)
            #print(all_puzzles)
        except:
            break
    
    for puz in range(len(all_puzzles)):
        letters = []
        for i in range(len(all_puzzles[puz]['grid'])):
            letters.append(all_puzzles[puz]['grid'][i])
            #print(all_puzzles[2]['grid'][i])
        
        let = [[y for y in x] for x in [x for x in all_puzzles[puz]['grid']]]
        l = np.array(let)
        l = np.rot90(l)
        l = np.flipud(l) 
        
        grid = []
        for r in range(len(l)):
            grid.append(l[r])
            
        rows = len(grid)
        cols = len(grid[0])
        size = all_puzzles[puz]['size']
        
        if(size != rows and size != cols):
            print("Error size conflict")
        
        wordLens = [int(x) for x in all_puzzles[puz]['lengths']]
        ansWords = len(wordLens)

        if len(wordLens) != ansWords:
            print("Error incorrect number of words")
        
        solPool = [[grid,[]]]

        for runs in range(ansWords):
            posSol2 = []
            for ans in solPool:
                posSol1 = []
                for r in range(rows):
                    for c in range(cols):
                        solution = traverse(posSol1, ans[gridCounter], r, c, wordLens[runs], rows, cols, "", [], PRE_DIC)
                        if solution:
                            posSol1.append(solution)

                for posSol in posSol1:
                    tempList = list(ans[wordCounter])
                    tempList.append(posSol[wordCounter])
                    
                    nextGrid = []
                    for row in range(rows):
                        tempRow = list(posSol[gridCounter][row])
                        nextGrid.append(tempRow)
                    
                    for stepTaken in posSol[stepCounter]:
                        x = stepTaken[xCounter]
                        y = stepTaken[yCounter]
                        nextGrid[x][y] = POSITION

                    applyGravity(nextGrid, rows, cols)
                    posSol2.append([nextGrid, tempList])
            
            solPool = posSol2

        solPool.sort()
        for ans in solPool:
            print(ans[wordCounter])
        print(".")