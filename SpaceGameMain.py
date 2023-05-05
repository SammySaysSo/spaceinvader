# -*- coding: utf-8 -*- Aug 8 2021 by sam brey
import pygame
import random
from pygame import mixer

# main game: hearts/lasers drop down(4 lives if get it?)
# other: options to turn sound/music on or off, fix lag?

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

background = pygame.image.load('background.jpg')
startingBackground = pygame.image.load('startingBGpic.jpg')
heart1 = pygame.image.load('heart.png')
heart2 = pygame.image.load('heart.png')
heart3 = pygame.image.load('heart.png')
emptyHeart1 = pygame.image.load('emptyHeart.png')
emptyHeart2 = pygame.image.load('emptyHeart.png')
emptyHeart3 = pygame.image.load('emptyHeart.png')

mixer.music.load('forceBGmusic.wav')
mixer.music.play(-1)
mixer.music.pause()

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
def player(x,y):
    screen.blit(playerImg, (x, y)) #blit = drawing image onto screen

bossImg = pygame.image.load('boss.png')
bossX = 336
bossY = 0
bossX_change = 3
bossHP = 185
checkB = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemies = 0
speed = 0

def createEnemies(num, s):
    for i in range(num):
        enemyImg.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(65, 735))
        enemyY.append(random.randint(0, 75))
        enemyX_change.append(s) # 3
        enemyY_change.append(32)

def enemy(x,y, i):
    screen.blit(enemyImg[i], (x, y))
    
#enemy2
enemyImg2 = []
enemyX2 = []
enemyY2 = []
enemyY2_change = []
numOfEnemies2 = 0
speed2 = .5

def createEnemies2(num, s): 
    for i in range(num):
        enemyImg2.append(pygame.image.load('enemy2.png'))
        enemyX2.append(random.randint(65, 735))
        enemyY2.append(random.randint(0, 75))
        enemyY2_change.append(s)

def enemy2(x,y, i):
    screen.blit(enemyImg2[i], (x, y))
    
#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = -7
bulletState = "ready"
def fireBullet(x,y):
    global bulletState
    global bulletX
    bulletX = x
    bulletState = "fire"
    screen.blit(bulletImg, (x+16, y+10))
#bullet2
bulletImg2 = pygame.image.load('bullet.png')
bulletX2 = 0
bulletY2 = 480
bulletY2_change = -7
bulletState2 = "ready"
def fireBullet2(x,y):
    global bulletState2
    global bulletX2
    bulletX2 = x
    bulletState2 = "fire"
    screen.blit(bulletImg2, (x+16, y+10))

red = (255, 0, 0)
white = (255, 255, 255)
lightRed = (255, 127, 127)
grey = (128,128,128)
black = (0, 0, 0)
green = (0,128,0)

score = 0
lives = 3
pause = False
c = 1
scoreFont = pygame.font.Font('freesansbold.ttf',32)
gameOver = pygame.font.Font('freesansbold.ttf',64)
startFont = pygame.font.Font('freesansbold.ttf',32)
startF = startFont.render("Start", True, white)
instructionsF = startFont.render("Instructions", True, white)
bts = startFont.render("Back to Start", True, white)
instructText = pygame.font.Font('freesansbold.ttf',25)
pauseText = gameOver.render("Pause", True, red)

textX = 10
textY = 10
def showScore(x,y):
    s = scoreFont.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(s, (x, y))

def collision(eX, eY, bX, bY):
    if eX >= bX and eX < bX+32 or bX >= eX and bX < eX+32:
        if eY >= bY and eY < bY+32 or bY >= eY and bY < eY+32:
            return True
    return False
def collisionBoss(eX, eY, bX, bY):
    if eX >= bX and eX < bX+32 or bX >= eX and bX < eX+96:
        if eY >= bY and eY < bY+32 or bY >= eY and bY < eY+96:
            return True
    return False

def startingScreen():
    screen.fill((0, 0, 0))
    screen.blit(startingBackground, (150,0))
    mixer.music.unpause()
    color1 = red
    color2 = red
    runningStart = True
    while runningStart:
        pygame.draw.rect(screen, color1, (275, 300, 250, 60))
        pygame.draw.rect(screen, color2, (275, 400, 250, 60))
        screen.blit(startF, (360, 315))
        screen.blit(instructionsF, (303, 415))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    x1, y2 = pygame.mouse.get_pos()
                    if x1 >= 275 and x1 < 525 and y2 >= 300 and y2 < 360: 
                        runningStart = False
                        mixer.music.pause()
                        main()
                        return
                    if x1 >= 275 and x1 < 525 and y2 >= 400 and y2 < 460: 
                        runningStart = False
                        instructionScreen()
                        return
            x, y = pygame.mouse.get_pos()
            if x >= 275 and x < 525 and y >= 300 and y < 360: color1 = lightRed
            else: color1 = red
            if x >= 275 and x < 525 and y >= 400 and y < 460: color2 = lightRed
            else: color2 = red
        clock.tick(60) #FPS: 30
        pygame.display.update()

def instructionScreen():
    screen.fill((0, 0, 0))
    screen.blit(startingBackground, (150,0))
    inText1 = instructText.render("Move left or right using the arrow or wsad keys", True, white)
    inText2 = instructText.render("Press spacebar to shoot at the aliens", True, white)
    inText3 = instructText.render("Don't let the aliens reach the bottom", True, white)
    inText4 = instructText.render("Press p to pause the game", True, white)
    inText5 = instructText.render("You have 3 lives. Have fun", True, white)
    
    color1 = red
    instructionStart = True
    while instructionStart:
        pygame.draw.rect(screen, color1, (275, 520, 250, 60))
        screen.blit(bts, (301, 535))
        screen.blit(inText1, (100, 300))
        screen.blit(inText2, (100, 335))
        screen.blit(inText3, (100, 370))
        screen.blit(inText4, (100, 405))
        screen.blit(inText5, (100, 440))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    x1, y2 = pygame.mouse.get_pos()
                    if x1 >= 275 and x1 < 525 and y2 >= 500 and y2 < 580: 
                        instructionStart = False
                        startingScreen()
                        return
        x, y = pygame.mouse.get_pos()
        if x >= 275 and x < 525 and y >= 520 and y < 580: color1 = lightRed
        else: color1 = red
        clock.tick(60) #FPS: 30
        pygame.display.update()

def endingScreen(s, bhp):
    screen.fill((0, 0, 0))
    screen.blit(startingBackground, (150,0))
    if bhp <= 0: go1 = gameOver.render("CONGRATULATIONS", True, white)
    else: go1 = gameOver.render("GAME OVER", True, white)
    go2 = scoreFont.render("Final Score: " + str(s), True, white)
    go3 = scoreFont.render("Made by Sam Brey", True, white)
    go4 = scoreFont.render("Play Again", True, white)
    go5 = scoreFont.render("Back to Start", True, white)
    if bhp <= 0: screen.blit(go1, (75, 300))
    else: screen.blit(go1, (200, 300))
    screen.blit(go2, (200, 400))
    screen.blit(go3, (200, 450))
    
    color1 = red
    color2 = red
    ending = True
    while ending:
        pygame.draw.rect(screen, color1, (100, 500, 250, 60))
        pygame.draw.rect(screen, color2, (450, 500, 250, 60))
        screen.blit(go4, (140, 515))
        screen.blit(go5, (475, 515))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    x1, y2 = pygame.mouse.get_pos()
                    if x1 >= 100 and x1 < 350 and y2 >= 500 and y2 < 560: 
                        ending = False
                        mixer.music.play(-1)
                        mixer.music.pause()
                        main()
                        return
                    if x1 >= 450 and x1 < 700 and y2 >= 500 and y2 < 560: 
                        ending = False
                        mixer.music.play(-1)
                        mixer.music.pause()
                        startingScreen()
                        return
            x, y = pygame.mouse.get_pos()
            if x >= 100 and x < 350 and y >= 500 and y < 560: color1 = lightRed
            else: color1 = red
            if x >= 450 and x < 700 and y >= 500 and y < 560: color2 = lightRed
            else: color2 = red
        clock.tick(60) #FPS: 30
        pygame.display.update()

def main():
    global playerX, score, bulletY, bulletX, bulletY_change, playerY, playerX_change, bulletState, numOfEnemies, numOfEnemies2, lives, pause, c, bulletY2, bulletX2, bulletY2_change, bulletState2, bossX, bossY, bossX_change, bossHP, checkB
    score = 0
    lives = 3
    level = 1
    speed = 3
    checkB = 0
    bossHP = 185
    pause = False
    c = 1
    speed2 = .5
    numOfEnemies = 3
    numOfEnemies2 = 0
    createEnemies(numOfEnemies, speed)
    createEnemies2(numOfEnemies2, speed2)
    mixer.music.unpause()
    running = True
    while running:
        screen.fill((0, 0, 0)) #make sure to draw this first then the player & everything else
        screen.blit(background, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_p:
                    if pause == False: 
                        pause = True
                        c += 1
                    else: 
                        c += 1
                        pause = False
                if event.key == pygame.K_LEFT and pause == False: playerX_change = -5
                elif event.key == pygame.K_RIGHT and pause == False: playerX_change = 5
                elif event.key == pygame.K_a and pause == False: playerX_change = -5
                elif event.key == pygame.K_d and pause == False: playerX_change = 5
                elif event.key == pygame.K_SPACE and pause == False and (bulletY == 480 or bulletY2 == 480):
                    if bulletY == 480:
                        fireBullet(playerX, bulletY)
                        laserSound = mixer.Sound('laser.wav')
                        laserSound.play()
                    elif bulletY2 == 480:
                        fireBullet2(playerX, bulletY2)
                        laserSound = mixer.Sound('laser.wav')
                        laserSound.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d: playerX_change = 0
        
        playerX += playerX_change
        if playerX <= 0: playerX = 0
        elif playerX >= 736: playerX = 736
        
        if score >= 50: #50, level 2
            if level == 1:
                for i in range(numOfEnemies):
                    enemyY[i] = random.randint(0, 100)
                createEnemies(5, speed)
                numOfEnemies += 5
                level += 1
        if score >= 250: #250, level 3
            if level == 2:
                speed = 5
                for i in range(numOfEnemies):
                    enemyY[i] = random.randint(0, 100)
                for i in range(numOfEnemies):
                    enemyX_change[i] = 5
                level += 1
        if score >= 400: #400, level 4
            if level == 3:
                for i in range(numOfEnemies):
                    enemyX_change[i] = 3
                numOfEnemies = 0
                numOfEnemies2 = 3
                speed2 = .5
                createEnemies2(numOfEnemies2, speed2)
                level += 1
        if score >= 550: #550, level 5
            if level == 4:
                speed2 = 1
                createEnemies2(1, speed2)
                numOfEnemies2 += 1
                for i in range(numOfEnemies2):
                    enemyY2[i] = 10
                for i in range(numOfEnemies2):
                    enemyY2_change[i] = 1
                level += 1
        if score >= 750: #750, level 6
            if level == 5:
                numOfEnemies2 = 3
                speed = 3
                speed2 = .5
                createEnemies(5, speed)
                numOfEnemies = 5
                for i in range(numOfEnemies):
                    enemyY[i] = random.randint(0, 100)
                for i in range(numOfEnemies2):
                    enemyY2[i] = 10
                for i in range(numOfEnemies2):
                    enemyY2_change[i] = .5
                level += 1
        if score >= 1200: #1200, level 7
            if level == 6:
                numOfEnemies2 += 2
                numOfEnemies += 5
                speed = 3
                speed2 = .5
                createEnemies(5, speed)
                createEnemies2(2, speed2)
                for i in range(numOfEnemies):
                    enemyX[i] = random.randint(0, 735)
                for i in range(numOfEnemies2):
                    enemyX2[i] = random.randint(0, 735)
                for i in range(numOfEnemies):
                    enemyY[i] = random.randint(0, 100)
                for i in range(numOfEnemies2):
                    enemyY2[i] = random.randint(0, 50)
                for i in range(numOfEnemies2):
                    enemyY2_change[i] = .5
                level += 1
        if score >= 2000: #2000, level 8
            if level == 7:
                speed2 = .75
                for i in range(numOfEnemies):
                    enemyX[i] = random.randint(0, 735)
                for i in range(numOfEnemies2):
                    enemyX2[i] = random.randint(0, 735)
                for i in range(numOfEnemies):
                    enemyY[i] = random.randint(0, 100)
                for i in range(numOfEnemies2):
                    enemyY2[i] = random.randint(0, 50)
                for i in range(numOfEnemies2):
                    enemyY2_change[i] = .75
                level += 1
        if score >= 3000: #3000, level 9
            if level == 8:
                numOfEnemies2 = 3
                numOfEnemies += 5
                speed = 5
                speed2 = 1
                createEnemies(5, speed)
                for i in range(numOfEnemies):
                    enemyX[i] = random.randint(0, 735)
                for i in range(numOfEnemies2):
                    enemyX2[i] = random.randint(0, 735)
                for i in range(numOfEnemies):
                    enemyY[i] = random.randint(0, 100)
                for i in range(numOfEnemies2):
                    enemyY2[i] = random.randint(0, 50)
                for i in range(numOfEnemies2):
                    enemyY2_change[i] = 1
                level += 1
        if score >= 4000: #400, level 10: boss
            if level == 9:
                numOfEnemies = 0
                numOfEnemies2 = 0
                level += 1
        
        for i in range(numOfEnemies):
            if pause == False:
                if enemyY[i] > 400: #400
                    if lives > 1:
                        for j in range(numOfEnemies):
                            enemyY[j] = 0
                        for j in range(numOfEnemies2):
                            enemyY2[j] = 0
                        lives -= 1
                    else:
                        for j in range(numOfEnemies):
                            enemyY[j] = 0
                        mixer.music.stop()
                        running = False
                        break
                
                if enemyX[i] >= 736 or enemyX[i] <= 0: 
                    enemyX_change[i] *= -1
                    enemyY[i] += enemyY_change[i]
                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= -5: 
                    enemyX[i] = 400
                
                collide = collision(enemyX[i], enemyY[i], bulletX, bulletY)
                collide2 = collision(enemyX[i], enemyY[i], bulletX2, bulletY2)
                if collide:
                    if level < 10:
                        enemyX[i] = random.randint(0, 735)
                        enemyY[i] = random.randint(0, 75)
                    else: 
                        enemyX[i] = bossX+32
                        enemyY[i] = bossY+128
                    bulletY = 480
                    bulletState = "ready"
                    score += 10
                    collideSound = mixer.Sound('explosion.wav')
                    collideSound.play()
                if collide2:
                    if level < 10:
                        enemyX[i] = random.randint(0, 735)
                        enemyY[i] = random.randint(0, 75)
                    else: 
                        enemyX[i] = bossX+32
                        enemyY[i] = bossY+128
                    bulletY2 = 480
                    bulletState2 = "ready"
                    score += 10
                    collideSound = mixer.Sound('explosion.wav')
                    collideSound.play()
                
                enemy(enemyX[i], enemyY[i], i)
        
        for i in range(numOfEnemies2):
            if pause == False:
                if enemyY2[i] > 400: #400
                    if lives > 1:
                        for j in range(numOfEnemies):
                            enemyY[j] = 0
                        for j in range(numOfEnemies2):
                            enemyY2[j] = 0
                        lives -= 1
                    else:
                        for j in range(numOfEnemies):
                            enemyY[j] = 0
                        mixer.music.stop()
                        running = False
                        break
            
                enemyY2[i] += enemyY2_change[i]
                
                collide3 = collision(enemyX2[i], enemyY2[i], bulletX, bulletY)
                collide4 = collision(enemyX2[i], enemyY2[i], bulletX2, bulletY2)
                if collide3:
                    if level < 10:
                        enemyX2[i] = random.randint(0, 735)
                        enemyY2[i] = random.randint(0, 75)
                    else: 
                        enemyX2[i] = bossX+32
                        enemyY2[i] = bossY+100
                    bulletY = 480
                    bulletState = "ready"
                    score += 10
                    collideSound = mixer.Sound('explosion.wav')
                    collideSound.play()
                if collide4:
                    if level < 10:
                        enemyX2[i] = random.randint(0, 735)
                        enemyY2[i] = random.randint(0, 75)
                    else: 
                        enemyX2[i] = bossX+32
                        enemyY2[i] = bossY+100
                    bulletY2 = 480
                    bulletState2 = "ready"
                    score += 10
                    collideSound = mixer.Sound('explosion.wav')
                    collideSound.play()
                    
                enemy2(enemyX2[i], enemyY2[i], i)
        
        if pause == True: 
            screen.blit(pauseText, (300, 100))
            mixer.music.pause()
            for j in range(numOfEnemies):
                enemyX_change[j] = 0
            for j in range(numOfEnemies2):
                enemyY2_change[j] = 0
        elif c % 2 == 1 and c != 1: 
            mixer.music.unpause()
            for j in range(numOfEnemies):
                enemyX_change[j] = speed
            for j in range(numOfEnemies2):
                enemyY2_change[j] = speed2
            c = 1
        
        if bulletY <= 0:
            bulletY = 480
            bulletState = "ready"
        if bulletState == "fire":
            bulletY += bulletY_change
            fireBullet(bulletX, bulletY)
        if bulletY2 <= 0:
            bulletY2 = 480
            bulletState2 = "ready"
        if bulletState2 == "fire":
            bulletY2 += bulletY2_change
            fireBullet2(bulletX2, bulletY2)
        
        if level == 10 and pause == False:
            if bossX <= 0: bossX_change *= -1
            elif bossX >= 671: bossX_change *= -1
            bossX += bossX_change
            collide = collisionBoss(bossX, bossY, bulletX, bulletY)
            collide2 = collisionBoss(bossX, bossY, bulletX2, bulletY2)
            if checkB == 0:
                numOfEnemies2 = 1
                numOfEnemies = 1
                speed = 5
                speed2 = 1
                createEnemies(1, speed)
                createEnemies2(1, speed2)
                for i in range(numOfEnemies2):
                    enemyX2[i] = bossX+32
                    enemyY2[i] = bossY+128
                for i in range(numOfEnemies):
                    enemyX[i] = bossX+32
                    enemyY[i] = bossY+128
                checkB += 1
            if collide:
                bossHP -= 5 #5
                bulletY = 480
                bulletState = "ready"
                score += 25
                if numOfEnemies2 < 2:
                    numOfEnemies2 += 1
                    createEnemies2(1, speed2)
            if collide2:
                bossHP -= 5 #5
                bulletY2 = 480
                bulletState2 = "ready"
                score += 25
                if numOfEnemies < 5:
                    numOfEnemies += 1
                    createEnemies(1, speed)
            if bossHP < 93 and checkB == 1:
                if bossX_change < 0: bossX_change -= 3
                else: bossX_change += 3
                numOfEnemies += 5
                createEnemies(5, speed)
                numOfEnemies2 += 2
                createEnemies2(3, speed2)
                for i in range(numOfEnemies2):
                    enemyY2_change[i] = .5
                checkB += 1
            pygame.draw.rect(screen, black, (10, 90, 190, 5))
            pygame.draw.rect(screen, black, (10, 150, 190, 5))
            pygame.draw.rect(screen, black, (10, 90, 5, 60))
            pygame.draw.rect(screen, black, (200, 90, 5, 65))
            pygame.draw.rect(screen, green, (15, 95, bossHP, 55))
            screen.blit(bossImg, (bossX, bossY))
        
        if bossHP <= 0:
            mixer.music.stop()
            running = False
            break
        
        player(playerX, playerY)
        showScore(textX, textY)
        if level < 10: showLevel = startFont.render("Level: " + str(level), True, white)
        else: showLevel = startFont.render("Level: BOSS", True, red)
        screen.blit(showLevel, (10, 50))
        pygame.draw.rect(screen, (0, 0, 0), (0, 460, 800, 10))
        
        if lives == 3:
            screen.blit(heart1, (578, 0))
            screen.blit(heart2, (652, 0))
            screen.blit(heart3, (726, 0))
        elif lives == 2:
            screen.blit(emptyHeart1, (578, 0))
            screen.blit(heart2, (652, 0))
            screen.blit(heart3, (726, 0))
        elif lives == 1:
            screen.blit(emptyHeart1, (578, 0))
            screen.blit(emptyHeart2, (652, 0))
            screen.blit(heart3, (726, 0))
        
        clock.tick(60) #FPS: 60
        pygame.display.update()
    
    endingScreen(score, bossHP)

startingScreen()