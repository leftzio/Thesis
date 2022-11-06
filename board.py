def in_board(x,y):
        if x>7 or x<0 or y>7 or y<0:
            return False
        return True

class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    # __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self, n):
        "Set up initial board configuration."

        self.pieces = [[0 for x in range(8)] for y in range(8)]
        self.bking = (7,4)
        self.wking = (0,4)
        self.direction_CURR=1
        self.direction_temp=1
        
        #setup the initial board
        for i in range(8):
            self.pieces[1][i] = 1
            self.pieces[6][i] = -1

        self.pieces[0][0] = 4
        self.pieces[0][1] = 2
        self.pieces[0][2] = 3
        self.pieces[0][3] = 5
        self.pieces[0][4] = 6
        self.pieces[0][5] = 3
        self.pieces[0][6] = 2
        self.pieces[0][7] = 4

        self.pieces[7][0] = -4
        self.pieces[7][1] = -2
        self.pieces[7][2] = -3
        self.pieces[7][3] = -5
        self.pieces[7][4] = -6
        self.pieces[7][5] = -3
        self.pieces[7][6] = -2
        self.pieces[7][7] = -4

        self.chess_map_from_alpha_to_index = {
            "a" : 0,
            "b" : 1,
            "c" : 2,
            "d" : 3,
            "e" : 4,
            "f" : 5,
            "g" : 6,
            "h" : 7
        }

        self.chess_map_from_index_to_alpha = {
            0: "a",
            1: "b",
            2: "c",
            3: "d",
            4: "e",
            5: "f",
            6: "g",
            7: "h"
        }

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def countDiff(self, color):
        """Counts the difference in material in the game"""
        # count = 0
        # for y in range(self.n):
        #     for x in range(self.n):
        #         if self[x][y]==color:
        #             count += 1
        #         if self[x][y]==-color:
        #             count -= 1
        # return count
    
    

    def get_legal_moves(self, color, direction):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.
        
        # Get all the squares with pieces of the given color.
        for y in range(8):
            for x in range(8):
                
                # if self[x][y] == 6:
                #     self.wking = x,y
                # elif self[x][y] == -6:
                #     self.bking = x,y

                if self[x][y]*color > 0:       #if this square is the same color as the player
                    newmoves = self.get_moves_for_square((x,y), direction)
                    moves.update(newmoves)
                 
        return list(moves)

    def has_legal_moves(self, color, direction):

        moves = self.get_legal_moves(color, direction)
        valids = [x for x in moves if not self.is_in_check(x[0],x[1],color,-direction)]

        return len(valids)>0
    
    def get_type(self, x, y):
        if self[x][y] > 0:
            color = 1
        elif self[x][y] < 0:
            color = -1
        else:
        # skip empty source squares.
            return None,None

        piecetype = self[x][y] * color

        return piecetype, color

    def printBoard(self):
        for x in range(8):
            top = ' '
            for y in range(8):
                if str(self[x][y])[0] == '-':
                    top = top[:-1]
                top+=str(self[x][y])
                top+="        "
            print(top)
        print("\n\n")
    



    def getRookMoves(self, pos,color):
        column, row = list(pos.strip().lower())
        row = int(row) - 1
        column = self.chess_map_from_alpha_to_index[column]
        i,j = row, column
        solutionMoves = []

        for k in range(1,8):
            try:
                temp = self.pieces[i + k][j]
                if temp * self[i][j] < 0:
                    solutionMoves.append([i + k, j])
                    break
                elif temp * self[i][j] > 0:
                    break
                else: 
                    solutionMoves.append([i + k, j])            
            except:
                pass 

        for k in range(1,8):
            try:
                temp = self.pieces[i - k][j]
                if temp * self[i][j] < 0:
                    solutionMoves.append([i - k, j])
                    break
                elif temp * self[i][j] > 0:
                    break
                else: 
                    solutionMoves.append([i - k, j])  
                
            except:
                pass

        for k in range(1,8):
            try:
                temp = self.pieces[i][j + k]
                if temp * self[i][j] < 0:
                    solutionMoves.append([i, j + k])
                    break
                elif temp * self[i][j] > 0:
                    break
                else: 
                    solutionMoves.append([i, j + k])
            except:
                pass

        for k in range(1,8):
            try:
                temp = self.pieces[i][j - k]
                if temp * self[i][j] < 0:
                    solutionMoves.append([i, j - k])
                    break
                elif temp * self[i][j] > 0:
                    break
                else:
                    solutionMoves.append([i, j - k])
                
            except:
                pass

        temp = [i for i in solutionMoves if i[0] >=0 and i[1] >=0]
        solutionMoves = ["".join([self.chess_map_from_index_to_alpha[i[1]], str(i[0] + 1)]) for i in temp]
        solutionMoves.sort()    

        return solutionMoves

    def getKnightMoves(self, pos, color):
        """ A function that returns the all possible moves
            of a knight stood on a given position
        """
        column, row = list(pos.strip().lower())
        row = int(row) - 1
        column = self.chess_map_from_alpha_to_index[column]
        i,j = row, column
        solutionMoves = []
        try:
            temp = self.pieces[i + 1][j - 2]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i + 1, j - 2])
        except:
            pass
        try:
            temp = self.pieces[i + 2][j - 1]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i + 2, j - 1])
        except:
            pass
        try:
            temp = self.pieces[i + 2][j + 1]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i + 2, j + 1])
        except:
            pass
        try:
            temp = self.pieces[i + 1][j + 2]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i + 1, j + 2])
        except:
            pass
        try:
            temp = self.pieces[i - 1][j + 2]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i - 1, j + 2])
        except:
            pass
        try:
            temp = self.pieces[i - 2][j + 1]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i - 2, j + 1])
        except:
            pass
        try:
            temp = self.pieces[i - 2][j - 1]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i - 2, j - 1])
        except:
            pass
        try:
            temp = self.pieces[i - 1][j - 2]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i - 1, j - 2])
        except:
            pass

        # Filter all negative values
        temp = [i for i in solutionMoves if i[0] >=0 and i[1] >=0]
        allPossibleMoves = ["".join([self.chess_map_from_index_to_alpha[i[1]], str(i[0] + 1)]) for i in temp]
        allPossibleMoves.sort()
        return allPossibleMoves

    def getBishopMoves(self, pos,color):
        column, row = list(pos.strip().lower())
        row = int(row) - 1
        column = self.chess_map_from_alpha_to_index[column]
        i,j = row, column
        solutionMoves = []

        # Compute the moves in Rank
        for k in range(1,8):
            try:
                temp = self.pieces[i + k][j + k]
                if temp * self[i][j] < 0:
                    solutionMoves.append([i + k, j + k])
                    break
                elif temp * self[i][j] > 0:
                    break
                else:
                    solutionMoves.append([i + k, j + k])            
            except:
                pass 

        for k in range(1,8):
            try:
                temp = self.pieces[i + k][j - k]
                if temp * self[i][j] < 0:
                    solutionMoves.append([i + k, j - k])
                    break
                elif temp * self[i][j] > 0:
                    break
                else: 
                    solutionMoves.append([i + k, j - k])  
                
            except:
                pass

        for k in range(1,8):
            try:
                temp = self.pieces[i - k][j + k]
                if temp * self[i][j] < 0:
                    solutionMoves.append([i - k, j + k])
                    break
                elif temp * self[i][j] > 0:
                    break
                else: 
                    solutionMoves.append([i - k, j + k])
            except:
                pass

        for k in range(1,8):
            try:
                temp = self.pieces[i - k][j - k]
                if temp * self[i][j] < 0:
                    solutionMoves.append([i - k, j - k])
                    break
                elif temp * self[i][j] > 0:
                    break
                else:
                    solutionMoves.append([i - k, j - k])
                
            except:
                pass
        
        # print(solutionMoves)
        
        # Filter all negative values
        temp = [i for i in solutionMoves if i[0] >=0 and i[1] >=0]

        solutionMoves = ["".join([self.chess_map_from_index_to_alpha[i[1]], str(i[0] + 1)]) for i in temp]
        solutionMoves.sort()
        return solutionMoves

    def getQueenMoves(self, pos, color):
        solutionMoves = self.getBishopMoves(pos, color) + self.getRookMoves(pos, color)
        solutionMoves.sort()
        return solutionMoves

    def getKingMoves(self, pos, color):

        column, row = list(pos.strip().lower())
        row = int(row) - 1
        column = self.chess_map_from_alpha_to_index[column]
        i,j = row, column
        solutionMoves = []
        
        try:
            temp = self.pieces[i + 1][j]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i + 1, j])
        except:
            pass
        try:
            temp = self.pieces[i - 1][j]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i - 1, j])
        except:
            pass
        try:
            temp = self.pieces[i][j + 1]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i, j + 1])
        except:
            pass
        try:
            temp = self.pieces[i][j - 1]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i, j - 1])
        except:
            pass
        try:
            temp = self.pieces[i - 1][j - 1]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i - 1, j - 1])
        except:
            pass
        try:
            temp = self.pieces[i + 1][j + 1]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i + 1, j + 1])
        except:
            pass
        try:
            temp = self.pieces[i + 1][j - 1]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i + 1, j - 1])
        except:
            pass
        try:
            temp = self.pieces[i - 1][j + 1]
            if temp * self[i][j] <= 0:
                solutionMoves.append([i - 1, j + 1])
        except:
            pass

        # Filter all negative values
        temp = [i for i in solutionMoves if i[0] >=0 and i[1] >=0]

        solutionMoves = ["".join([self.chess_map_from_index_to_alpha[i[1]], str(i[0] + 1)]) for i in temp]
        solutionMoves.sort()
        return solutionMoves

    def getPawnMoves(self, pos, direction):

        column, row = list(pos.strip().lower())
        row = int(row) - 1
        column = self.chess_map_from_alpha_to_index[column]
        i,j = row, column
        solutionMoves = []
        
        if direction > 0:   
           
          try:
              temp = self.pieces[i + 1][j]
              if temp * self[i][j] == 0:
                  solutionMoves.append([i + 1, j])
          except:
              pass
          try:
              temp = self.pieces[i + 1][j + 1]
              if temp * self[i][j] < 0:
                  solutionMoves.append([i + 1, j + 1])
          except:
              pass
          try:
              temp = self.pieces[i + 1][j - 1]
              if temp * self[i][j] < 0:
                  solutionMoves.append([i + 1, j - 1])
          except:
              pass
          try:
              temp = self.pieces[i+2][j]
              if temp * self[i][j] == 0 and self.pieces[i+1][j] == 0 and i == 1:
                  solutionMoves.append([i+2, j])
          except:
              pass
        
    
        else:
            
          try:
              temp = self.pieces[i - 1][j]
              if temp * self[i][j] == 0:
                  solutionMoves.append([i - 1, j])
          except:
              pass
          try:
              temp = self.pieces[i - 1][j - 1]
              if temp * self[i][j] < 0:
                  solutionMoves.append([i - 1, j - 1])
          except:
              pass
          try:
              temp = self.pieces[i - 1][j + 1]
              if temp * self[i][j] < 0:
                  solutionMoves.append([i - 1, j + 1])
          except:
              pass
          try:
              temp = self.pieces[i-2][j]
              if temp * self[i][j] == 0 and self.pieces[i-1][j] == 0 and i == 6:
                  solutionMoves.append([i-2, j])
          except:
              pass
                
                
                
                        # Filter all negative values
        temp = [i for i in solutionMoves if i[0] >=0 and i[1] >=0]

        solutionMoves = ["".join([self.chess_map_from_index_to_alpha[i[1]], str(i[0] + 1)]) for i in temp]
        solutionMoves.sort()
        return solutionMoves

    def get_moves_for_square(self, square, direction):
        """Returns all the legal moves that use the given square as a base."""
        (x,y) = square
        move = self.chess_map_from_index_to_alpha[y] + str(x+1)

        # determine the color of the piece.
        piecetype, color = self.get_type(x,y)

        if piecetype == None:
            return []

        # search all possible directions.
        moves = []

        if abs(piecetype) == 1:
            moves = self.getPawnMoves(move, direction)
            # moves = self.getPawnMoves(move)
        elif abs(piecetype) ==2:
            moves = self.getKnightMoves(move, color)
        elif abs(piecetype) ==3:
            moves = self.getBishopMoves(move, color) 
        elif abs(piecetype) ==4:
            moves = self.getRookMoves(move, color)
        elif abs(piecetype) ==5:
            moves = self.getQueenMoves(move, color)
        elif abs(piecetype) ==6:
            moves = self.getKingMoves(move, color)

        ret = [(move, x) for x in moves]

        
        # return the generated move list
        return ret

    



    def execute_move(self, old_pos, move, en_passant=False):
        """Perform the given move on the board; flips pieces as necessary.
        """
        #self.direction_CURR = -self.direction_CURR
        #move = (col, row) in chess terms
        x, y = int(move[1]) - 1, self.chess_map_from_alpha_to_index[move[0]]

        x_old, y_old = int(old_pos[1]) - 1, self.chess_map_from_alpha_to_index[old_pos[0]]
        
        self[x][y] = self[x_old][y_old]
        self[x_old][y_old] = 0

        if en_passant:
            self[x_old][y_new] = 0

        #promotion
        if self[x][y] == 1:
            if x == 0 or x == 7:
                self[x][y] = 5
        
        if self[x][y] == -1:
            if x == 0 or x == 7:
                self[x][y] = -5


    def insufficientMaterial(self):
        temp = Board(self.pieces)

        wbishop = False
        bbishop = False

        firstW = True
        firstB = True

        whiteSquare = (9,9)
        blackSquare = (9,9)

        for i in range(0,8):
            for j in range (0,8):
                #white
                if temp[i][j] > 0:
                    if temp[i][j] == 6: #king
                        continue
                    elif temp[i][j] >= 4 or temp[i][j] == 1: #rook or queen or pawn
                        return False
                    elif temp[i][j] == 2:   #knight
                        
                        #A black piece has already been found
                        if firstB == False:
                            return False

                        #This is the first white knight or bishop found
                        if firstW == True:
                            firstW = False
                        else:
                            return False

                    elif temp[i][j] == 3:   #bishop
                        
                        #A black piece has already been found that is not a bishop
                        if firstB == False and bbishop == False:
                            return False

                        #This is the first white knight or bishop found
                        if firstW == True:
                            firstW = False
                            wbishop = True
                            whiteSquare = (i,j)
                        else:
                            return False

                #black
                if temp[i][j] < 0:
                    if temp[i][j] == -6: #king
                        continue
                    elif temp[i][j] <= 4 or temp[i][j] == -1: #rook or queen or pawn
                        return False
                    elif temp[i][j] == -2:   #knight
                        
                        #A white piece has already been found
                        if firstW == False:
                            return False

                        #This is the first black knight or bishop found
                        if firstB == True:
                            firstB = False
                        else:
                            return False

                    elif temp[i][j] == -3:   #bishop
                        
                        #A white piece has already been found that is not a bishop
                        if firstW == False and wbishop == False:
                            return False

                        #This is the first black knight or bishop found
                        if firstB == True:
                            firstB = False
                            bbishop = True
                            blackSquare = (i,j)
                        else:
                            return False
                        

        #At this point, we have insufficient material or two opposite color bishops
        
        #Only kings are on the board
        if (firstB and firstW) == True:
            return True

        #Only a black or a white piece exists. Insufficient material
        if (firstB or firstW) == True:
            return True

        
        #At this point, both sides have at least one bishop or one knight

        #One bishop for each player. Check the colors.
        if (bbishop and wbishop) == True:
            #function to check if they are on different colors

            xWhite, yWhite = whiteSquare
            xBlack, yBlack = blackSquare
            
            #same x
            if (xWhite % 2) == (xBlack % 2):
                #same y
                return ( (yWhite % 2) == (yBlack % 2) )
                    
                #different x
            else:
                #different y
                return ( (yWhite % 2) != (yBlack % 2) )
                    


    def is_in_check(self, old_pos, move, player, direction, en_passant = False):
        """player: player who is in check after the move
           direction: direction of OPPONENT player

        """

        x_old, y_old = int(old_pos[1]) - 1, self.chess_map_from_alpha_to_index[old_pos[0]]
        #The piece we are moving
        piece = self[x_old][y_old]

        #move = (col, row) in chess terms
        x, y = int(move[1]) - 1, self.chess_map_from_alpha_to_index[move[0]]
        captured_piece = self[x][y]
        
        flag = False
        #Do the move to check if it puts you in check
        self[x][y] = self[x_old][y_old]
        self[x_old][y_old] = 0

        if en_passant:
            temp_pawn = self[x_old][y_new]
            self[x_old][y_new] = 0

        # if self[x][y] == 6:
        #     self.wking = x,y
        # if self[x][y] == -6:
        #     self.bking = x,y


        piecetype, _ = self.get_type(x,y)

        color = player

        # if color > 0:
        #     x_king, y_king = self.wking
        # else:
        #     x_king, y_king = self.bking

        #king position
        for i in range(8):
            for j in range(8):
                if self[i][j] * color == 6:
                    x_king, y_king = i,j
                    break


        #x+
        for i in range(x_king+1, 8):
            if self[i][y_king] * color > 0:
                break
            elif self[i][y_king] * color < 0:
                enemy_piece, _ = self.get_type(i, y_king)
                if enemy_piece == 4 or enemy_piece == 5:
                    flag = True
                    break
                elif enemy_piece == 6 and i - x_king == 1:
                    flag = True
                    break
                else:
                    break
        
        if flag == True:
            #revert the board
            self[x][y] = captured_piece
            self[x_old][y_old] = piece

            if en_passant:
                self[x_old][y_new] = temp_pawn

            # if self[x_old][y_old] == 6:
            #     self.wking = x_old,y_old
            # if self[x_old][y_old] == -6:
            #     self.bking = x_old,y_old

            return flag


        #x-
        for i in range(x_king-1, -1, -1):
            if self[i][y_king] * color > 0:
                break
            elif self[i][y_king] * color < 0:
                enemy_piece, _ = self.get_type(i, y_king)
                if enemy_piece == 4 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and x_king-i == 1:
                    flag = True
                break
        
        if flag == True:
            #revert the board
            self[x][y] = captured_piece
            self[x_old][y_old] = piece

            if en_passant:
                self[x_old][y_new] = temp_pawn

            # if self[x_old][y_old] == 6:
            #     self.wking = x_old,y_old
            # if self[x_old][y_old] == -6:
            #     self.bking = x_old,y_old
            
            return flag  



        #y+
        for i in range(y_king+1, 8):
            if self[x_king][i] * color > 0:
                break
            elif self[x_king][i] * color < 0:
                enemy_piece, _ = self.get_type(x_king, i)
                if enemy_piece == 4 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and i-y_king == 1:
                    flag = True
                break
        
        if flag == True:
            #revert the board
            self[x][y] = captured_piece
            self[x_old][y_old] = piece

            if en_passant:
                self[x_old][y_new] = temp_pawn

            # if self[x_old][y_old] == 6:
            #     self.wking = x_old,y_old
            # if self[x_old][y_old] == -6:
            #     self.bking = x_old,y_old

            return flag            

        
        #y-
        for i in range(y_king-1, -1, -1):
            
            if self[x_king][i] * color > 0:
                break
            elif self[x_king][i] * color < 0:
                enemy_piece, _ = self.get_type(x_king, i)
                if enemy_piece == 4 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and y_king-i == 1:
                    flag = True
                break
        
        if flag == True:
            #revert the board
            self[x][y] = captured_piece
            self[x_old][y_old] = piece

            if en_passant:
                self[x_old][y_new] = temp_pawn

            # if self[x_old][y_old] == 6:
            #     self.wking = x_old,y_old
            # if self[x_old][y_old] == -6:
            #     self.bking = x_old,y_old
            return flag


        #diagonals
        #upper right
        for i in range(1, 8):
            if x_king+i > 7 or y_king+i > 7:
                break

            if self[x_king+i][y_king+i] * color > 0:
                break
            elif self[x_king+i][y_king+i] * color < 0:
                enemy_piece, _ = self.get_type(x_king+i, y_king+i)
                if enemy_piece == 3 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and i == 1:
                    flag = True
                elif enemy_piece == 1 and direction == -1 and i == 1: #enemy pawn above you in the diagonal can capture you only if its direction is negative
                    flag = True
                break
        
        if flag == True:
            #revert the board
            self[x][y] = captured_piece
            self[x_old][y_old] = piece

            if en_passant:
                self[x_old][y_new] = temp_pawn

            # if self[x_old][y_old] == 6:
            #     self.wking = x_old,y_old
            # if self[x_old][y_old] == -6:
            #     self.bking = x_old,y_old
            return flag
        
        #upper left
        for i in range(1, 8):
            if x_king+i > 7 or y_king-i < 0:
                break

            if self[x_king+i][y_king-i] * color > 0:
                break
            elif self[x_king+i][y_king-i] * color < 0:
                enemy_piece, _ = self.get_type(x_king+i, y_king-i)
                if enemy_piece == 3 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and i == 1:
                    flag = True
                elif enemy_piece == 1 and direction == -1 and i == 1: #enemy pawn above you in the diagonal can capture you only if its direction is negative
                    flag = True
                break

        if flag == True:
            #revert the board
            self[x][y] = captured_piece
            self[x_old][y_old] = piece

            if en_passant:
                self[x_old][y_new] = temp_pawn

            # if self[x_old][y_old] == 6:
            #     self.wking = x_old,y_old
            # if self[x_old][y_old] == -6:
            #     self.bking = x_old,y_old
            return flag

        #lower right
        for i in range(1, 8):
            if x_king-i < 0 or y_king+i > 7:
                break

            if self[x_king-i][y_king+i] * color > 0:
                break
            elif self[x_king-i][y_king+i] * color < 0:
                enemy_piece, _ = self.get_type(x_king-i, y_king+i)
                if enemy_piece == 3 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and i == 1:
                    flag = True
                elif enemy_piece == 1 and direction == 1 and i == 1: #enemy pawn below you in the diagonal can capture you only if its direction is positive
                    flag = True
                break

        if flag == True:
            #revert the board
            self[x][y] = captured_piece
            self[x_old][y_old] = piece

            if en_passant:
                self[x_old][y_new] = temp_pawn

            # if self[x_old][y_old] == 6:
            #     self.wking = x_old,y_old
            # if self[x_old][y_old] == -6:
            #     self.bking = x_old,y_old
            return flag


        #lower left
        for i in range(1, 8):
            if x_king-i < 0 or y_king-i < 0:
                break

            if self[x_king-i][y_king-i] * color > 0:
                break
            elif self[x_king-i][y_king-i] * color < 0:
                enemy_piece, _ = self.get_type(x_king-i, y_king-i)
                if enemy_piece == 3 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and i == 1:
                    flag = True
                elif enemy_piece == 1 and direction == 1 and i == 1: #enemy pawn below you in the diagonal can capture you only if its direction is positive
                    flag = True
                break

        if flag == True:
            #revert the board
            self[x][y] = captured_piece
            self[x_old][y_old] = piece

            if en_passant:
                self[x_old][y_new] = temp_pawn

            # if self[x_old][y_old] == 6:
            #     self.wking = x_old,y_old
            # if self[x_old][y_old] == -6:
            #     self.bking = x_old,y_old
            return flag

        #knight move checks

        if in_board(x_king+1, y_king+2):
            if self[x_king+1][y_king+2] * color < 0 and abs(self[x_king+1][y_king+2]) == 2:
                flag = True

        if in_board(x_king+1, y_king-2):
            if self[x_king+1][y_king-2] * color < 0 and abs(self[x_king+1][y_king-2]) == 2:
                flag = True

        if in_board(x_king+2, y_king+1):
            if self[x_king+2][y_king+1] * color < 0 and abs(self[x_king+2][y_king+1]) == 2:
                flag = True
        
        if in_board(x_king+2, y_king-1):
            if self[x_king+2][y_king-1] * color < 0 and abs(self[x_king+2][y_king-1]) == 2:
                flag = True


        if in_board(x_king-1, y_king+2):
            if self[x_king-1][y_king+2] * color < 0 and abs(self[x_king-1][y_king+2]) == 2:
                flag = True

        if in_board(x_king-1, y_king-2):
            if self[x_king-1][y_king-2] * color < 0 and abs(self[x_king-1][y_king-2]) == 2:
                flag = True

        if in_board(x_king-2, y_king+1):
            if self[x_king-2][y_king+1] * color < 0 and abs(self[x_king-2][y_king+1]) == 2:
                flag = True
        
        if in_board(x_king-2, y_king-1):
            if self[x_king-2][y_king-1] * color < 0 and abs(self[x_king-2][y_king-1]) == 2:
                flag = True
        
            #revert the board
        self[x][y] = captured_piece
        self[x_old][y_old] = piece

        if en_passant:
                self[x_old][y_new] = temp_pawn

        # if self[x_old][y_old] == 6:
        #     self.wking = x_old,y_old
        # if self[x_old][y_old] == -6:
        #     self.bking = x_old,y_old
        return flag


    


    def is_in_check_now(self, player, direction):
        flag = False

        color = player
        
        #king position
        for i in range(8):
            for j in range(8):
                if self[i][j] * color == 6:
                    x_king, y_king = i,j
                    break
                    
        #x+
        for i in range(x_king+1, 8):
            if self[i][y_king] * color > 0:
                break
            elif self[i][y_king] * color < 0:
                enemy_piece, _ = self.get_type(i, y_king)
                if enemy_piece == 4 or enemy_piece == 5:
                    flag = True
                    break
                elif enemy_piece == 6 and i - x_king == 1:
                    flag = True
                    break
                else:
                    break
        
        if flag == True:
            return flag

        #x-
        for i in range(x_king-1, -1, -1):
            if self[i][y_king] * color > 0:
                break
            elif self[i][y_king] * color < 0:
                enemy_piece, _ = self.get_type(i, y_king)
                if enemy_piece == 4 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and x_king-i == 1:
                    flag = True
                break

        if flag == True:
            return flag  



        #y+
        for i in range(y_king+1, 8):
            if self[x_king][i] * color > 0:
                break
            elif self[x_king][i] * color < 0:
                enemy_piece, _ = self.get_type(x_king, i)
                if enemy_piece == 4 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and i-y_king == 1:
                    flag = True
                break


        if flag == True:
            return flag        

        
        #y-
        for i in range(y_king-1, -1, -1):
            if self[x_king][i] * color > 0:
                break
            elif self[x_king][i] * color < 0:
                enemy_piece, _ = self.get_type(x_king, i)
                if enemy_piece == 4 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and y_king-i == 1:
                    flag = True
                break
        

        if flag == True:
            return flag


        #diagonals
        #upper right
        for i in range(1, 8):
            if x_king+i > 7 or y_king+i > 7:
                break

            if self[x_king+i][y_king+i] * color > 0:
                break
            elif self[x_king+i][y_king+i] * color < 0:
                enemy_piece, _ = self.get_type(x_king+i, y_king+i)
                if enemy_piece == 3 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and i == 1:
                    flag = True
                elif enemy_piece == 1 and direction == -1 and i == 1: #enemy pawn above you in the diagonal can capture you only if its direction is negative
                    flag = True
                break
        

        if flag == True:
            return flag
        
        #upper left
        for i in range(1, 8):
            if x_king+i > 7 or y_king-i < 0:
                break

            if self[x_king+i][y_king-i] * color > 0:
                break
            elif self[x_king+i][y_king-i] * color < 0:
                enemy_piece, _ = self.get_type(x_king+i, y_king-i)
                if enemy_piece == 3 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and i == 1:
                    flag = True
                elif enemy_piece == 1 and direction == -1 and i == 1: #enemy pawn above you in the diagonal can capture you only if its direction is negative
                    flag = True
                break


        if flag == True:
            return flag

        #lower right
        for i in range(1, 8):
            if x_king-i < 0 or y_king+i > 7:
                break

            if self[x_king-i][y_king+i] * color > 0:
                break
            elif self[x_king-i][y_king+i] * color < 0:
                enemy_piece, _ = self.get_type(x_king-i, y_king+i)
                if enemy_piece == 3 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and i == 1:
                    flag = True
                elif enemy_piece == 1 and direction == 1 and i == 1: #enemy pawn below you in the diagonal can capture you only if its direction is positive
                    flag = True
                break


        if flag == True:
            return flag


        #lower left
        for i in range(1, 8):
            if x_king-i < 0 or y_king-i < 0:
                break

            if self[x_king-i][y_king-i] * color > 0:
                break
            elif self[x_king-i][y_king-i] * color < 0:
                enemy_piece, _ = self.get_type(x_king-i, y_king-i)
                if enemy_piece == 3 or enemy_piece == 5:
                    flag = True
                elif enemy_piece == 6 and i == 1:
                    flag = True
                elif enemy_piece == 1 and direction == 1 and i == 1: #enemy pawn below you in the diagonal can capture you only if its direction is positive
                    flag = True
                break


        if flag == True:
            return flag

        #knight move checks

        if in_board(x_king+1, y_king+2):
            if self[x_king+1][y_king+2] * color < 0 and abs(self[x_king+1][y_king+2])*color == 2*(-color):
                flag = True

        if in_board(x_king+1, y_king-2):
            if self[x_king+1][y_king-2] * color < 0 and abs(self[x_king+1][y_king-2])*color == 2*(-color):
                flag = True

        if in_board(x_king+2, y_king+1):
            if self[x_king+2][y_king+1] * color < 0 and abs(self[x_king+2][y_king+1])*color == 2*(-color):
                flag = True
        
        if in_board(x_king+2, y_king-1):
            if self[x_king+2][y_king-1] * color < 0 and abs(self[x_king+2][y_king-1])*color == 2*(-color):
                flag = True


        if in_board(x_king-1, y_king+2):
            if self[x_king-1][y_king+2] * color < 0 and abs(self[x_king-1][y_king+2])*color == 2*(-color):
                flag = True

        if in_board(x_king-1, y_king-2):
            if self[x_king-1][y_king-2] * color < 0 and abs(self[x_king-1][y_king-2])*color == 2*(-color):
                flag = True

        if in_board(x_king-2, y_king+1):
            if self[x_king-2][y_king+1] * color < 0 and abs(self[x_king-2][y_king+1])*color == 2*(-color):
                flag = True
        
        if in_board(x_king-2, y_king-1):
            if self[x_king-2][y_king-1] * color < 0 and abs(self[x_king-2][y_king-1])*color == 2*(-color):
                flag = True


        return flag
        


    # material_count()

    #castling()

    #en_passant()
