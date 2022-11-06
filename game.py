import numpy as np

class ChessGame():  

    #THIS BELONGS IN CHESSGAME CLASS  
    pieces =   {-6:"bking",
                -5:"bqueen",
                -4:"brook", 
                -3:"bbishop",
                -2:"bknight",
                -1:"bpawn",
                 0:"-",
                1:"wpawn",
                2:"wknight",
                3:"wbishop",
                4:"wrook",
                5:"wqueen",
                6:"wking" }

    def __init__(self): 
        self.n =8
        self.board = Board(self.n) 
        self.progress = 0 
        self.rep = 0 
        self.direction = 1 
        self.moves = 0         
        
        self.en_passant = []

        #dict for counting the number a position has been  reached 
        self.posCounter = {} 
        
        #starting position 
        self.posCounter[self.stringRepresentation(self.board.pieces)] = 1
        

    def getInitBoard(self):  # return initial board (numpy board)         
        b=Board(self.n) 
        return  np.array(b.pieces)
        

    def revertBoard(self): 

        self.board = Board(self.n) # ??? 

        self.progress=0
        self.rep=0
        self.direction=1
        self.moves=0

        self.en_passant = []

        #dict for counting the number a position has been reached
        self.posCounter = {}
        #starting position
        self.posCounter[self.stringRepresentation(self.board.pieces)] = 1
        


    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        size = (64*64) # maybe add castling etc (+74)
        return size
   
    def getValidMoves(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)
        # for i in range(8):
        #     for j in range(8):
        #         if b.pieces[i][j] == 6:
        #             b.wking = (i,j)
        #         elif b.pieces[i][j] == -6:
        #             b.bking = (i,j)
                
        b.direction_CURR=player

        legalMoves =  b.get_legal_moves(player, self.direction) #(old_pos, new_pos)
        size = self.getActionSize()
        valids = np.zeros((64, 64))
        moves = [x for x in legalMoves if not b.is_in_check(x[0],x[1],player,-self.direction)]

        #en passant list is list of touples (x,y)
        #the first item is the square the pawn will land
        if len(self.en_passant)>0:
            target = self.en_passant[0] #where the pawn will go 
            new = ([b.chess_map_from_index_to_alpha[target[1]], str(target[0] + 1)])
            
            for i in range(1,len(en_passant)):
                old = ([b.chess_map_from_index_to_alpha[i[1]], str(i[0] + 1)])

                if b.is_in_check(old,new,player,-self.direction,en_passant=True) == False:
                    moves.append(i,target)
            
        for old, new in moves:
            row = int(old[1]) - 1
            column = b.chess_map_from_alpha_to_index[old[0]]
            old = (row, column)
            
            row = int(new[1]) - 1
            column = b.chess_map_from_alpha_to_index[new[0]]
            new = (row, column)

            valids[8*old[0] + old[1]][8*new[0] + new[1]] = 1


        # #!!!add castling and underpromotions!!!
        # padding = np.zeros(74)

        # return np.append(valids.flatten(),padding)
        return valids.flatten()

    
    def getGameEnded(self,board,player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        
        b = Board(self.n)
        b.pieces = np.copy(board)

        #--------------------------------------
        #These checks also happen in MCTS.search()
        
        #3-fold repetition draw
        stringB = self.stringRepresentation(b.pieces)
        if stringB in self.posCounter:
            if self.posCounter[stringB] >= 3:
               
                # print(stringB)
                # print(f'{self.posCounter[stringB]} -> number')
                return 1e-4

        #progress (pawn moves)
        if self.progress >= 50:
            # draw has a very little value 
            
            return 1e-4
            
        #--------------------------------------



        b.direction_CURR=player

        #insufficient material
        if b.insufficientMaterial():
            # draw has a very little value 
            return 1e-4

        #if opponent is in check
        if b.is_in_check_now(-player, self.direction): 
           
            return player

        if b.has_legal_moves(player, self.direction):
            return 0
        else:
            if b.is_in_check_now(player, -self.direction): 
                
                return -player
            else:
                #stalemate
                # draw has a very little value 
                return 1e-4
        


    def getNextState(self, board, player, action):
        # return next (board,player)
        # action must be a valid move

        self.progress += 1
        self.moves += 1

        b = Board(self.n)
        b.pieces = np.copy(board)

      
        b.direction_CURR=-player
        old, new = np.unravel_index(action, (64,64))

        x_old, y_old = np.unravel_index(old, (8,8))
        x_new, y_new = np.unravel_index(new, (8,8))

        # capture
        if b[x_old][y_old] * b[x_new][y_new] < 0:
            self.progress = 0
        
        # pawn move
        if b[x_old][y_old] == 1 or b[x_old][y_old] == -1:
            self.progress = 0



        if b[x_new][y_new] == 6 or b[x_new][y_new] == -6:
            print("--------------------------------")
            print("ERROR! KING CAPTURE!")
            print(b.pieces)
            print(x_old,y_old)
            print(x_new,y_new)

            assert(False)


        old = b.chess_map_from_index_to_alpha[y_old] + str(x_old+1)
        new = b.chess_map_from_index_to_alpha[y_new] + str(x_new+1)

        en_passant_flag = False
        #en passant move 
        if b[x_old][y_old] == 1 or b[x_old][y_old] == -1:
            if abs(x_old-x_new) == 1 and abs(y_old-y_new) == 1 and b[x_new][y_new] == 0:
                en_passant_flag = True

        b.execute_move(old, new, en_passant_flag)
       
        self.direction = - self.direction

        self.en_passant = []
        if b[x_old][y_old] == 1 or b[x_old][y_old] == -1:
            self.en_passant.append( (x_old+x_new)/2, y_new )
            if abs(x_old - x_new) == 2:
                if y_new+1 < 8:
                    self.en_passant.append(x_new,y_new+1)
                if y_new-1 > 0:
                    self.en_passant.append(x_new,y_new-1)


        stringB = self.stringRepresentation(self.getCanonicalForm(b.pieces,player))
        if stringB in self.posCounter:
            self.posCounter[stringB] += 1
        else:
            self.posCounter[stringB] = 1

        return (b.pieces, -player)


    def stringRepresentation(self, board):
        return str(np.array(board))

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):

        assert(len(pi) == 64*64)

        return [(board, list(pi))]

        # # mirror, rotational        
        # pi_board = np.reshape(pi, (64, 64))
        # l = []
        # for i in range(1, 5):
        #     for j in [True, False]:
        #         newB = np.rot90(board, i)
        #         newPi = np.rot90(pi_board, i)
        #         if j:
        #             newB = np.fliplr(newB)
        #             newPi = np.fliplr(newPi)
        #         l += [(newB, list(newPi.ravel()))]
        # return l
