"""
Ok. Here's how it works.
Let's take a sample board and a sample rack:

	----------------------------------------------------------------
	|  | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O |
	----------------------------------------------------------------
	|01|TWS|   |   |DLS|   |   |   |TWS|   |   |   |DLS|   |   |TWS|
	----------------------------------------------------------------
	|02|   |DWS|   |   |   |TLS|   |   |   |TLS|   |   |   |DWS|   |
	----------------------------------------------------------------
	|03|   |   |DWS|   |   |   |DLS|   |DLS|   |   |   |DWS|   |   |
	----------------------------------------------------------------
	|04|DLS|   |   |DWS|   |   |   |DLS|   |   |   |DWS|   |   |DLS|
	----------------------------------------------------------------
	|05|   |   |   |   |DWS|   |   |   |   |   |DWS|   |   |   |   |
	----------------------------------------------------------------
	|06|   |TLS|   |   |   |TLS|   |   |   |TLS|   |   |   |TLS|   |
	----------------------------------------------------------------
	|07|   |   |DLS|   |   |   |DLS|   |DLS|   |   |   |DLS|   |   |
	----------------------------------------------------------------
	|08|TWS|   |   |DLS|   |   |   | R | A | D | I | C | A | L |TWS|
	----------------------------------------------------------------
	|09|   |   |DLS|   |   |   |DLS|   |DLS|   |   |   |DLS|   |   |
	----------------------------------------------------------------
	|10|   |TLS|   |   |   |TLS|   |   |   |TLS|   |   |   |TLS|   |
	----------------------------------------------------------------
	|11|   |   |   |   |DWS|   |   |   |   |   |DWS|   |   |   |   |
	----------------------------------------------------------------
	|12|DLS|   |   |DWS|   |   |   |DLS|   |   |   |DWS|   |   |DLS|
	----------------------------------------------------------------
	|13|   |   |DWS|   |   |   |DLS|   |DLS|   |   |   |DWS|   |   |
	----------------------------------------------------------------
	|14|   |DWS|   |   |   |TLS|   |   |   |TLS|   |   |   |DWS|   |
	----------------------------------------------------------------
	|15|TWS|   |   |DLS|   |   |   |TWS|   |   |   |DLS|   |   |TWS|
	----------------------------------------------------------------

With a rack:

	['A', 'M', 'A', 'Z', 'I', 'N', 'G']
	
Steps:

1)  Find all words on rack. This is done with cpu.CPU.gacc, which stands for getAllCorrectCombinations, using itertools.permutations. Pretty simple.
2)  Get all the positions to play at. This takes all the places on the board, in utils.board.getPlaces, and uses all of the points adjacent to it.
2a) If there are no tiles on the board, simply add all tiles in the 8th row and 8th column.
3)  Loop through all the points to play at, all of the words, and the directions (Across, 'A', and Down, 'D').  For each play, check if it's a valid play, then yield it.
4) 


How to check if a play is valid:
1) Get the words on the board. This is done in utils.board.getWords.
	Each word is represented as a collections.orderedDict object. 
	Each key-value pair is letter: (row, column).
	For the board this is the list that is returned:

		[OrderedDict([('R', (8, 8)), ('A', (8, 9)), ('D', (8, 10)), ('I', (8, 11)), ('C', (8, 12)), ('A1', (8, 13)), ('L', (8, 14))])]





"""




from utils import *
import blueprint as bp

class CPU():
    def __init__(self, strategy=bp.BlueprintBase):
        self.board = Board()
        
        self.rack = []
        self.distribution = distribution[:]
        self.drawTiles()
            
        self.checkWord = self.board.checkWord
        self.extraList = self.board.extraList

        self.score = 0

        self.BlueprintCreator = strategy
        
        self.name = "CPU"
        
    def drawTiles(self):
        print('drawing tiles!')
        while len(self.rack)<7 and len(self.distribution)>0:
            letter = random.choice(self.distribution)
            self.rack.append(letter.upper())
            self.distribution.remove(letter)
                
    def gacc(self, iterable, maxDepth):
        for word in self.gac(iterable, maxDepth):
            if self.checkWord(word):
                yield word
    
    def displayBoard(self, board):
        
        count = 0
        text = "-"*64
        text += "\n"
        text += "|"
        for i in range(16):
            line = board[i]
            for j in line:
                if j == " ":
                    if i == 0:
                        j = "  "
                    else:
                        j = "   "
                if (j[0] in string.ascii_uppercase  or j == "*") and len(j) < 3:
                    j = " " + j[0] + " "
                text += j
                text += "|"
                count += 1
                if count == 16 and i != 15:
                    text += "\n"
                    text += "-" * 64
                    text += "\n"
                    text += "|"
                    count = 0
        text += "\n"
        text += "-" * 64
        text += "\n"
        print(text)

    def generate(self):
        prevBoard = self.rNab()
        words = self.board.removeDuplicates(self.gacc(self.rack, len(self.rack)))
        places = self.board.getPlaces(self.board.board)
        plays = []
        neighbors = []

        if places == []:
            for i in range(1, 15):
                places.append((i, 8))
                places.append((8, i))
        across, down = [], []
        for place in places:
            r, c = place
            neighbors.append((r+1,c))
            neighbors.append((r-1,c))
            neighbors.append((r,c+1))
            neighbors.append((r,c-1))
        neighbors = self.board.removeDuplicates(neighbors)
        for word in words:
            for neighbor in neighbors:
                rIndex, cIndex = neighbor
                for direc in ['A', 'D']:
                    newBoard = self.rNab()
                    if self.playWord(word, rIndex, cIndex, direc, newBoard):
                        play = Move(word, newBoard, rIndex, cIndex, direc, prevBoard, self.rack)
                        yield play
                        continue
                        
                    newBoard = self.rNab()
                    if self.playWordOpp(word, rIndex, cIndex, direc, newBoard):
                        play = Move(word, newBoard, rIndex, cIndex, direc, prevBoard, self.rack, revWordWhenScoring=False)
                        yield play
                        
        for (d, row) in enumerate(self.board.board[1:]):
            yield from self.complete(self.slotify(row[1:]), 'A', d+1)
            
        for (d, col) in enumerate([[row[i] for row in self.board.board[1:]] for i in range(len(self.board.board))]):
            yield from self.complete(self.slotify(col), 'D', d)


    def proxyBoard(self):
        return Board(copy.deepcopy(self.board.board))

    def playWord(self, word, row, col, direc, board):
        for letter in reversed(word):
            if row>15 or col>15:
                return False
            if board.board[row][col] in string.ascii_uppercase:
                return False
            board.board[row][col] = letter
            if direc=='A':
                col -= 1
            else:
                row -= 1
        if board.checkBoard(board.board):
            return True
        return False

    def playWordOpp(self, word, row, col, direc, board, skip=False):
        i = 0
        #for letter in word:
        while i < len(word):
            if row>15 or col>15:
                return False
            if board.board[row][col] in string.ascii_uppercase:
                if skip:
                    i -= 1
                else:
                    return False
            else:
                board.board[row][col] = word[i]
            if direc=='A':
                col += 1
            else:
                row += 1
            i += 1
        if board.checkBoard(board.board):
            return True
        return False
    
    def rNab(self):
        return Board([[col[:] for col in row] for row in self.board.board])

    def gac(self, iterable, maxDepth):
        allWords = []
        for depth in range(1, maxDepth + 1): 
            for word in itertools.permutations(iterable, depth):
                allWords.append("".join(word))
        return allWords
    
    def place(self, slot, pos, word, direc, depth):
        slot, reps = slot
        currPos = pos
        newSlot = list(slot)

        index = 0
        w=False
        while index < len(word):
            newPos = currPos + index
            if newPos>=len(newSlot):
                return False
            if newSlot[newPos] != '.':
                currPos += 1
                index -= 1
            else:
                newSlot[newPos] = word[index]
                if not w:
                    wordPos = currPos+index
                    w=True
            index += 1
        if w:
            wordPos += 1
        else:
            return False
        #print(wordPos == slot.index(slot.strip('.')[0]))
        newSlot = ''.join(letter for letter in newSlot)

        if not all(self.checkWord(i) for i in newSlot.strip('.').split('.') if i != ''):
            return False

        newBoardSlot = []
        for (index, newLetter) in enumerate(newSlot):
            if newLetter == '.':
                newBoardSlot.append(reps[index])
            else:
                newBoardSlot.append(newLetter)
        newBoard = self.rNab()
        oldBoard = self.rNab()
        row, col = depth, depth
        if direc == 'A':
            newBoardSlot.insert(0, str(depth).zfill(2))
            newBoard.board[depth] = newBoardSlot[:]
            col = wordPos
        else:
            for (index, row) in enumerate(newBoard.board[1:]):
                row[depth] = newBoardSlot[index]

            row = wordPos
        move = Move(word, newBoard, row, col, direc, oldBoard, self.rack, doNotScoreWord=True)
        if move.board.checkBoard(move.board.board):
            return move
        return False
        
    def complete(self, slot, direc, depth):
        if depth==0:
            return []
        words = self.board.removeDuplicates(self.gac(self.rack, 7))
        newSlots = []
        slotForLen = slot[0]
        if slotForLen != '...............':
            edgeFinder = [i[0] for i in enumerate(slotForLen) if i[1] !='.']
            for word in words:
                for pos in range(edgeFinder[0], edgeFinder[-1]+len(word)+2):
                    if pos-len(word) in range(len(slotForLen)):
                        if slotForLen[pos-len(word)] == '.':
                            yield self.place(slot, pos-len(word), word, direc, depth)

        #return newSlots

    def slotify(self, slot):
        slotForReps = slot
        slot = ''.join(i for i in slot)
        slot = slot.replace(' ', '.')
        for i in self.extraList:
            slot = slot.replace(i, '.')
        #print(slot)
        return slot, slotForReps


    def exchange(self):
        if len(distribution)<7:
            return []
        exchs = self.gac(self.rack, len(self.rack))
        for i in exchs:
            exch = Move(i, self.board, 0, 0, 0, self.board, self.rack, _type = 'e')
            exch.score = 0
            exch.getEvaluation(self.rack)
            yield exch

    def _run(self):
        print(self.rack)

        strategy = self.BlueprintCreator(self.generate(), self.rack)
        b = strategy.pick()
        t='p'
        
        if b is None:
            strategy.setMoves(self.exchange())
            b = strategy.pick()
            t='e'
            
        if b is None:
            print('I must pass...')
            return False
        
        if t != 'e':
            s = skips_formatted(b)
            print(s)
            print(b.row, b.col)
            print(b.score, b.valuation)
            
            self.board = b.board
            self.score += b.score
        else:
            print('Exchanging: {}\nValuation: {}'.format(b.word, b.valuation))

        for i in b.word:
            try:
                self.rack.remove(i)
            except:
                pass
        self.displayBoard(self.board.board)
        self.drawTiles()
        return b

        

