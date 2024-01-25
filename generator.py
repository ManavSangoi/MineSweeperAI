import random
def create_board():
    global board
    board=[]
    for i in range(5):
        list=[0]*5
        board.append(list)
    
def show_board():
    for i in board:
        for j in i:
            print(j,end=" ")
        print()   

def isvalid(x,y):
    if(x>=0 and y>=0 and x<5 and y<5):
        return True
    
    
def neighbours(x,y):
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if(isvalid(i,j)):
                if(board[i][j]=='B'):
                    continue
                elif(board[i][j]==0):
                    board[i][j] =1
                else:
                    board[i][j] +=1
    
    
def place_bombs():
    i=0
    while i<5:
        x=random.randrange(0,5)
        y=random.randrange(0,5)
        if(board[x][y]== 'B'):
            continue
        else:
            board[x][y] = 'B'
            neighbours(x,y)
            i+=1
        

def generate():
    create_board()
    place_bombs()
    show_board()
    
if __name__=='__main__':
    generate()
    