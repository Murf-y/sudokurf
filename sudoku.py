import pygame
from pygame.locals import *
import math
import random

Black= (20,20,20)
Grey = (120,120,120)
White= (255,255,255)
Red= (255,0,0)
Light_Red = (255,127,127)
Green= (0,255,0)
Blue= (0,0,255)
Yellow= (255,255,0)
Magenta= (255,0,255)
Cyan= (0,255,255)
background= (222,222,222)

class Cell:
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 60
        self.height = 60
        self.border = 1
        self.hoverd=False
        self.state = 0
        self.clickable = True

    def draw_cell(self, window):
        pygame.draw.rect(window ,self.color, (self.x, self.y, self.width, self.height),self.border)

    def change_color(self,window,color):
        self.color = color
        self.draw_cell(window)

    def check_hover(self,window, mouse_pos):
        cellX= math.ceil(self.x/60)
        cellY = math.ceil(self.y/60)
        mouse_in_cell_coords = get_mousepos_in_cell_coords(mouse_pos)
        
        if(mouse_in_cell_coords == (cellX,cellY)):
            
            self.hoverd = True
        else:
            self.hoverd=False

    def handle_hover(self,window):
        if(self.hoverd):
            if(not self.clickable):
                pygame.draw.rect(window ,Light_Red, (self.x, self.y, self.width, self.height))
            else:
                pygame.draw.rect(window ,Grey, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(window ,self.color, (self.x, self.y, self.width, self.height),self.border)
    def clicked(self,window):
        if(not self.clickable):
            return
        
        if(self.state == 9):
            self.state = 0
        self.state+=1
        self.draw_text(window)

    def cleared(self,window):
        if(not self.clickable):
            return
        self.state = 0
        self.draw_text(window)

    def draw_text(self,window):
        if(self.state!=0):
            txt = font.render(str(self.state), True, Black)
            window.blit(txt, (self.x+20,self.y+15))

    
pygame.init()
font = pygame.font.Font(None, 48)

WIDTH=540
HEIGHT=540

window = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('sudoku by Murf')

rows = WIDTH//60
columns = HEIGHT//60

cells={}

def get_mousepos_in_cell_coords(mouse_pos):
    mousex,mousey = mouse_pos
    return (math.floor(mousex/60),math.floor(mousey/60))

def draw_cells(window):
    x=0
    y=0
    for row in range(rows):
        x=0
        for column in range(columns):
            cell = Cell(x,y,Black)
            cell.draw_cell(window)
            cells[(x,y)] = cell
            x+=60
        y+=60

def draw_special_lines(window):
    pygame.draw.rect(window ,Black, (3*60,0,4,540))
    pygame.draw.rect(window ,Black, (6*60,0,4,540))
    pygame.draw.rect(window ,Black, (0,3*60,540,4))
    pygame.draw.rect(window ,Black, (0,6*60,540,4))
    pygame.draw.rect(window ,Black, (0,0,540,6))
    pygame.draw.rect(window ,Black, (0,0,6,540))
    pygame.draw.rect(window ,Black, (535,0,6,540))
    pygame.draw.rect(window ,Black, (0,535,540,6))



def update_cells(window):
    for pos in cells:
        cells[pos].draw_cell(window)
        cells[pos].handle_hover(window)
        cells[pos].draw_text(window)


running = True


draw_cells(window)


def cells_obj_to_states_arr(cells):
    states = [[],[],[],[],[],[],[],[],[]]
    elemnt = 0
    row = 0
    for pos in cells:
        raw_state = str(cells[pos].state) if cells[pos].state != 0 else "."
        states[row].append(raw_state)
        elemnt += 1
        if(elemnt ==9):
            row+=1
            elemnt=0
    return states

def isValidSudoku(board):
      for i in range(9):
         row = {}
         column = {}
         block = {}
         row_cube = 3 * (i//3)
         column_cube = 3 * (i%3)
         for j in range(9):
            if board[i][j]!='.' and board[i][j] in row:
                return False
            row[board[i][j]] = 1
            if board[j][i]!='.' and board[j][i] in column:
                return False
            column[board[j][i]] = 1
            rc= row_cube+j//3
            cc = column_cube + j%3
            if board[rc][cc] in block and board[rc][cc]!='.':
                return False
         block[board[rc][cc]]=1
      return True

def generate_random_numbers_on_cells(cells):
        for i in range(20):
            rand_state = random.randint(1,9)
            rand_cellx = random.randint(0,8)
            rand_celly = random.randint(0,8)
            rand_cell = cells[(rand_cellx*60,rand_celly*60)]
            rand_cell.state = rand_state
            rand_cell.clickable = False
        generated_states = cells_obj_to_states_arr(cells)
        if (not isValidSudoku(generated_states)):
            for pos in cells:
                cells[pos].state = 0
                cells[pos].clickable = True
            generate_random_numbers_on_cells(cells)

generate_random_numbers_on_cells(cells)

while running:
    window.fill(background)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOUSEMOTION:
            for pos in cells:
                cells[pos].check_hover(window, event.pos)

        if event.type == MOUSEBUTTONDOWN:

            cellX,cellY = get_mousepos_in_cell_coords(event.pos)
            absolute_mouse_pos = (cellX*60, cellY*60)

            if(cells[absolute_mouse_pos].hoverd):
                # left mouse click
                if(event.button == 1):
                    cells[absolute_mouse_pos].clicked(window)
                   

                # right mouse click
                if(event.button == 3):
                    cells[absolute_mouse_pos].cleared(window)
    update_cells(window)
    draw_special_lines(window)

    pygame.display.update()
        

pygame.quit()


