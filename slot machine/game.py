import pygame
import time
from random import randrange

pygame.font.init()
pygame.init()

WIN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("slot machine")

clock = pygame.time.Clock()

MenuBG = pygame.image.load("MenuBG.png")
slotMachine = pygame.image.load("slotMachine.png")

MenuBG = pygame.transform.scale(MenuBG, WIN.get_size())
slotMachine = pygame.transform.scale(slotMachine, WIN.get_size())

BAR = pygame.transform.scale(pygame.image.load("bar.png"), (190,190))
BELL = pygame.transform.scale(pygame.image.load("bell.png"), (190,190))
CHERRY = pygame.transform.scale(pygame.image.load("cherry.png"), (190,190))
DIAMOND = pygame.transform.scale(pygame.image.load("diamond.png"), (190,190))
GRAPE = pygame.transform.scale(pygame.image.load("grape.png"), (190,190))
ORANGE = pygame.transform.scale(pygame.image.load("orange.png"), (190,190))
SEVEN = pygame.transform.scale(pygame.image.load("seven.png"), (190,190))
WATERMELON = pygame.transform.scale(pygame.image.load("watermelon.png"), (190,190))

bet_amount = 1
balance = 100

FONT = pygame.font.SysFont("Arial", 30)

def pause_screen():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False

def drawMainMenu():
    width, height = WIN.get_size()
    WIN.blit(MenuBG, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    quit_rect = pygame.Rect(width//2 - 200, height - height//6, 400, 100)
    options_rect = pygame.Rect(width//2 - 200, height - height//3, 400, 100)
    start_rect = pygame.Rect(width//2 - 200, height - height//2, 400, 100)

    quit_color = "gray" if quit_rect.collidepoint(mouse_pos) else "white"
    options_color = "gray" if options_rect.collidepoint(mouse_pos) else "white"
    start_color = "gray" if start_rect.collidepoint(mouse_pos) else "white"

    quit_button = pygame.draw.rect(WIN, quit_color, quit_rect)
    options_button = pygame.draw.rect(WIN, options_color, options_rect)
    start_button = pygame.draw.rect(WIN, start_color, start_rect)

    quit_text = FONT.render("QUIT", True, "black")
    options_text = FONT.render("OPTIONS", True, "black")
    start_text = FONT.render("START", True, "black")

    WIN.blit(quit_text, quit_text.get_rect(center=quit_button.center))
    WIN.blit(options_text, options_text.get_rect(center=options_button.center))
    WIN.blit(start_text, start_text.get_rect(center=start_button.center))

    pygame.display.update()
    return quit_button, options_button, start_button

def mainMenu():
    run = True
    while run:
        quit_button, options_button, start_button = drawMainMenu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    run = False
                if options_button.collidepoint(event.pos):
                    options()
                if start_button.collidepoint(event.pos):
                    Game()

    pygame.quit()

def drawOptions():
    width, height = WIN.get_size()
    WIN.blit(MenuBG, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    betUp_rect = pygame.Rect(width//2 + 300 , height - height//2, 100, 100)
    betDown_rect = pygame.Rect(width//2 - 400, height - height//2, 100, 100)
    showBet_rect = pygame.Rect(width//2 - 200, height - height//2, 400, 100)
    balanceUp_rect = pygame.Rect(width//2 + 300 , height//4, 100, 100)
    balanceDown_rect = pygame.Rect(width//2 - 400, height//4, 100, 100)
    showBalance_rect = pygame.Rect(width//2 - 200, height//4, 400, 100)
    ok_rect = pygame.Rect(width//2 - 150, height - height//6, 300, 100)

    betUp_button = pygame.draw.rect(WIN, "gray" if betUp_rect.collidepoint(mouse_pos) else "white", betUp_rect)
    betDown_button = pygame.draw.rect(WIN, "gray" if betDown_rect.collidepoint(mouse_pos) else "white", betDown_rect)
    balanceUp_button = pygame.draw.rect(WIN, "gray" if balanceUp_rect.collidepoint(mouse_pos) else "white", balanceUp_rect)
    balanceDown_button = pygame.draw.rect(WIN, "gray" if balanceDown_rect.collidepoint(mouse_pos) else "white", balanceDown_rect)
    showBalance_button = pygame.draw.rect(WIN,"white", showBalance_rect)
    showBet_button = pygame.draw.rect(WIN,"white", showBet_rect)
    ok_button = pygame.draw.rect(WIN, "gray" if ok_rect.collidepoint(mouse_pos) else "white", ok_rect)

    ShowBetAmount_text = FONT.render(f"Bet Amount: {bet_amount}", True, "black")
    ShowBalance_text = FONT.render(f"Balance: {balance}", True, "black")
    ok_text = FONT.render("OK", True, "black")


    WIN.blit(ShowBetAmount_text, ShowBetAmount_text.get_rect(center=showBet_button.center))
    WIN.blit(ShowBalance_text, ShowBalance_text.get_rect(center=showBalance_button.center))
    WIN.blit(ok_text, ok_text.get_rect(center=ok_button.center))

    pygame.display.update()
    return betUp_button, betDown_button, balanceUp_button, balanceDown_button, ok_button

def options():
    global bet_amount, balance
    run = True

    while run:
        buttons = drawOptions()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].collidepoint(event.pos) and balance > bet_amount:
                    bet_amount += 1
                if buttons[1].collidepoint(event.pos) and bet_amount > 1:
                    bet_amount -= 1
                if buttons[2].collidepoint(event.pos):
                    balance += 10
                if buttons[3].collidepoint(event.pos) and balance > bet_amount:
                    balance -= 10
                if buttons[4].collidepoint(event.pos):
                    return

def drawGame(c1, c2, c3, cutscene):
    width, height = WIN.get_size()

    WIN.blit(MenuBG, (0, 0))
    WIN.blit(slotMachine, (0, 0))

    if c1 == 1: WIN.blit(BAR, (width//2-300, height//2-120))
    elif c1 == 2: WIN.blit(BELL, (width//2-300, height//2-120))
    elif c1 == 3: WIN.blit(CHERRY, (width//2-300, height//2-120))
    elif c1 == 4: WIN.blit(DIAMOND, (width//2-300, height//2-120))
    elif c1 == 5: WIN.blit(GRAPE, (width//2-300, height//2-120))
    elif c1 == 6: WIN.blit(ORANGE, (width//2-300, height//2-120))
    elif c1 == 7: WIN.blit(SEVEN, (width//2-300, height//2-120))
    elif c1 == 8: WIN.blit(WATERMELON, (width//2-300, height//2-120))

    if c2 == 1: WIN.blit(BAR, (width//2-100, height//2-120))
    elif c2 == 2: WIN.blit(BELL, (width//2-100, height//2-120))
    elif c2 == 3: WIN.blit(CHERRY, (width//2-100, height//2-120))
    elif c2 == 4: WIN.blit(DIAMOND, (width//2-100, height//2-120))
    elif c2 == 5: WIN.blit(GRAPE, (width//2-100, height//2-120))
    elif c2 == 6: WIN.blit(ORANGE, (width//2-100, height//2-120))
    elif c2 == 7: WIN.blit(SEVEN, (width//2-100, height//2-120))
    elif c2 == 8: WIN.blit(WATERMELON, (width//2-100, height//2-120))

    if c3 == 1: WIN.blit(BAR, (width//2+120, height//2-120))
    elif c3 == 2: WIN.blit(BELL, (width//2+120, height//2-120))
    elif c3 == 3: WIN.blit(CHERRY, (width//2+120, height//2-120))
    elif c3 == 4: WIN.blit(DIAMOND, (width//2+120, height//2-120))
    elif c3 == 5: WIN.blit(GRAPE, (width//2+120, height//2-120))
    elif c3 == 6: WIN.blit(ORANGE, (width//2+120, height//2-120))
    elif c3 == 7: WIN.blit(SEVEN, (width//2+120, height//2-120))
    elif c3 == 8: WIN.blit(WATERMELON, (width//2+120, height//2-120))

    WIN.blit(FONT.render(f"Balance: {balance}", True, "white"), (20, 20))
    WIN.blit(FONT.render(f"Bet: {bet_amount}", True, "white"), (20, 60))

    if cutscene:
        WIN.blit(FONT.render("JACKPOT!", True, "yellow"), (width//2 - 100, height//2 + 150))

    pygame.display.update()

def Game():
    global balance, bet_amount

    c1 = c2 = c3 = 7

    cutscene = False
    cutscene_start = 0
    cutscene_duration = 2

    cooldown = 2
    last_play_time = 0

    spinning1 = False
    spin_start_time1 = 0
    spin_duration1 = 0.5
    spin_speed1 = 0.02
    last_spin_update1 = 0

    spinning2 = False
    spin_start_time2 = 0
    spin_duration2 = 1
    spin_speed2 = 0.02
    last_spin_update2 = 0

    spinning3 = False
    spin_start_time3 = 0
    spin_duration3 = 1.5
    spin_speed3 = 0.02
    last_spin_update3 = 0

    run = True
    while run:
        clock.tick(60)
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pauseMenu()

                if event.key == pygame.K_SPACE:
                    if balance >= bet_amount and not cutscene and not spinning1 and not spinning2 and not spinning3 and current_time - last_play_time >= cooldown:
                        spinning1 = True
                        spinning2 = True
                        spinning3 = True
                        spin_start_time1 = current_time
                        spin_start_time2 = current_time
                        spin_start_time3 = current_time
                        last_play_time = current_time

        if spinning1:
            if current_time - last_spin_update1 > spin_speed1:
                c1 = randrange(1, 9)
                last_spin_update1 = current_time

            if current_time - spin_start_time1 > spin_duration1:
                spinning1 = False


        if spinning2:
            if current_time - last_spin_update2 > spin_speed2:
                c2 = randrange(1, 9)
                last_spin_update2 = current_time

            if current_time - spin_start_time2 > spin_duration2:
                spinning2 = False


        if spinning3:
            if current_time - last_spin_update3 > spin_speed3:
                c3 = randrange(1, 9)
                last_spin_update3 = current_time

            if current_time - spin_start_time3 > spin_duration3:
                spinning3 = False

                if c1 == c2 == c3:
                    cutscene = True
                    cutscene_start = current_time
                    balance += bet_amount * 100
                else:
                    balance -= bet_amount

        if cutscene and current_time - cutscene_start > cutscene_duration:
            cutscene = False

        drawGame(c1, c2, c3, cutscene)

def pauseMenu():
    run = True
    while run:
        quit_b, opt_b, res_b = drawPauseMenu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_b.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                if opt_b.collidepoint(event.pos):
                    options()
                if res_b.collidepoint(event.pos):
                    return

def drawPauseMenu():
    width, height = WIN.get_size()
    WIN.blit(MenuBG, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    quit_rect = pygame.Rect(width//2 - 200, height - height//6, 400, 100)
    options_rect = pygame.Rect(width//2 - 200, height - height//3, 400, 100)
    resume_rect = pygame.Rect(width//2 - 200, height - height//2, 400, 100)

    quit_b = pygame.draw.rect(WIN, "gray" if quit_rect.collidepoint(mouse_pos) else "white", quit_rect)
    opt_b = pygame.draw.rect(WIN, "gray" if options_rect.collidepoint(mouse_pos) else "white", options_rect)
    res_b = pygame.draw.rect(WIN, "gray" if resume_rect.collidepoint(mouse_pos) else "white", resume_rect)

    quit_text = FONT.render("QUIT", True, "black")
    options_text = FONT.render("OPTIONS", True, "black")
    resume_text = FONT.render("RESUME", True, "black")


    WIN.blit(quit_text, quit_text.get_rect(center=quit_b.center))
    WIN.blit(options_text, options_text.get_rect(center=opt_b.center))
    WIN.blit(resume_text, resume_text.get_rect(center=res_b.center))

    pygame.display.update()
    return quit_b, opt_b, res_b

mainMenu()