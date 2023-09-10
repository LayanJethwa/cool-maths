import pygame
import sys
import random
import math
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Fisik')
running = True
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
clock = pygame.time.Clock()
boxes = []
speeds = []
obstacles = []
for i in range(100):
    boxes.append(pygame.Rect(random.randint(0,750), random.randint(0,750), random.randint(25,50), random.randint(25,50)))
    if i%5 == 0:
        obstacles.append(pygame.Rect(random.randint(0,750), random.randint(0,750), random.randint(25,50), random.randint(25,50)))
    speeds.append(0)

g = 9.80665
rot = 90
border = [pygame.Rect(0,0,800,800)]

while running:
    screen.fill(white)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            exit()
            quit()
    key = pygame.key.get_pressed()
    if (key[pygame.K_LEFT]):
        rot += 1
    elif (key[pygame.K_RIGHT]):
        rot -= 1
    for i in range(len(obstacles)):
        surf1 = pygame.Surface((obstacles[i].width,obstacles[i].height))
        surf1.fill(red)
        screen.blit(surf1,obstacles[i])
    for i in range(len(boxes)):
        surf = pygame.Surface((boxes[i].width,boxes[i].height))
        surf.fill(black)
        screen.blit(surf,boxes[i])
        if clock.get_fps() > 0:
            speeds[i] += g/clock.get_fps()
        if clock.get_fps() > 0:
            boxes[i].left -= speeds[i]*math.sin(math.radians(rot))
            boxes[i].top += speeds[i]*math.cos(math.radians(rot))
        if boxes[i].collidelist(boxes) != -1:
            try:
                speeds[i]-=((0.5*(boxes[i].width*boxes[i].height)*(speeds[i]**2))/(boxes[i].width*boxes[i].height))/2
                speeds[(boxes[i].collidelist(boxes))]+=((0.5*(boxes[i].width*boxes[i].height)*(speeds[i]**2))/(boxes[(boxes[i].collidelist(boxes))].width*boxes[(boxes[i].collidelist(boxes))].height))/0.5
            except:
                None
        if boxes[i].collidelist(obstacles) != -1:
            speeds[i] = -1*0.5*speeds[i]
        if boxes[i].collidelist(border):
            try:
                if (boxes[i].left - speeds[i]*math.sin(math.radians(rot))) > 800 or (boxes[i].left - speeds[i]*math.sin(math.radians(rot))) < 0:
                    speeds[i] = 0
                elif (boxes[i].top - speeds[i]*math.cos(math.radians(rot))) > 800 or (boxes[i].top - speeds[i]*math.cos(math.radians(rot))) < 0:
                    speeds[i] = 0
            except:
                None
    screen.blit(pygame.transform.rotate(screen, rot), (0, 0))
    clock.tick()
    pygame.display.update()
