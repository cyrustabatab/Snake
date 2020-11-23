import pygame
import random


FOOD_IMAGE = pygame.image.load('apple.png').convert()
FOOD_IMAGE = pygame.transform.scale(FOOD_IMAGE,(20,20))
FOOD_IMAGE.set_colorkey((77,193,249),pygame.RLEACCEL)


APPLE_SOUND_EFFECT = pygame.mixer.Sound('apple_bite.wav')



class Food:

    def __init__(self,rows,cols,snake,square_length=20,top_offset=0):
        
        self.rows = rows
        self.cols = cols
        self.snake = snake
        self.square_length = square_length
        self.top_offset = top_offset
        self.move_to_new_location(snake.body_rows_and_cols())
        #self.x,self.y = random.randint(0,self.cols - 1) * square_length,random.randint(0,self.rows - 1) * square_length + top_offset
        self.image = FOOD_IMAGE


    def draw(self,screen):

        screen.blit(self.image,(self.x,self.y))
    
    def is_eaten(self,info_bar):
        head = self.snake.head

        if head.topleft == (self.x,self.y):
            APPLE_SOUND_EFFECT.play()
            self.move_to_new_location(self.snake.body_rows_and_cols())
            info_bar.increment_score()
            self.snake.make_bigger()


    def move_to_new_location(self,snake_body):
        valid_rows_and_cols = [(row,col) for row in range(self.rows) for col in range(self.cols) if (row,col) not in snake_body]
        #self.x,self.y = random.randint(0,self.cols - 1) * self.square_length,random.randint(0,self.rows - 1) * self.square_length + self.top_offset
        self.x,self.y = random.choice(valid_rows_and_cols)
        self.x *= self.square_length
        self.y = self.y * self.square_length + self.top_offset



