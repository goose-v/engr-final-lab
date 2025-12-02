import pygame 
import random
import sys
from button import Button
from pygame.locals import *

pygame.init()

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#set up display and frame speed
dis = pygame.display.set_mode((1000,800))
dis.fill(WHITE)
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
#Player 
class Player:
    def initPlayer(num):
        def __init__(self) -> None:
            self.num = num
            self.hand = []
            self.score = 0 

#Deck
class Deck:
    def __init__(self) -> None:
        deck = [0]
        self.initDeck()
        self.shuffleDeck(deck)
        
        def initDeck():
            for i in range(1,13):
                for a in range(i):
                    deck.append(i)
            for i in range(3):
                deck.append("flip3")
                deck.append("freeze")
                deck.append("second chance")
        def shuffleDeck(deck):
            random.shuffle(deck)
            
#Play game screen
def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

#Instruction of how to play                    
def howTo():
    while True:
        HOWTO_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        HOWTO_TEXT = get_font(45).render("This is the HOWTO screen.", True, "Black")
        HOWTO_RECT = HOWTO_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(HOWTO_TEXT, HOWTO_RECT)

        HOWTO_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        HOWTO_BACK.changeColor(HOWTO_MOUSE_POS)
        HOWTO_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HOWTO_BACK.checkForInput(HOWTO_MOUSE_POS):
                    main_menu()

        pygame.display.update()
        
BG = pygame.image.load("assets/bg.png")

#Main menu screen (first screen you see)
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HOWTO_BUTTON = Button(image=pygame.image.load("assets/HOWTO Rect.png"), pos=(640, 400), 
                            text_input="HOWTO", font=get_font(75), base_color="#d7fcd4", hovering_color="White")


        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, HOWTO_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if HOWTO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    HOWTO()

        pygame.display.update()

main_menu()