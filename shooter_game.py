#импорты
from pygame import *
from random import randint
import pygame
import time as clocks 
pygame.init()

#Класс GameSprite()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, image_x, image_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (image_x, image_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Класс Player(), наследник класса GameSprite()
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 1300:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > -11:
            self.rect.x -= self.speed
    def fire(self):
        global bullets
        sprite_center_x = self.rect.centerx
        sprite_top = self.rect.top
        bullet = Bullet('water.png', sprite_center_x, sprite_top, 10, 10, 20)
        bullets.add(bullet) 

#Класс Enemy(), наследник класса GameSprite()
lost = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y >= 0:
            self.direction = 'down'
        if self.rect.y >= 670:
            self.rect.y = randint(0, 100)
            self.rect.x = randint(0, 1300)
            lost = lost + 1
        if self.direction == 'down':
            self.rect.y += self.speed

#Класс Asteroid(), наследник класса GameSprite()
class Asteroid(GameSprite):
    def update(self):
        global lost
        if self.rect.y >= 0:
            self.direction = 'down'
        if self.rect.y >= 670:
            self.rect.y = randint(0, 100)
            self.rect.x = randint(0, 1300)
        if self.direction == 'down':
            self.rect.y += self.speed

#Создание класса Bullet(), наследник класса GameSprite()
score1 = 0
class Bullet(GameSprite):
    def update(self):
        global score1
        if self.rect.y <= 0:
            self.kill()
        if self.rect.y <= 650 and self.rect.y > 0:
            self.direction = 'up'
        if self.direction == 'up':
            self.rect.y -= self.speed
        if sprite.groupcollide(monsters, bullets, True, True):
            score1 = score1 + 1
        if sprite.groupcollide(asteroids, bullets, False, True):
            pass

#Создание окна
window = display.set_mode()
display.set_caption('                                                                                               Шутер')

#Загрузка заднего фона
background = transform.scale(image.load('Eiffel-Tower.jpg'),(1366,768))

#Создание основных координат персонажей
x1 = 25
y1 = 650  
y2 = 0

#FPS
clock = time.Clock()
FPS = 60        
 
#Добавление фоновой музыки
mixer.init()
mixer.music.load('pesnya.mp3')
mixer.music.play()

#Уменьшение громкости фоновой музыки
mixer.music.set_volume(0.05)

#Создание надписей победы и поражения
font.init()
my_font = pygame.font.SysFont('bahnschrift', 20)
new_font = pygame.font.SysFont('bahnschrift', 60)
start_font = pygame.font.SysFont('bahnschrift', 50)
win = new_font.render('Ура, победа!', 1, (255, 215, 0))
defeat = new_font.render('О нет, ты проиграл!', 1, (255, 0, 0))
restart = my_font.render('Нажмите <TAB>, чтобы начать заново', 1, (255, 255, 255))
start = start_font.render('Нажмите <Enter>, чтобы начать', 1, (255, 255, 255))
reloads = my_font.render('Перезарядка...', 1, (255, 0, 0))


#Загрузка спрайта игрока
player = Player('pistol.png', x1, y1, 15 , 70, 70)

#Создание спрайтов врагов
monsters = sprite.Group()
for i in range(20):
    enemy_speed = randint(1, 3)
    monster = Enemy('sigma.png', randint(50, 1300)  , randint(0, 100), enemy_speed, 70, 60)
    monsters.add(monster)

#Создание спрайтов астероидов
asteroids = sprite.Group()
for i in range(15):
    enemy_speed = randint(1, 3)
    asteroid = Asteroid('cat.png', randint(50, 1300)  , randint(0, 100), enemy_speed, 70, 50)
    asteroids.add(asteroid)

#Создание группы пуль
bullets = sprite.Group()

#Загрузка звука стрельбы
mixer.init()
phew = mixer.Sound('bulk.ogg')

#Загрузка звука победы
win1 = mixer.Sound('win1.ogg')

#Загрузка звука проигрыша
defeat1 = mixer.Sound('defeat.ogg')

#Уменьшение громкости звукового эффекта стрельбы
phew.set_volume(0.1)

#Уменьшение громкости звукового эффекта победы
win1.set_volume(0.1)

#Уменьшение громкости звукового эффекта проигрыша
defeat1.set_volume(0.2)

#Создание цикла игры
game = True
finish = False
num_fire = 0
rel_time = False

while game:

    #...Пока не достигнут финиш
    if finish != True:

        #Размещение заднего фона
        window.blit(background, (0, 0))

        #Размещение счёта и пропусков
        skipped = my_font.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        score = my_font.render('Счёт: ' + str(score1), 1, (255, 255, 255))
        window.blit(score, (10, 20))
        window.blit(skipped, (10, 50))    
        
        #Размещение игрока, монстров, астероидов и пуль
        player.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        #Обновление спрайта игрока, cпрайтов врагов, спрайтов астероидов и спрайтов пуль при каждом движении
        player.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        #Подключение FPS            
        clock.tick(FPS)

        #Поражение при столкновении с врагом или астероидом, а также при 30 пропусках
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False) or lost >= 50:

            #Отображение надписи проигрыша
            window.blit(defeat, (380, 320))
            window.blit(restart, (450, 400))

            #Остановка фоновой музыки
            mixer.music.pause()

            #Проигрывание звукового эффекта поражения
            defeat1.play()

            #...Финиш достигнут
            finish = True

        #Победа при счёте, равному 20
        if score1 >= 15:

            #Отображение надписи победы
            window.blit(win, (490, 320))
            window.blit(restart, (500, 400))

            #Остановка фоновой музыки
            mixer.music.pause()

            #Проигрывание звукового эффекта победы
            win1.play()

            #...Финиш достигнут
            finish = True

     
    #Закрытие игры при нажатии на крестик
    for e in event.get():
        if e.type == QUIT:

            #...Игра окончена
            game = False

        #Стрельба по кнопке 'Пробел'
        elif e.type == KEYDOWN:
            if num_fire <= 10 and rel_time != True:
                if e.key == K_SPACE:

                    #Стрельба, если очередь пуль меньше 5 
                    if num_fire < 10:
                        player.fire()
                        phew.play()
                        num_fire += 1

            #Перезапуск по кнопе 'Tab'
            if e.key == K_TAB and finish != False:
                finish = False
                lost = 0
                score1 = 0
                num_fire = 0
                monsters.empty()
                asteroids.empty()
                mixer.music.play()
                for i in range(20):
                    enemy_speed = randint(1, 3)
                    monster = Enemy('sigma.png', randint(50, 1300)  , randint(0, 100), enemy_speed, 70, 60)
                    monsters.add(monster)
                for i in range(15):
                    enemy_speed = randint(1, 2)
                    asteroid = Asteroid('cat.png', randint(50, 1300)  , randint(0, 100), enemy_speed, 70, 50)
                    asteroids.add(asteroid)

    #Начало отсчёта перезарядки       
    if num_fire >= 10 and rel_time != True:
        rel_time = True
        clock1 = clocks.time()
        
    #Если идёт перезарядка...
    if rel_time == True:
        clock2 = clocks.time()
        timer = round(clock2 - clock1, 0)
        if timer < 2:
            window.blit(reloads, (625, 25))
        if timer >= 2:
            num_fire = 0
            rel_time = False

    #Обновление экрана
    display.update()
