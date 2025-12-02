import pygame 
import random
import sys
from button import Button
from pygame.locals import *

pygame.init()
#set up display and frame speed
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Menu")

#unified font function
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.otf", size)

# Function to wrap text within a given width
def wrap_text(text, font, max_width):
    """Return a list of text lines that fit within max_width."""
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    return lines

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
        font_title = get_font(55)
        font_body = get_font(32) 
        instructions = [
            "How to play a round",
            "Turns: Play proceeds clockwise, starting with the player to the dealer's left.",
            "Hit or Stay: On your turn, you can either \"hit\" (take another card) or \"stay\" (end your turn and lock in your points).",
            "Busting: If you draw a duplicate number card, you \"bust\" and score zero for the round. This can happen from \"hitting\" or from an action card.",
            "Scoring: If you \"stay,\" you add up the value of your unique cards at the end of the round. The game continues until someone reaches 200 points.",
            "Action cards: Special action cards can be played on yourself or opponents to help or hinder their progress.",
            "Freeze: Forces a player to end their round immediately.",
            "Flip three: Forces another player to take three more cards, one by one.",
            "Second chance: Protects you from busting once if you draw a duplicate."
        ]
        y = 50
        for i, line in enumerate(instructions):
            lines = wrap_text(line, font_body, max_width=1200)
            for wrapped in lines:
                surf = (font_title if i == 0 else font_body).render(wrapped, True, "Black")
                rect = surf.get_rect(center=(640, y))
                SCREEN.blit(surf, rect)
                y += surf.get_height() + 6
            y += 4  # extra spacing after each bullet section

        HOWTO_BACK = Button(image=None, pos=(640, 700), 
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
        
BG = pygame.transform.scale(pygame.image.load("assets/bg.png"), (1280, 800))

#Main menu screen (first screen you see)
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("assets/button.png"), pos=(640, 450), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HOWTO_BUTTON = Button(image=pygame.image.load("assets/button.png"), pos=(640, 600), 
                            text_input="RULES", font=get_font(75), base_color="#d7fcd4", hovering_color="White")


        image = pygame.transform.scale(pygame.image.load("assets/title.png"), (500, 300))
        image_rect = image.get_rect()
        image_rect.center = (640, 220)
        SCREEN.blit(image, image_rect)

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
                    howTo()

        pygame.display.update()

main_menu()