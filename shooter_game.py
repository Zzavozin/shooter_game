#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
win = display.set_mode((800,600))

display.set_caption('game')
background = transform.scale(image.load('galaxy.jpg'),(800, 600))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.2)
fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.2)
mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (x,y))
        self.rect = self.image.get_rect()  
        
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = speed
        

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 8:
            self.rect.x-= 5
        if key_pressed[K_d] and self.rect.x < 725:
            self.rect.x += 5
    
    def fire(self):
        bullet = Bullet('bullet.png', 0, 0, 5,10, 40)
        bullet.rect.centerx = self.rect.centerx
        bullet.rect.bottom = self.rect.top
        bullets.add(bullet)
        

lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >600:
            self.rect.y = 0 
            self.rect.x = randint(1,599)
            lost +=1

             
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

rocket = Player('rocket.png', 360, 480, 2, 60,100)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range (5):
    monster = Enemy('ufo.png',randint(10, 750), randint(-50, 0), 1.5, 70, 45)
    monsters.add(monster)

for i in range (3): 
    asteroid = Enemy('asteroid.png',randint(10, 750), randint(-50, 0), 1, 70, 45) 
    asteroids.add(asteroid)

game = True
finish = True
clock = time.Clock()

font.init()
font_1 = font.SysFont('Arial', 36)
game_font = font.SysFont('Arial', 50)
win_text = game_font.render('Вы выиграли!', True, (0, 255, 255))
lose_text = game_font.render('Вы проиграли!', True, (255, 0, 0))\


num_fire = False
count_fire = 0

live = 10

score = 0
while game != False:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if count_fire < 7 and num_fire == False:
                    count_fire += 1
                    fire_sound.play() 
                    rocket.fire()
                elif count_fire >= 7 and num_fire == False:
                    last_time = timer()
                    num_fire = True
                    
                    

            if e.key == K_r:
                finish = True
                score = 0
                lost = 0
                for i in monsters:
                    i.kill()
                for i in bullets:
                    i.kill()
                for i in asteroids:
                    i.kill()
                time.delay(3000)
                for i in range (5):
                    monster = Enemy('ufo.png',randint(10, 750), randint(-50, 0), 1.5, 70, 45)
                    monsters.add(monster)
                for i in range (3): 
                    asteroid = Enemy('asteroid.png',randint(10, 750), randint(-50, 0), 1, 70, 45) 
                    asteroids.add(asteroid)
                live = 10 

                display.update()
                

    if finish != False:
        win.blit(background, (0,0))
        rocket.reset()
        rocket.update()
        
        monsters.draw(win)
        lose = font_1.render(
            'Пропущено: ' + str(lost), 1, (255,255,255)
        )
        winnn = font_1.render(
            'Счет: ' + str(score), 1, (255,255,255)
        )
        win.blit(lose, (1,30))
        win.blit(winnn, (1,1))
        bullets.draw(win) 
        asteroids.draw(win)
        collides = sprite.groupcollide(monsters, bullets, True, True)

        for i in collides:
            score +=1
            monster = Enemy('ufo.png', randint(10,750), randint(-50, 0), 2, 70, 45)
            monsters.add(monster)

        if score == 10:
            finish = False
            win.blit(win_text, (250, 250))

        if sprite.spritecollide(rocket, monsters, False) or sprite.spritecollide(rocket, asteroids, False):
            sprite.spritecollide(rocket, monsters, True)
            sprite.spritecollide(rocket, asteroids, True)
            live -= 1
    
            
        if live == 0 or lost >=5:
            finish = False                                                                                               
            win.blit(lose_text, (250, 250))
        
        if num_fire == True:
            second_time = timer()
            if second_time - last_time <= 1.5 :
                reload = font_1.render('Перезарядка', True, (255,0,0))
                win.blit(reload, (250,550))
            else:
                num_fire = False
                count_fire = 0

        text_live = font_1.render('кол-во жизней: ' + str(live), True, (255,255,255) )
        win.blit(text_live, (565, 10))
        asteroids.update()        
        bullets.update()  
        monsters.update()
    display.update()
    clock.tick(60)

quit()
