import pygame 
import random
import sys
from button import Button
from pygame.locals import *

#Set up display and frame speed
pygame.init()
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Menu")

#Variables
MAX_PLAYERS = 4
players = []
turn_index = 0        # which player is currently playing
pointer_y = 310       # y-position for pointer triangle
pointer_color = (255, 255, 0)   # yellow indicator
deck_pointer = 0      # index in card deck

BG = pygame.transform.scale(pygame.image.load("assets/bg.png"), (1280, 800)) #game background

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

#game logic functions
def final(player):
    SCREEN.fill("black")
    font = get_font(80)
    text = font.render(f"Player {player.number} wins!", True, (255, 255, 0))
    SCREEN.blit(text, text.get_rect(center=(640, 400)))
    pygame.display.update()
    pygame.time.delay(5000)  # Show for 5 seconds
    pygame.quit()
    sys.exit()

def end_round(player):
    """
    Ends the current round for a player.
    - Checks for bust (duplicate number card)
    - Checks if player has 7 number cards
    - Updates player's round and total score
    """
    number_cards = [c for c in player.hand if isinstance(c, int)]

    # Bust if duplicates
    if len(number_cards) != len(set(number_cards)):
        print(f"Player {player.number} busted!")
        player.round_score = 0
    # Bust if 7 number cards
    elif len(number_cards) >= 7:
        print(f"Player {player.number} reached 7 cards!")
        player.round_score = sum(number_cards)
    else:
        player.round_score = sum(number_cards)

    player.total_score += player.round_score
    player.hand.clear()  # Clear hand for next round

    print(f"Player {player.number} gained {player.round_score} points. Total: {player.total_score}")


def end_game(players, deck):
    """
    Checks if any player has reached 200 points or if the deck is empty.
    Returns True if game ended, False otherwise.
    """
    # Check for 200+ points
    for player in players:
        if player.total_score >= 200:
            final(player)
            return True

    # Check if deck is empty
    if not deck.deck:
        # Highest score wins
        winner = max(players, key=lambda p: p.total_score)
        final(winner)
        return True

    return False

#Player 
class Player:
    def __init__(self, number):
        self.number = number
        self.hand = []
        self.round_score = 0    
        self.total_score = 0
        self.freeze = False
        self.second_chance = False
#Deck
class Deck:
    def __init__(self):
        self.deck = []
        self.initDeck()
        self.shuffleDeck()

    def initDeck(self):
        # number cards
        for i in range(1, 13):
            for _ in range(i):
                self.deck.append(i)

        # special cards
        for _ in range(3):
            self.deck.append("flip3")
            self.deck.append("freeze")
            self.deck.append("second chance")

        # bonus cards
        self.deck += ["+2", "+6", "+10", "+4", "+8", "*2"]

    def shuffleDeck(self):
        random.shuffle(self.deck)

    def draw(self):
        """Returns the next card, or None if deck is empty."""
        if self.deck:
            return self.deck.pop()
        return None

    def display_player_cards(self, surface, player, position):
        """
        Draws the player's cards.
        Returns list of clickable special card rects: [(rect, card_name), ...]
        """
        NUMBER_WIDTH, NUMBER_HEIGHT = 90, 120
        SMALL_WIDTH, SMALL_HEIGHT = 70, 55
        font = get_font(34)

        num_cards = [c for c in player.hand if isinstance(c, int)]
        bonus_cards = [c for c in player.hand if isinstance(c, str) and c not in ("freeze", "flip3", "second chance")]
        special_cards = [c for c in player.hand if c in ("freeze", "flip3", "second chance")]
        for p in players:
            round_score = sum(num_cards) 
            
        clickable_rects = []

        # Starting position by player
        if position == "top":
            x, y = 300, 140
            dx, dy = SMALL_WIDTH + 10, 0
            number_y_offset = SMALL_HEIGHT + 14
        elif position == "bottom":
            x, y = 300, 620
            dx, dy = SMALL_WIDTH + 10, 0
            number_y_offset = SMALL_HEIGHT + 14
        elif position == "left":
            x, y = 80, 220
            dx, dy = 0, SMALL_HEIGHT + 10
            number_y_offset = NUMBER_HEIGHT + 15
        elif position == "right":
            x, y = 1080, 220
            dx, dy = 0, SMALL_HEIGHT + 10
            number_y_offset = NUMBER_HEIGHT + 15

        # Draw bonus + special cards first (small)
        for card in bonus_cards + special_cards:
            rect = pygame.Rect(x, y, SMALL_WIDTH, SMALL_HEIGHT)
            color = (240, 210, 50) if card in bonus_cards else (110, 110, 180)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 3)
            text = font.render(str(card), True, (0, 0, 0))
            surface.blit(text, text.get_rect(center=rect.center))

            if card in special_cards:
                clickable_rects.append((rect, card))

            x += dx
            y += dy

        # Draw number cards in a row/column
        if position in ("top", "bottom"):
            x = 200
            y += number_y_offset
            for card in num_cards[:7]:
                rect = pygame.Rect(x, y, NUMBER_WIDTH, NUMBER_HEIGHT)
                pygame.draw.rect(surface, (255, 255, 255), rect)
                pygame.draw.rect(surface, (0, 0, 0), rect, 3)
                text = font.render(str(card), True, (0, 0, 0))
                surface.blit(text, text.get_rect(center=rect.center))
                x += NUMBER_WIDTH + 15
        else:
            x += SMALL_WIDTH + 10
            for card in num_cards[:7]:
                rect = pygame.Rect(x, y, NUMBER_WIDTH, NUMBER_HEIGHT)
                pygame.draw.rect(surface, (255, 255, 255), rect)
                pygame.draw.rect(surface, (0, 0, 0), rect, 3)
                text = font.render(str(card), True, (0, 0, 0))
                surface.blit(text, text.get_rect(center=rect.center))
                y += NUMBER_HEIGHT + 15

        return clickable_rects


         
#variable to keep track of incoming page 
pagePervious = "main_menu"

#Play game screen
def play():
    global pagePervious, turn_index, players
    deck = Deck()
    
    while True:
        #cover up the main screen
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        target_select_mode = False
        choosing_card = None
        choosing_owner = None
        
        #create buttons
        DECK = Button(image=None, pos=(640, 400), 
                            text_input="DECK", font=get_font(75), base_color="White", hovering_color="Red")#same as hit
        PLAY_RULE = Button(image=None, pos=(640, 450), 
                            text_input="RULE", font=get_font(35), base_color="White", hovering_color="Green")
        STAY = Button(image=None, pos=(640, 500),
                            text_input="STAY", font=get_font(75), base_color="White", hovering_color="Blue")#end round for current player
        
        PLAY_RULE.changeColor(PLAY_MOUSE_POS)
        PLAY_RULE.update(SCREEN)
        DECK.changeColor(PLAY_MOUSE_POS)
        DECK.update(SCREEN)
        STAY.changeColor(PLAY_MOUSE_POS)
        STAY.update(SCREEN)

        #indicate current player            
        def draw_pointer(surface, x, y):
            pygame.draw.polygon(surface, pointer_color, [(x, y), (x-15, y-30), (x+15, y-30)])

        #player action 
        def draw_card(p):
            global deck_pointer
            if deck_pointer < len(deck):
                p.hand.append(deck[deck_pointer])
                deck_pointer += 1

        #Sepcial action cards
        def use_freeze(target_player):
            target_player.freeze = True

        def use_second_chance(p):
            if p.hand:
                p.hand.pop()                                

        def use_draw3(p):
            for _ in range(3):
                draw_card(p)
        
        #create player areas for special card targeting
        player_area_rects = {}  # store player: rect for click detection
        # Bottom player
        if len(players) > 0:
            rect = pygame.Rect(540, 750, 200, 50)  # centered bottom
            pygame.draw.rect(SCREEN, (0, 0, 255), rect)
            pygame.draw.rect(SCREEN, (0, 0, 0), rect, 3)
            text = get_font(30).render(f"Player {players[0].number}", True, "white")
            SCREEN.blit(text, text.get_rect(center=rect.center))
            player_area_rects[players[0]] = rect
            score_text = get_font(20).render(f"Score: {players[0].total_score}", True, "black")
            SCREEN.blit(score_text, score_text.get_rect(center=(rect.centerx, rect.centery + 15)))
            player_area_rects[players[0]] = rect
        # Left player
        if len(players) > 1:
            rect = pygame.Rect(0, 300, 60, 200)  # middle-left
            pygame.draw.rect(SCREEN, (0, 0, 255), rect)
            pygame.draw.rect(SCREEN, (0, 0, 0), rect, 3)
            text = get_font(40).render(f"{players[1].number}", True, "white")
            SCREEN.blit(text, text.get_rect(center=rect.center))
            player_area_rects[players[1]] = rect
            score_text = get_font(20).render(f"{players[1].total_score}", True, "black")
            SCREEN.blit(score_text, score_text.get_rect(center=(rect.centerx, rect.centery + 30)))
            player_area_rects[players[1]] = rect

        # Top player
        if len(players) > 2:
            rect = pygame.Rect(540, 0, 200, 50)  # top-middle
            pygame.draw.rect(SCREEN, (0, 0, 255), rect)
            pygame.draw.rect(SCREEN, (0, 0, 0), rect, 3)
            text = get_font(30).render(f"Player {players[2].number}", True, "white")
            SCREEN.blit(text, text.get_rect(center=rect.center))
            player_area_rects[players[2]] = rect
            score_text = get_font(20).render(f"Score: {players[2].total_score}", True, "black")
            SCREEN.blit(score_text, score_text.get_rect(center=(rect.centerx, rect.centery + 15)))
            player_area_rects[players[2]] = rect

        # Right player
        if len(players) > 3:
            rect = pygame.Rect(1220, 300, 60, 200)  # middle-right
            pygame.draw.rect(SCREEN, (0, 0, 255), rect)
            pygame.draw.rect(SCREEN, (0, 0, 0), rect, 3)
            text = get_font(40).render(f"{players[3].number}", True, "white")
            SCREEN.blit(text, text.get_rect(center=rect.center))
            player_area_rects[players[3]] = rect
            score_text = get_font(20).render(f"{players[3].total_score}", True, "black")
            SCREEN.blit(score_text, score_text.get_rect(center=(rect.centerx, rect.centery + 30)))
            player_area_rects[players[3]] = rect

        # Display player cards and collect clickable special cards
        all_clickables = []
        positions = ["bottom", "left", "top", "right"]
        for i, p in enumerate(players):
            clickables = deck.display_player_cards(SCREEN, p, positions[i])
            all_clickables.extend([(p, rect, card) for rect, card in clickables])
        #buttons actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos 
                #button event
                if PLAY_RULE.checkForInput(PLAY_MOUSE_POS):
                    pagePervious = "play"
                    rule()
                if DECK.checkForInput(PLAY_MOUSE_POS):
                    card = deck.draw()
                    if card is not None:
                        players[turn_index].hand.append(card)
                        number_cards = [c for c in players[turn_index].hand if isinstance(c, int)]
                        if len(number_cards) != len(set(number_cards)) or len(number_cards) >= 7:
                            end_round(players[turn_index])
                            turn_index = (turn_index + 1) % len(players)
                            if end_game(players, deck):
                                return
                if STAY.checkForInput(PLAY_MOUSE_POS):
                    end_round(players[turn_index])
                    # Move to next player
                    turn_index = (turn_index + 1) % len(players)
                    if end_game(players, deck):
                        return  

                #special cards
                for owner, rect, card in all_clickables:
                    if rect.collidepoint(mx, my):
                        choosing_card = card
                        choosing_owner = owner
                        target_select_mode = True
                        break

                #for special card: selecting a target player (if in target selection mode)
                if target_select_mode:
                    for p in players:
                        if p != choosing_owner:  # cannot target self
                            player_rect = player_area_rects[p]
                            if player_rect.collidepoint(mx, my):
                                # Apply effect
                                if choosing_card == "freeze":
                                    use_freeze(p)
                                elif choosing_card == "flip3":
                                    use_draw3(p)
                                elif choosing_card == "second chance":
                                    use_second_chance(choosing_owner)

                                choosing_owner.hand.remove(choosing_card)
                                target_select_mode = False
                                break


        pygame.display.update()
        
#Choose number of players
def ask_num_players():
    global players
    chosen = 0

    # Create buttons once
    pl2 = Button(None, (450, 350), "2", get_font(60), "white", "green")
    pl3 = Button(None, (640, 350), "3", get_font(60), "white", "green")
    pl4 = Button(None, (830, 350), "4", get_font(60), "white", "green")
    buttons = [pl2, pl3, pl4]

    while chosen == 0:
        SCREEN.fill("black")
        prompt = get_font(50).render("CHOOSE PLAYERS (2-4)", True, "white")
        SCREEN.blit(prompt, (300, 200))

        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # Draw and hover effect
        for btn in buttons:
            btn.changeColor(PLAY_MOUSE_POS)
            btn.update(SCREEN)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pl2.checkForInput(PLAY_MOUSE_POS):
                    chosen = 2
                elif pl3.checkForInput(PLAY_MOUSE_POS):
                    chosen = 3
                elif pl4.checkForInput(PLAY_MOUSE_POS):
                    chosen = 4

        pygame.display.update()

    # Initialize players and start game
    players = [Player(k+1) for k in range(chosen)]
    play()
  
#Instruction of how to play                    
def rule():
    while True:
        RULE_MOUSE_POS = pygame.mouse.get_pos()

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

        RULE_BACK = Button(image=None, pos=(640, 700), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        RULE_BACK.changeColor(RULE_MOUSE_POS)
        RULE_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RULE_BACK.checkForInput(RULE_MOUSE_POS):
                    if pagePervious == "main_menu":
                        main_menu()
                    elif pagePervious == "play":
                        play()

        pygame.display.update()
        

#Main menu screen (first screen you see)
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("assets/button.png"), pos=(640, 450), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        RULE_BUTTON = Button(image=pygame.image.load("assets/button.png"), pos=(640, 600), 
                            text_input="RULES", font=get_font(75), base_color="#d7fcd4", hovering_color="White")


        image = pygame.transform.scale(pygame.image.load("assets/title.png"), (500, 300))
        image_rect = image.get_rect()
        image_rect.center = (640, 220)
        SCREEN.blit(image, image_rect)

        for button in [PLAY_BUTTON, RULE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ask_num_players()
                if RULE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pagePervious = "main_menu"
                    rule()

        pygame.display.update()

main_menu()