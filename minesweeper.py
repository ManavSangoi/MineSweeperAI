# import pygame
# import random
# pygame.init()
# screen=pygame.display.set_mode((500,500))
# pygame.display.set_caption("Mine Sweeper")
# screen.fill("White")
# done=False
# image=pygame.image.load('mine.jpeg')
# colors=["Red", "Green", "Yellow", "Blue", "White"]
# while True:
#     screen.fill("Red")
#     screen.blit(image,(0,0))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#     pygame.display.update()

import random


class sentence:
    def __init__(self,nodes,mines):
        self.nodes=set(nodes)
        self.no_of_mines=mines
        
    def __str__(self):
        return f"{self.nodes} : {self.no_of_mines}"
    
    def __eq__(self, other):
        if self.nodes == other.nodes and self.no_of_mines== other.no_of_mines:
            return True
        else:
            return False
    
    def __hash__(self) -> int:
        return hash((tuple(self.nodes),self.no_of_mines))
    
    def mark_mine(self,mine):
        if mine in self.nodes:
            self.nodes.discard(mine)
            self.no_of_mines-=1

    def mark_safe(self,mine):
        if mine in self.nodes:
            self.nodes.discard(mine)
            
    def safes(self):
        if self.no_of_mines==0 and len(self.nodes)!=0:
            return self.nodes
        else:
            return set()
    
    def mines(self):
        if len(self.nodes)==self.no_of_mines:
            return self.nodes
        else:
            return set()
            

class minesweeper:
    def __init__(self):
        self.board=[]
        self.initialize()
    
    def initialize(self):
        self.rows=9
        self.columns=9
        self.no_of_mines=10
        self.known_mines=set()
        self.known_safes=set()
        self.knowledge_base=set()
        self.moves_made=set()
        self.unexplored=set()
        for x in range(0,self.rows):
            for y in range(0,self.columns):
                self.unexplored.add((x,y))
    
    def create_board(self):
        self.board=[]
        for i in range(self.rows):
            list=[0]*self.rows
            self.board.append(list)
            
    def isvalid(self,x,y):
        if(x>=0 and y>=0 and x<self.rows and y<self.rows):
            return True
                
    def number_update(self,x,y):
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if(self.isvalid(i,j)):
                    if(self.board[i][j]=='B'):
                        continue
                    else:
                        self.board[i][j] +=1
    
    def place_bombs(self):
        i=0
        while i<self.no_of_mines:
            x=random.randrange(0,self.rows)
            y=random.randrange(0,self.columns)
            if(self.board[x][y]== 'B'):
                continue
            else:
                self.board[x][y] = 'B'
                self.number_update(x,y)
                i+=1
    
    def show_board(self):
        for i in self.board:
            for j in i:
                print(j,end=" ")
            print()   
        
    def mark_mine(self,move):
        self.known_mines.add(move)
        self.moves_made.add(move)
        self.unexplored.remove(move)
        for sen in self.knowledge_base:
            sen.mark_mine(move)
    
    def mark_safe(self,move):
        self.known_safes.add(move)
        for sen in self.knowledge_base:
            sen.mark_safe(move)
    
    def make_sentence(self,move):
        x,y=move
        nodes=set()
        mines=self.board[x][y]
        for i in range(-1,2):
            for j in range(-1,2):
                if self.isvalid(x+i,y+j):
                    if (x+i,y+j) in self.known_mines:
                        mines-=1
                    elif (x+i,y+j) not in self.known_safes:
                        nodes.add((x+i,y+j))
                        
        sen=sentence(nodes,mines)
        return sen
    
    
    def update_knowledge_base(self):
        self.show_knowledge_base()
        for sen in self.knowledge_base.copy():
            if len(sen.nodes)==0:
                self.knowledge_base.discard(sen)

        for sen in self.knowledge_base:
            for move in sen.safes().copy():
                self.mark_safe(move)
            
            for move in sen.mines().copy():
                self.mark_mine(move)
        
        self.show_knowledge_base()
        
        while True:
            new_sentences=[]
            for sen1 in self.knowledge_base:
                for sen2 in self.knowledge_base:
                    if sen1!=sen2 and sen1.nodes.issubset(sen2.nodes):
                        newsen=sentence(
                            sen2.nodes.difference(sen1.nodes),
                            sen2.no_of_mines-sen1.no_of_mines
                        )
                        if newsen not in new_sentences and newsen not in self.knowledge_base:
                            print("newsentence",newsen)
                            new_sentences.append(newsen)
            
            # if len(new_sentences)==0:
            for i in new_sentences:
                self.knowledge_base.add(i)
            break
            
            # print(new_sentences)
            
            for i in new_sentences:
                self.knowledge_base.add(i)
        self.show_knowledge_base()
                
            
    
    def make_safe_move(self):
        print("making safe move")
        moves=0
        for move in self.known_safes:
            if move not in self.moves_made:
                moves+=1
                self.moves_made.add(move)
                self.unexplored.remove(move)
                sen=self.make_sentence(move)
                self.knowledge_base.add(sen)
                
        self.update_knowledge_base()
        self.cnt+=moves
        if moves==0:
            self.make_random_move()
        
    
    def make_random_move(self):
        print("making random move")
        move=random.choice(list(self.unexplored))
        x,y=move
        print(move)
        self.cnt+=1
        if self.board[x][y]=='B':
            print("Game Over!")
            exit(0)
        else:
            self.mark_safe(move)
            self.moves_made.add(move)
            self.unexplored.remove(move)
            sen=self.make_sentence(move)
            print(sen)
            self.knowledge_base.add(sen)
            self.update_knowledge_base()


    def show_knowledge_base(self):
        print("\nKnowledge Base")
        for i in self.knowledge_base:
            print(i)       
        print()

    def known_board(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if(i,j) in self.known_mines:
                   print("F",end=" ")
                elif (i,j) in self.moves_made:
                   print(self.board[i][j],end=" ")
                else:
                    print("X",end=" ")
            print()
        
    def start(self):
        self.create_board()
        self.place_bombs()
        self.show_board()
        self.cnt=0
        # self.make_random_move()
        while(len(self.known_mines)!=self.no_of_mines):
            self.known_board()
            self.cnt+=1
            self.make_safe_move()
            self.show_knowledge_base()
            print("cnt=",self.cnt)
        print(self.known_safes,self.moves_made,self.known_mines,sep="\n\n")
if __name__ == '__main__':
    mine=minesweeper()
    mine.start()
