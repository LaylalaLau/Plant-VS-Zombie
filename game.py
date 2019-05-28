#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 00:45:57 2019

@author: liushuxuan
"""

import pygame
from network import Network
import random, sys, time
from pygame.locals import *

class Player():
    
    width, height = 50, 50
    FPS = 60

    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 8
        self.color = color

    def draw(self, g):
        #pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)
        playerImage = pygame.image.load('SnowPea.gif')
        playerRect = playerImage.get_rect()
        #playerRect = playerImage.get_rect()
        playerRect.centerx = self.x
        playerRect.centery = self.y
        g.blit(playerImage, playerRect)      

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """
        if dirn == 0:
            self.x = self.x + self.velocity
        elif dirn == 1:
            self.x = self.x - self.velocity
        elif dirn == 2:
            self.y = self.y -self.velocity
        else:
            self.y = self.y + self.velocity

            
class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(200, 180) #initial position of the two players. 
        self.player2 = Player(100,100) 
        self.canvas = Canvas(self.width, self.height, "Plant VS Zombie") 

    def run(self):
        clock = pygame.time.Clock()
        
        WINDOWWIDTH = 1024
        WINDOWHEIGHT = 600
        ADDNEWBULLETRATE = 10
        ZOMBIESIZE = 80 #includes newKindZombies
        ADDNEWZOMBIERATE = 50
        ADDNEWKINDZOMBIE = ADDNEWZOMBIERATE
        MAXGOTTENPASS = 1
        BULLETSPEED = 10
        NORMALZOMBIESPEED = 6
        NEWKINDZOMBIESPEED = NORMALZOMBIESPEED / 2
        
        TEXTCOLOR = (255, 255, 255)
        RED = (255, 0, 0)
        
        run = True
        shoot = False
        bullets = []
        zombies = []
        newKindZombies = []
        bulletAddCounter = 40
        zombieAddCounter = 0
        newKindZombieAddCounter = 0
        
        score = 0
        zombiesGottenPast = 0
        
        backgroundImage = pygame.image.load('background.png')
        rescaledBackground = pygame.transform.scale(backgroundImage, (1024, 600))
        
        pygame.init()
        pygame.mixer.music.load('grasswalk.mp3')
        pygame.mixer.music.play(-1)
        gameOverSound = pygame.mixer.Sound('gameover.wav')
        
        font = pygame.font.SysFont(None, 48)
        
        def drawText(text, font, surface, x, y):
            textobj = font.render(text, 1, TEXTCOLOR)
            textrect = textobj.get_rect()
            textrect.topleft = (x, y)
            surface.blit(textobj, textrect)
            
        def waitForPlayerToPressKey():
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        terminate()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE: # pressing escape quits
                            terminate()
                        if event.key == K_RETURN:
                            return

        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        windowSurface.blit(rescaledBackground, (0, 0))
        pygame.mouse.set_visible(True)
            
        drawText('Plant VS Zombie', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('Press Enter to start', font, windowSurface, (WINDOWWIDTH / 3) - 10, (WINDOWHEIGHT / 3) + 50)
        pygame.display.update()
        waitForPlayerToPressKey()
        
        while run:
            
            bulletImage = pygame.image.load('SnowPeashooterBullet.gif')
            bulletRect = bulletImage.get_rect()
            playerImage = pygame.image.load('SnowPea.gif')
            playerRect = playerImage.get_rect()
            zombieImage = pygame.image.load('BucketheadZombie.png')
            newKindZombieImage = pygame.image.load('ConeheadZombieAttack.gif')
            
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.K_ESCAPE:
                    run = False
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        shoot = True
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        shoot = False      
                        
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                if self.player.x <= self.width - self.player.velocity: #按右键，不出圈就能动
                    self.player.move(0)

            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity:
                    self.player.move(3)
                
            bulletAddCounter += 1
            if bulletAddCounter >= ADDNEWBULLETRATE and shoot == True:
                bulletAddCounter = 0
                bullet_x = self.player.x+10
                bullet_y = self.player.y-25
                newBullet = {'rect':pygame.Rect(bullet_x, bullet_y, bulletRect.width, bulletRect.height),
						 'surface':pygame.transform.scale(bulletImage, (bulletRect.width, bulletRect.height)),
						}
                bullets.append(newBullet)
            
            # Add new zombies at the top of the screen, if needed.
            zombieAddCounter += 1
            if zombieAddCounter == ADDNEWKINDZOMBIE:
                zombieAddCounter = 0
                zombieSize = ZOMBIESIZE       
                newZombie = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-zombieSize-10), zombieSize, zombieSize),
                            'surface':pygame.transform.scale(zombieImage, (zombieSize, zombieSize)),
                            }
                zombies.append(newZombie)
    
            # Add new newKindZombies at the top of the screen, if needed.
            newKindZombieAddCounter += 1
            if newKindZombieAddCounter == ADDNEWZOMBIERATE:
                newKindZombieAddCounter = 0
                newKindZombiesize = ZOMBIESIZE
                newCrawler = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-newKindZombiesize-10), newKindZombiesize, newKindZombiesize),
                            'surface':pygame.transform.scale(newKindZombieImage, (newKindZombiesize, newKindZombiesize)),
                            }
                newKindZombies.append(newCrawler)

            
            def bulletHasHitZombie(bullets, zombies):
                for b in bullets:
                    if b['rect'].colliderect(z['rect']):
                        bullets.remove(b)
                        return True
                return False
            
            def bulletHasHitCrawler(bullets, newKindZombies):
                for b in bullets:
                    if b['rect'].colliderect(c['rect']):
                        bullets.remove(b)
                        return True
                return False

            # Draw the game world on the window.
            #self.canvas.screen.blit(rescaledBackground, (0, 0))

            # Draw the player's rectangle, rails
            self.canvas.screen.blit(playerImage, playerRect)
   
                #if self.player.x <= self.width and self.player.y <= self.height:
                #self.player.grow(self.player.x)                          

            # Send Network Stuff
            self.player2.x, self.player2.y, score2 = self.parse_data(self.send_data(self.player.x, self.player.y, score))
        
            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            
            for z in zombies[:]:
                if z['rect'].left < 0:
                    zombies.remove(z)
                    zombiesGottenPast += 1
                if bulletHasHitZombie(bullets, zombies):
                    score += 1
                    zombies.remove(z)
                z['rect'].move_ip(-1*NORMALZOMBIESPEED, 0)
                self.canvas.screen.blit(z['surface'], z['rect'])
            
            for c in newKindZombies[:]:
                if c['rect'].left <0:
                    newKindZombies.remove(c)
                    zombiesGottenPast += 1
                if bulletHasHitCrawler(bullets, newKindZombies):
                    score += 1
                    newKindZombies.remove(c)    
                c['rect'].move_ip(-1*NEWKINDZOMBIESPEED,0)
                self.canvas.screen.blit(c['surface'], c['rect'])
    		
            for b in bullets[:]:
                if b['rect'].right>WINDOWWIDTH:
                    bullets.remove(b)
                b['rect'].move_ip(BULLETSPEED, 0)
                self.canvas.screen.blit(b['surface'], b['rect'])
            
            drawText('score: %s' % (score), font, self.canvas.screen, 20, 50)
            drawText('opponent score: %s' % (score2), font, self.canvas.screen, 20, 100)
            
            self.canvas.update()
 
            if zombiesGottenPast >= MAXGOTTENPASS:
                pygame.mixer.music.stop()   
                gameOverSound.play()
                time.sleep(8)
                break
        
        waitForPlayerToPressKey()

    def send_data(self, x, y, s):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(x) + "," + str(y) + "," + str(s) 
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1]), int(d[2])
        except:
            return 0,0,0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    '''def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))'''

    def grow(self, x, y):
        playerImage = pygame.image.load('SnowPea.gif')
        playerRect = playerImage.get_rect()
        playerRect.centerx = x
        playerRect.centery = y
        self.screen.blit(playerImage, playerRect)

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        #self.screen.fill((255,255,255))
        backgroundImage = pygame.image.load('background.png')
        rescaledBackground = pygame.transform.scale(backgroundImage, (1024, 600))

        # show the "Start" screen
        self.screen.blit(rescaledBackground, (0, 0))
