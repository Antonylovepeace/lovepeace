#module
import pygame ,sys
import numpy as np
import asyncio

#initialize
pygame.init()

#variables
screen_width = 1000
screen_height = 1080
board_row = round(screen_height // 3)
board_col = round(screen_width // 3)
square_size = 200
grid_lenth = square_size * 3
line_width = 6
circle_radius = square_size // 3
circle_width = 10
space = square_size // 4
cross_width = 25
#color
red = (255, 0, 0)
bg_color = (55, 64, 70)
line_color = (23, 145, 135)
circle_color = (100, 210, 200)
cross_color = (180, 100, 37)
grid = (90, 180, 150)

screen = pygame.display.set_mode( (screen_width, screen_height) )
#board
board = np.zeros( (board_row, board_col) )

def tic_tac_toe_screen():   
    pygame.display.set_caption( "TIC-TAC-TOE" )
    screen.fill( bg_color )
    draw_grid()

def load_img():
    #1.加載圖片
    img1 = pygame.image.load("img-removebg-preview.png") #如果你要嘗試，要麼圖片放在原位，要麼改變路徑
    #img2 = pygame.image.load("board4.png")
    #2.渲染圖片
    #blit(渲染對象，座標)
    screen.blit(img1, (1040, 400))
    #screen.blit(img2, (10, 10))
    #3.刷新顯示頁面
    #1.第一次刷新用它 pygame.display.flip()
    #2.不是第一次刷新
    pygame.display.update() #刷新
    
#畫網格線
def draw_grid():
    for x in range ( 1, 3 ):
        pygame.draw.line( screen, grid, (0, x * square_size), (grid_lenth, x * square_size), line_width )
        pygame.draw.line( screen, grid, (x * square_size, 0), (x * square_size, grid_lenth), line_width )

#draw circle & cross
def draw_figure():
    for row in range( board_row ):
        for col in range( board_col ):
            if board[row][col] == 1:
                pygame.draw.circle( screen, circle_color, (int( col * square_size + square_size // 2 ), int( row * square_size + square_size // 2)), circle_radius, circle_width)
            elif board[row][col] == 2:
                pygame.draw.line( screen, cross_color, (col * square_size + space, row * square_size +square_size - space), (col * square_size + square_size - space, row * square_size + space), cross_width )
                pygame.draw.line( screen, cross_color, (col * square_size + space, row * square_size + space), (col * square_size + square_size - space, row * square_size +square_size - space), cross_width )

#mark 
def mark_square(row, col, player):
    board[row][col] = player

#search available square
def available_square(row, col):
    return board[row][col] == 0

#is the board full?
def is_board_full():
    for row in range( board_row ):
        for col in range( board_col ):
            if board[row][col] == 0:
                return False
    return True            

#check winner
def win_check(player):
    #vertical win check
    for col in range( board_col ):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True
        
    #horizontal win check
    for row in range( board_row ):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True
        
    #asc win check
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        draw_asc_winning_line(player)
        return True
    
    #desc win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_winning_line(player)
        return True
    
    return False

#draw winning line*4
def draw_vertical_winning_line(col, player):
    posx = col * square_size + square_size // 2

    if player == 1:
        color = circle_color
    elif player == 2:
        color = cross_color

    pygame.draw.line( screen, color, (posx, 15), (posx, grid_lenth - 15), 15)

def draw_horizontal_winning_line(row, player):
    posy = row * square_size + square_size // 2

    if player == 1:
        color = circle_color
    elif player == 2:
        color = cross_color

    pygame.draw.line( screen, color, (15, posy), (grid_lenth - 15, posy), 15)

def draw_asc_winning_line(player):
    if player == 1:
        color = circle_color
    elif player == 2:
        color = cross_color

    pygame.draw.line( screen, color, (15, grid_lenth - 15), (grid_lenth - 15, 15), 15)

def draw_desc_winning_line(player):
    if player == 1:
        color = circle_color
    elif player == 2:
        color = cross_color

    pygame.draw.line( screen, color, (15, 15), (grid_lenth - 15, grid_lenth - 15), 15)

#restart game
def restart():
    screen.fill( bg_color )
    draw_grid()
    player = 1
    for row in range( board_row ):
        for col in range( board_col ):
            board[row][col] = 0
    
    load_img()



tic_tac_toe_screen()
load_img()



async def main():

    #main loop
    player = 1
    game_over = False
    
    while True:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                
                mousex = event.pos[0]
                mousey = event.pos[1]

                clicked_col = int(mousex // square_size)
                clicked_row = int(mousey // square_size)

                if clicked_row < 3 and clicked_col < 3:
                    if available_square( clicked_row, clicked_col):
                        mark_square( clicked_row, clicked_col, player )
                        if win_check( player ):
                            game_over = True

                        draw_figure()

                        player = player % 2 + 1                
                                    

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    game_over = False

        pygame.display.update()

        await asyncio.sleep(0)      # This line is critical; ensure you keep the sleep time at 0

#call main loop
asyncio.run(main())
