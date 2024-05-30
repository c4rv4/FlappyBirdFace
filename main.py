import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864

screen_height = 936

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Bird")

#fuente de letra

font = pygame.font.SysFont("Bauhaus 93", 60)

#color

white = (255, 255, 255) 

#variables
    
gs = 0
ss = 4
fly = False
go = False
pipe_gap = 150
pipe_f = 1500 #ms
last_pipe = pygame.time.get_ticks() - pipe_f
re = 0
passp = False

#imagenes
bg = pygame.image.load("imagenes/bg.png")
g = pygame.image.load("imagenes/ground.png")
bim = pygame.image.load("imagenes/restart.png")

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
    
def resett():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height/2)
    re = 0
    return re

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range (1, 4):
            img = pygame.image.load(f"imagenes/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False


    def update(self):
        if fly == True:
            #gravedad
            
            self.vel += 0.5
            if self.vel >8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
        
        if go == False:
            
            #salto (con mouse)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
            #animacion
            self.counter += 1
            flap_cooldown = 5
            
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotacion
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
                
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imagenes/pipe.png")
        self.rect = self.image.get_rect()
        #posicion 1 es para
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) 
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]
            
    def update(self):
        self.rect.x -= ss
        if self.rect.right < 0:
            self.kill() 


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        
    def draw(self):
        
        c=False
        
        #posicion mouse
        pos = pygame.mouse.get_pos()
        
        #mouse en
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                c=True
        
        #boton
        
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return c

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)  

#crear boton

button = Button(screen_width //2 - 50, screen_height // 2 -100, bim)

run = True
while run:
    
    clock.tick(fps)
    
    #Fondo
    screen.blit(bg, (0,0))
    
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    
    #suelo
    screen.blit(g, (gs,768))
    
    #Puntuación
    
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and passp == False:
                passp = True
        if passp == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                re += 1
                passp = False
                

    draw_text(str(re), font, white, int(screen_width / 2), 20)                    
    
    #colicion
    
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        go = True
    
    #condicion endgame
    
    if flappy.rect.bottom >= 768:
        go = True
        fly == False
    if go == False and fly == True:
        
        #generación de obstaculos
        
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_f:
            pipe_h = random.randint(-100, 100)
            
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_h, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_h, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        
        #fondo desplazable
        gs -= ss
        if abs(gs) > 35:
            gs=0
        pipe_group.update()
    
    #reset
    if go == True:
        if button.draw() == True:
            go = False
            re = resett()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and fly == False and go == False:
            fly = True
            
    pygame.display.update()

pygame.quit()