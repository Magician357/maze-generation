import pygame
from growingtree import generate_growing_tree_maze
from random import randint

def choose_index(length):
    return length-1 if randint(1,2) == 2 else 0 if randint(1,2) == 1 else randint(0,length-1)

pygame.font.init()
# print(pygame.font.get_fonts())
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

directions=[[0 for _ in range(maze_width)] for _ in range (maze_height)]

start=(randint(0,maze_width-1),randint(0,maze_height-1))
end=start
while end == start:
    end=(randint(0,maze_width-1),randint(0,maze_height-1))

def cell_to_pos(cx,cy):
    return (100+(line_width*(cx+0.5)),100+(line_height*(cy+0.5)))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_s]:
        # print("s is pressed")
        start=(randint(0,maze_width-1),randint(0,maze_height-1))
        end=start
        while end == start:
            end=(randint(0,maze_width-1),randint(0,maze_height-1))
    elif pressed[pygame.K_h]:
        # add maze solving code here
        pass

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    draw_text("Press S to randomize start and end points",(10,10),screen,font_large)
    draw_text("Press and hold H to solve maze")

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

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # limits FPS to 60

pygame.quit()