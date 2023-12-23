import pygame,sys
from pygame.locals import *
import random
from tract import *

pygame.init()

    # create the window

screen = pygame.display.set_mode( (width, height) )
pygame.display.set_caption('racing car ')
fpsClock= pygame.time.Clock()
gameplay=True
lane_move= 0
    # game settings
clock = pygame.time.Clock()
fps = 120
pause = False
gameover = False
speed = 3
score = 0
High_score=0
def board():
            screen.fill(green)
            pygame.draw.rect(screen,gray,road)
            pygame.draw.rect(screen,yellow,(100,0,10,height))
            pygame.draw.rect(screen,yellow,(500,0,10,height))

class Vehicle(pygame.sprite.Sprite):
        def __init__(self, image, x, y):
            pygame.sprite.Sprite.__init__(self)
            # scale the image down so it's not wider than the lane
            image_scale = 65 / image.get_rect().width
            new_width = image.get_rect().width * image_scale
            new_height = image.get_rect().height * image_scale
            self.image = pygame.transform.scale(image, (new_width, new_height))
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
class PlayerVehicle(Vehicle):

        def __init__(self, x, y):
            image = pygame.image.load('car-game/images/car.png')
            PlayerVehicle.lives = 3

            PlayerVehicle.image_index = 0
            # image =pygame.transform.scale2x(image)
            super().__init__(image, x, y)


def score_display(game_state):
        if game_state== 'main game':
            text = font.render('Score: ' + str(score), True, black)
            text_rect = text.get_rect()
            text_rect.center = (50, 400)
            screen.blit(text, text_rect)
            htext = font.render('HighScore: ' + str(High_score), True, black)
            htext_rect = htext.get_rect()
            htext_rect.center = (50, 450)
            screen.blit(htext, htext_rect)
            stext = font.render('speed: ' + str(speed)+' mph', True, black)
            stext_rect = stext.get_rect()
            stext_rect.center = (50, 500)
            screen.blit(stext, stext_rect)
        if game_state== 'gameover':
            text = font.render(f'Score:   {int(score)}', True, white)
            text_rect = text.get_rect()
            text_rect.center = (300, 250)
            screen.blit(text, text_rect)
            htext = pygame.font.Font(pygame.font.get_default_font(), 50)
            htext = font.render(f'HighScore:  {int(High_score)}', True, white)
            htext_rect = htext.get_rect()
            htext_rect.center = (300, 280)
            screen.blit(htext, htext_rect)
def update_score(score,High_score):
        if score > High_score:
            High_score=score
        return High_score
def addvihi():
     # add a vehicle
            if len(vehicle_group) < 3:
                add_vehicle = True
                # ensure there's enough gap between vehicles
                for vehicle in vehicle_group:
                    if vehicle.rect.top < vehicle.rect.height * 1.5:
                        add_vehicle = False

                if add_vehicle:

                    # select a random lane
                    lane = random.choice(lanes)

                    # select a random vehicle image
                    image = random.choice(images_list)
                    vehicles = Vehicle(image, lane, height / -2)
                    vehicle_group.add(vehicles)
def drawpause():
        font = pygame.font.Font('debrosee-font/Debrosee-ALPnL.ttf', 30)
        font2 = pygame.font.Font('freedom-font/Freedom-10eM.ttf', 50)
        pygame.draw.rect(screen,gray,(0,0,width,height))
        pygame.draw.rect(screen,white,[150,150,300,50],0,10)
        restart = pygame.draw.rect(screen,white,[150,250,300,50],0,10)
        quit = pygame.draw.rect(screen,white,[150,350,300,50],0,10)
        screen.blit(font2.render('Car racing',True,green),(150,50))
        screen.blit(font.render('Game paused',True,black),(200,160))
        screen.blit(font.render('Restart',True,black),(200,260))
        screen.blit(font.render('Quit',True,black),(200,360))
        screen.blit(screen,(0,0))
        return restart,quit
def drawstart():
        font = pygame.font.Font('debrosee-font/Debrosee-ALPnL.ttf', 30)
        font2 = pygame.font.Font('freedom-font/Freedom-10eM.ttf', 50)
        pygame.draw.rect(screen,gray,(0,0,width,height))
        pygame.draw.rect(screen,white,[150,150,300,50],0,10)
        start = pygame.draw.rect(screen,white,[150,250,300,50],0,10)
        screen.blit(font2.render('Car racing',True,green),(150,50))
        screen.blit(font.render('start',True,black),(200,260))
        screen.blit(screen,(0,0))
        return start
    # sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

    # create the player's car
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

    # load the vehicle images
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
images_list = []
for image_filename in image_filenames:
        image = pygame.image.load('car-game/images/' + image_filename)
        images_list.append(image)

    # load the crash image and gameover
crash = pygame.image.load('car-game/images/crash1.png')
crash_rect = crash.get_rect()
over = pygame.image.load('car-game/images/game-over.png')
over_rect = over.get_rect()
mixer = pygame.mixer.Sound('gameover.wav')
heart_images = []
heart_image_index = 0
for i in range(8):
        heart_image = pygame.image.load(f'car-game/images/tree{i}.png').convert_alpha()
        heart_images.append(heart_image)
    # game loop
running =True


while running:
        clock.tick(fps)
        if pause :
            restart,quit = drawpause()
        for event in pygame.event.get():
            if event.type == QUIT:
                    running=False
                    sys.exit()

            if event.type == KEYDOWN:

                if not pause:
                    if event.key == pygame.K_r:
                            speed = 2
                            score = 0
                            vehicle_group.empty()
                            player.rect.center = [player_x, player_y]
                    if event.key == pygame.K_UP:
                            speed +=1
                    if event.key == pygame.K_DOWN:
                            speed -=1


                    if event.key == K_LEFT and player.rect.center[0] > left:
                        player.rect.x -= 150
                    if event.key == K_RIGHT and player.rect.center[0] < right:
                        player.rect.x += 150
                if event.key == pygame.K_ESCAPE:
                        if pause :
                            pause = False
                        else:
                            pause = True
            if event.type == pygame.MOUSEBUTTONDOWN and pause:
                    if restart.collidepoint(event.pos):
                        pause = False
                        speed = 2
                        score = 0
                        PlayerVehicle.lives = 3
                        vehicle_group.empty()
                        player.rect.center = [player_x, player_y]
                    if quit.collidepoint(event.pos):
                        running=False
                        sys.exit()

        for vehicles in vehicle_group:
                if pygame.sprite.collide_rect(player,vehicles):
                        PlayerVehicle.lives -= 1

        # check if there's a head on collision
        if pygame.sprite.spritecollide(player,vehicle_group,True):
            crash_rect.center=[player.rect.center[0],player.rect.top]

        if not pause :
            board()
                        #white lane
            lane_move +=speed
            if lane_move >= streetheight * 2:
                        lane_move=0
            for y in range (streetheight* -2,height,streetheight*2):
                                pygame.draw.rect(screen,white,(left+45,y+lane_move,streetwidth,streetheight))
                                pygame.draw.rect(screen,white,(center+45,y+lane_move,streetwidth,streetheight))
            # draw the player's car

            player_group.draw(screen)
            addvihi()

            # make the vehicles move
            for vehicles in vehicle_group:
                vehicles.rect.y += speed

                # remove vehicle once it goes off screen
                if vehicles.rect.top >= height:
                    vehicles.kill()
                    # add score
                    score += 1

                    # speed up the game
                    if score > 0 and score % 5 == 0:
                        speed += 1
               # display remaining lives
            for i in range(PlayerVehicle.lives):
                    heart_image = heart_images[int(heart_image_index)]
                    heart_x = 10 + i * (heart_image.get_width() + 10)
                    heart_y = 10
                    screen.blit(heart_image, (heart_x, heart_y))
                    if heart_image_index >= len(heart_images):
                        heart_image_index = 0
        # draw the vehicles
            vehicle_group.draw(screen)
        #score
            font = pygame.font.Font(pygame.font.get_default_font(), 15)
            score_display('main game')
        #gameover
        if PlayerVehicle.lives == 0 :
            screen.blit(crash,crash_rect)
            gameover=True
            # pygame.draw.rect(screen, red, (0, 50, width, 100))
            mixer.play()
            screen.blit(over,(250,100))
            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            High_score=update_score(score,High_score)
            score_display('gameover')
            text = font.render('Play again? (Enter Y or N)', True, white)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 310)
            screen.blit(text, text_rect)

        pygame.display.update()
        while gameover:

            clock.tick(fps)

            for event in pygame.event.get():

                if event.type == QUIT:
                    gameover = False
                    running = False

                # get the user's input (y or n)
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        # reset the game
                        gameover = False
                        speed = 2
                        score = 0
                        PlayerVehicle.lives = 3
                        vehicle_group.empty()
                        player.rect.center = [player_x, player_y]
                    elif event.key == K_n:
                        # exit the loops
                        gameover = False
                        running = False

        pygame.display.update()
