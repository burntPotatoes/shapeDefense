from functions import components
from functions import creditParse
from functions import waveParse
from functions import enemyParse
from classes import spawner
from classes import tower
from classes import map
from classes import explosion
from classes import enemy
import os.path
import time
import pygame
import random
import math
import time
from pygame import gfxdraw
import sys


def load_pics(folder, name):
    location = folder + name + ".png"
    return pygame.image.load(location).convert_alpha()


def display_stats(sel_tower):
    global msgTimer, msgText, money, mousePressed, income
    if not sel_tower.placed:
        # not enough money
        if sel_tower.cost > money:
            # display cost as red text
            components.create_text(screen, (disL - 150, 400), "$" + str(sel_tower.cost),
                                   True, levelTowerFont2, (200, 25, 25))
        # enough monies
        else:
            # display cost
            components.create_text(screen, (disL - 150, 400), "$" + str(sel_tower.cost),
                                   True, levelTowerFont2, (0, 0, 0))
        # power pic
        if sel_tower.energy > 0:
            screen.blit(energyMiniPic, (disL - 88, 390))
            # not enough power
            if energy[0] - sel_tower.energy < 0:
                components.create_text(screen, (disL - 70, 400), str(sel_tower.energy),
                                       False, levelTowerFont2, (200, 25, 25))
            # enough power
            else:
                components.create_text(screen, (disL - 70, 400), str(sel_tower.energy),
                                       False, levelTowerFont2, (0, 0, 0))

    # placed tower, display level
    elif sel_tower.placed:
        temp_str = "level "
        if sel_tower.curLevel > 1 and sel_tower.curLevel == sel_tower.maxLevel:  # max level
            temp_str += "MAX"
        elif sel_tower.maxLevel == 1:  # not upgradable (i.e. walls)
            temp_str = ""
        else:  # add level and max level to string
            temp_str += str(sel_tower.curLevel)
            temp_str += str(" / " + str(sel_tower.maxLevel))
        # level :D
        components.create_text(screen, (disL - 270, 400), temp_str,
                               False, levelTowerFont2, (0, 0, 0))
        
        # energies
        if sel_tower.energy > 0:
            screen.blit(energyMiniPic, (disL - 88, 390))
            components.create_text(screen, (disL - 70, 400), str(sel_tower.energy),
                                       False, levelTowerFont2, (0, 0, 0))

    # name
    components.create_text(screen, (disL - 150, 365), sel_tower.name, True,
                           levelTowerTitleFont, (0, 50, 175))

    # display stats
    if sel_tower.type == 'turret':
        # damage
        components.create_text(screen, (disL - 280, 430), '  Dmg:', False, levelTowerFont, (0, 0, 0))
        components.create_text(screen, (disL - 225, 430), str(sel_tower.damage), False, levelTowerFont, (0, 0, 100))
        # firerate
        components.create_text(screen, (disL - 280, 460), '  Rate:', False, levelTowerFont, (0, 0, 0))
        components.create_text(screen, (disL - 225, 460), str(round(sel_tower.rate, 2)), False, levelTowerFont, (0, 0, 100))
        # range
        components.create_text(screen, (disL - 280, 490), 'Range:', False, levelTowerFont, (0, 0, 0))
        components.create_text(screen, (disL - 225, 490), str(round(sel_tower.range, 2)), False, levelTowerFont, (0, 0, 100))
        # proj speed
        components.create_text(screen, (disL - 280, 520), ' P.Spd:', False, levelTowerFont, (0, 0, 0))
        components.create_text(screen, (disL - 225, 520), str(round(sel_tower.projSpd, 2)), False, levelTowerFont, (0, 0, 100))
    if sel_tower.targeting != 'projectile' and sel_tower.targeting != 'none':
        components.create_text(screen, (disL - 280, 550), sel_tower.targeting + ":", False, levelTowerFont, (0, 0, 0))
        components.create_text(screen, (disL - 225, 550), sel_tower.targetingVal, False, levelTowerFont, (0, 0, 100))
    if sel_tower.special != 'none':
        components.create_text(screen, (disL - 280, 580), sel_tower.special + ":", False, levelTowerFont, (0, 0, 0))
        components.create_text(screen, (disL - 225, 580), sel_tower.specialVal, False, levelTowerFont, (0, 0, 100))

    # display upgrade cost
    if sel_tower.curLevel < sel_tower.maxLevel and sel_tower.placed:
        screen.blit(imgUpArrow, (disL - 158 - len(str(sel_tower.finalUpCost)) * 5, 384))
        if money >= sel_tower.finalUpCost:
            components.create_text(screen, (disL - 135, 400), str(sel_tower.finalUpCost), True, levelTowerFont2, (0, 0, 0))
        else:
            components.create_text(screen, (disL - 135, 400), str(sel_tower.finalUpCost), True, levelTowerFont2, (200, 25, 25))
    # draw buttons
    if sel_tower.placed:
        cur_stat = 0
        for i in [sel_tower.dmgLevel, sel_tower.rateLevel, sel_tower.rangeLevel, sel_tower.targetingLevel, sel_tower.specialLevel]:
            # if it is not max level, draw the button
            if i[0] < i[1]:
                # get input
                screen.blit(imgPlus, (butUpgradeTower[cur_stat][0], butUpgradeTower[cur_stat][1]))
                pygame.draw.rect(screen, (25, 25, 25), butUpgradeTower[cur_stat], 1)
                # preview the stat increase
                if butUpgradeTower[cur_stat].collidepoint(mousePos[0], mousePos[1]):
                    components.create_text(screen, (disL - 120, butUpgradeTower[cur_stat][1] + 10),
                                           "+" + str(sel_tower.upgrade_preview(cur_stat)), False, levelTowerFont, (25, 175, 25))
                    # draw outline if you have enough money
                    if money >= sel_tower.finalUpCost:
                        pygame.draw.rect(screen, (25, 150, 25), butUpgradeTower[cur_stat], 1)

                    # upgrade tower on press if you have enough money
                    if mousePressed[0] == 1:
                        if money >= sel_tower.finalUpCost: # enough money
                            if sel_tower.special == 'income':  # update income
                                income -= sel_tower.specialVal
                            money -= sel_tower.finalUpCost
                            sel_tower.upgrade(cur_stat)
                            soundUpgrade.play()
                            # update income on upgrade
                            if sel_tower.special == 'income':
                                income += sel_tower.specialVal
                            
                            # update boosts
                            adjacentTowerList = []
                            for i in placedTowers:
                                # calculate distance to tower and check if it equals one
                                if abs(sel_tower.pos[0] - i.pos[0]) + abs(sel_tower.pos[1] - i.pos[1]) == 1:
                                    adjacentTowerList.append(i)
                            # update each adjacent tower if booster
                            if sel_tower.type == "booster":
                                for i in adjacentTowerList:
                                    secAdjTowerList = []
                                    for j in placedTowers:
                                        # calculate distance to tower and check if it equals one
                                        if abs(i.pos[0] - j.pos[0]) + abs(i.pos[1] - j.pos[1]) == 1:
                                            secAdjTowerList.append(j)

                                    i.calc_boost(secAdjTowerList)
                            
                        # not enough money; yell at player :D
                        elif money < sel_tower.finalUpCost: # not enough money
                            soundError.play()
                            msgTimer = 0.5
                            msgText = "Can't afford upgrade!"

            cur_stat += 1

# This is a simple tower defence, written in Python
# It may be moved into unity later
# Made by Tommy H
# Project started 2018-08-12
# TODO: add difficulties
# Easy: -15% cost for stuff, -15% enemy HP, -25% score
# Normal: default values
# Hard: +15% cost for stuff, +15% enemy HP, +25% score


# ---- SETUP (only ran once) ----
# setup pygame
pygame.mixer.pre_init(22050, -16, 8, 512)
pygame.init()
pygame.font.init()
pygame.mixer.init()
time.sleep(0.5)

# setup display and clock
clock = pygame.time.Clock()
fps = 60
disL = 1300  # right 300 used for buying stuff and menu
disH = 750  # all 750 used for the map (1000 x 750 = 20 x 15 tiles)
screen = pygame.display.set_mode((disL, disH))
pygame.display.set_caption("Shape Defense")

intro = True

# font stuff: ms = menu screen
msLevelSelectFont = pygame.font.SysFont('Trebuchet MS', 32, False)
msMenuButFont = pygame.font.SysFont('Trebuchet MS', 45, True)
msHeaderFont = pygame.font.SysFont('Trebuchet MS', 40, True)
msHeaderFont.set_underline(True)

levelInfoFont = pygame.font.SysFont('Trebuchet MS', 28, False)
levelSmallInfoFont = pygame.font.SysFont('Trebuchet MS',18, False)
levelTowerTitleFont = pygame.font.SysFont('Trebuchet MS', 24, True)
levelTowerTitleFont.set_underline(True)
levelTowerFont = pygame.font.SysFont('Trebuchet MS', 16, False)
levelTowerFont2 = pygame.font.SysFont('Trebuchet MS', 18, True)
levelNextWaveFont = pygame.font.SysFont('Trebuchet MS', 40, True)
levelFastFont = pygame.font.SysFont('Trebuchet MS', 12, False)
creditHeaderFont = pygame.font.SysFont('Trebuchet MS', 30, True)
creditBodyFont = pygame.font.SysFont('Trebuchet MS', 24, False)

# initialize maps
mapList = ["1", "2", "3", "4", "5", "6"]  # map file names
selectedMap = "none"  # map class

# initialize sounds
soundClick = pygame.mixer.Sound("sounds/UI/button.wav")
soundError = pygame.mixer.Sound("sounds/UI/error.wav")
soundSell = pygame.mixer.Sound("sounds/UI/sell.wav")
soundPlaced = pygame.mixer.Sound("sounds/game/placed_down.wav")
soundLevelSelect = pygame.mixer.Sound("sounds/UI/level_select.wav")
soundNextWave = pygame.mixer.Sound("sounds/UI/next_wave.wav")
soundUpgrade = pygame.mixer.Sound("sounds/UI/upgrade.wav")

# colours of stuff
colBackground = [200, 225, 255]
colPurchaseMenu = [220, 220, 240]
colIntro = [150, 165, 200, 255]

# list to hold rect objects and their colour
levelBut = []
levelButCol = []

# misc images
imgUpArrow = load_pics("images/UI/", "upgrade_arrow")
imgPlus = load_pics("images/UI/", "plus_sign")

# create list of level select levelBut and their colour
mapInfo = []
for i in range(len(mapList)):
    mapInfo.append(map.Map(mapList[i]))
    levelButCol.append([mapInfo[i].colBackground, mapInfo[i].colObs])
    if i % 2 == 0:
        levelBut.append(pygame.Rect(470, 360 + (i // 2) * 100, 80, 80))
    else:
        levelBut.append(pygame.Rect(570, 360 + (i // 2) * 100, 80, 80))

# create list of menu levelBut (e.g. play, settings, etc.)

menuButText = ["PLAY", "info", "credits"]
menuButCol = [[100, 240, 100], [240, 230, 120], [240, 230, 120]]
menuBut = [pygame.Rect(90, 310 + i * 115, 250, 100) for i in range(len(menuButText))]
butPressed = 'none'

# load hardcoded images
picTitle = load_pics("images/UI/", "title")
picCircle = load_pics("images/UI/", "dots")
picShapes = load_pics("images/UI/", "shapes")
circleX = [0, 425, 850, 1275]
shapesX = [-425, 0, 425, 850]
picSpawnArrow = load_pics("images/UI/", "arrow")
picExitArrow = load_pics("images/UI/", "arrow2")

moneyPic = load_pics("images/UI/", "symbol_money")
lifePic = load_pics("images/UI/", "symbol_life")
energyPic = load_pics("images/UI/", "symbol_electricity")
energyMiniPic = load_pics("images/UI/", "symbol_electricity_2")

armourPic = load_pics("images/UI/", "armour")
# credits
creditText = creditParse.parse("data/credits")

# ---- LOAD CLASSES ----
# list of purchasable towers (turrets, boosters)
towerNames = ['Wall', 'Basic Turret', 'Freezer', 'Machinegun', 'Sniper Turret', 'Rocket Launcher',  'Laser Turret',
              'Power Station', 'Bank', 'damage module', 'rate module', 'range module']
# list of towers and boosters available for purchase, taken from towerNames and boosterNames
towerList = []
# UI button initialization
butListTowers = []

# create tower levelBut and add the tower classes
for i in range(len(towerNames)):
    towerList.append(tower.Turret(towerNames[i]))
    towerList[i].rotate(90)

# create turret buttons
for i in range(6):
    if i % 3 == 0:
        butListTowers.append(pygame.Rect(disL - 270, 155 + (i // 3) * 80, 70, 70))
    elif i % 3 == 1:
        butListTowers.append(pygame.Rect(disL - 185, 155 + (i // 3) * 80, 70, 70))
    elif i % 3 == 2:
        butListTowers.append(pygame.Rect(disL - 100, 155 + (i // 3) * 80, 70, 70))

# projectile image loading (uses a dictionary)
explosionImgList = {}
for i in range(len(towerList)):
    # get name of projectile
    nextImgName = towerList[i].stats['sprite_proj'][0] + "-hit"
    explosionImgList[nextImgName] = []
    curImg = 0
    while True:
        explosionImgList[nextImgName].append(load_pics("images/hit_effects/", nextImgName + str(curImg)))
        if os.path.isfile("images/hit_effects/" + nextImgName + str(curImg + 1) + ".png"):
            curImg += 1
        else:
            break

# switch page button image for puchase menu
imgNextPage = load_pics("images/UI/", "nextPg")
imgPrevPage = load_pics("images/UI/", "prevPg")
butNextPage = pygame.Rect(disL - 125 + 2, butListTowers[0][1] + 153 + 2,
                          imgNextPage.get_width() - 4, imgNextPage.get_height() - 4)
butPrevPage = pygame.Rect(disL - 205 + 2, butListTowers[0][1] + 153 - 2,
                          imgPrevPage.get_width() - 4, imgPrevPage.get_height() - 4)

# selling a tower button
butSell = pygame.Rect(disL - 250, disH - 120, 200, 30)

# upgrading tower buttons
butUpgrades = [pygame.Rect(disL - 60, 470 + i * 50, 30, 30) for i in range(5)]

# menu NEXT WAVE button
butNextWave = pygame.Rect(disL - 275, disH - 70, 250, 60)
colNextWaveBut = [[175, 175, 175], [15, 215, 110]]  # colour for round in progress vs. not in progress

# upgrade tower buttons (there are 4)
# x = 280
# 460, 495, 530, 565, 600
butUpgradeTower = [pygame.Rect(disL - 60, 420 + i * 30, 20, 20) for i in range(6)]
del(butUpgradeTower[3])  # delete proj_spd button


# ---- OUTER LOOP ----
while True:
    # ---- INTRO SCREEN ----
    outro = -1
    # intro music
    musicMenu = pygame.mixer.music.load('sounds/menu.ogg')
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)
    while intro:
        # should make it 60FPS max
        # dt is the number of seconds since the last frame, use this for calculations instead of fps to make it smoother
        dt = clock.tick(fps) / 1000
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
                    soundClick.play()
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
                    if pygame.mouse.get_pressed()[0] == 1 and outro < 0:
                        soundLevelSelect.play()
                        selectedMap = mapInfo[i]
                        outro = 45

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

        elif butPressed == "credits":
            # credit title
            components.create_text(screen, (400, 340), creditText[0], False, creditHeaderFont, (0, 0, 0))
            # create rest of credits
            for i in range(1, len(creditText)):
                components.create_text(screen, (400, 340 + i * 30), creditText[i], False, creditBodyFont, (0, 0, 0))

        # title text
        screen.blit(picTitle, (250, 50))
        # move circles using list comprehension
        circleX = [x - 140 * dt for x in circleX]
        for i in range(len(circleX)):
            if circleX[i] < - 425:
                circleX[i] += 1700
            # draw dot under title!
            screen.blit(picCircle, (int(circleX[i]), 175))
        # move other shapes using list comprehension
        shapesX = [x + 70 * dt for x in shapesX]
        for i in range(len(shapesX)):
            if shapesX[i] > 1325:
                shapesX[i] -= 1700
            # draw shapes!
            screen.blit(picShapes, (int(shapesX[i]), 225))

        # border
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, disL, disH), 3)

        # outro
        if outro > 0:
            outro -= 1
            colIntro[3] = 250 - outro * 5.5
            pygame.gfxdraw.filled_polygon(screen, [[0, 0], [disL, 0], [disL, disH], [0, disH]], colIntro)
        elif outro == 0:
            pygame.gfxdraw.filled_polygon(screen, [[0, 0], [disL, 0], [disL, disH], [0, disH]], [150, 165, 200, 255])
            intro = False

        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()

    # stop intro song
    pygame.mixer.music.stop()

    # ---- IN-GAME SETUP and reset variables----
    curWave = -1  # current wave, displayed value is 1 more than this (starts at -1)
    money = 500  # starting monies
    energy = [5, 5]  # amount of power left vs maximum
    income = 100  # monies per round
    interest = 0.05  # interest (10%) -> get this much bonus gold per unspent gold
    life = 50  # lose 1 life per enemy; 10 per boss
    currentlyInWave = False  # True when enemies are spawning
    deathTimer = -10000

    # page that its on
    curPurchasePage = 0

    # developer cheats (konami code)
    cheatVal = 0  # +1 everytime you press the correct key, otherwise resets to 0
    cheatList = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN,
                 pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_b]

    # mouse stuff
    mousePressed = pygame.mouse.get_pressed()
    selectedTower = 'none'
    selectedXY = [0, 0]
    selectedPos = [0, 0]

    # viewing placed towers
    viewedTower = -1  # index position of a placed tower, -1 if no tower

    # standard error messages
    msgTimer = -1  # timer in seconds
    msgText = ""

    # placed towers
    placedTowers = []  # list of tower objects, placed down
    placedTowersLoc = []  # used so that you cant overlap two towers

    # music change
    musicGame = pygame.mixer.music.load('sounds/ingame.ogg')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    # parse wave info
    waveInfo = waveParse.parse_wave_info("waveData")
    masterWaveTimer = 0

    # spawners
    curSpawnPoint = 0
    spawnerList = []  # active spawners

    # enemy lists
    enemyInfo = enemyParse.get_data('enemyData')
    enemyList = []  # list of active enemy objects

    # projectile list
    projList = []

    # projectile variables
    projExplosionList = []  # list of explosion classes

    # intro variables
    introScreen = 45

    # OBSTACLE PATHING
    updatePath = False
    path = selectedMap.find_path(placedTowersLoc)
    pathRect = [pygame.Rect(path[i][1][0] * 50 - 50, path[i][1][1] * 50 - 50, 50, 50) for i in range(len(path))]
    pathRect2 = [pygame.Rect(path[i][-2][0] * 50 - 50, path[i][-2][1] * 50 - 50, 50, 50) for i in range(len(path))]
    # arrowPics
    arrowPics = []
    for i in range(len(path)):
        # go right
        if path[i][0][0] < path[i][1][0]:
            arrowPics.append([components.rot_center(picSpawnArrow, 0), components.rot_center(picExitArrow, 0)])
        # go down
        elif path[i][0][1] < path[i][1][1]:
            arrowPics.append([components.rot_center(picSpawnArrow, 270), components.rot_center(picExitArrow, 270)])
        # go left
        elif path[i][0][0] > path[i][1][0]:
            arrowPics.append([components.rot_center(picSpawnArrow, 180), components.rot_center(picExitArrow, 180)])
        else:  # go up
            arrowPics.append([components.rot_center(picSpawnArrow, 90), components.rot_center(picExitArrow, 90)])

    # fast forward
    fastForward = False
    ffCounter = 1  # multiply by this to counter the effects of fast forwarding

    # ---- GAME LOOP ----
    while not intro:
        # should make it 60FPS max
        # dt is the number of seconds since the last frame, use this for calculations instead of fps to make it smoother
        dt = clock.tick(fps) / 1000
        if dt > 0.04:
            dt = 0.04

        mousePressed = [0, 0, 0]  # reset mouse presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = pygame.mouse.get_pressed()
            if event.type == pygame.KEYDOWN:
                # secret konami code!!! shh....
                if event.key == cheatList[cheatVal]:
                    cheatVal += 1
                    if cheatVal > len(cheatList) - 1:
                        # give a ton of money and life
                        cheatVal = 0
                        money = 9999
                        life = 200
                else:  # reset value if the cheat wasnt properly done
                    cheatVal = 0

        # get inputs
        mousePos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        hovered = False  # whether or not the mouse is hovering over a tower purchase button

        # fast forward
        if keys[pygame.K_SPACE]:
            fastForward = True
        else:
            fastForward = False
        if fastForward:
            fps = 120
            dt *= 3
            ffCounter = 1/3
        else:
            fps = 60
            dt *= 1
            ffCounter = 1

        # timers
        if deathTimer >= 0:
            deathTimer -= dt * ffCounter
        msgTimer -= dt * ffCounter
        if msgTimer < 0:
            msgTimer = -1

        if currentlyInWave:
            masterWaveTimer += dt
        else:
            masterWaveTimer = 0

        i = 0
        while i < len(projExplosionList):
            projExplosionList[i].show(screen, dt)
            if projExplosionList[i].stopped:
                del(projExplosionList[i])
            else:
                i += 1

        # ---- BACKGROUND ----
        screen.fill(selectedMap.colBackground)
        # obstacles
        if not currentlyInWave:
            components.draw_grid(screen, 0, 0, disL - 300, disH, 50, selectedMap.colGrid, False)
        selectedMap.draw_obstacles(screen)

        # path display stuff
        if not currentlyInWave:
            for i in range(len(path)):
                for j in range(len(path[i])):
                    pygame.draw.circle(screen, (0, 0, 0), (path[i][j][0] * 50 - 25, path[i][j][1] * 50 - 25), 2)

        # path line indicators (on hover)
        for i in range(len(pathRect)):
            if pathRect[i].collidepoint(mousePos[0], mousePos[1]) \
                    or pathRect2[i].collidepoint(mousePos[0], mousePos[1]):
                lines = [[path[i][a][0] * 50 - 26, path[i][a][1] * 50 - 26] for a in range(len(path[i]))]
                pygame.draw.lines(screen, (200, 50, 50), False, lines, 5)

        # path arrow indicators
        for i in range(len(arrowPics)):
            # spawn and exit indicator arrows
            screen.blit(arrowPics[i][0], (path[i][1][0] * 50 - 50, path[i][1][1] * 50 - 50))
            screen.blit(arrowPics[i][1], (path[i][-2][0] * 50 - 50, path[i][-2][1] * 50 - 50))

        # ---- ENEMY SPAWNING AND MOVEMENT ----
        # spawning
        if currentlyInWave:
            i = 0
            # create new spawners at the given intervals
            while i < len(waveInfo[curWave]):
                if waveInfo[curWave][i][2] <= masterWaveTimer:
                    # delete the wave info and create a spawner from it
                    spawnerList.append(spawner.Spawner(waveInfo[curWave][i],
                                                       enemyInfo[waveInfo[curWave][i][0]]))
                    del(waveInfo[curWave][i])
                    i -= 1

                i += 1

            # at certain intervals, spawners will spawn their designated enemy
            i = 0
            while i < len(spawnerList):
                spawnerList[i].timer += dt
                if spawnerList[i].timer >= spawnerList[i].interval:
                    # reset timer
                    spawnerList[i].timer -= spawnerList[i].interval
                    # append an enemy object to the list
                    enemyList.append(spawnerList[i].spawn_enemy(selectedMap.spawnList[curSpawnPoint], curSpawnPoint,
                                                                curWave))
                    # alternate between spawn locations
                    curSpawnPoint += 1
                    if curSpawnPoint >= len(selectedMap.spawnList):
                        curSpawnPoint = 0

                    # delete old spawners
                    if spawnerList[i].amount == 0:
                        del(spawnerList[i])
                        i -= 1

                i += 1

            # movement and enemy display
            i = 0
            while i < len(enemyList):
                enemyList[i].move(path[enemyList[i].path_number], dt)
                # enemy reaches end, take off lives, dont give monies
                if enemyList[i].reachedEnd and enemyList[i].endTimer <= 0:
                    #  money += enemyList[i].bounty  -> this is to give money even if enemy escapes
                    if enemyList[i].stats['type'] == 'BOSS':
                        life -= 10
                    else:
                        life -= 1
                    del (enemyList[i])
                else:
                    screen.blit(enemyList[i].stats['sprite'], (enemyList[i].posPx[0] - 35, enemyList[i].posPx[1] - 35))
                    i += 1

        # stop wave after defeating all enemies and spawners
        if len(enemyList) == 0 and len(spawnerList) == 0 and len(waveInfo[curWave]) == 0 and currentlyInWave:
            currentlyInWave = False
            # INCOME! :D
            money += income
            money *= (1 + interest)

        # ---- TOWERS ----
        # draw placed towers:
        # tower base
        for i in range(len(placedTowers)):
            placedTowers[i].draw_tower_base(screen, [placedTowers[i].pos[0] * 50 - 25,
                                                     placedTowers[i].pos[1] * 50 - 25])
        # if a tower is viewed, draw the red outline here (before gun, after base)
        if viewedTower >= 0:
            pygame.draw.rect(screen, (200, 75, 75), (placedTowers[viewedTower].pos[0] * 50 - 50,
                                                     placedTowers[viewedTower].pos[1] * 50 - 50, 50, 50), 3)

        # tower gun
        for i in range(len(placedTowers)):
            placedTowers[i].draw_tower_gun(screen, [placedTowers[i].pos[0] * 50 - 25,
                                                    placedTowers[i].pos[1] * 50 - 25])

        # unselect a tower
        if (mousePos[0] > disL - 300 and mousePressed[0] == 1 or keys[pygame.K_ESCAPE]) and selectedTower != 'none':
            mousePressed = [0, 0]  # so you don't select another tower when unselecting
            selectedTower = 'none'

        # choose where to place down the tower, click to place
        if selectedTower != 'none':
            # calculate the validity of the current placement
            valid = False
            if 10 <= mousePos[0] <= disL - 310 and 10 <= mousePos[1] <= disH - 10 and selectedMap.calc_valid(mousePos)\
                    and components.xy_to_pos(mousePos) not in placedTowersLoc:
                valid = True

            # lock to grid inside it and draw range when valid
            if valid:
                gridLoc = components.xy_to_pos(mousePos)
                selectedTower.pos = [gridLoc[0], gridLoc[1]]
                selectedTower.draw_tower_full(screen, (selectedTower.pos[0] * 50 - 25,
                                                       selectedTower.pos[1] * 50 - 25))
                if selectedTower.type == "turret":
                    selectedTower.draw_range(screen, valid)
                elif selectedTower.type == "booster":
                    # draw adjacent squares
                    selectedTower.draw_boost_range(screen, valid)

                # place down the tower when selected
                if mousePressed[0] == 1:
                    # append the location to the list
                    placedTowersLoc.append(selectedTower.pos)
                    # if the tower is too expensive or it blocks the path, play an error sound
                    if money < selectedTower.cost:
                        soundError.play()
                        del(placedTowersLoc[-1])
                        msgTimer = 0.5
                        msgText = "Can't afford this tower!"
                    elif energy[0] - selectedTower.energy < 0:
                        soundError.play()
                        del (placedTowersLoc[-1])
                        msgTimer = 0.5
                        msgText = "Insufficient energy!"
                    elif selectedMap.find_path(placedTowersLoc) == -1:
                        soundError.play()
                        del (placedTowersLoc[-1])
                        msgTimer = 0.5
                        msgText = "Tower blocks path!"
                    else:
                        soundPlaced.play()
                        # copy as a NEW object
                        placedTowers.append(tower.Turret(selectedTower.name))
                        # energy
                        if selectedTower.energy < 0:
                            energy[1] -= selectedTower.energy
                            energy[0] -= selectedTower.energy
                        else:
                            energy[0] -= selectedTower.energy
                        if placedTowers[-1].special == 'income':  # update income on buy
                            income += int(placedTowers[-1].specialVal)
                        placedTowers[-1].pos = selectedTower.pos
                        placedTowers[-1].placed = True  # set it to be placed!!
                        # lower monies
                        money -= selectedTower.cost
                        # update pathing
                        updatePath = True

                        # find all towers adjacent to it
                        adjacentTowerList = []
                        for i in placedTowers:
                            # calculate distance to tower and check if it equals one
                            if abs(placedTowers[-1].pos[0] - i.pos[0]) + abs(placedTowers[-1].pos[1] - i.pos[1]) == 1:
                                adjacentTowerList.append(i)
                        
                        # update self if turret
                        if placedTowers[-1].type == "turret":
                            placedTowers[-1].calc_boost(adjacentTowerList)

                        # update each adjacent tower if booster
                        elif placedTowers[-1].type == "booster":
                            for i in adjacentTowerList:
                                secAdjTowerList = []
                                for j in placedTowers:
                                    # calculate distance to tower and check if it equals one
                                    if abs(i.pos[0] - j.pos[0]) + abs(i.pos[1] - j.pos[1]) == 1:
                                        secAdjTowerList.append(j)

                                i.calc_boost(secAdjTowerList)

            # don't lock to grid if out of bounds
            elif not valid:
                selectedTower.draw_tower_full(screen, [mousePos[0], mousePos[1]])
                if selectedTower.type == "turret":
                    selectedTower.draw_range(screen, valid, xy=[mousePos[0], mousePos[1]])
                elif selectedTower.type == "booster":
                    pass
                if mousePressed[0] == 1:  # error if user tries to place invalid tower
                    soundError.play()

        # enemy lists and stuffs
        enemyPosList = []
        enemyDistLeftList = []
        enemyRadList = []
        for i in range(len(enemyList)):
            enemyPosList.append(enemyList[i].posPx)
            enemyDistLeftList.append(enemyList[i].distance)
            enemyRadList.append(enemyList[i].stats['radius'])

        # targeting and shooting
        if currentlyInWave:
            for i in range(len(placedTowers)):
                if placedTowers[i].type == "turret":
                    placedTowers[i].calc_rotation(enemyPosList, enemyDistLeftList, enemyRadList, dt)
                    if placedTowers[i].canFire:
                        projList.append(placedTowers[i].fire_projectile())
        else:  # rotate to face the first enemy if its a turret
            for i in range(len(placedTowers)):
                if placedTowers[i].type == "turret":
                    placedTowers[i].rotate(90)

        i = 0
        # displaying bullets and stuffs
        while i < len(projList):  # use while loops instead of  for loops cuz of element deletion
            enemyHit = projList[i].update(dt, screen, enemyList)
            # see if it hits an enemy(s) using masks
            if enemyHit != []:
                # sound
                projList[i].sound.play()
                # do all maths
                j = 0
                # apply damages and stuffs
                for j in range(len(enemyHit)):
                    # inflict damage
                    enemyHit[j].inflict_damage(projList[i].damage, projList[i].special)
                    # enemy dies
                    if enemyHit[j].curHP <= 0:
                        money += enemyHit[j].bounty
                        # spawn additional enemies on death if condition is met
                        if enemyHit[j].stats["death_spawn_enemy"] != "none":
                            spawnedEnemy = enemyInfo[enemyHit[j].stats["death_spawn_enemy"]]
                            for k in range(int(enemyHit[j].stats["death_spawn_val"])):
                                enemyList.append(enemy.Enemy(spawnedEnemy, enemyHit[j].tileLoc, enemyHit[j].path_number, curWave))
                                enemyList[-1].posPx[0] += random.randint(-5, 5)
                                enemyList[-1].posPx[1] += random.randint(-5, 5)
                                enemyList[-1].status.append(['slow', 1.0, k*0.1 + random.uniform(0,0.05)])
                        # delete if from the table
                        del(enemyList[enemyList.index(enemyHit[j])])

                # add explosion pic
                if projList[i].targeting[0] == 'splash' or projList[i].targeting[0] == 'aura':
                    projExplosionList.append(explosion.Explosion(projList[i].posXYPx,
                                                                 explosionImgList[projList[i].exp], float(projList[i].targeting[1]) * 100, projList[i].angle))
                    del (projList[i])
                    i -= 1

                # if it has piercing, keep going
                elif projList[i].targeting[0] == 'piercing' and len(projList[i].hitlist) > projList[i].targeting[1]:
                    projExplosionList.append(explosion.Explosion(projList[i].posXYPx,
                                                                explosionImgList[projList[i].exp], -1, projList[i].angle))
                    del (projList[i])
                    i -= 1
                else:
                    projExplosionList.append(explosion.Explosion(projList[i].posXYPx,
                                                                 explosionImgList[projList[i].exp], -1, projList[i].angle))
                    del (projList[i])
                    i -= 1

            elif projList[i].distance[0] > projList[i].distance[1]:  # projectile expires
                del(projList[i])
                i -= 1

            i += 1

        # display explosions
        i = 0
        while i < len(projExplosionList):
            projExplosionList[i].show(screen, dt)
            if projExplosionList[i].stopped:
                del projExplosionList[i]
            else:
                i += 1

        # if a tower is viewed, draw its range
        if viewedTower >= 0:
            if placedTowers[viewedTower].type == "turret":
                placedTowers[viewedTower].draw_range(screen, True)
            elif placedTowers[viewedTower].type == "booster":
                placedTowers[viewedTower].draw_boost_range(screen, True)

        # display enemy healthbar and armour
        if currentlyInWave:
            for i in range(len(enemyList)):
                enemyList[i].draw_bar(screen, armourPic)

        # ---- UI ELEMENTS ----
        # ui background
        pygame.draw.rect(screen, colPurchaseMenu, (disL - 300, 0, 300, disH), 0)

        # borders
        pygame.draw.rect(screen, selectedMap.colObs, (0, 0, disL, disH), 4)
        pygame.draw.line(screen, selectedMap.colObs, (disL - 300, 0), (disL - 300, disH), 3)

        # sub dividers, from top to bottom
        pygame.draw.line(screen, (70, 70, 70), (disL - 300, butListTowers[0][1] - 18), (disL, butListTowers[0][1] - 18))
        pygame.draw.line(screen, (70, 70, 70), (disL - 300, butListTowers[0][1] + 185),
                         (disL, butListTowers[0][1] + 185))
        pygame.draw.line(screen, (70, 70, 70), (disL - 300, disH - 80),
                         (disL, disH - 80))

        # next wave button
        colNextWaveText = [0, 0, 0]
        if currentlyInWave:  # in wave
            pygame.draw.rect(screen, colNextWaveBut[0], butNextWave)
            pygame.draw.rect(screen, (0, 0, 0), butNextWave, 1)
            colNextWaveText = [55, 55, 55]
            components.create_text(screen, (disL - 150, disH - 20), 'spacebar to fast forward',
                                   True, levelFastFont, (0, 0, 0))
        elif not currentlyInWave:  # not in wave
            pygame.draw.rect(screen, colNextWaveBut[1], butNextWave)
            pygame.draw.rect(screen, (0, 0, 0), butNextWave, 1)
            # get hover
            if butNextWave.collidepoint(mousePos[0], mousePos[1]):
                pygame.draw.rect(screen, (0, 0, 0), butNextWave, 3)
                # START NEXT WAVE :O
                if mousePressed[0] == 1:
                    soundNextWave.play()
                    curWave += 1
                    currentlyInWave = True
                    curSpawnPoint = random.randint(0, len(selectedMap.spawnList) - 1)
                    # make sure you don't place towers during a wave
                    selectedTower = 'none'
                    # reset tower CD
                    for i in placedTowers:
                        i.reload = 0.05

        # next wave text
        components.create_text(screen, (butNextWave[0] + butNextWave[2] // 2, butNextWave[1] + butNextWave[3] // 2),
                               "NEXT WAVE", True, levelNextWaveFont, colNextWaveText)

        # switch page buttons
        if curPurchasePage > 0:  # previous page
            screen.blit(imgPrevPage, (disL - 205, butListTowers[0][1] + 153))
            # get hit box and mouse click
            if butPrevPage.collidepoint(mousePos[0], mousePos[1]) and mousePressed[0] == 1:
                soundClick.play()
                curPurchasePage -= 1
        if curPurchasePage < (len(towerList) - 1) // 6:  # next page
            screen.blit(imgNextPage, (disL - 125, butListTowers[0][1] + 153))
            # get hit box and mouse click
            if butNextPage.collidepoint(mousePos[0], mousePos[1]) and mousePressed[0] == 1:
                soundClick.play()
                curPurchasePage += 1

        # purchase tower images
        mul6 = curPurchasePage * 6
        # purchase tower actual buttons and outline
        for i in range(6):
            # select a tower
            if i + mul6 < len(towerList):
                pygame.draw.rect(screen, (230, 230, 250), (butListTowers[i]))
                # on hover
                if butListTowers[i].collidepoint(mousePos[0], mousePos[1]) and selectedTower == 'none' \
                        and not currentlyInWave:
                    hovered = True
                    display_stats(towerList[i + mul6])
                    # user has enough money to buy the tower
                    if towerList[i + mul6].cost <= money and energy[0] - towerList[i + mul6].energy >= 0:
                        pygame.draw.rect(screen, (255, 255, 255), (butListTowers[i]), 2)
                        # select tower on click
                        if mousePressed[0] == 1:
                            soundClick.play()
                            selectedTower = towerList[i + mul6]
                    else:  # not enough money, play meep merp on purchase attempt
                        if mousePressed[0] == 1:
                            soundError.play()
                            selectedTower = 'none'
                            if towerList[i + mul6].cost > money:
                                msgText = "Can't afford this tower!"
                                msgTimer = 0.5
                            elif towerList[i + mul6].energy + energy[0] > energy[1]:
                                msgText = "Insufficient energy!"
                                msgTimer = 0.5

                # Let the user know you can't buy towers during a wave
                elif butListTowers[i].collidepoint(mousePos[0], mousePos[1]) \
                        and mousePressed[0] == 1 and currentlyInWave:
                    soundError.play()
                    msgText = "Cannot buy towers during a wave"
                    msgTimer = 0.75

        for i in range(mul6, mul6 + 6, 1):
            # draw towers on top of the buttons
            if i < len(towerList):
                # draw base + gun for turret
                towerList[i].draw_tower_full(screen, [butListTowers[i - mul6][0] + butListTowers[i - mul6][2] // 2,
                                                      butListTowers[i - mul6][1] + butListTowers[i - mul6][3] // 2])

        # show stats of selected tower
        if selectedTower != 'none':  # while placing
            # display stats of selected tower
            display_stats(selectedTower)
            viewedTower = -1
        else:  # tower on ground
            if mousePressed[0] == 1:
                if components.xy_to_pos(mousePos) in placedTowersLoc and mousePos[0] < 1000:
                    soundClick.play()
                    viewedTower = placedTowersLoc.index(components.xy_to_pos(mousePos))
                # deselect viewed tower
                elif mousePos[0] < 1000:
                    viewedTower = -1

            # draw range of da tower
            if viewedTower >= 0:
                if not hovered:
                    # stats
                    display_stats(placedTowers[viewedTower])

                    # sell button
                    pygame.draw.rect(screen, (225, 100, 100), butSell)
                    # text of sell button
                    components.create_text(screen, (butSell[0] + butSell[2] // 2, butSell[1] + butSell[3] // 2),
                                           'SELL FOR $' + str(int(placedTowers[viewedTower].sellPrice)),
                                           True, levelTowerFont, (0, 0, 0))
                    # interact with sell button
                    if butSell.collidepoint(mousePos[0], mousePos[1]) and not currentlyInWave:
                        pygame.draw.rect(screen, (0, 0, 0), butSell, 3)
                        if mousePressed[0] == 1:  # on click, sell the tower
                            # energy check
                            if energy[0] < 0 - placedTowers[viewedTower].energy:
                                soundError.play()
                                msgText = 'Energy too low!'
                                msgTimer = 0.75
                            else:  # passes energy check
                                if placedTowers[viewedTower].energy < 0:
                                    energy[1] += placedTowers[viewedTower].energy
                                    energy[0] += placedTowers[viewedTower].energy
                                else:  # remove da tower
                                    energy[0] += placedTowers[viewedTower].energy
                                # update monies
                                money += int(placedTowers[viewedTower].sellPrice)
                                soundSell.play()
                                if placedTowers[viewedTower].special == 'income':  # update income on sell
                                    income -= placedTowers[viewedTower].specialVal
                                
                                # check boosts
                                placedTowers[viewedTower].specialVal = 0
                                adjacentTowerList = []
                                for i in placedTowers:
                                    # calculate distance to tower and check if it equals one
                                    if abs(placedTowers[viewedTower].pos[0] - i.pos[0]) + abs(placedTowers[viewedTower].pos[1] - i.pos[1]) == 1:
                                        adjacentTowerList.append(i)
                                # update each adjacent tower if booster
                                if placedTowers[viewedTower].type == "booster":
                                    for i in adjacentTowerList:
                                        secAdjTowerList = []
                                        for j in placedTowers:
                                            # calculate distance to tower and check if it equals one
                                            if abs(i.pos[0] - j.pos[0]) + abs(i.pos[1] - j.pos[1]) == 1:
                                                secAdjTowerList.append(j)

                                        i.calc_boost(secAdjTowerList)

                                del placedTowers[viewedTower]
                                del placedTowersLoc[viewedTower]
                                updatePath = True  # reset path
                                viewedTower = -1  # reset viewed tower
                    elif mousePressed[0] == 1 and butSell.collidepoint(mousePos[0], mousePos[1]) and currentlyInWave:
                        soundError.play()
                        msgText = 'Cannot sell towers during a wave'
                        msgTimer = 0.75
                    else:
                        pygame.draw.rect(screen, (0, 0, 0), butSell, 1)

        # limit money to 9999
        if money > 9999:
            money = 9999

        # info about money, life, etc.
        # life
        screen.blit(lifePic, (disL - 280, 20))
        components.create_text(screen, (disL - 230, 40), str(life), False, levelInfoFont, (0, 0, 0))
        # wave
        components.create_text(screen, (disL - 140, 40), "wave  " + str(curWave + 1), False, levelInfoFont, (0, 0, 0))
        # money
        screen.blit(moneyPic, (disL - 280, 70))
        components.create_text(screen, (disL - 230, 90), str(int(money)), False, levelInfoFont, (0, 0, 0))
        components.create_text(screen, (disL - 225, 112), str(int(income)) + " + " + str(int(interest*100)) + "%", False, levelSmallInfoFont, (0, 0, 0))
        # energy
        screen.blit(energyPic, (disL - 150, 70))
        components.create_text(screen, (disL - 110, 90), str(energy[0]) + "/" + str(energy[1]),
                               False, levelInfoFont, (0, 0, 0))
        
        if life <= 0 and deathTimer < -100:
            msgTimer = 2
            msgText = "You died!"
            deathTimer = 2
        # standard message (bottom of screen)
        if msgTimer >= 0:
            components.create_text(screen, (500, disH - 100), msgText, True, levelInfoFont, (150, 25, 25))

        # show a fading bluish screen after selecting the level
        if introScreen > 0:
            introScreen -= 1
            colIntro[3] = 10 + introScreen * 5.5
            pygame.gfxdraw.filled_polygon(screen, [[0, 0], [disL, 0], [disL, disH], [0, disH]], colIntro)
        
        # update path ONCE if it was true at all:
        if updatePath:
            path = selectedMap.find_path(placedTowersLoc)
            updatePath = False

        # update display!
        pygame.display.update()

        if -100 < deathTimer < 0:
            intro = True
