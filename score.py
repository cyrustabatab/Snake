import pygame


APPLE_IMAGE = pygame.image.load('apple.png').convert()
APPLE_IMAGE = pygame.transform.scale(APPLE_IMAGE,(30,30))
APPLE_IMAGE.set_colorkey((77,193,249),pygame.RLEACCEL)

TROPHY_IMAGE = pygame.image.load('trophy.png').convert()
TROPHY_IMAGE = pygame.transform.scale(TROPHY_IMAGE,(30,30))
TROPHY_IMAGE.set_colorkey((77,193,249),pygame.RLEACCEL)



BLACK = (0,0,0)
font = pygame.font.Font("atari.ttf",20)
LEFT_OFFSET = 5
TOP_OFFSET= 5

class InfoBar:


    def __init__(self,screen,high_scores_file_name):
        self.score = 0
        self.apple_image = APPLE_IMAGE
        self.trophy_image = TROPHY_IMAGE
        self.text = font.render(str(self.score),True,BLACK)
        self.high_scores_file_name = high_scores_file_name
        self.high_scores = self._get_scores()
        self.high_scores_text = font.render(str(self.high_scores[0]),True,BLACK)
        self.high_score = self.high_scores[0]

    def reset(self):
        self.score = 0
        self.text = font.render(str(self.score),True,BLACK)

    
    def _get_scores(self):

        with open(self.high_scores_file_name,'r') as f:
            scores = f.readlines()

        scores = list(map(int,scores))


        return scores

    def increment_score(self): 
        self.score += 1
        if self.score > self.high_scores[0]:
            self.high_scores_text = font.render(str(self.score),True,BLACK)
            self.high_score = self.score
        self.text = font.render(str(self.score),True,BLACK)

    def display_score(self,screen):
        screen.blit(self.apple_image,(LEFT_OFFSET,TOP_OFFSET))
        screen.blit(self.text,(2 * LEFT_OFFSET + self.apple_image.get_width(),TOP_OFFSET))
        screen.blit(self.high_scores_text,(screen.get_width() - LEFT_OFFSET - self.high_scores_text.get_width(),TOP_OFFSET))
        screen.blit(self.trophy_image,(screen.get_width() - 2 * LEFT_OFFSET - self.high_scores_text.get_width() - self.trophy_image.get_width(),TOP_OFFSET))



    def update_high_scores_if_needed(self):

        if self.score > self.high_scores[-1]:
            self.high_scores.pop()
            self.high_scores.append(self.score)
            self.high_scores.sort(reverse=True)

            
            with open(self.high_scores_file_name,'w') as f:
                for score in self.high_scores:
                    f.write(str(score) + '\n')
                





