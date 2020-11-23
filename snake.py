import pygame
from collections import deque

LEFT = 0
RIGHT =1 
UP = 2
DOWN = 3
RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
TONGUE_COLOR = BLACK
THICKNESS = 1

vec = pygame.math.Vector2

class Snake:
    
    TONGUE_WIDTH = 5
    TONGUE_LENGTH = 10

    def __init__(self,start_x=400,start_y=400,square_length=20,top_gap=40):
        self.squares = []
        self.start_x = start_x
        self.start_y = start_y
        self.square_length = square_length
        self.vel = vec(square_length,0)
        self.pos = vec(start_x,start_y)
        self.square_length = square_length
        self.direction = RIGHT
        self.create_snake()
        self.frame_number =-1
        self.show_tongue = True
        self.top_gap =top_gap
    

    def body_rows_and_cols(self):
        return {(square.y//20,(square.x)//20) for square in self.squares}
    
    def reset(self):
        self.squares =[]
        self.vel = vec(self.square_length,0)
        self.pos = vec(self.start_x,self.start_y)
        self.direction = RIGHT
        self.frame_number = -1
        self.show_tongue = True
        self.create_snake()

    def create_snake(self):

        
        for i in range(3):
            square = pygame.Rect(self.start_x - self.square_length * i,self.start_y,self.square_length,self.square_length)
            self.squares.append(square)


        self.head = self.squares[0]
    

    def draw(self,screen):

        for square in self.squares:
            pygame.draw.rect(screen,RED if square is not self.head else BLUE,square)
            pygame.draw.rect(screen,BLACK,square,THICKNESS)
        

        if self.show_tongue:
            x,y = self.head.topleft
            if self.direction == UP:

                pygame.draw.rect(screen,TONGUE_COLOR,(x + self.square_length//2 - self.TONGUE_WIDTH//2,y - self.TONGUE_LENGTH,self.TONGUE_WIDTH,self.TONGUE_LENGTH))
            elif self.direction == DOWN:
                pygame.draw.rect(screen,TONGUE_COLOR,(x + self.square_length//2 - self.TONGUE_WIDTH//2,y + self.square_length,self.TONGUE_WIDTH,self.TONGUE_LENGTH))
            elif self.direction == RIGHT:
                pygame.draw.rect(screen,TONGUE_COLOR,(x + self.square_length,y + self.square_length//2 - self.TONGUE_WIDTH//2,self.TONGUE_LENGTH,self.TONGUE_WIDTH))
            elif self.direction == LEFT:
                pygame.draw.rect(screen,TONGUE_COLOR,(x - self.TONGUE_LENGTH,y + self.square_length//2 - self.TONGUE_WIDTH//2,self.TONGUE_LENGTH,self.TONGUE_WIDTH))


    def make_bigger(self):
        tail = self.squares[-1]
        new_square = pygame.Rect(*tail.topleft,self.square_length,self.square_length)
        self.squares.append(new_square)
    
    def up(self):
        if self.direction != DOWN and self.direction != UP:
            self.vel.x = 0
            self.vel.y = -self.square_length
            self.direction = UP


    def left(self):
        if self.direction != RIGHT and self.direction != LEFT:
            self.vel.y = 0
            self.vel.x = -self.square_length
            self.direction = LEFT
    
    def right(self):
        if self.direction != LEFT and self.direction != RIGHT:
            self.vel.y = 0
            self.vel.x = self.square_length
            self.direction = RIGHT

    def down(self):
        if self.direction != UP and self.direction != DOWN:
            self.vel.x = 0
            self.vel.y = self.square_length
            self.direction = DOWN


    def update(self):
        for i in range(len(self.squares) - 1,-1,-1):
            square = self.squares[i]
            square.topleft = self.squares[i-1].topleft

        

        self.pos += self.vel
        self.head.topleft = (self.pos.x,self.pos.y)
        self.frame_number += 1
        if self.frame_number % 10 == 0:
            self.show_tongue = not self.show_tongue
            self.frame_number = 0

    
    def has_collided_with_wall(self,top_y,bottom_y,left_x,right_x):
        head = self.head
        collided = False
        if head.top < top_y or head.bottom > bottom_y or head.left < left_x or head.right > right_x:
            collided = True

        return collided


    def has_collided_with_tail(self):
        

        for i in range(1,len(self.squares)):
            square = self.squares[i]
            if self.head.colliderect(square):
                #print('collided with tail')
                #directions = ['left','right','up','down']
                #print(directions[self.direction])
                return True
        

        return False


    @property
    def size(self):
        return len(self.squares)
