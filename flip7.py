import pygame 
from pygame.locals import *

pygame.init()

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#set up display and frame speed
dis = pygame.display.set_mode((300,300))
dis.fill(WHITE)
FPS = 60
FramePerSec = pygame.time.Clock()
pygame.display.set_caption("Flip 7")

#Player 
class Player:
    def initPlayer(num):
        player = pygame.Rect((50, 50), (50, 50))
        return player

#Deck
class Deck:
    def initDeck():
        deck = []
        for i in range(1, 11):
            deck.append(i)
        return deck

#Game loop
while True:
    
    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()