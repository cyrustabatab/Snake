import pygame

def get_snake_animations():
    
    snake_surfaces = []
    for number in range(1,9):
        snake_surface = pygame.image.load(f"top-down/snake{number}.png").convert_alpha()
        snake_surface = pygame.transform.rotate(snake_surface,180)
        snake_surfaces.append(snake_surface)


        
    return snake_surfaces


class AnimatedSnake:
    
    snake_surfaces = get_snake_animations()
    frame_switch = 1
    def __init__(self,x,y,speed=10):
        self.x = x
        self.y = y
        self.surface_index = 0
        self.snake_surface = self.snake_surfaces[0]
        self.frame_number = 0
        self.speed = speed

    
    def move(self):
        self.y += self.speed

    def draw(self,screen):
        screen.blit(self.snake_surface,(self.x,self.y))


    def update(self):

        self.move()
        self.frame_number += 1

        if self.frame_number == self.frame_switch:
            self.surface_index = (self.surface_index + 1) % len(self.snake_surfaces)
            self.snake_surface = self.snake_surfaces[self.surface_index]
            self.frame_number = 0








