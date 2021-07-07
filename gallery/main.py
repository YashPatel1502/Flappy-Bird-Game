import random #for generating random numbers
import sys    # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

# Global, Variable for the game
FPS = 32 # Frames per second  #width=289  #height=511
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/photos/bird.png'
BACKGROUND = 'gallery/photos/bg.png'
PIPE = 'gallery/photos/pipe.png'

def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True: 
        for event in pygame.event.get(): #get all user inputs 
            # if user clicks on cross button then closes the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

                # if the user presses space or up key , start grame.
            elif event.type == KEYDOWN and (event.key==K_ESCAPE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS) #control frames per second

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # create  2 types for blitting on screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #my list for upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},

    ]
    #my list for Lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},

    ]

   
    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # Velocity while flapping
    playerFlapped = False # It is true only when bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type ==QUIT or(event.type ==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP ):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
            
        crashTest = isCollide(playerx, playery , upperPipes, lowerPipes) # this function will return true if player is crashed
        if crashTest:
            return 
        
        #check for Score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] +GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < playerMidPos + 4:
                score +=1
                print("Your Score is {score}")
            GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerFlapAccv

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        #move pipe to the left
        for upperPipe , lowerpipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerpipe['x'] +=pipeVelX
        #Add a new pipe when the 1 pipe about to go to left

        if 0<upperPipes[0]['x']<5:
            newpipe =getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
        # if pipe out of screen remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
           
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset,SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery , upperPipes, lowerPipes):
    return False


def getRandomPipe():
    """
    generate positions of two pipes(one bottom straight and top rotated) for blitting oj the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset =SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 +offset
    pipe = [
        {'x': pipeX, 'y': -y1}, # - because upper pipe
        {'x': pipeX, 'y': y2} # lower pipe

    ]
    return pipe


if __name__ == "__main__":
    # This will be the main function from where our game will start0
    pygame.init() # initialize all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird By Yash Patel")
    GAME_SPRITES['numbers']=(
        pygame.image.load('gallery/photos/0.png').convert_alpha(),
        pygame.image.load('gallery/photos/1.png').convert_alpha(),
        pygame.image.load('gallery/photos/2.png').convert_alpha(),
        pygame.image.load('gallery/photos/3.png').convert_alpha(),
        pygame.image.load('gallery/photos/4.png').convert_alpha(),
        pygame.image.load('gallery/photos/5.png').convert_alpha(),
        pygame.image.load('gallery/photos/6.png').convert_alpha(),
        pygame.image.load('gallery/photos/7.png').convert_alpha(),
        pygame.image.load('gallery/photos/8.png').convert_alpha(),
        pygame.image.load('gallery/photos/9.png').convert_alpha(),
        #convert alpha function to render on screen(image get optimise for game)
    )

    GAME_SPRITES['message'] = pygame.image.load('gallery/photos/message.jpg')#.convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/photos/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180),
    pygame.image.load( PIPE).convert_alpha()
    )

    # Game Sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/die.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/die.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/die.mp3')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/die.mp3')
    
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() # Shows welcome screen to user unitll any button is pressed
        mainGame() # This is the main game function 










