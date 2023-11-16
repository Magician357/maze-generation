import base
from random import shuffle, randint

# https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking

# [Checked, North, South, East, West, display=" ",extra1,extra2]

# move amounts for each direction
directions=[1,2,3,4]
dx=[0,0,1,-1]
dy=[-1,1,0,0]
opposite={1:2,2:1,3:4,4:3}

def carve_passages_from(currentX,currentY,maze,depth=0):    
    shuffle(directions)
    
    # print(depth)
    
    for direction in directions:
        newX,newY=currentX+dx[direction-1], currentY+dy[direction-1] # Store next position
        # print(currentX,currentY)
        # print(newX,newY)
        
        if newX >= 0 and newX < maze.width and newY >= 0 and newY < maze.height and maze[newX,newY][0]<=0:
            
            maze[currentX,currentY][direction]=0
            maze[newX,newY][opposite[direction]]=0
            
            maze[currentX,currentY][0]+=1
            maze[newX,newY][0]+=1
            
            # maze[currentX,currentY][5]=str(maze[currentX,currentY][0])
            # maze[newX,newY][5]=str(maze[newX,newY][0])
            
            # print(depth)
            # print(maze.display)
            # print(currentX,currentY)
            # print(newX,newY)
            
            carve_passages_from(newX,newY,maze,depth+1)

def generate_backtrack_maze(width,height,startpos: tuple):
    cur=base.maze(height,width)
    carve_passages_from(startpos[0],startpos[1],cur)
    return cur

print(generate_backtrack_maze(10,10,(randint(0,9),randint(0,9))).display)