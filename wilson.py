import base
from random import choice, randint, shuffle

# [Checked, North, South, East, West, display=" ",direction,extra2]

# https://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm

directions=[1,2,3,4]
dx=[0,0,0,1,-1]
dy=[0,-1,1,0,0]
opposite={1:2,2:1,3:4,4:3}

def generate_maze(width,height):
    maze=base.maze(height,width)
    unchecked=(width*height)-1
    maze[randint(0,width-1),randint(0,height-1)][0]+=1
    while unchecked > 0:
        #choose start
        startx,starty=randint(0,width-1),randint(0,height-1)
        print(maze[startx,starty])
        print(startx,starty)
        if maze[startx,starty][0] == 0: # if cell is not visited
            #walk
            # print("walking")
            walking=True
            cx,cy=startx,starty
            while walking:
                shuffle(directions)
                for direction in directions:
                    nx,ny=cx+dx[direction],cy+dy[direction]
                    if nx >= 0 and nx < width and ny >= 0 and ny < height:
                        maze[cx,cy][6]=direction
                        if maze[nx,ny][0] > 0:
                            walking=False
                            break
                        else:
                            cx,cy=nx,ny
                            break
            #trace
            # print("tracing")
            tracing=True
            cx,cy=startx,starty
            while tracing and unchecked >= 1:
                direction=maze[cx,cy][6]
                # print("direction:",direction)
                nx,ny=cx+dx[direction],cy+dy[direction]
                # print("next:",maze[nx,ny])
                # print("current",maze[cx,cy])
                
                if maze[nx,ny][0]!=0 or direction == 0:
                    tracing=False
                    # print("trace finished")
                    break
                unchecked-=1
                
                maze[cx,cy][direction]=0
                maze[cx,cy][5]=str(maze[cx,cy][0]+1)
                # maze[cx,cy][0]+=1
                
                maze[nx,ny][opposite[direction]]=0
                maze[nx,ny][0]+=1
                
                
                # print(maze.display)(
                # input()
                cx,cy=nx,ny
            maze[startx,starty][5]="C"
            print(maze.display)
            input()
    return maze
                
print("final:")
print(generate_maze(5,5).display)