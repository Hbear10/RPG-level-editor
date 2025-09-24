import pygame
import math
import pygame_widgets
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.button import Button
# from pygame_widgets.textbox import TextBox
#import pygame_textinput

from Map import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill((120,255,120))

tiles = {}
map,tiles = map_load("open", tiles)
map,tiles = map_load("blank",tiles)

def draw_world():#draw map
    #screen.fill((0,0,0))
    for y in range(0,10):#0-9
        for x in range(0,10):#0-9
            # square = pygame.Rect(64*x,64*y,64,64)
            # pygame.draw.rect(screen,(map[y][x].img),square)

            #square_img = pygame.image.load("Assets/"+map[y][x].img).convert()
            square_rect = tiles[map[y][x].img].get_rect()
            square_rect.center = (64*x+364,64*y+72)
            screen.blit(tiles[map[y][x].img],square_rect)


def draw_tiles(tile_list):
    #print(tile_list)
    

    for n in range(len(tile_list)):
        if list(tile_list.keys())[n] == selected_tile:
            box = True
        else: 
            box = False

        tile = tile_list[list(tile_list.keys())[n]]
        #print(tile)
        square_rect = tile.get_rect()
        square_rect.center = (64*(n%5)+32,64*(n//5)+72)
        screen.blit(tile,square_rect)
        if box:
            selection_box = pygame.Rect(64*(n%5),64*(n//5)+40,64,64)
            pygame.draw.rect(screen,(255,0,0),selection_box,2)


dropdown = Dropdown(
    screen, 1000, 45, 100, 50, name='Select type',
    choices=['Path','Wall','Heal',"Enemy","Random","Leave"],
    borderRadius=3, colour=pygame.Color(255,255,255), values=["p", "w", 'h', "e","r","l"], direction='down', textHAlign='left')        


extra_info = ""
# def set_info():
#     global extra_info
#     extra_info = "hi"

# extra_info_box = TextBox(screen, 1000, 600, 200, 60, fontSize=25,
#                   borderColour=(255, 0, 0), textColour=(0, 200, 0),
#                   onSubmit=None, radius=10, borderThickness=5)

#extra_info_box = pygame_textinput.TextInputVisualizer()


def file_output():
    file = open("output.txt", "w")
    output_line = ""
    for y in map:
        output_line = ""
        for x in y:
            if len(x.extra_info) == 0:
                #print(x.type)
                #print(x.img)
                
                
                output_line+=(str(x.type)[0])+"-"+str(x.img)+","
            else:
                
                # ex = ""
                # if x.type != "wall":
                #     for i in x.extra_info:
                #         ex+=i+"~"#

                output_line+=(str(x.type)[0])+"-"+str(x.img)+"-"+str(x.extra_info)+","
        file.write(output_line[:-1]+"\n")
    file.close()

done_button = button = Button(
    screen, 10, 10, 100, 50, text='Print Value', fontSize=30,
    margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
    radius=5, onClick=file_output, font=pygame.font.SysFont('calibri', 10),
    textVAlign='bottom'
)


def extra_input():
    global extra_info
    inp = input(":")
    if inp == "":
        extra_info = ""
    else:
        extra_info = inp

extra_info_input = button = Button(
    screen, 1000, 600, 100, 50, text='Input Extra_info', fontSize=30,
    margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
    radius=5, onClick=extra_input, font=pygame.font.SysFont('calibri', 10),
    textVAlign='bottom'
)

selected_tile = "Brick"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0]:
            try:
                
            
            # if event.button == 1:
                
                if event.pos[0] < 320 and event.pos[1] > 36 and event.pos[1]<math.ceil(len(tiles)/5)*64+36:#in range of max coords for tiles
                    #print((event.pos[0])//64)
                    if event.pos[1]<math.ceil(len(tiles)/5)*64-28 or ((event.pos[0])//64<len(tiles)%5 and len(tiles)%5!=0) or ((event.pos[0])//64<5 and len(tiles)%5==0): #in range of all tiles
                        index = event.pos[0]//64+(5*((event.pos[1]-36)//64))
                        #print(index)
                        selected_tile = list(tiles.keys())[index]
                elif event.pos[0] >= 332 and event.pos[0] < 972 and event.pos[1] >= 40 and event.pos[1] <= 680: 
                    #print("GRID")
                    x = (event.pos[0]-332)//64
                    y=(event.pos[1]-40)//64
                    #print(map[y][x].img)
                    
                    if dropdown.getSelected() != None:
                        if extra_info == "":
                            map[y][x] = tile(selected_tile,dropdown.getSelected())
                        else:
                            map[y][x] = tile(selected_tile,dropdown.getSelected(),extra_info)

                
            except AttributeError:
                 pass

        #extra_info_box.update(pygame.event.get())
        # Blit its surface onto the screen
        

        screen.fill((120,255,120))
        #screen.blit(extra_info_box.surface, (200, 200))
        draw_world()
        draw_tiles(tiles)

        pygame_widgets.update(pygame.event.get())
        pygame.display.flip()


pygame.quit()