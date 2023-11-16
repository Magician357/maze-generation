import base
from random import randint, shuffle

# https://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm

directions=[1,2,3,4]
dx=[0,0,1,-1]
dy=[-1,1,0,0]
opposite={1:2,2:1,3:4,4:3}


def generate_growing_tree_maze(height,width,index_choose_function,start=None):
    maze=base.maze(height,width)
    current=[(randint(0,width-1),randint(0,height-1))] if start==None else [start]
    
    while len(current) > 0:
        index=index_choose_function(len(current))
        x,y=current[index]
        
        shuffle(directions)
        local_directions=directions.copy()
        for direction in local_directions:
            newX,newY=x+dx[direction-1], y+dy[direction-1] # Store next position
            if newX >= 0 and newX < maze.width and newY >= 0 and newY < maze.height and maze[newX,newY][0]==0:
                
                current.append((newX,newY))
                
                index=None
                maze[x,y][direction]=0
                maze[newX,newY][opposite[direction]]=0
                
                maze[x,y][0]+=1
                maze[newX,newY][0]+=1
        
        if index != None: 
            current.pop(index)
    
    return maze

def newest(length):
    return length-1

def random_index(length):
    return randint(0,length-1)

def oldest(length):
    return 0

def random_newest(length):  
    # editable variables:
    chance1=1
    chance2=2
    choice=randint(0,chance1+chance2)
    if choice <= chance1:
        return random_index(length)
    else:
        return newest(length)

if __name__ == "__main__":    
    print("Newest (recursive backtrack)")
    print(generate_growing_tree_maze(5,10,newest,(4,0)).display)
    print("\nRandom")
    print(generate_growing_tree_maze(5,10,random_index,(4,0)).display)
    print("\nOldest")
    print(generate_growing_tree_maze(5,10,oldest,(4,0)).display)
    print("\nNewest and Random (split, check program for chances)")
    print(generate_growing_tree_maze(5,10,random_newest,(4,0)).display)

# a=generate_growing_tree_maze(5,10,random_newest,(4,0)).aslist
# for row in a:
#     for cell in row:
#         print(" " if cell == 0 else "■",end="")
#     print("")