from functions import components
from classes import enemy
from classes import projectile
from classes import tower
from classes import map
import savefiles
import classes
import data
import sounds
import random
import time
import pygame
from pygame import gfxdraw
import sys


def load_pics(folder, name):
    location = folder + name + ".png"
    return pygame.image.load(location).convert_alpha()


# This is a simple tower defence, written in Python
# It may be moved into unity later
# Made by Tommy H
# Project started 2018-08-12
# music: main menu wii music!! ingame atlas plug
# easy: -25% hp on enemies, long path (85), -25% score
# med: no speed modification, normal path (73), normal score
# hard: +25% hp on enemies, short path (56), +25% score


# ---- SETUP (only ran once) ----
# setup pygame
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.init()
pygame.font.init()
pygame.mixer.init()
time.sleep(0.5)

# setup display and clock
clock = pygame.time.Clock()
disL = 1300  # right 300 used for buying stuff and menu
disH = 750  # all 750 used for the map (1000 x 750 = 20 x 15 tiles)
screen = pygame.display.set_mode((disL, disH))
pygame.display.set_caption("Shape Defense")

intro = True

# font stuff
msLevelSelectFont = pygame.font.SysFont('Arial', 30, False)
msMenuButFont = pygame.font.SysFont('Arial', 50, True)
msHeaderFont = pygame.font.SysFont('Arial', 45, True)
msHeaderFont.set_underline(True)  # sets underline for a font
levelInfoFont = pygame.font.SysFont('Arial', 30, True)

# initialize maps
mapList = ["1", "2", "3", "4", "5", "6"]  # map file names
selectedMap = "none"  # map class

# colours of stuff
colBackground = [200, 225, 255]
colPurchaseMenu = [220, 220, 240]

# list to hold rect objects and their colour
levelBut = []
levelButCol = []

# create list of level select levelBut and their colour
mapInfo = []
for i in range(len(mapList)):
    mapInfo.append(map.Map(mapList[i]))
    levelButCol.append([mapInfo[i].colBackground, mapInfo[i].colObs])
    if i % 2 == 0:
        levelBut.append(pygame.Rect(450, 360 + (i // 2) * 100, 80, 80))
    else:
        levelBut.append(pygame.Rect(550, 360 + (i // 2) * 100, 80, 80))

# create list of menu levelBut (e.g. play, settings, etc.)
menuButText = ["PLAY", "settings"]
menuButCol = [[100, 225, 100], [200, 200, 75]]
menuBut = [pygame.Rect(75, 340 + i * 125, 250, 100) for i in range(len(menuButText))]
butPressed = 'none'

# load hardcoded images
titlePic = load_pics("images/UI/", "title")
circlePic = load_pics("images/UI/", "dots")
otherShapesPic = load_pics("images/UI/", "shapes")
circleX = [0, 425, 850, 1275]
shapesX = [-425, 0, 425, 850]

moneyPic = load_pics("images/UI/", "symbol_money")
lifePic = load_pics("images/UI/", "symbol_life")
energyPic = load_pics("images/UI/", "symbol_electricity")


# ---- LOAD CLASSES ----
# list of purchasable towers (turrets + boosters)
turretNames = ['wall', 'basic turret', "wall", 'wall', 'basic turret', 'wall', 'basic turret', 'basic turret']
boosterNames = []
# list of towers and boosters available for purchase, taken from towerNames and boosterNames
turretList = []
boosterList = []
# UI button initialization
butListTowers = []

# create tower levelBut and add the tower classes
for i in range(len(turretNames)):
    turretList.append(tower.Turret(turretNames[i]))
    # append rect objects to the list

# create booster levelBut and add the booster classes
for i in range(len(boosterNames)):
    boosterList.append(tower.Booster(boosterNames[i]))
    # append rect objects to the list

# create turret buttons
for i in range(6):
    if i % 3 == 0:
        butListTowers.append(pygame.Rect(disL - 270, 170 + (i // 3) * 80, 70, 70))
    elif i % 3 == 1:
        butListTowers.append(pygame.Rect(disL - 185, 170 + (i // 3) * 80, 70, 70))
    elif i % 3 == 2:
        butListTowers.append(pygame.Rect(disL - 100, 170 + (i // 3) * 80, 70, 70))


# load pictures of towers
turretBasePics = [load_pics("images/towers/", turretList[x].spriteBase) for x in range(len(turretList))]
turretGunPics = [load_pics("images/towers/", turretList[x].spriteGun) for x in range(len(turretList))]
turretProjPics = [load_pics("images/towers/", turretList[x].spriteProj) for x in range(len(turretList))]
boosterPics = [load_pics("images/towers/", boosterList[x].spriteBase) for x in range(len(boosterList))]

# switch page levelBut
imgNextPage = load_pics("images/UI/", "nextPg")
imgPrevPage = load_pics("images/UI/", "prevPg")
butNextPage = pygame.Rect(disL - 150 + 2, butListTowers[0][1] + 152 + 2,
                          imgNextPage.get_width() - 4, imgNextPage.get_height() - 4)
butPrevPage = pygame.Rect(disL - 180 + 2, butListTowers[0][1] + 152 - 2,
                          imgPrevPage.get_width() - 4, imgPrevPage.get_height() - 4)

# ---- OUTER LOOP ----
while True:
    # ---- INTRO SCREEN ----
    while intro:
        # should make it 60FPS max
        # dt is the number of seconds since the last frame, use this for calculations instead of fps to make it smoother
        dt = clock.tick(60) / 1000
        if dt > 0.05:  # maximum delta time
            dt = 0.05
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # background
        screen.fill(colBackground)

        # menu levelButCol
        for i in range(len(menuButText)):
            pygame.draw.rect(screen, menuButCol[i], menuBut[i])
            components.create_text(screen, (int(menuBut[i][0] + menuBut[i][2] / 2),
                                            int(menuBut[i][1] + menuBut[i][3] / 2)),
                                   menuButText[i], True, msMenuButFont, (0, 0, 0))

        # get mouse press on a button
        mousePos = pygame.mouse.get_pos()

        # draw menu levelBut
        for i in range(len(menuBut)):
            if menuBut[i].collidepoint(mousePos[0], mousePos[1]):
                # draw thicker outline on hover
                pygame.draw.rect(screen, (0, 0, 0), menuBut[i], 3)
                if pygame.mouse.get_pressed()[0] == 1 and butPressed != menuButText[i]:
                    butPressed = menuButText[i]
            # draw a thick red outline if it was selected
            if butPressed == menuButText[i]:
                pygame.draw.rect(screen, (150, 25, 25), menuBut[i], 3)
            # otherwise don't draw anything
            else:
                pygame.draw.rect(screen, (0, 0, 0), menuBut[i], 1)

        # draw level select levelBut after play is clicked
        if butPressed == "PLAY":
            for i in range(len(levelBut)):
                if levelBut[i].collidepoint(mousePos[0], mousePos[1]):
                    # on hover, draw thicker outline and a preview of the map
                    pygame.draw.rect(screen, (0, 0, 0), levelBut[i], 3)
                    # map preview:
                    mapInfo[i].draw_preview(screen, disL - 500, 360, 0.4)
                    pygame.draw.rect(screen, (0, 0, 0), (disL - 500, 360, 400, 300), 1)
                    components.create_text(screen, [disL - 300, 340], mapInfo[i].mapName, True,
                                           msLevelSelectFont, (0, 0, 0))

                    # on click, set map and close out intro
                    if pygame.mouse.get_pressed()[0] == 1:
                        selectedMap = mapInfo[i]
                        intro = False

            # draw the levelBut and their text
            for i in range(len(levelBut)):
                pygame.draw.rect(screen, levelButCol[i][0], levelBut[i])
                pygame.draw.rect(screen, (0, 0, 0), levelBut[i], 1)
                # create a the button text based on the name and difficulty of the map
                components.create_text(screen,
                                       (levelBut[i][0] + levelBut[i][2] // 2, levelBut[i][1] + levelBut[i][3] // 2),
                                       i + 1, True, msLevelSelectFont, (15, 15, 15))

            # draw prompt msg
            components.create_text(screen, (int(levelBut[0][0] + levelBut[1][0] + levelBut[0][2] * 1 + 10) / 2, 315),
                                   "Choose a level", True, msHeaderFont, (0, 0, 0))

        # title text
        screen.blit(titlePic, (250, 50))
        # move circles using list comprehension
        circleX = [x - 100 * dt for x in circleX]
        for i in range(len(circleX)):
            if circleX[i] < - 425:
                circleX[i] += 1700
            # draw dot under title!
            screen.blit(circlePic, (int(circleX[i]), 175))
        # move other shapes using list comprehension
        shapesX = [x + 50 * dt for x in shapesX]
        for i in range(len(shapesX)):
            if shapesX[i] > 1325:
                shapesX[i] -= 1700
            # draw shapes!
            screen.blit(otherShapesPic, (int(shapesX[i]), 225))

        # border
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, disL, disH), 3)

        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()

    # ---- IN-GAME SETUP and reset variables----
    curWave = 0  # current wave
    money = 300  # monies
    energy = [0, 10]  # amount of power used vs maximum
    income = 50  # monies per turn
    life = 50  # lose 1 life per enemy; 10 per boss

    # page that its on
    curPurchasePage = 0

    # mouse stuff
    mousePressed = pygame.mouse.get_pressed()

    # ---- GAME LOOP ----
    while not intro:
        # should make it 60FPS max
        # dt is the number of seconds since the last frame, use this for calculations instead of fps to make it smoother
        dt = clock.tick(60) / 1000
        mousePressed = [0, 0, 0]  # reset mouse presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = pygame.mouse.get_pressed()

        # get inputs
        mousePos = pygame.mouse.get_pos()

        # make sure money doesn't go over maximum of 10000, and energy for 50
        if money > 10000:
            money = 10000
        if energy[0] > 50:
            energy[0] = 50

        # ---- BACKGROUND ----
        screen.fill(selectedMap.colBackground)
        # path and obstacles
        components.draw_grid(screen, 0, 0, disL - 300, disH, 50, selectedMap.colGrid, False)
        selectedMap.draw_obstacles(screen)

        # ---- UI ELEMENTS ----
        # ui background
        pygame.draw.rect(screen, colPurchaseMenu, (disL - 300, 0, 300, disH), 0)

        # borders
        pygame.draw.rect(screen, selectedMap.colObs, (0, 0, disL, disH), 3)
        pygame.draw.line(screen, selectedMap.colObs, (disL - 300, 0), (disL - 300, disH), 3)

        # sub dividers
        pygame.draw.line(screen, (70, 70, 70), (disL - 300, butListTowers[0][1] - 20), (disL, butListTowers[0][1] - 20))
        pygame.draw.line(screen, (70, 70, 70), (disL - 300, butListTowers[0][1] + 180),
                         (disL, butListTowers[0][1] + 180))
        pygame.draw.line(screen, (70, 70, 70), (disL - 300, disH - 80),
                         (disL, disH - 80))

        # switch page buttons
        if curPurchasePage > 0:  # previous page
            screen.blit(imgPrevPage, (disL - 180, butListTowers[0][1] + 152))
            if butPrevPage.collidepoint(mousePos[0], mousePos[1]) and mousePressed[0] == 1:
                curPurchasePage -= 1
        elif curPurchasePage < (len(turretList) + len(boosterList)) // 6:  # next page
            screen.blit(imgNextPage, (disL - 150, butListTowers[0][1] + 152))
            if butNextPage.collidepoint(mousePos[0], mousePos[1]) and mousePressed[0] == 1:
                curPurchasePage += 1

        # purchase tower images
        mul6 = curPurchasePage * 6
        for i in range(mul6, mul6 + 6, 1):
            # draw turrets, then boosters depending on page
            if i < len(turretList):
                # draw base + gun
                screen.blit(turretBasePics[i], (butListTowers[i - mul6][0] + 10, butListTowers[i - mul6][1] + 10))
                temp = [turretGunPics[i].get_rect()[2] / 2, turretGunPics[i].get_rect()[3] / 2]
                screen.blit(turretGunPics[i],
                            (butListTowers[i - mul6][0] + 35 - temp[0], butListTowers[i - mul6][1] + 35 - temp[1]))
            elif i - len(turretList) < len(boosterList):
                screen.blit(boosterPics[i], (butListTowers[i - mul6][0] + 10, butListTowers[i - mul6][1] + 10))

        # purchase tower actual buttons and outline
        for i in range(6):
            if butListTowers[i].collidepoint(mousePos[0], mousePos[1]) and \
                                    i + mul6 < len(turretList) + len(boosterList):
                pygame.draw.rect(screen, (70, 70, 70), (butListTowers[i]), 1)

        # info about money, life, etc.
        # life
        screen.blit(lifePic, (disL - 275, 20))
        components.create_text(screen, (disL - 210, 50), str(life), False, levelInfoFont, (0, 0, 0))
        # wave
        components.create_text(screen, (disL - 150, 50), "wave: " + str(curWave), False, levelInfoFont, (0, 0, 0))
        # money
        screen.blit(moneyPic, (disL - 275, 80))
        components.create_text(screen, (disL - 210, 110), str(money), False, levelInfoFont, (0, 0, 0))
        # energy
        screen.blit(energyPic, (disL - 150, 80))
        components.create_text(screen, (disL - 100, 110), str(energy[0]) + "/" + str(energy[1]),
                               False, levelInfoFont, (0, 0, 0))

        # update display!
        pygame.display.update()
