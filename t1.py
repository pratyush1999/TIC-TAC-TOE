'''
Naming convention followed across the simulator is:
- BigBoard = big_boards[0] + big_boards[1]
- big_board[i] = small_boards[0] + small_boards[1] + small_boards[2] + .... + small_boards[7] + small_boards[8]
- small_board[i] = cell[0] + cell[1] + cell[2] + .... + cell[7] + cell[8]
'''

import sys
import random
import signal
import time
import copy
import traceback
from dj import Player7
from parth import Team72v3
TIME = 24
MAX_PTS = 86


class TimedOutExc(Exception):
    pass


def handler(signum, frame):
    # print 'Signal handler called with signal', signum
    raise TimedOutExc()


class Random_Player():
    def __init__(self):
        pass

    def move(self, board, old_move, flag):
        # You have to implement the move function with the same signature as this
        # Find the list of valid cells allowed
        cells = board.find_valid_move_cells(old_move)
        return cells[random.randrange(len(cells))]


class Manual_Player:
    def __init__(self):
        self.hashx= [[[0 for k in range(3)] for j in range(3)] for i in range(2)]
        self.ply = "x"
        self.conj = "o"
        self.starttime=0
        self.dict={}
        self.block_hash=[[[0 for k in range(3)] for j in range(3)] for i in range(2)]
        self.block_zob=[(2**i)for i in range(18)]
        self.infi=1000000000
        self.level=2
        self.ply_blk_won=0
        self.conj_blk_won=0
        self.ply_last_blk_won=0
    def init_zobrist(self, board):
    	self.dict={}
    	for k in range(2):
	    	for i in range(3):
	    		for j in range(3):
	    			self.block_hash[k][i][j]=0
	    			c=0
	    			for m in range(3):
	    				for z in range(3):
	    					if board.big_boards_status[k][3*i+m][3*j+z]==self.ply:
	    						self.block_hash[k][i][j]^=self.block_zob[2*c]
	    					elif board.big_boards_status[k][3*i+m][3*j+z]==self.conj:
	    						self.block_hash[k][i][j]^=self.block_zob[2*c+1]
	    					c+=1
	            
	    						
    # def chck(self,board,old_move,ply):
    #     conj = self.conj
    #     ply = self.ply
    #     i=old_move[0]
    #     j=old_move[1]/3
    #     k=old_move[2]/3
    #     for m in range(3):
    #         countp = 0
    #         countj = 0
    #         for z in range(3):
    #             if board.big_boards_status[i][j*3+m][k*3+z] == ply:
    #                 countp = countp + 1
    #             elif board.big_boards_status[i][j*3+m][k*3+z] == conj:
    #                 countj = countj + 1
    #         if countp == 3 :
    #             return 1000
    #         elif countp == 1 and countj == 2:
    #             return 500    
    #     for m in range(3):
    #         countp = 0
    #         countj = 0
    #         for z in range(3):
    #             if board.big_boards_status[i][j*3+z][k*3+m] == ply:
    #                 countp = countp + 1
    #             elif board.big_boards_status[i][j*3+z][k*3+m] == conj:
    #                 countj = countj + 1
    #         if countp == 3 :
    #             return 1000
    #         elif countp == 1 and countj == 2:
    #             return 500  
        
    #     countp = 0
    #     countj = 0
    #     for m in range(3):
    #         if board.big_boards_status[i][j*3+m][k*3+m] == ply:
    #             countp = countp + 1
    #         elif board.big_boards_status[i][j*3+m][k*3+m] == conj:
    #             countj = countj + 1
    #     if countp == 3 :
    #             return 1000
    #     elif countp == 1 and countj == 2:
    #             return 500  

    #     countp = 0
    #     countj = 0
    #     for m in range(3):
    #         if board.big_boards_status[i][j*3 + 2 - m][k*3 + 2 - m] == ply:
    #             countp = countp + 1
    #         elif board.big_boards_status[i][j*3 + 2 - m][k*3 + 2 - m] == conj:
    #             countj = countj + 1
    #     if countp == 3 :
    #             return 1000
    #     elif countp == 1 and countj == 2:
    #             return 500  

    #     return 0

    def update_zubrist_block(self, move, ply):
    	if ply==self.ply:
    		self.block_hash[move[0]][move[1]/3][move[2]/3]^=self.block_zob[(3*(move[1]%3)+(move[2]%3))<<1]
    	else:
    		self.block_hash[move[0]][move[1]/3][move[2]/3]^=self.block_zob[((3*(move[1]%3)+(move[2]%3))<<1)+1]

    def move(self, board, old_move, flag):
        # print 'Enter your move: <format:board row column> (you\'re playing with', flag + ")"
        # mvp = raw_input()
        # mvp = mvp.split()
        if self.conj == flag:
           self.conj = "x"
           self.ply = "o"

        self.ply_blk_won=0
        self.conj_blk_won=0
        if self.ply_last_blk_won:
            self.ply_blk_won^=1

        cells = board.find_valid_move_cells(old_move)
      	self.starttime=time.time()
        bestval = -self.infi
      	self.init_zobrist(board)
        selected=cells[random.randrange(len(cells))]
        self.level=5
       
        if old_move==(-1,-1,-1):
            return selected

        while self.level<6:
            self.init_zobrist(board)    
            for c in cells:
                temp_big_boards_status = board.big_boards_status[c[0]][c[1]][c[2]]
                temp_small_boards_status = board.small_boards_status[c[0]
                                                                     ][c[1]/3][c[2]/3]
                self.update_zubrist_block(c, flag)
                temp_ply_blk_won=self.ply_blk_won
                temp_conj_blk_won=self.conj_blk_won
                jhuth, won=board.update(old_move, c, flag)
                if won:
                   self.ply_blk_won^=1
                d=-self.infi
                if self.ply_blk_won:
                    d = self.minimax(1, 0, -self.infi, self.infi, c, flag, board)
                    self.ply_blk_won=0                 
                else:
                    d = self.minimax(1, 0, -self.infi, self.infi, c, self.conj, board) 
                self.update_zubrist_block(c, flag)
                self.ply_blk_won=temp_ply_blk_won
                self.conj_blk_won=temp_conj_blk_won
                if d > bestval:
                    bestval = d
                    selected = c
                board.big_boards_status[c[0]][c[1]
                                              ][c[2]] = temp_big_boards_status
                board.small_boards_status[c[0]][c[1] /
                                                3][c[2]/3] = temp_small_boards_status
            self.level+=1

        c=selected
        temp_big_boards_status = board.big_boards_status[c[0]][c[1]][c[2]]
        temp_small_boards_status = board.small_boards_status[c[0]][c[1]/3][c[2]/3]
        val, won=board.update(old_move, selected, flag)
        board.big_boards_status[c[0]][c[1]][c[2]] = temp_big_boards_status
        board.small_boards_status[c[0]][c[1]/3][c[2]/3] = temp_small_boards_status
        if won:
            self.ply_last_blk_won^=1
        else:
            self.ply_last_blk_won=0
        return selected

    def new_heuristic(self, ply, move, board):
    	boardstate=board.find_terminal_state()
    	if boardstate[1]=='WON':
    		if ply==self.ply:
    			return self.infi
    		else:
    			return -self.infi
    	for i in range(2):
    		for j in range(3):
    			for k in range(3):
    				if board.small_boards_status[i][j][k]==self.ply:
    					self.hashx[i][j][k]=self.infi/100
    				elif board.small_boards_status[i][j][k]==self.conj:
    					self.hashx[i][j][k]=-self.infi/100
    				else:
    					if self.block_hash[i][j][k] in self.dict:
    						self.hashx[i][j][k]=self.dict[self.block_hash[i][j][k]]
    						if len(self.dict)>100:
    							self.dict={}
    					else:
    						self.hashx[i][j][k]=self.computecost(board, i, j, k)
    						self.dict[self.block_hash[i][j][k]]=self.hashx[i][j][k]
    	return self.computeTotalCost(board)
#        self.inc_costs = [0,1, 100, 10000, 100000]
    def computeTotalCost(self, board):
        ohash=0
        for k in range(2):
            for i in range(3):
                sumx = 0
                countp=0
                countq=0
                for j in range(3):
                    sumx = sumx + self.hashx[k][i][j]
                    if board.small_boards_status[k][i][j]==self.ply:
                        countp+=1
                    if board.small_boards_status[k][i][j]==self.conj:
                        countq+=1
                if countp==0 or countq==0:
                    ohash+=sumx

            for i in range(3):
                sumx = 0
                countp=0
                countq=0
                for j in range(3):
                    sumx = sumx + self.hashx[k][j][i]
                    if board.small_boards_status[k][j][i]==self.ply:
                        countp+=1
                    if board.small_boards_status[k][j][i]==self.conj:
                        countq+=1
                if countp==0 or countq==0:
                    ohash+=sumx                    
               
            sumx = 0
            countp=0
            countq=0
            for i in range(3):
                sumx = sumx + self.hashx[k][i][i]
                if board.small_boards_status[k][i][i]==self.ply:
                    countp+=1
                if board.small_boards_status[k][i][i]==self.conj:
                    countq+=1
            if countp==0 or countq==0:
                ohash+=sumx           

            sumx = 0
            countp=0
            countq=0
            for i in range(3):
                sumx = sumx + self.hashx[k][2 - i][2 - i]
                if board.small_boards_status[k][2-i][2-i]==self.ply:
                    countp+=1
                if board.small_boards_status[k][2-i][2-i]==self.conj:
                    countq+=1
            if countp==0 or countq==0:
                ohash+=sumx            
        if ohash>0:
            return ohash

        for i in range(2):
            for j in range(3):
                for k in range(3):
                    ohash+=self.hashx[i][j][k]
        return ohash
    def computecost(self, board, i, j, k):
    	conj = self.conj
        ply = self.ply
        self.hashx[i][j][k]=0
        for m in range(3):
            countp = 0
            countj = 0
            for z in range(3):
                if board.big_boards_status[i][j*3+m][k*3+z] == ply:
                    countp = countp + 1
                elif board.big_boards_status[i][j*3+m][k*3+z] == conj:
                    countj = countj + 1
            if countp == 3:
                self.hashx[i][j][k] = self.hashx[i][j][k] + 10000
            elif countp == 2 and countj == 0:
                self.hashx[i][j][k] = self.hashx[i][j][k] + 100
            elif countp == 0 and countj == 2:
                self.hashx[i][j][k] = self.hashx[i][j][k] - 100
            elif countp == 0 and countj == 3:
                self.hashx[i][j][k] = self.hashx[i][j][k] - 10000
            elif countp == 1 and countj == 0:
                self.hashx[i][j][k] = self.hashx[i][j][k] + 1
            elif countp == 0 and countj == 1:
                self.hashx[i][j][k] = self.hashx[i][j][k] - 1

        for m in range(3):
            countp = 0
            countj = 0
            for z in range(3):
                if board.big_boards_status[i][j*3+z][k*3+m] == ply:
                    countp = countp + 1
                elif board.big_boards_status[i][j*3+z][k*3+m] == conj:
                    countj = countj + 1
            if countp == 3:
                self.hashx[i][j][k] = self.hashx[i][j][k] + 10000
            elif countp == 2 and countj == 0:
                self.hashx[i][j][k] = self.hashx[i][j][k] + 100
            elif countp == 0 and countj == 2:
                self.hashx[i][j][k] = self.hashx[i][j][k] - 100
            elif countp == 0 and countj == 3:
                self.hashx[i][j][k] = self.hashx[i][j][k] - 10000
            elif countp == 1 and countj == 0:
                self.hashx[i][j][k] = self.hashx[i][j][k] + 1
            elif countp == 0 and countj == 1:
                self.hashx[i][j][k] = self.hashx[i][j][k] - 1
        countp = 0
        countj = 0
        for m in range(3):
            if board.big_boards_status[i][j*3+m][k*3+m] == ply:
                countp = countp + 1
            elif board.big_boards_status[i][j*3+m][k*3+m] == conj:
                countj = countj + 1
        if countp == 3:
            self.hashx[i][j][k] = self.hashx[i][j][k] + 10000
        elif countp == 2 and countj == 0:
            self.hashx[i][j][k] = self.hashx[i][j][k] + 100
        elif countp == 0 and countj == 2:
            self.hashx[i][j][k] = self.hashx[i][j][k] - 100
        elif countp == 0 and countj == 3:
            self.hashx[i][j][k] = self.hashx[i][j][k] - 10000
        elif countp == 1 and countj == 0:
            self.hashx[i][j][k] = self.hashx[i][j][k] + 1
        elif countp == 0 and countj == 1:
            self.hashx[i][j][k] = self.hashx[i][j][k] - 1
        countp = 0
        countj = 0
        for m in range(3):
            if board.big_boards_status[i][j*3 + 2 - m][k*3 + 2 - m] == ply:
                countp = countp + 1
            elif board.big_boards_status[i][j*3 + 2 - m][k*3 + 2 - m] == conj:
                countj = countj + 1
        if countp == 3:
            self.hashx[i][j][k] = self.hashx[i][j][k] + 10000
        elif countp == 2 and countj == 0:
            self.hashx[i][j][k] = self.hashx[i][j][k] + 100
        elif countp == 0 and countj == 2:
            self.hashx[i][j][k] = self.hashx[i][j][k] - 100
        elif countp == 0 and countj == 3:
            self.hashx[i][j][k] = self.hashx[i][j][k] - 10000
        elif countp == 1 and countj == 0:
            self.hashx[i][j][k] = self.hashx[i][j][k] + 1
        elif countp == 0 and countj == 1:
            self.hashx[i][j][k] = self.hashx[i][j][k] - 1
    	return self.hashx[i][j][k]
	
    # def heuristic(self, ply, old_move, depth, board):
    #     conj = self.conj
    #     ply = self.ply
    #     i=old_move[0]
    #     j=old_move[1]/3
    #     k=old_move[2]/3
    #     temp=self.hashx[i][j][k]
    #     self.hashx[i][j][k]=0
    #     for m in range(3):
    #         countp = 0
    #         countj = 0
    #         for z in range(3):
    #             if board.big_boards_status[i][j*3+m][k*3+z] == ply:
    #                 countp = countp + 1
    #             elif board.big_boards_status[i][j*3+m][k*3+z] == conj:
    #                 countj = countj + 1
    #         if countp == 3:
    #             self.hashx[i][j][k] = self.hashx[i][j][k] + 100
    #         elif countp == 2 and countj == 0:
    #             self.hashx[i][j][k] = self.hashx[i][j][k] + 10
    #         elif countp == 0 and countj == 2:
    #             self.hashx[i][j][k] = self.hashx[i][j][k] - 10
    #         elif countp == 0 and countj == 3:
    #             self.hashx[i][j][k] = self.hashx[i][j][k] - 100
    #         elif countp == 1 and countj == 0:
    #             self.hashx[i][j][k] = self.hashx[i][j][k] + 1
    #         elif countp == 0 and countj == 1:
    #             self.hashx[i][j][k] = self.hashx[i][j][k] - 1

    #     for m in range(3):
    #         countp = 0
    #         countj = 0
    #         for z in range(3):
    #             if board.big_boards_status[i][j*3+z][k*3+m] == ply:
    #                 countp = countp + 1
    #             elif board.big_boards_status[i][j*3+z][k*3+m] == conj:
    #                 countj = countj + 1
    #         if countp == 3:
    #             self.hashx[i][j][k] = self.hashx[i][j][k] + 100
    #         elif countp == 2 and countj == 0:
    #             self.hashx[i][j][k] = self.hashx[i][j][k] + 10
    #         elif countp == 0 and countj == 2:
    #             self.hashx[i][j][k] = self.hashx[i][j][k] - 10
    #         elif countp == 0 and countj == 3:
    #             self.hashx[i][j][k] = self.hashx[i][j][k] - 100
    #         elif countp == 1 and countj == 0:
    #             self.hashx[i][j][k] = self.hashx[i][j][k] + 1
    #         elif countp == 0 and countj == 1:
    #             self.hashx[i][j][k] = self.hashx[i][j][k] - 1
    #     countp = 0
    #     countj = 0
    #     for m in range(3):
    #         if board.big_boards_status[i][j*3+m][k*3+m] == ply:
    #             countp = countp + 1
    #         elif board.big_boards_status[i][j*3+m][k*3+m] == conj:
    #             countj = countj + 1
    #     if countp == 3:
    #         self.hashx[i][j][k] = self.hashx[i][j][k] + 100
    #     elif countp == 2 and countj == 0:
    #         self.hashx[i][j][k] = self.hashx[i][j][k] + 10
    #     elif countp == 0 and countj == 2:
    #         self.hashx[i][j][k] = self.hashx[i][j][k] - 10
    #     elif countp == 0 and countj == 3:
    #         self.hashx[i][j][k] = self.hashx[i][j][k] - 100
    #     elif countp == 1 and countj == 0:
    #         self.hashx[i][j][k] = self.hashx[i][j][k] + 1
    #     elif countp == 0 and countj == 1:
    #         self.hashx[i][j][k] = self.hashx[i][j][k] - 1
    #     countp = 0
    #     countj = 0
    #     for m in range(3):
    #         if board.big_boards_status[i][j*3 + 2 - m][k*3 + 2 - m] == ply:
    #             countp = countp + 1
    #         elif board.big_boards_status[i][j*3 + 2 - m][k*3 + 2 - m] == conj:
    #             countj = countj + 1
    #     if countp == 3:
    #         self.hashx[i][j][k] = self.hashx[i][j][k] + 100
    #     elif countp == 2 and countj == 0:
    #         self.hashx[i][j][k] = self.hashx[i][j][k] + 10
    #     elif countp == 0 and countj == 2:
    #         self.hashx[i][j][k] = self.hashx[i][j][k] - 10/5
    #     elif countp == 0 and countj == 3:
    #         self.hashx[i][j][k] = self.hashx[i][j][k] - 100/5
    #     elif countp == 1 and countj == 0:
    #         self.hashx[i][j][k] = self.hashx[i][j][k] + 1
    #     elif countp == 0 and countj == 1:
    #         self.hashx[i][j][k] = self.hashx[i][j][k] - 1/5

    #     ohash = 0
    #     if depth<depth_limit:
    #         return ohash
    #     self.hashx[i][j][k]=temp    
    #     for k in range(2):
    #         for i in range(3):
    #             sumx = 0
    #             for j in range(3):
    #                 sumx = sumx + self.hashx[k][i][j]
    #             if abs(sumx) >= 0 and abs(sumx) < 1:
    #                 ohash = ohash + sumx
    #             elif abs(sumx) >= 1 and abs(sumx) < 2:
    #                 ohash = ohash + 1*(sumx-1)/abs(sumx-1) + (10-1)*(sumx-1)
    #             elif abs(sumx) >= 2 and abs(sumx) < 3:
    #                 ohash = ohash + 10*(sumx-2)/abs(sumx-2) + (100-90)*(sumx-2)
    #             else:
    #                 ohash=100*sumx/abs(sumx)

    #         for i in range(3):
    #             sumx = 0
    #             for j in range(3):
    #                 sumx = sumx + self.hashx[k][j][i]
    #             if abs(sumx) >= 0 and abs(sumx) < 1:
    #                 ohash = ohash + sumx
    #             elif abs(sumx) >= 1 and abs(sumx) < 2:
    #                 ohash = ohash + 1*(sumx-1)/abs(sumx-1) + (10-1)*(sumx-1)
    #             elif abs(sumx) >= 2 and abs(sumx) < 3:
    #                 ohash = ohash + 10*(sumx-2)/abs(sumx-2) + (100-90)*(sumx-2)
    #             else:
    #                 ohash=100*sumx/abs(sumx)
    #         sumx = 0

    #         for i in range(3):
    #             sumx = sumx + self.hashx[k][i][i]
    #         if abs(sumx) >= 0 and abs(sumx) < 1:
    #             ohash = ohash + sumx
    #         elif abs(sumx) >= 1 and abs(sumx) < 2:
    #             ohash = ohash + 1*(sumx-1)/abs(sumx-1) + (10-1)*(sumx-1)
    #         elif abs(sumx) >= 2 and abs(sumx) < 3:
    #             ohash = ohash + 10*(sumx-2)/abs(sumx-2) + (100-90)*(sumx-2)
    #         else:
    #             ohash=100*sumx/abs(sumx)

    #         sumx = 0
    #         for i in range(3):
    #             sumx = sumx + self.hashx[k][2 - i][2 - i]
    #         if abs(sumx) >= 0 and abs(sumx) < 1:
    #             ohash = ohash + sumx
    #         elif abs(sumx) >= 1 and abs(sumx) < 2:
    #             ohash = ohash + 1*(sumx-1)/abs(sumx-1) + (10-1)*(sumx-1)
    #         elif abs(sumx) >= 2 and abs(sumx) < 3:
    #             ohash = ohash + 10*(sumx-2)/abs(sumx-2) + (100-90)*(sumx-2)
    #         else:
    #             ohash=100*sumx/abs(sumx)

    #     return ohash

    def minimax(self, depth, maximise, alpha, beta, old_move, ply, board):
        conj = "o"
        if conj == ply:
            conj = "x"

        if self.ply==ply:
            maximise=1
        else:
            maximise=0

        if  board.find_terminal_state()!= ('CONTINUE', '-')or depth>=self.level:
        	return self.new_heuristic(conj, old_move, board)
        	
        possible_moves = board.find_valid_move_cells(old_move)
        
        if maximise:
            bestvalue = -self.infi
            for c in possible_moves:
                temp_big_boards_status = board.big_boards_status[c[0]][c[1]][c[2]]
                temp_small_boards_status = board.small_boards_status[c[0]][c[1]/3][c[2]/3]
                val, won=board.update(old_move, c, ply)
                temp_ply_blk_won=self.ply_blk_won
                temp_conj_blk_won=self.conj_blk_won
                if won:
                    if self.ply==ply:
                        self.ply_blk_won^=1
                    else:
                        self.conj_blk_won^=1
               	self.update_zubrist_block(c, ply)
                val=-self.infi
                if self.ply==ply and self.ply_blk_won:
                    val = self.minimax(depth+1, 0, alpha, beta, c, ply, board)
                    self.ply_blk_won=0
                elif self.ply!=ply and self.conj_blk_won:
                    val = self.minimax(depth+1, 0, alpha, beta, c, ply, board) 
                    self.conj_blk_won=0                   
                else:
                    val = self.minimax(depth+1, 0, alpha, beta, c, conj, board) 
                bestvalue = max(val, bestvalue)
                alpha = max(alpha, bestvalue)
                board.big_boards_status[c[0]][c[1]
                                              ][c[2]] = temp_big_boards_status
                board.small_boards_status[c[0]][c[1] /
                                                3][c[2]/3] = temp_small_boards_status
                self.update_zubrist_block(c, ply)
                self.ply_blk_won=temp_ply_blk_won
                self.conj_blk_won=temp_conj_blk_won
                if beta <= alpha:
                    return bestvalue
            return bestvalue
        else:
            bestvalue = self.infi
            for c in possible_moves:
                temp_big_boards_status = board.big_boards_status[c[0]][c[1]][c[2]]
                temp_small_boards_status = board.small_boards_status[c[0]
                                                                     ][c[1]/3][c[2]/3]
                val, won=board.update(old_move, c, ply)
                temp_ply_blk_won=self.ply_blk_won
                temp_conj_blk_won=self.conj_blk_won
                if won:
                    if self.ply==ply:
                        self.ply_blk_won^=1
                    else:
                        self.conj_blk_won^=1
                self.update_zubrist_block(c, ply)
                val=-self.infi
                if self.ply==ply and self.ply_blk_won:
                    val = self.minimax(depth+1, 0, alpha, beta, c, ply, board)
                    self.ply_blk_won=0
                elif self.ply!=ply and self.conj_blk_won:
                    val = self.minimax(depth+1, 0, alpha, beta, c, ply, board) 
                    self.conj_blk_won=0                   
                else:
                    val = self.minimax(depth+1, 0, alpha, beta, c, conj, board) 

                bestvalue = min(val, bestvalue)
                beta = min(beta, bestvalue)
                board.big_boards_status[c[0]][c[1]
                                              ][c[2]] = temp_big_boards_status
                board.small_boards_status[c[0]][c[1] /
                                                3][c[2]/3] = temp_small_boards_status
                self.update_zubrist_block(c, ply)
                self.ply_blk_won=temp_ply_blk_won
                self.conj_blk_won=temp_conj_blk_won
                if beta <= alpha:
                    return bestvalue
            return bestvalue


class BigBoard:

    def __init__(self):
        # big_boards_status is the game board
        # small_boards_status shows which small_boards have been won/drawn and by which player
        self.big_boards_status = (
            [['-' for i in range(9)] for j in range(9)], [['-' for i in range(9)] for j in range(9)])
        self.small_boards_status = (
            [['-' for i in range(3)] for j in range(3)], [['-' for i in range(3)] for j in range(3)])

 
        	
    def print_board(self):
        # for printing the state of the board
        print '================BigBoard State================'
        for i in range(9):
            if i % 3 == 0:
                print
            for k in range(2):
                for j in range(9):
                    if j % 3 == 0:
                        print "",
                    print self.big_boards_status[k][i][j],
                if k == 0:
                    print "   ",
            print
        print

        print '==============SmallBoards States=============='
        for i in range(3):
            for k in range(2):
                for j in range(3):
                    print self.small_boards_status[k][i][j],
                if k == 0:
                    print "  ",
            print
        print '=============================================='
        print
        print

    def find_valid_move_cells(self, old_move):
        # returns the valid cells allowed given the last move and the current board state
        allowed_cells = []
        allowed_small_board = [old_move[1] % 3, old_move[2] % 3]
        # checks if the move is a free move or not based on the rules
        if old_move == (-1, -1, -1) or (self.small_boards_status[0][allowed_small_board[0]][allowed_small_board[1]] != '-' and self.small_boards_status[1][allowed_small_board[0]][allowed_small_board[1]] != '-'):
            for k in range(2):
                for i in range(9):
                    for j in range(9):
                        if self.big_boards_status[k][i][j] == '-' and self.small_boards_status[k][i/3][j/3] == '-':
                            allowed_cells.append((k, i, j))

        else:
            for k in range(2):
                if self.small_boards_status[k][allowed_small_board[0]][allowed_small_board[1]] == "-":
                    for i in range(3*allowed_small_board[0], 3*allowed_small_board[0]+3):
                        for j in range(3*allowed_small_board[1], 3*allowed_small_board[1]+3):
                            if self.big_boards_status[k][i][j] == '-':
                                allowed_cells.append((k, i, j))

        return allowed_cells

    def find_terminal_state(self):
        # checks if the game is over(won or drawn) and returns the player who have won the game or the player who has higher small_boards in case of a draw

        cntx = 0
        cnto = 0
        cntd = 0

        for k in range(2):
            bs = self.small_boards_status[k]
            for i in range(3):
                for j in range(3):
                    if bs[i][j] == 'x':
                        cntx += 1
                    if bs[i][j] == 'o':
                        cnto += 1
                    if bs[i][j] == 'd':
                        cntd += 1
            for i in range(3):
                row = bs[i]
                col = [x[i] for x in bs]
                # print row,col
                # checking if i'th row or i'th column has been won or not
                if (row[0] == 'x' or row[0] == 'o') and (row.count(row[0]) == 3):
                    return (row[0], 'WON')
                if (col[0] == 'x' or col[0] == 'o') and (col.count(col[0]) == 3):
                    return (col[0], 'WON')
            # check diagonals
            if(bs[0][0] == bs[1][1] == bs[2][2]) and (bs[0][0] == 'x' or bs[0][0] == 'o'):
                return (bs[0][0], 'WON')
            if(bs[0][2] == bs[1][1] == bs[2][0]) and (bs[0][2] == 'x' or bs[0][2] == 'o'):
                return (bs[0][2], 'WON')

        if cntx+cnto+cntd < 18:  # if all small_boards have not yet been won, continue
            return ('CONTINUE', '-')
        elif cntx+cnto+cntd == 18:  # if game is drawn
            return ('NONE', 'DRAW')

    def check_valid_move(self, old_move, new_move):
        # checks if a move is valid or not given the last move
        if (len(old_move) != 3) or (len(new_move) != 3):
            return False
        for i in range(3):
            if (type(old_move[i]) is not int) or (type(new_move[i]) is not int):
                return False
        if (old_move != (-1, -1, -1)) and (old_move[0] < 0 or old_move[0] > 1 or old_move[1] < 0 or old_move[1] > 8 or old_move[2] < 0 or old_move[2] > 8):
            return False
        cells = self.find_valid_move_cells(old_move)
        return new_move in cells

    def update(self, old_move, new_move, ply):
        # updating the game board and small_board status as per the move that has been passed in the arguements
        if(self.check_valid_move(old_move, new_move)) == False:
            return 'UNSUCCESSFUL', False

        self.big_boards_status[new_move[0]][new_move[1]][new_move[2]] = ply

        x = new_move[1]/3
        y = new_move[2]/3
        k = new_move[0]
        fl = 0

        # checking if a small_board has been won or drawn or not after the current move
        bs = self.big_boards_status[k]
        for i in range(3):
            # checking for horizontal pattern(i'th row)
            if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == ply):
                self.small_boards_status[k][x][y] = ply
                return 'SUCCESSFUL', True
            # checking for vertical pattern(i'th column)
            if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == ply):
                self.small_boards_status[k][x][y] = ply
                return 'SUCCESSFUL', True
        # checking for diagonal patterns
        # diagonal 1
        if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == ply):
            self.small_boards_status[k][x][y] = ply
            return 'SUCCESSFUL', True
        # diagonal 2
        if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == ply):
            self.small_boards_status[k][x][y] = ply
            return 'SUCCESSFUL', True
        # checking if a small_board has any more cells left or has it been drawn
        for i in range(3):
            for j in range(3):
                if bs[3*x+i][3*y+j] == '-':
                    return 'SUCCESSFUL', False
        self.small_boards_status[k][x][y] = 'd'

        return 'SUCCESSFUL', False




def player_turn(game_board, old_move, obj, ply, opp, flg):
    temp_big_boards_status = copy.deepcopy(game_board.big_boards_status)
    temp_small_boards_status = copy.deepcopy(game_board.small_boards_status)
    signal.alarm(TIME)
    WINNER = ''
    MESSAGE = ''
    pts = {"P1": 0, "P2": 0}
    to_break = False
    p_move = ''

    try:  # try to get player 1's move
        p_move = obj.move(game_board, old_move, flg)
    except TimedOutExc:  # timeout error
        #                  print e
        WINNER = opp
        MESSAGE = 'TIME OUT'
        pts[opp] = MAX_PTS
        return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False
    except Exception as e:
        WINNER = opp
        MESSAGE = "THREW AN EXCEPTION"
        traceback.print_exc()
        pts[opp] = MAX_PTS
        return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False
    signal.alarm(0)

    # check if board is not modified and move returned is valid
    if (game_board.small_boards_status != temp_small_boards_status) or (game_board.big_boards_status != temp_big_boards_status):
        WINNER = opp
        MESSAGE = 'MODIFIED THE BOARD'
        pts[opp] = MAX_PTS
        return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False

    update_status, small_board_won = game_board.update(old_move, p_move, flg)
    if update_status == 'UNSUCCESSFUL':
        WINNER = opp
        MESSAGE = 'INVALID MOVE'
        pts[opp] = MAX_PTS
        return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False

    # find if the game has ended and if yes, find the winner
    status = game_board.find_terminal_state()
    print status
    if status[1] == 'WON':  # if the game has ended after a player1 move, player 1 would win
        pts[ply] = MAX_PTS
        WINNER = ply
        MESSAGE = 'WON'
        return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False
    # in case of a draw, each player gets points equal to the number of small_boards won
    elif status[1] == 'DRAW':
        WINNER = 'NONE'
        MESSAGE = 'DRAW'
        return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False

    return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], False, small_board_won


def gameplay(obj1, obj2):  # game simulator

    game_board = BigBoard()
    fl1 = 'x'
    fl2 = 'o'
    old_move = (-1, -1, -1)
    WINNER = ''
    MESSAGE = ''
    pts1 = 0
    pts2 = 0

    game_board.print_board()
    signal.signal(signal.SIGALRM, handler)
    while(1):
        # player 1 turn
        p1_move, WINNER, MESSAGE, pts1, pts2, to_break, small_board_won = player_turn(
            game_board, old_move, obj1, "P1", "P2", fl1)

        if to_break:
            break

        old_move = p1_move
        game_board.print_board()

        if small_board_won:
            p1_move, WINNER, MESSAGE, pts1, pts2, to_break, small_board_won = player_turn(
                game_board, old_move, obj1, "P1", "P2", fl1)

            if to_break:
                break

            old_move = p1_move
            game_board.print_board()

        # do the same thing for player 2
        p2_move, WINNER, MESSAGE, pts1, pts2, to_break, small_board_won = player_turn(
            game_board, old_move, obj2, "P2", "P1", fl2)

        if to_break:
            break

        game_board.print_board()
        old_move = p2_move

        if small_board_won:
            p2_move, WINNER, MESSAGE, pts1, pts2, to_break, small_board_won = player_turn(
                game_board, old_move, obj2, "P2", "P1", fl2)

            if to_break:
                break

            old_move = p2_move
            game_board.print_board()

    game_board.print_board()

    print "Winner:", WINNER
    print "Message", MESSAGE

    x = 0
    d = 0
    o = 0
    for k in range(2):
        for i in range(3):
            for j in range(3):
                if game_board.small_boards_status[k][i][j] == 'x':
                    x += 1
                if game_board.small_boards_status[k][i][j] == 'o':
                    o += 1
                if game_board.small_boards_status[k][i][j] == 'd':
                    d += 1
    print 'x:', x, ' o:', o, ' d:', d

    if MESSAGE == 'DRAW':
        for k in range(2):
            for i in range(3):
                for j in range(3):
                    val = 6
                    if is_corner(i, j):
                        val = 4
                    elif is_centre(i, j):
                        val = 3
                    if game_board.small_boards_status[k][i][j] == 'x':
                        pts1 += val
                    if game_board.small_boards_status[k][i][j] == 'o':
                        pts2 += val

    return (pts1, pts2)


def is_centre(row, col):
    if row == 1 and col == 1:
        return 1
    return 0


def is_corner(row, col):
    if row == 0 and col == 0:
        return 1
    if row == 0 and col == 2:
        return 1
    if row == 2 and col == 0:
        return 1
    if row == 2 and col == 2:
        return 1
    return 0


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'Usage: python simulator.py <option>'
        print '<option> can be 1 => Random player vs. Random player'
        print '                2 => Human vs. Random Player'
        print '                3 => Human vs. Human'
        sys.exit(1)

    obj1 = ''
    obj2 = ''
    option = sys.argv[1]
    if option == '1':
        obj1 = Random_Player()
        obj2 = Random_Player()

    elif option == '2':
        obj2 = Random_Player()
        obj1 = Manual_Player()
    elif option == '3':
        obj1 = Manual_Player()
        obj2 = Manual_Player()
    elif option == '4':
        obj1 = Manual_Player()
        obj2 = Team72v3()
    else:
        print 'Invalid option'
        sys.exit(1)

    x = gameplay(obj1, obj2)
    print "Player 1 points:", x[0]
    print "Player 2 points:", x[1]
