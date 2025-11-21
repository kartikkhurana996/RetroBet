import pygame
import sys
import random
from blackjack_logic import play_blackjack, hand_value, is_blackjack
import rps_logic

pygame.init()

# ---------------------------- WINDOW ----------------------------
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Must come first

# ---------------------------- WINDOW ICON ----------------------------
icon_img = pygame.image.load("assets/ui/icon.png").convert_alpha()
pygame.display.set_icon(icon_img)

# ---------------------------- WINDOW TITLE & CLOCK ----------------------------
pygame.display.set_caption("RetroBet")
clock = pygame.time.Clock()

# ---------------------------- BACKGROUND MUSIC ----------------------------
pygame.mixer.init()  # Initialize the mixer
pygame.mixer.music.load("assets/music/jazz.mp3")  # Load your MP3 file
pygame.mixer.music.set_volume(0.3)  # Adjust volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # -1 makes it loop infinitely

fire_fx = pygame.mixer.Sound("assets/music/fire.mp3")
fire_fx.set_volume(0.3)
fire_fx.play(-1)   # loop forever


# ---------------------------- BANKRUPT POPUP ----------------------------
# Load your custom UI images
BANKRUPT_POPUP_IMG = pygame.image.load("assets/ui/end.png").convert_alpha()
BANKRUPT_POPUP_IMG = pygame.transform.scale(BANKRUPT_POPUP_IMG, (400, 200))
OK_BTN_IMG = pygame.image.load("assets/ui/exit.png").convert_alpha()
OK_BTN_IMG = pygame.transform.scale(OK_BTN_IMG, (120, 50))
OK_BTN_IMGH = pygame.image.load("assets/ui/exith.png").convert_alpha()
OK_BTN_IMGH = pygame.transform.scale(OK_BTN_IMGH, (120, 50))

show_bankrupt_popup = False  # Flag to show popup
ok_button_rect = None  # Will hold rect of OK button

def trigger_bankrupt_popup():
    global show_bankrupt_popup
    show_bankrupt_popup = True

def draw_bankrupt_popup():
    global ok_button_rect
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Draw popup image
    popup_x = WIDTH//2 - 200
    popup_y = HEIGHT//2 - 100
    screen.blit(BANKRUPT_POPUP_IMG, (popup_x, popup_y))

    # Draw OK button
    ok_x = WIDTH//2 - 60
    ok_y = HEIGHT//2 + 30

    # Store rect for click detection
    ok_button_rect = pygame.Rect(ok_x, ok_y, OK_BTN_IMG.get_width(), OK_BTN_IMG.get_height())
    mx, my = pygame.mouse.get_pos()
    if ok_button_rect.collidepoint(mx, my):
        screen.blit(OK_BTN_IMGH, (ok_x, ok_y))
    else:
        screen.blit(OK_BTN_IMG, (ok_x, ok_y))
    return ok_button_rect


# ---------------------------- SOUND EFFECTS ----------------------------
hover_sfx = pygame.mixer.Sound("assets/sfx/hover.mp3")
click_sfx = pygame.mixer.Sound("assets/sfx/click.mp3")

hover_sfx.set_volume(0.5)
click_sfx.set_volume(0.6)

last_hover_button = None  # to prevent hover sound spamming



# ---------------------------- HELPER ----------------------------
def update_balance(amount):
    """Update balance and trigger bankrupt popup if balance reaches 0"""
    global balance
    balance += amount
    if balance <= 0:
        trigger_bankrupt_popup()

def handle_hover_sound(button_name, is_hovering):
    global last_hover_button
    if is_hovering:
        if last_hover_button != button_name:
            hover_sfx.play()
            last_hover_button = button_name
    else:
        if last_hover_button == button_name:
            last_hover_button = None
def animate_card_flip(surface, x, y, back_img, front_img, duration=300):
    """
    Plays a flip animation at (x,y).
    duration = milliseconds
    """

    start_time = pygame.time.get_ticks()
    half = duration // 2
    running = True

    while running:
        now = pygame.time.get_ticks()
        elapsed = now - start_time

        # First half → shrink card
        if elapsed < half:
            progress = elapsed / half
            new_w = max(1, int(CARD_WIDTH * (1 - progress)))
            img = back_img

        # Second half → grow card
        elif elapsed < duration:
            progress = (elapsed - half) / half
            new_w = max(1, int(CARD_WIDTH * progress))
            img = front_img

        else:
            running = False
            break

        # Clear only the card area (optional)
        pygame.draw.rect(surface, (0,0,0), (x, y, CARD_WIDTH, CARD_HEIGHT))

        scaled = pygame.transform.scale(img, (new_w, CARD_HEIGHT))
        surface.blit(scaled, (x + (CARD_WIDTH - new_w)//2, y))

        pygame.display.update()
        pygame.time.delay(10)



# ---------------------------- ASSETS ----------------------------
BG = pygame.image.load("assets/bg/background.png")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

NAVBAR = pygame.image.load("assets/ui/navbar_base.png")
MENU_BJ = pygame.image.load("assets/ui/12.png")
MENU_BJH = pygame.image.load("assets/ui/menu_bj.png")
MENU_RPS = pygame.image.load("assets/ui/13.png")
MENU_RPSH = pygame.image.load("assets/ui/menu_rps.png")
CHOOSE_BET_TEXT = pygame.image.load("assets/ui/choose_your_bet_text.png")
BET_BAR = pygame.image.load("assets/ui/bet_bar.png")
PLUS_BTN = pygame.image.load("assets/ui/plus.png")
MINUS_BTN = pygame.image.load("assets/ui/minus.png")
PLAY_BTN = pygame.image.load("assets/ui/play_button.png")
PLAY_BTNH = pygame.image.load("assets/ui/playh.png")
DEALER_TEXT = pygame.image.load("assets/ui/dealer_text.png")
PLAYER_TEXT = pygame.image.load("assets/ui/player_text.png")
HIT_BTN = pygame.image.load("assets/ui/hit_button.png")
STAND_BTN = pygame.image.load("assets/ui/stand_button.png")
RESTART_BTN = pygame.image.load("assets/ui/restart_button.png")
BACK_BTN = pygame.image.load("assets/ui/back_button.png")

HIT_BTNH = pygame.image.load("assets/ui/hith.png")
STAND_BTNH = pygame.image.load("assets/ui/standh.png")
RESTART_BTNH = pygame.image.load("assets/ui/restarth.png")
BACK_BTNH = pygame.image.load("assets/ui/backh.png")

ROCK_IMG = pygame.image.load("assets/rps/rock.png")
PAPER_IMG = pygame.image.load("assets/rps/paper.png")
SCISSORS_IMG = pygame.image.load("assets/rps/scissors.png")
CHOOSE_GAME_TEXT = pygame.image.load("assets/ui/choose_game.png")
ROCK_HOVER_IMG = pygame.image.load("assets/rps/rockh.png")
PAPER_HOVER_IMG = pygame.image.load("assets/rps/paperh.png")
SCISSORS_HOVER_IMG = pygame.image.load("assets/rps/scissorsh.png")
ROCK_IMGO = pygame.image.load("assets/rps/opponent_rock.png")
PAPER_IMGO = pygame.image.load("assets/rps/opponent_paper.png")
SCISSORS_IMGO = pygame.image.load("assets/rps/opponent_scissors.png")


BETTING_BG_BJ = pygame.image.load("assets/bg/bjbg.png")
BETTING_BG_BJ = pygame.transform.scale(BETTING_BG_BJ, (WIDTH, HEIGHT))

BETTING_BG_RPS = pygame.image.load("assets/bg/rpsbg.png")
BETTING_BG_RPS = pygame.transform.scale(BETTING_BG_RPS, (WIDTH, HEIGHT))

PLUS_BTNH = pygame.image.load("assets/ui/plush.png")
MINUS_BTNH = pygame.image.load("assets/ui/minush.png")

BLACKJACK_BG = pygame.image.load("assets/bg/bgame.png")
BLACKJACK_BG = pygame.transform.scale(BLACKJACK_BG, (WIDTH, HEIGHT))

RPS_BG_G = pygame.image.load("assets/bg/rpsgg.png")
RPS_BG_G = pygame.transform.scale(RPS_BG_G, (WIDTH, HEIGHT))



# ---------------------------- FONTS ----------------------------
font_medium = pygame.font.Font("assets/fonts/superstar.ttf", 21)
font_black = pygame.font.Font("assets/fonts/superstar.ttf", 21)
font_bet = pygame.font.Font("assets/fonts/superstar.ttf", 35)

# ---------------------------- GLOBALS ----------------------------
balance = 10000
current_screen = "menu"
selected_game = None
bet_amount = 100
MIN_BET = 100

# Blackjack state
bj_game = None

# RPS state
rps_game = {
    "player_choice": None,
    "cpu_choice": None,
    "result_text": "",
    "finished": False
}

# ---------------------------- CARD IMAGES ----------------------------
CARD_IMAGES = {}
CARD_WIDTH, CARD_HEIGHT = 80, 120
suits = {'S':'Spades','H':'Hearts','D':'Diamonds','C':'Clubs'}
ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

for suit_code, suit_name in suits.items():
    for rank in ranks:
        filename = f"assets/cards/{rank}{suit_code}.png"
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
        CARD_IMAGES[(rank, suit_name)] = img

BACK_CARD_IMG = pygame.image.load("assets/cards/back.png").convert_alpha()
BACK_CARD_IMG = pygame.transform.scale(BACK_CARD_IMG, (CARD_WIDTH, CARD_HEIGHT))

# ---------------------------- NAVBAR ----------------------------
def draw_navbar():
    screen.blit(NAVBAR, (0, 0))
    bal_text = font_black.render(f"${balance}", True, (255, 255, 255))
    screen.blit(bal_text, (696.79 , 24))

# ---------------------------- MENU ----------------------------
menu_bj_rect = pygame.Rect(270, 382, MENU_BJ.get_width(), MENU_BJ.get_height())
menu_rps_rect = pygame.Rect(450, 382, MENU_RPS.get_width(), MENU_RPS.get_height())

def menu_screen():
    mx, my = pygame.mouse.get_pos()
#    screen.blit(CHOOSE_GAME_TEXT, (323, 111))
    draw_navbar()
    if menu_bj_rect.collidepoint(mx,my):
        handle_hover_sound("menu_bj", True)
        screen.blit(MENU_BJH, (270,382))
    else:
        handle_hover_sound("menu_bj", False)
        screen.blit(MENU_BJ, (270, 382))
        
    if menu_rps_rect.collidepoint(mx, my):
        handle_hover_sound("menu_rps", True)
        screen.blit(MENU_RPSH, (450, 382))
    else:
        handle_hover_sound("menu_rps", False)
        screen.blit(MENU_RPS, (450, 382))

# ---------------------------- BETTING ----------------------------
plus_rect = pygame.Rect(670, 230, PLUS_BTN.get_width(), PLUS_BTN.get_height())
minus_rect = pygame.Rect(180, 230, MINUS_BTN.get_width(), MINUS_BTN.get_height())
play_rect = pygame.Rect(355, 360, PLAY_BTN.get_width(), PLAY_BTN.get_height())

def betting_screen_bj():
    mx, my = pygame.mouse.get_pos()
    screen.blit(BETTING_BG_BJ, (0, 0))
    draw_navbar()
    if plus_rect.collidepoint(mx, my):
        handle_hover_sound("menu_plus", True)
        screen.blit(PLUS_BTNH, plus_rect.topleft)
    else:
        handle_hover_sound("menu_plus", False)
        screen.blit(PLUS_BTN, plus_rect.topleft)
    if minus_rect.collidepoint(mx, my):
        handle_hover_sound("menu_minus", True)
        screen.blit(MINUS_BTNH, minus_rect.topleft)
    else:
        handle_hover_sound("menu_minus", False)
        screen.blit(MINUS_BTN, minus_rect.topleft)
    if play_rect.collidepoint(mx, my):
        handle_hover_sound("menu_play", True)
        screen.blit(PLAY_BTNH, play_rect.topleft)
    else:
        handle_hover_sound("menu_play", False)
        screen.blit(PLAY_BTN, play_rect.topleft)
    bet_text = font_bet.render(f"${bet_amount}", True, (0, 0, 0))
    screen.blit(bet_text, (415, 240))
    
def betting_screen_rps():
    mx, my = pygame.mouse.get_pos()
    screen.blit(BETTING_BG_RPS, (0, 0))
    draw_navbar()
    if plus_rect.collidepoint(mx, my):
        handle_hover_sound("menu_plus", True)
        screen.blit(PLUS_BTNH, plus_rect.topleft)
    else:
        handle_hover_sound("menu_plus", False)
        screen.blit(PLUS_BTN, plus_rect.topleft)
    if minus_rect.collidepoint(mx, my):
        handle_hover_sound("menu_minus", True)
        screen.blit(MINUS_BTNH, minus_rect.topleft)
    else:
        handle_hover_sound("menu_minus", False)
        screen.blit(MINUS_BTN, minus_rect.topleft)
    if play_rect.collidepoint(mx, my):
        handle_hover_sound("menu_play", True)
        screen.blit(PLAY_BTNH, play_rect.topleft)
    else:
        handle_hover_sound("menu_play", False)
        screen.blit(PLAY_BTN, play_rect.topleft)
        
    bet_text = font_bet.render(f"${bet_amount}", True, (0, 0, 0))
    screen.blit(bet_text, (415, 240))

# ---------------------------- DECK ----------------------------
class Deck:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    def __init__(self):
        self.cards = [(rank, suit) for suit in self.SUITS for rank in self.RANKS]
        random.shuffle(self.cards)
    def deal(self):
        return self.cards.pop() if self.cards else None

# ---------------------------- HELPER ----------------------------

def check_blackjack_or_bust(bj_game):
    player_val = hand_value(bj_game["player"])
    dealer_val = hand_value(bj_game["dealer"])

    if player_val == 21:
        bj_game["message"] = "Blackjack! You Win!"
        update_balance(int(bj_game["bet"] * 2.5))
        bj_game["show_dealer_cards"] = True
        return "player21"
    elif player_val > 21:
        bj_game["message"] = "Bust! Dealer Wins"
        bj_game["show_dealer_cards"] = True
        if balance<=0:
            trigger_bankrupt_popup()
        return "player_bust"

    elif dealer_val == 21:
        bj_game["message"] = "Dealer Blackjack! You Lose"
        bj_game["show_dealer_cards"] = True
        return "dealer21"
    elif dealer_val > 21:
        bj_game["message"] = "Dealer Bust! You Win"
        update_balance(bj_game["bet"] * 2)
        bj_game["show_dealer_cards"] = True
        return "dealer_bust"
    return None

# ---------------------------- BLACKJACK SCREEN ----------------------------
hit_rect = pygame.Rect(200, 530, HIT_BTN.get_width(), HIT_BTN.get_height())
stand_rect = pygame.Rect(350, 530, STAND_BTN.get_width(), STAND_BTN.get_height())
restart_rect = pygame.Rect(500, 530, RESTART_BTN.get_width(), RESTART_BTN.get_height())
back_rect = pygame.Rect(50, 530, BACK_BTN.get_width(), BACK_BTN.get_height())

def blackjack_screen():
    screen.blit(BLACKJACK_BG, (0, 0))
    draw_navbar()

    if bj_game:
        # Dealer cards
        x = 150
        for i, card in enumerate(bj_game["dealer"]):
            if i == 1 and not bj_game.get("show_dealer_cards", False):
                screen.blit(BACK_CARD_IMG, (x, 150))
            else:
                img = CARD_IMAGES.get(card)
                if img:
                    screen.blit(img, (x, 150))
                else:
                    pygame.draw.rect(screen, (255,255,255), (x, 150, 60, 90))
            x += 80

        # Player cards
        x = 150
        for card in bj_game["player"]:
            img = CARD_IMAGES.get(card)
            if img:
                screen.blit(img, (x, 380))
            else:
                pygame.draw.rect(screen, (255,255,255), (x, 380, 60, 90))
            x += 80

        # Result
        if bj_game.get("message"):
            msg_surf = font_medium.render(bj_game["message"], True, (255,255,255))
            screen.blit(msg_surf, (510, 530))

    # Buttons
    mx, my = pygame.mouse.get_pos()
    
    # HIT BUTTON
    if hit_rect.collidepoint(mx, my):
        handle_hover_sound("hit_btn", True)
        screen.blit(HIT_BTNH, hit_rect.topleft)
    else:
        handle_hover_sound("hit_btn", False)
        screen.blit(HIT_BTN, hit_rect.topleft)

    # STAND BUTTON
    if stand_rect.collidepoint(mx, my):
        handle_hover_sound("stand_btn", True)
        screen.blit(STAND_BTNH, stand_rect.topleft)
    else:
        handle_hover_sound("stand_btn", False)
        screen.blit(STAND_BTN, stand_rect.topleft)

    # RESTART BUTTON
    if restart_rect.collidepoint(mx, my):
        handle_hover_sound("restart_btn", True)
        screen.blit(RESTART_BTNH, restart_rect.topleft)
    else:
        handle_hover_sound("restart_btn", False)
        screen.blit(RESTART_BTN, restart_rect.topleft)

    # BACK BUTTON
    if back_rect.collidepoint(mx, my):
        handle_hover_sound("back_btn", True)
        screen.blit(BACK_BTNH, back_rect.topleft)
    else:
        handle_hover_sound("back_btn", False)
        screen.blit(BACK_BTN, back_rect.topleft)

# ---------------------------- RPS SCREEN ----------------------------
RPS_WIDTH, RPS_HEIGHT = 100, 100
ROCK_IMG = pygame.transform.scale(ROCK_IMG, (RPS_WIDTH, RPS_HEIGHT))
PAPER_IMG = pygame.transform.scale(PAPER_IMG, (RPS_WIDTH, RPS_HEIGHT))
SCISSORS_IMG = pygame.transform.scale(SCISSORS_IMG, (RPS_WIDTH, RPS_HEIGHT))
ROCK_HOVER_IMG = pygame.transform.scale(ROCK_HOVER_IMG, (RPS_WIDTH, RPS_HEIGHT))
PAPER_HOVER_IMG = pygame.transform.scale(PAPER_HOVER_IMG, (RPS_WIDTH, RPS_HEIGHT))
SCISSORS_HOVER_IMG = pygame.transform.scale(SCISSORS_HOVER_IMG, (RPS_WIDTH, RPS_HEIGHT))

rock_x, rock_y = 275, 400
paper_x, paper_y = 400, 400
scissors_x, scissors_y = 525, 400

rock_rect = pygame.Rect(rock_x, rock_y, RPS_WIDTH, RPS_HEIGHT)
paper_rect = pygame.Rect(paper_x, paper_y, RPS_WIDTH, RPS_HEIGHT)
scissors_rect = pygame.Rect(scissors_x, scissors_y, RPS_WIDTH, RPS_HEIGHT)

cpu_x, cpu_y = 400, 150
result_container_rect = pygame.Rect(225, 260, 440, 40)
restart_x, restart_y = 720, 530
restart_rect = pygame.Rect(restart_x, restart_y, RESTART_BTN.get_width(), RESTART_BTN.get_height())
back_x, back_y = 50, 530
back_rect = pygame.Rect(back_x, back_y, BACK_BTN.get_width(), BACK_BTN.get_height())

def rps_screen():
    screen.blit(RPS_BG_G, (0, 0))
    draw_navbar()
    mx, my = pygame.mouse.get_pos()

    # Player choices
    if rock_rect.collidepoint(mx, my):
        handle_hover_sound("rps_rock", True)
        screen.blit(ROCK_HOVER_IMG, (rock_x, rock_y))
    else:
        handle_hover_sound("rps_rock", False)
        screen.blit(ROCK_IMG, (rock_x, rock_y))

    if paper_rect.collidepoint(mx, my):
        handle_hover_sound("rps_paper", True)
        screen.blit(PAPER_HOVER_IMG, (paper_x, paper_y))
    else:
        handle_hover_sound("rps_paper", False)
        screen.blit(PAPER_IMG, (paper_x, paper_y))

    if scissors_rect.collidepoint(mx, my):
        handle_hover_sound("rps_scissors", True)
        screen.blit(SCISSORS_HOVER_IMG, (scissors_x, scissors_y))
    else:
        handle_hover_sound("rps_scissors", False)
        screen.blit(SCISSORS_IMG, (scissors_x, scissors_y))


    # CPU choice
    if rps_game["cpu_choice"]:
        img_map = {"rock": ROCK_IMGO, "paper": PAPER_IMGO, "scissors": SCISSORS_IMGO}
        screen.blit(img_map[rps_game["cpu_choice"]], (cpu_x, cpu_y))

    # Result
    if rps_game["result_text"]:
        res_surf = font_medium.render(rps_game["result_text"], True, (255, 255, 255))
        res_rect = res_surf.get_rect(center=result_container_rect.center)
        screen.blit(res_surf, res_rect)

    mx, my = pygame.mouse.get_pos()

    # Restart button
    if restart_rect.collidepoint(mx, my):
        handle_hover_sound("restart_btn_rps", True)
        screen.blit(RESTART_BTNH, restart_rect.topleft)
    else:
        handle_hover_sound("restart_btn_rps", False)
        screen.blit(RESTART_BTN, restart_rect.topleft)

    # Back button
    if back_rect.collidepoint(mx, my):
        handle_hover_sound("back_btn_rps", True)
        screen.blit(BACK_BTNH, back_rect.topleft)
    else:
        handle_hover_sound("back_btn_rps", False)
        screen.blit(BACK_BTN, back_rect.topleft)


# ---------------------------- MAIN LOOP ----------------------------
running = True
deck = None

while running:
    screen.blit(BG, (0, 0))

    if current_screen == "menu":
        menu_screen()
    elif current_screen == "betting_bj":
        betting_screen_bj()
    elif current_screen == "betting_rps":
        betting_screen_rps()
    elif current_screen == "blackjack":
        blackjack_screen()
    elif current_screen == "rps":
        rps_screen()
        
    mx, my = pygame.mouse.get_pos()
    
    if show_bankrupt_popup:
        ok_button_rect = draw_bankrupt_popup()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if hit_rect.collidepoint(mx, my):
                click_sfx.play()

            if show_bankrupt_popup and ok_button_rect and ok_button_rect.collidepoint(mx, my):
                pygame.quit()
                sys.exit()




            # MENU
            if current_screen == "menu":
                if menu_bj_rect.collidepoint(mx,my):
                    click_sfx.play()
                    selected_game = "bj"
                    current_screen = "betting_bj"

                elif menu_rps_rect.collidepoint(mx,my):
                    click_sfx.play()
                    selected_game = "rps"
                    current_screen = "betting_rps"


            # ---------------------------- BETTING LOGIC ----------------------------
            elif current_screen == "betting_bj":

                # Increase bet
                if plus_rect.collidepoint(mx, my) and bet_amount + 100 <= balance:
                    click_sfx.play()
                    bet_amount += 100

                # Decrease bet
                elif minus_rect.collidepoint(mx, my) and bet_amount - 100 >= MIN_BET:
                    click_sfx.play()
                    bet_amount -= 100

                # PLAY button clicked (start game)
                elif play_rect.collidepoint(mx, my):
                    click_sfx.play()

                    # Deduct bet from balance
                    balance -= bet_amount

                    # ---------------------------- BLACKJACK ----------------------------
                    if selected_game == "bj":
                        deck = Deck()
                        bj_game = {
                            "player": [deck.deal(), deck.deal()],
                            "dealer": [deck.deal(), deck.deal()],
                            "message": "",
                            "show_dealer_cards": False,
                            "bet": bet_amount,
                            "deck": deck
                        }

                        current_screen = "blackjack"

                        # Check immediate blackjack (player)
                        if hand_value(bj_game["player"]) == 21:
                            bj_game["message"] = "Blackjack! You Win!"
                            update_balance(int(bet_amount * 2.5))
                            bj_game["show_dealer_cards"] = True

                        # Dealer blackjack
                        elif hand_value(bj_game["dealer"]) == 21:
                            bj_game["message"] = "Dealer Blackjack! You Lose"
                            bj_game["show_dealer_cards"] = True

                            # Check bankrupt
                            if balance <= 0:
                                trigger_bankrupt_popup()

            # ---------------------------- BETTING LOGIC FOR RPS ----------------------------
            elif current_screen == "betting_rps":

                # Increase bet
                if plus_rect.collidepoint(mx, my) and bet_amount + 100 <= balance:
                    bet_amount += 100

                # Decrease bet
                elif minus_rect.collidepoint(mx, my) and bet_amount - 100 >= MIN_BET:
                    bet_amount -= 100

                # PLAY button clicked (start game)
                elif play_rect.collidepoint(mx, my):

                    # Deduct bet
                    balance -= bet_amount

                    # Initialize RPS game
                    rps_game = {
                        "player_choice": None,
                        "cpu_choice": None,
                        "result_text": "",
                        "finished": False,
                        "bet": bet_amount
                    }

                    current_screen = "rps"

            # BLACKJACK
            elif current_screen == "blackjack" and bj_game:
                if not bj_game["message"]:
                    if hit_rect.collidepoint(mx, my):
                        click_sfx.play()
                        
                        new_card = bj_game["deck"].deal()      # GET CARD
                        bj_game["player"].append(new_card)     # ADD TO PLAYER HAND

                        # Animate
                        x = 150 + 80 * (len(bj_game["player"]) - 1)
                        y = 380
                        animate_card_flip(screen, x, y, BACK_CARD_IMG, CARD_IMAGES[new_card])

                        check_blackjack_or_bust(bj_game)

                    elif stand_rect.collidepoint(mx, my):
                        click_sfx.play()
                        bj_game["show_dealer_cards"] = True
                        while hand_value(bj_game["dealer"]) < 17:
                            new_card = bj_game["deck"].deal()
                            bj_game["dealer"].append(new_card)

                            x = 150 + 80 * (len(bj_game["dealer"]) - 1)
                            y = 150
                            animate_card_flip(screen, x, y, BACK_CARD_IMG, CARD_IMAGES[new_card])


                        p_val = hand_value(bj_game["player"])
                        d_val = hand_value(bj_game["dealer"])

                        if p_val > 21:
                            bj_game["message"] = "Bust! Dealer Wins"
                            if balance<=0:
                                trigger_bankrupt_popup() 
                        elif d_val > 21:
                            bj_game["message"] = "Dealer Bust! You Win"
                            update_balance(bj_game["bet"]*2)
                        elif p_val > d_val:
                            bj_game["message"] = "Player Wins"
                            update_balance(bj_game["bet"]*2)
                        elif d_val > p_val:
                            bj_game["message"] = "Dealer Wins"
                            if balance<=0:
                                trigger_bankrupt_popup()
                        else:
                            bj_game["message"] = "Push"
                            update_balance(bj_game["bet"])

                elif restart_rect.collidepoint(mx, my):
                    click_sfx.play()
                    current_screen = "betting_bj"
                elif back_rect.collidepoint(mx, my):
                    click_sfx.play()
                    current_screen = "menu"

            # RPS
            elif current_screen == "rps":
                if not rps_game["finished"]:
                    if rock_rect.collidepoint(mx,my):
                        click_sfx.play()
                        rps_game["player_choice"] = "rock"
                    elif paper_rect.collidepoint(mx,my):
                        click_sfx.play()
                        rps_game["player_choice"] = "paper"
                    elif scissors_rect.collidepoint(mx,my):
                        click_sfx.play()
                        rps_game["player_choice"] = "scissors"

                    if rps_game["player_choice"]:
                        rps_game["cpu_choice"] = random.choice(["rock","paper","scissors"])
                        p = rps_game["player_choice"]
                        c = rps_game["cpu_choice"]
                        if p == c:
                            rps_game["result_text"] = "Tie! Bet Refunded"
                            update_balance(rps_game["bet"])
                        elif (p=="rock" and c=="scissors") or (p=="paper" and c=="rock") or (p=="scissors" and c=="paper"):
                            payout = int(round(rps_game["bet"]*1.96))
                            rps_game["result_text"] = f"You Win! Payout: ${payout}"
                            update_balance(payout)
                        else:
                            rps_game["result_text"] = "You Lose!"
                            if balance<=0:
                                trigger_bankrupt_popup()
                        rps_game["finished"] = True

                elif restart_rect.collidepoint(mx,my):
                    click_sfx.play()
                    current_screen = "betting_rps"
                elif back_rect.collidepoint(mx,my):
                    click_sfx.play()
                    current_screen = "menu"
                    



    pygame.display.update()
    clock.tick(60)
