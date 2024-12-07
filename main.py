import os
import pygame
import random
# pygame setup
pygame.init()


width = 1280
height = 720

screenwidth, screenheight = pygame.display.Info().current_w, pygame.display.Info().current_h
x = (screenwidth/2) - width/2
y = (screenheight/2) - height/2

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)



#width = screenwidth

#screen = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((width, height), flags=pygame.SCALED, vsync=1) 
pygame.display.set_caption("THE CRUNCHY GAME")
clock = pygame.time.Clock()
dt = 0
running = True
paused = False

playerImg = pygame.image.load("ASSETS/circle.svg")
orgPlayerScale = 20
playerScale = orgPlayerScale
playerWidth = playerScale * 2
player_pos = pygame.Vector2(screen.get_width()/2, height - playerScale)
flor = height - playerScale
fpsCap = 60
baseSpeed = 0.5
speed = baseSpeed
#direction faced
playerDir = 0
#ground height is "280.0"

isJump = False
JumpHeight = 40
jumpCount = JumpHeight
negNum = 0.02
fallSpeed = 2

tripJump = True

poundTrip = True

tripLeft = False
canAttackLeft = False
canAttackRight = False
tripRight = False
attacking_rect = 0
attackSizeX = 90
attackSizeY = playerScale * 2
freeze = 125
goFreeze = False
gPenessx = playerScale
gpenessy = 0


dashTemps = 5
dashNum = 0
dashing = False
dashSpeed = baseSpeed * 2

bcgColor = "lightgrey"

clock = pygame.time.Clock()


##SCOREBOARD
scor = 0

titleFontSize = 50
titlefont = pygame.font.Font('ASSETS/font1.ttf', titleFontSize)
title = titlefont.render('THE CRUNCHY GAME', True, "#1E1E1E", None)
titleRect = title.get_rect()
titleRect.center = (width/2, (titleFontSize/2)+10)
        
scoreFontSize = 32
scorefont = pygame.font.Font('ASSETS/font1.ttf', scoreFontSize)
score = scorefont.render(('Score:'+ str(scor)), True, "#1E1E1E", None)
scoreRect = score.get_rect()
scoreRect.bottomleft = (50, 150)


#NUMBER OF ENEMONEIS ENCREASES
tock = 0
secsPerSpawn = 3
spawnTimeIncrease = 2

##SPAWNING (LETS TRY AGAIN)
recycle = False
enemyPos = []
enemyImg = []
enemyRect = []
enemyDir = []
alive = []
pace = []
class EnemyController:
    wantedEnemies = 3
    osEnemies = 0
    spawnIncrement = 0
    spawnField = 1000

class Grunt:
    gruntScale = 25
    posx = 500
    posy = 100
    minSpeed = 20 #divided by 100
    maxSpeed = 30 #divided by 100
    spawnPoint = [1, -1]
    vulnPont = ["all"]
    specEffect = ["none"]
    deathEffect = ["grenade"]

for i in range(EnemyController.wantedEnemies):
    dir = random.choice(Grunt.spawnPoint)
    if dir == -1:
            enemyX = screen.get_width() + random.randint(0, EnemyController.spawnField)
    elif dir == 1:
        enemyX = 0 - random.randint(0, EnemyController.spawnField)
    enemyY = height - Grunt.gruntScale
    enemyDir.append(dir)
    sped = (random.randrange(Grunt.minSpeed, Grunt.maxSpeed))/100
    pace.append(dir*sped)
    enemyPos.append(pygame.Vector2(enemyX, enemyY))
    enemyImg.append(pygame.draw.circle(screen, "blue", (enemyX, enemyY), Grunt.gruntScale, Grunt.gruntScale))
    enemyRect.append(pygame.Rect((enemyX-Grunt.gruntScale, enemyY-Grunt.gruntScale, 2*Grunt.gruntScale,2*Grunt.gruntScale)))
    alive.append("TRUE")

EnemyController.osEnemies = EnemyController.wantedEnemies


while running:
    ##increase number of enemies requested
    #pygame.time.set_timer(INCREASE_ENEMY_WANTS, 200)
    tock += dt
    if tock > (secsPerSpawn*1000):
        EnemyController.wantedEnemies += 1
        secsPerSpawn += spawnTimeIncrease
        tock = 0 # reset it to 0 so you can count again

    keys = pygame.key.get_pressed()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

    def scoreboard(width, height, scor):
        backScore = pygame.Rect(0, 0, width, height/1.65)
        pygame.draw.rect(screen, "darkgrey", backScore)

        score = scorefont.render(('Score:'+ str(scor)), True, "#1E1E1E", None)
        screen.blit(title, titleRect)
        screen.blit(score, scoreRect)


    #PAUSING
    if keys[pygame.K_ESCAPE]:
        if paused == False:
            paused = True
        else:
            paused = False
        

    #Jumping
    if keys[pygame.K_w] or keys[pygame.K_UP]:
    #    player_pos.y -= speed * dt
        if player_pos.y == flor:
            if not isJump and tripJump:
                isJump = True
                tripJump = False
    else: 
        tripJump = True

    #sliding/GPing
    if keys[pygame.K_s] or keys[pygame.K_DOWN]: #and player_pos.y < height - playerScale
    #    player_pos.y += speed * dt
        dashing = True
        if player_pos.y != flor:
            if poundTrip:
                attacking_rect = pygame.Rect((player_pos.x-playerScale), player_pos.y + playerScale, playerScale*2, height - player_pos.y)
                groundPound()
                goFreeze = True
                poundTrip = False  

    else:
        dashing = False  
        poundTrip = True 

    #Attack left 
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:

        #player_pos.x -= speed * dt
        if playerDir != -1:
            playerDir = -1
            canAttackLeft = False
            tripLeft = False
        elif playerDir == -1:
            if tripLeft and not dashing and not isJump:
                attacking_rect = pygame.Rect((player_pos.x - attackSizeX), player_pos.y - playerScale, attackSizeX, attackSizeY)
                attackLeft()
                canAttackLeft = False
                goFreeze = True
                tripLeft = False
    else:
        tripLeft = True           


    #Attack right
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        #player_pos.x += speed * dt
        if playerDir != 1:
            playerDir = 1  
            canAttackRight = False
            tripRight = False
        elif playerDir == 1:
            if tripRight and not dashing and not isJump:
                attacking_rect = pygame.Rect((player_pos.x), player_pos.y - playerScale, attackSizeX, attackSizeY)
                attackRight()
                canAttackRight = False
                tripRight = False
                goFreeze = True
    else: 
        tripRight = True




    #MOOP
    if playerDir == -1 and player_pos.x > playerScale:
        player_pos.x -= speed * dt
    elif playerDir == 1 and player_pos.x < width - playerScale:
        player_pos.x += speed * dt

    if dashing and not isJump:
        speed = dashSpeed
        playerScale = orgPlayerScale
        playerWidth = 500
    else: 
        playerScale = orgPlayerScale
        speed = baseSpeed


    if isJump:
        if jumpCount >= -JumpHeight:
            neg = negNum
            if jumpCount < 0:
                neg = -neg
            player_pos.y -= (jumpCount ** 2) * neg
            jumpCount -= fallSpeed
        else:
            isJump = False  
            jumpCount = JumpHeight




    #ATTACKING    
    def attackLeft():
        bcgColor = "#1E1E1E"
        #attacking_rect = pygame.Rect((player_pos.x - attackSizeX - playerScale), player_pos.y - playerScale, attackSizeX, attackSizeY)
        screen.fill(bcgColor)
        pygame.draw.circle(screen, "lightgrey", player_pos, playerScale)
        pygame.draw.rect(screen, "red", attacking_rect)

    def attackRight():
        bcgColor = "#1E1E1E"
        #attacking_rect = pygame.Rect((player_pos.x + playerScale), player_pos.y - playerScale, attackSizeX, attackSizeY)
        screen.fill(bcgColor)
        pygame.draw.circle(screen, "lightgrey", player_pos, playerScale)
        pygame.draw.rect(screen, "red", attacking_rect)

    def groundPound():
        bcgColor = "#1E1E1E"
        #attacking_rect = pygame.Rect((player_pos.x-playerScale), player_pos.y + playerScale, playerScale*2, height - player_pos.y)
        screen.fill(bcgColor)
        pygame.draw.circle(screen, "lightgrey", player_pos, playerScale)
        pygame.draw.rect(screen, "red", attacking_rect)


    #ADD NEW ENEMIES
    if EnemyController.wantedEnemies > EnemyController.osEnemies:
        dir = random.choice(Grunt.spawnPoint)
        #enemyX = random.randint(Grunt.gruntScale,screen.get_width())
        if dir == -1:
            enemyX = screen.get_width() + random.randint(0, EnemyController.spawnField)
        elif dir == 1:
            enemyX = 0 - random.randint(0, EnemyController.spawnField)
        enemyY = height - Grunt.gruntScale
        enemyDir.append(dir)
        sped = (random.randrange(Grunt.minSpeed, Grunt.maxSpeed))/100
        pace.append(dir*sped)
        enemyPos.append(pygame.Vector2(enemyX, enemyY))
        enemyImg.append(pygame.draw.circle(screen, "blue", (enemyX, enemyY), Grunt.gruntScale, Grunt.gruntScale))
        enemyRect.append(pygame.Rect((enemyX-Grunt.gruntScale, enemyY-Grunt.gruntScale, 2*Grunt.gruntScale,2*Grunt.gruntScale)))
        alive.append("TRUE")
        EnemyController.osEnemies += 1
    
    #MOOP BUT FOR ENEMIES
    for i in range(EnemyController.osEnemies):
        posix = enemyPos[i].x
        pac = pace[i] * dt
        if dir == 1:
            if posix > screenwidth:
                enemyPos[i].x = 0 - random.randint(0, EnemyController.spawnField)
            else:
                enemyPos[i].x += pac
        if dir == -1:
            if posix < 0:
                enemyPos[i].x = screen.get_width() + random.randint(0, EnemyController.spawnField)
            else:
                enemyPos[i].x += pac
        enemyImg[i] = pygame.draw.circle(screen, "blue", (enemyPos[i].x, enemyPos[i].y), Grunt.gruntScale, Grunt.gruntScale)
        enemyRect[i] = (pygame.Rect((enemyPos[i].x-Grunt.gruntScale, enemyPos[i].y-Grunt.gruntScale, 2*Grunt.gruntScale,2*Grunt.gruntScale)))


    #COLLISION DETECTION BUT HOPEFULY IT WONT BREAK SHIT
    if attacking_rect != 0:
        for i in range(EnemyController.osEnemies):
            if pygame.Rect.colliderect(enemyRect[i], attacking_rect):
                scor+= 1
                alive[i] = "FALSE"
                recycle = True
    attacking_rect = 0
    #RECYCLE THE FUCKERS

    if recycle:
        for i in range(EnemyController.osEnemies):
            if alive[i] == "FALSE":
                dir = random.choice(Grunt.spawnPoint)
                if dir == -1:
                    enemyX = screen.get_width() + random.randint(0, EnemyController.spawnField)
                elif dir == 1:
                    enemyX = 0 - random.randint(0, EnemyController.spawnField)
                enemyY = height - Grunt.gruntScale
                enemyDir[i] = dir
                sped = (random.randrange(Grunt.minSpeed, Grunt.maxSpeed))/100
                pace[i] = dir*sped
                enemyPos[i] = pygame.Vector2(enemyX, enemyY)
                enemyImg[i] = pygame.draw.circle(screen, "blue", (enemyPos[i].x, enemyPos[i].y), Grunt.gruntScale, Grunt.gruntScale)
                enemyRect[i] = pygame.Rect((enemyPos[i].x-Grunt.gruntScale, enemyPos[i].y-Grunt.gruntScale, 2*Grunt.gruntScale,2*Grunt.gruntScale))
                alive[i] = "TRUE"
        recycle = False


    scoreboard(width, height, scor)
    pygame.display.update()
    #pygame.display.flip

        

    if goFreeze is True:
        pygame.time.delay(freeze)
        goFreeze = False
        dt = clock.tick(fpsCap)
    else:
        #set back to normal
        screen.fill("lightgrey")
        #pygame.draw.circle(screen, "#1E1E1E", player_pos, playerScale, playerWidth)
        screen.blit(playerImg, (player_pos.x-20, player_pos.y-20))
        
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    #print(clock.get_fps())
    dt = clock.tick(fpsCap)


pygame.quit()