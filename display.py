import pygame
from growingtree import generate_growing_tree_maze
from random import randint, shuffle
from math import floor

cur_index_counter=1
def choose_index(length):
    global cur_index_counter
    cur_index_counter=(cur_index_counter%4)+1
    return length-1 if cur_index_counter == 1 else floor(length/2) if cur_index_counter == 2 else randint(0,length-1)

# north, south, east, west

opposite={1:2,2:1,3:4,4:3}

def generate_directions_dfs(maze,start_point,end_point):
    directions=[1,2,3,4]
    dx=[0,0,0,1,-1]
    dy=[0,-1,1,0,0]
    cx,cy=start_point
    shuffle(directions)
    for direction in directions:
        nx=cx+dx[direction]
        ny=cy+dy[direction]
        if nx >= 0 and ny >= 0 and nx < maze_width and ny < maze_height and directions_list[ny][nx] == 0:
            # if (nx,ny) == end_point:
            #     return
            if maze[cx,cy][direction] == 0:
                directions_list[ny][nx]=opposite[direction]
                generate_directions_dfs(maze,(nx,ny),end_point)

    dir_string=[" ","N","S","E","W","#"]
    for y in range(maze_height):
        for x in range(maze_width):
            maze[x,y][5]=dir_string[directions_list[y][x]]

def generate_directions_bfs(maze,start_point,end_point):
    backlog=[start_point]
    directions=[1,2,3,4]
    dx=[0,0,0,1,-1]
    dy=[0,-1,1,0,0]
    while len(backlog)>0:
        cx,cy=backlog[0]
        
        for direction in directions:
            nx=cx+dx[direction]
            ny=cy+dy[direction]
            if nx >= 0 and ny >= 0 and nx < maze_width and ny < maze_height and directions_list[ny][nx] == 0 and maze[cx,cy][direction] == 0:
                backlog.append((nx,ny)) # add to list to be used again
                directions_list[ny][nx]=opposite[direction] # log path to point
        
        backlog.pop(0)
    
    dir_string=[" ","N","S","E","W","#"]
    for y in range(maze_height):
        for x in range(maze_width):
            maze[x,y][5]=dir_string[directions_list[y][x]]
            
                
def generate_path_from(cx,cy,curpath,sx,sy):
    
    if not sx or not sy:
        sx,sy=cx,cy

    print(cx,cy)
    direction=directions_list[int(cy)][int(cx)]
    if direction == 5:
        return [(sx,sy)]+curpath
    else:
        dx=[0,0,0,1,-1]
        dy=[0,-1,1,0,0]
        nx=cx+dx[direction]
        ny=cy+dy[direction]
        curpath.append((nx,ny))
        return generate_path_from(nx,ny,curpath,sx,sy)

pygame.font.init()
# print(pygame.font.get_fonts()
my_font = pygame.font.SysFont('Arial', 10)
font_large= pygame.font.SysFont('Arial',30)
def draw_text(text:str,pos,screen,font=my_font,color=(0,0,0)):
    text_surface = font.render(text, False, color)
    screen.blit(text_surface,pos)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
running = True

background = pygame.Rect(100,100,600,600)

maze_width=8
maze_height=8

line_width=600/maze_width
line_height=600/maze_height

maze=generate_growing_tree_maze(maze_width,maze_height,choose_index)
print(maze.display)
maze_list=maze.grid

directions_list=[[0 for _ in range(maze_width)] for _ in range (maze_height)]

start=(randint(0,maze_width-1),randint(0,maze_height-1))
end=start
while end == start:
    end=(randint(0,maze_width-1),randint(0,maze_height-1))

def cell_to_pos(cx,cy):
    return (100+(line_width*(cx+0.5)),100+(line_height*(cy+0.5)))

def tCell_to_pos(pos):
    cx,cy=pos
    return (100+(line_width*(cx+0.5)),100+(line_height*(cy+0.5)))

solved=False
sCurX=0
sCurY=0

path=[]
paths=[]
paths_extra=[]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_s] or pressed[pygame.K_m]:
        if pressed[pygame.K_s]:
            # print("s is pressed")
            start=(randint(0,maze_width-1),randint(0,maze_height-1))
            end=start
            while end == start:
                end=(randint(0,maze_width-1),randint(0,maze_height-1))
            solved=False
            path=[]
            paths=[]
        if pressed[pygame.K_m]:
            maze=generate_growing_tree_maze(maze_width,maze_height,choose_index)
            print(maze.display)
            maze_list=maze.grid
            solved=False
            path=[]
            paths=[]
    elif pressed[pygame.K_h]:
        print("h pressed")
        if not solved:
            print("solving maze")
            solved=True
            sCurX, sCurY = start    
            directions_list=[[0 for _ in range(maze_width)] for _ in range (maze_height)]
            directions_list[sCurY][sCurX]=5
            path=[]
            
            generate_directions_bfs(maze,start,end)
            print(maze.display)
            path=generate_path_from(end[0],end[1],[],end[0],end[1])
            print(",".join([str(a) for a in path]))
            paths=[path]
    elif pressed[pygame.K_v]:
        if not solved:
            solved=True
            sCurX, sCurY = start    
            directions_list=[[0 for _ in range(maze_width)] for _ in range (maze_height)]
            directions_list[sCurY][sCurX]=5
            generate_directions_bfs(maze,start,end)
            
        for y in range(maze_height):
            for x in range(maze_width):
                curpath=generate_path_from(x,y,[],end[0],end[1])
                paths_extra.append(curpath)
        if len(paths) <= 1:
            paths+=paths_extra
        else:
            paths=paths_extra

    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    draw_text("Press S to randomize start and end points",(10,10),screen,font_large)
    draw_text("Press and hold H to solve maze",(10,40),screen,font_large)
    draw_text("Press and hold M to re-generate maze",(10,70),screen,font_large)

    # draw background
    pygame.draw.rect(screen,(240,240,240),background)
    
    # draw borders
    pygame.draw.line(screen,0,(100,100),(100,700),width=5)
    pygame.draw.line(screen,0,(100,700),(700,700),width=5)
    pygame.draw.line(screen,0,(700,700),(700,100),width=5)
    pygame.draw.line(screen,0,(700,100),(100,100),width=5)
    
    # draw maze
    for n, row in enumerate(maze_list):
        curY=100+(line_height*(n))
        for i, cell in enumerate(row):
            
            curX=100+(line_width*(i))
            if cell[3] == 1:
                pygame.draw.line(screen,0,(curX+line_width,curY),(curX+line_width,curY+line_height))
                # draw_text(f"e({i},{n})",(curX+line_width,curY+(line_height/2)),screen,color=(255,0,0))
            if cell[2] == 1:
                pygame.draw.line(screen,0,(curX,curY+line_height),(curX+line_width,curY+line_height))
                # draw_text(f"s({i},{n})",(curX+(line_width/2),curY+line_height),screen,color=(255,0,0))
                
            # draw_text(f"({curX}, {curY})",(curX,curY),screen)
            # draw_text(str(cell[1:5]),(curX+5,curY+5),screen,color=(0,0,100))
            # draw_text(f"({i},{n})",(curX+line_width/2,curY+line_height/2),screen)

    # draw points
    pygame.draw.circle(screen,(0,255,0),cell_to_pos(start[0],start[1]),10)
    pygame.draw.circle(screen,(255,0,0),cell_to_pos(end[0],end[1]),10)

    # draw path
    for curpath in paths:
        if len(curpath) >=2:
            for n in range(len(curpath)-1):
                pygame.draw.line(screen,(255,0,255),tCell_to_pos(curpath[n]),tCell_to_pos(curpath[n+1]))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # limits FPS to 60

pygame.quit()