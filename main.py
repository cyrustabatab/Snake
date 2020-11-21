import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "100,30"

import pygame,sys,random
from snake import Snake


pygame.mixer.pre_init(44100,-16,2,512) #frequency,size,channels,buffer_szie
pygame.init()

BOARD_WIDTH,  BOARD_HEIGHT = 700,740
screen = pygame.display.set_mode((BOARD_WIDTH,BOARD_HEIGHT))
from food import Food
from score import InfoBar
from animated_snake import AnimatedSnake
CELL_WIDTH = 20
ROWS = COLS = 35

clock = pygame.time.Clock()
BLACK = (0,0,0)
GREEN = (0,255,0)
LIGHT_GREEN = (50,205,50)
LIGHT_BLUE = (173,216,230)
RED = (255,0,0)
FPS = 15 #18,25

pygame.display.set_caption("Snake")




def draw_board():
    '''    
    for row in range(ROWS):
        pygame.draw.line(screen,BLACK,(0,row * CELL_WIDTH),(BOARD_WIDTH,row * CELL_WIDTH))

    for col in range(ROWS):
        pygame.draw.line(screen,BLACK,(col * CELL_WIDTH,0),(col * CELL_WIDTH,BOARD_HEIGHT))
    '''
    
    top_offset = 40
    colors = (LIGHT_GREEN,GREEN) 
    number = 0
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen,colors[col % 2],(col * CELL_WIDTH,top_offset + row * CELL_WIDTH,CELL_WIDTH,CELL_WIDTH))
        if row % 2 == 0:
            colors = (GREEN,LIGHT_GREEN)
        else:
            colors = (LIGHT_GREEN,GREEN)


def game_over():
    
    # TODO add buttons for play again and back to main menu

    pygame.mixer.music.load("Retro_No hope.ogg")
    pygame.mixer.music.play()
    done = False
    game_over_font = pygame.font.SysFont("comicsansms",50)
    game_over_text = game_over_font.render("GAME OVER",True,RED)
    play_again_text = game_over_font.render("PLAY AGAIN",True,GREEN,RED)
    menu_text = game_over_font.render("MENU",True,GREEN,RED)
    gap = 20
    play_again_text_top_left  = BOARD_WIDTH//2 - play_again_text.get_width()//2 ,BOARD_HEIGHT//2 + game_over_text.get_height()//2 + gap
    play_again_rect = play_again_text.get_rect(topleft=play_again_text_top_left)
    menu_text_top_left = BOARD_WIDTH//2 - menu_text.get_width()//2,play_again_rect.bottom + gap
    menu_text_rect = menu_text.get_rect(topleft=menu_text_top_left)



    screen.blit(game_over_text,(BOARD_WIDTH//2 - game_over_text.get_width()//2,BOARD_HEIGHT//2 - game_over_text.get_height()//2))
    screen.blit(play_again_text,play_again_rect)
    screen.blit(menu_text,menu_text_rect)
    pygame.display.update()
    menu = False
    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True,None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(x,y):
                    done = True
                elif menu_text_rect.collidepoint(x,y):
                    done = True
                    menu = True

    
    pygame.mixer.music.stop()
    return False ,menu


def game():
    snake = Snake()
    food = Food(ROWS,COLS,CELL_WIDTH,40)
    high_scores_file_name = 'high_scores.txt'
    info_bar = InfoBar(screen,high_scores_file_name)

    hit_sound = pygame.mixer.Sound('vgdeathsound.ogg')
    pygame.mixer.music.load('Arizona-Sunset.mp3')
    pygame.mixer.music.play(-1)
    done = False

    while not done:
        
        changed_direction = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif not changed_direction and event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    changed_direction = True
                    snake.up()
                elif event.key == pygame.K_DOWN:
                    changed_direction = True
                    snake.down()
                elif event.key == pygame.K_LEFT:
                    changed_direction = True
                    snake.left()
                elif event.key == pygame.K_RIGHT:
                    changed_direction = True
                    snake.right()
        

        snake.update()
        if snake.has_collided_with_wall(40,BOARD_HEIGHT,0,BOARD_WIDTH) or snake.has_collided_with_tail():
            hit_sound.play()
            info_bar.update_high_scores_if_needed()
            pygame.mixer.music.stop()
            done,menu = game_over()
            if menu:
                return
            if not done:
                pygame.mixer.music.load('Arizona-Sunset.mp3')
                pygame.mixer.music.play(-1)
                snake.reset()
                food = Food(ROWS,COLS,CELL_WIDTH,40) #or just reset
                info_bar.reset()
        food.is_eaten(snake,info_bar)
        screen.fill(LIGHT_BLUE) 
        draw_board()
        food.draw(screen)
        snake.draw(screen)
        info_bar.display_score(screen)
        if not done:
            pygame.display.update()
        clock.tick(FPS)

    return done


def high_score_screen():
    high_scores_file_name = "high_scores.txt"

    with open(high_scores_file_name,'r') as f:
        scores = list(map(int,f.readlines()))
    
    high_score_heading_font = pygame.font.SysFont('comicsansms',50)
    high_score_font = pygame.font.SysFont('comicsansms',40)
    
    screen.fill(LIGHT_GREEN)
    high_score_heading_text = high_score_heading_font.render("HIGH SCORES",True,RED)
    high_score_heading_position = 20
    screen.blit(high_score_heading_text,(BOARD_WIDTH//2 - high_score_heading_text.get_width()//2,high_score_heading_position))

    left_gap = BOARD_WIDTH//2 - 20 
    
    top_gap = high_score_heading_position + high_score_heading_text.get_height() +  20
    gap_between_scores = 75
    for i in range(5):
        score = scores[i]
        score_text = high_score_font.render(f"{i + 1}. {score:>02}",True,RED)
        screen.blit(score_text,(left_gap - score_text.get_width(),top_gap + (i * gap_between_scores)))


    left_gap = BOARD_WIDTH//2  + 20
    for i in range(5,len(scores)):
        score = scores[i]
        score_text = high_score_font.render(f"{i + 1}. {score:>02}",True,RED)
        screen.blit(score_text,(left_gap,top_gap + ((i - 5) * gap_between_scores)))

    
    back_button_text = high_score_font.render("BACK",True,BLACK,RED)
    back_button_text_rect = back_button_text.get_rect(center=(BOARD_WIDTH//2,BOARD_HEIGHT-30))
    back_button_text_rect.bottom = BOARD_HEIGHT - 100
    
    screen.blit(back_button_text,back_button_text_rect)


    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()

                if back_button_text_rect.collidepoint(x,y):
                    return
























def menu():
    # add button for high scores

    title_font = pygame.font.SysFont('comicsansms',50)
    instructions_font = pygame.font.SysFont('comicsansms',25)
    title_text = title_font.render('SNAKE',True,RED)
    instructions_text_1= instructions_font.render('PRESS ARROWS KEYS TO TURN AND COLLECT APPLES!',True,RED)
    instructions_text_2 = instructions_font.render("AVOID HITTING YOUR TAIL AND THE WALLS!",True,RED) 
    instructions_text_3 = instructions_font.render("HIT ENTER TO PLAY!",True,RED) 
    high_scores_text = instructions_font.render("VIEW HIGH SCORES",True,BLACK,RED)
    center = (BOARD_WIDTH//2,BOARD_HEIGHT//2)
    high_scores_rect = high_scores_text.get_rect(center=center)


    SPAWNSNAKE = pygame.USEREVENT



    def draw_menu(): 
        top_offset = 10
        gap = 20
        screen.fill(LIGHT_GREEN)
        for animated_snake in list(animated_snakes):
            animated_snake.update()
            if animated_snake.y >= BOARD_HEIGHT:
                animated_snakes.remove(animated_snake)
            animated_snake.draw(screen)
        title_text_top_location = top_offset
        screen.blit(title_text,(BOARD_WIDTH//2 - title_text.get_width()//2,title_text_top_location))
        instructions_text_1_location = title_text_top_location + title_text.get_height() + gap
        screen.blit(instructions_text_1,(BOARD_WIDTH//2 - instructions_text_1.get_width()//2,instructions_text_1_location))
        instructions_text_2_location = instructions_text_1_location + instructions_text_1.get_height() + gap
        screen.blit(instructions_text_2,(BOARD_WIDTH//2 - instructions_text_2.get_width()//2,instructions_text_2_location))

        instructions_text_3_location = instructions_text_2_location + instructions_text_2.get_height() + gap

        screen.blit(instructions_text_3,(BOARD_WIDTH//2 - instructions_text_3.get_width()//2,instructions_text_3_location))
        screen.blit(high_scores_text,high_scores_rect)
        pygame.display.update()

    #draw_menu()
    done = False
    animated_snakes = []
    pygame.time.set_timer(SPAWNSNAKE,3000)
    pygame.mixer.music.load('Intro Theme.mp3')
    pygame.mixer.music.play(loops=-1)
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    done = game()
                    if not done:
                        #draw_menu()
                        animated_snakes = []
                        pygame.mixer.music.load('Intro Theme.mp3')
                        pygame.mixer.music.play(loops=-1)
                        pygame.time.set_timer(SPAWNSNAKE,0)
                        pygame.time.set_timer(SPAWNSNAKE,3000)
            if event.type == pygame.MOUSEBUTTONDOWN:
                coordinate = pygame.mouse.get_pos()

                if high_scores_rect.collidepoint(coordinate):
                    high_score_screen()




            if event.type == SPAWNSNAKE:
                animated_snake = AnimatedSnake(random.randint(20,BOARD_WIDTH - 20),random.randint(-100,-50))
                animated_snakes.append(animated_snake)
        

        draw_menu() 
        pygame.display.update()
        clock.tick(FPS)



if __name__ == "__main__":

    menu()
    pygame.quit()
    sys.exit()

