import pygame, sys, random as rand
from pygame.locals import *
pygame.init()

#screen
WIDTH = 800
HEIGHT = 600
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up colors
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (34, 177, 76)
BLUE = (0, 0, 255)
GRAY = (75, 75, 75)
YELLOW = (255, 255, 0)

#game variables
gameover = False
play_x = 50
play_y = 275
enemies = []
collided = False
high_scores = [0,0,0,0,0]
velocity = 3.5

#set up max fps
FPS = 60
fpsClock = pygame.time.Clock()
dt = 0
time_elapsed = 0
gas = 100

#Text
videoGameFont = pygame.font.SysFont('franklingothicmedium', 32)

#set up window
pygame.display.set_caption("Retro Racer")
basicFont = pygame.font.SysFont(None, 48)
background = pygame.image.load('DIRTROADBG.png').convert()
background = pygame.transform.smoothscale(background, windowSurface.get_size())
windowSurface.blit(background, (0, 0))

title = pygame.image.load('Retro Racer Title.png')

#import player and enemy car image
player_car = pygame.image.load('BlueCar.png')
enemy1 = pygame.image.load('Car_Red_Front.png')
start_btn = pygame.image.load('start_btn_img.png')

#screen variables
screen = 'start'

#coin variables
coins_ls = []



class Coins():
    def __init__(self):
        self.coin_img = pygame.image.load('gas_can.png')

        self.coin_rect = self.coin_img.get_rect(center = (400, 300))
    def display(self):
        windowSurface.blit(self.coin_img, self.coin_rect)
    def is_hit(self, obj):
        if self.coin_rect.colliderect(obj):
            return True
        return False
    def set_pos(self, x, y):
        self.coin_rect.center = (x, y)
    
def generate_coins():
    coin = Coins()
    return coin
    
class player:
    def __init__(self):
        self.player_car = pygame.image.load('BlueCar.png')
        self.player_rect = self.player_car.get_rect(center = (50, 275))
        self.play_x = 50
        self.play_y = 275

    def draw_player(self):
        self.player_rect.center = (self.play_x,self.play_y)
        windowSurface.blit(self.player_car, self.player_rect)
        
        return self.player_rect
    
    def move_player(self):
        if pygame.key.get_pressed()[K_LEFT]:
            if self.play_x > 0:
                self.play_x -=velocity
        if pygame.key.get_pressed()[K_RIGHT]:
            if self.play_x < WIDTH:
                self.play_x += velocity
        if pygame.key.get_pressed()[K_UP]:
            if self.play_y > 50:
                self.play_y -= velocity
        if pygame.key.get_pressed()[K_DOWN]:
            if self.play_y < 500:
                self.play_y+= velocity
                
    def set_car(self, car_img):
        self.player_car = pygame.image.load(car_img)
        self.player_rect = self.player_car.get_rect()
        
    def get_rect(self):
        return self.player_rect
    
    def hit(self):
        for enemy in enemies:
            if self.player_rect.colliderect(enemy.enemy_rect):
                return True
        return False



'''
update to add multiple cars
maybe
in the future
'''
class Car:
    def ___init___(self, img, price):
        self.car_img = pygame.image.load(img)
        self.car_rect = self.car_img.get_rect()
        self.price = price
        self.purchased = False
        
    def display(self):
        if self.purchased:
            windowSurface.blit(self.car_img, self.car_rect)
    
    def buy_car(self):
        self.purchased = True
        
    

class Enemy():
    def __init__(self, x, y):
        self.enemy_img = pygame.image.load('Car_Red_Front.png')
        self.enemy_rect = self.enemy_img.get_rect(left=x, top=y)

    def move_enemy(self, x_move):
        x = self.enemy_rect.left-x_move
        y = self.enemy_rect.top
        if x <= 2:
            x = 830
            y = rand.randint(50, 500)
        self.enemy_rect.left, self.enemy_rect.top = x, y
        windowSurface.blit(self.enemy_img, self.enemy_rect)
    
    #check to see if enemy hit player  
    def hit_player(self, player):
        if self.enemy_rect.left + 10 < player.right and (self.enemy_rect.top+10 < player.bottom or self.enemy_rect.bottom-10 > player.top):
            return True
        return False
        

#ask player if they want to play again
def play_again_msg():

        play_again_msg = 'Would you like to play again?'
        text = videoGameFont.render(play_again_msg, True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.centerx = 400
        textRect.centery = 300

        pygame.draw.rect(windowSurface, BLACK, pygame.Rect(textRect.left-20, textRect.top-20, textRect.width+40, textRect.height+100))

        yes_msg = 'Yes!'
        yesText = videoGameFont.render(yes_msg, True, WHITE, GREEN)
        yesRect = yesText.get_rect()
        yesRect.width += 20
        yesRect.height += 10
        yesRect.right = textRect.centerx - 10
        yesRect.top = textRect.bottom + 20
        
        yes_btn = pygame.draw.rect(windowSurface, GREEN, pygame.Rect(yesRect.right-100, yesRect.top-10, 100, 60))

        #make no button
        no_msg = "No"
        noText = videoGameFont.render(no_msg, True, WHITE, RED)
        noRect = noText.get_rect()
        noRect.width = yesRect.width
        noRect.height = yesRect.height
        noRect.left = textRect.centerx + 40
        noRect.top = textRect.bottom + 20

        no_btn = pygame.draw.rect(windowSurface, RED, pygame.Rect(410, noRect.top-10, 100, 60))

        windowSurface.blit(text, textRect)
        windowSurface.blit(yesText, yesRect)
        windowSurface.blit(noText, noRect)
        
        return yes_btn, no_btn

#show the score while playing
def display_score(score):
    msg = str(score)
    text = videoGameFont.render(msg, True, BLACK, GREEN)
    textRect = text.get_rect()
    textRect.right = 775
    textRect.top = 25
    windowSurface.blit(text, textRect)

#restart the game
def reset_game():
    score = 0
    gas = 100
    score_added = False
    enemies = []
    play_x, play_y = 50, 275
    pos = 800
    coins_ls = []
    p1 = player()
        
    for _ in range(8):
        enemies.append(Enemy(pos, rand.randint(50, 500)))
        pos += rand.randint(100,150)
    
    return score, gas, score_added, enemies, play_x, play_y, pos, coins_ls, p1

#checks if one obejct is above another
def is_over(thing):
    if thing.collidepoint(pygame.mouse.get_pos()):
        return True
    return False

#checks to see if something was clicked
def is_clicked(thing):
    over = is_over(thing)
    if over and pygame.mouse.get_pressed()[0]:
        return True
    return False

#allows user to play in full screen
#sort of janky
def full_screen():
        if pygame.key.get_pressed()[K_f] or pygame.key.get_pressed()[K_ESCAPE]:
            pygame.display.toggle_fullscreen()
            pygame.time.delay(100)

#TODO implement pause screen
def pause_screen():
    pygame.draw.rect(windowSurface, BLACK, pygame.Rect(WIDTH/2, HEIGHT/2, 100, 100))

#initallize the variables
score, gas, score_added, enemies, play_x, play_y, pos, coins_ls, p1 = reset_game()

#main game loop
while not gameover:
    #check to see if user quit the game
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
    #start button screen
    if screen == 'start':
        windowSurface.blit(background, (0, 0))

        start_btn_rect = start_btn.get_rect(center = (WIDTH/2-16, 400))
        windowSurface.blit(start_btn, start_btn_rect)
        
        windowSurface.blit(title, title.get_rect(center = (WIDTH/2, 200)))
        if is_clicked(start_btn_rect):
            screen = 'playing'
    
    #playing screen
    if screen == 'playing':
        windowSurface.blit(background, (0, 0))

        #add to score and show it
        score += 1
        display_score(score)
        
        #move and draw player
        p1.move_player()
        p1.draw_player()
        #move enemies left

        
        for enemy in enemies:
            move = 3 + score/1000
            if move > 10:
                move = 10
            enemy.move_enemy(move)
        
        pygame.draw.rect(windowSurface, WHITE, pygame.Rect(10, 10, gas*2, 20))

        if score % 300 == 0:
            c = generate_coins()
            c.set_pos(rand.randint(50,WIDTH-200), rand.randint(50,500))
            coins_ls.append(c)

        for c in coins_ls:
            c.display()
            if c.is_hit(p1.get_rect()):
                gas += 10
                coins_ls.pop(coins_ls.index(c))
                
        #decrease gas
        time_elapsed += dt
        if time_elapsed > 500:
            gas -= 1
            time_elapsed = 0
            
            
        collided = p1.hit()
        
        if collided or gas <= 0:
            screen = 'play again'
            pygame.time.delay(700)
    
        '''
        pause_btn =  pygame.draw.rect(windowSurface, BLACK, pygame.Rect(WIDTH/2+10, 10, 20, 20))
        if is_clicked(pygame.mouse.get_pos(), pause_btn):
            show_pause = True
            
        if show_pause:
            pause_screen()
        '''
    
    #asking user to play again screen
    if screen == 'play again':
        
        if not score_added:
            for i in range(len(high_scores)):
                if score > high_scores[i]:
                    high_scores.insert(i, score)
                    score_added = True
                    break
            
        yes_btn, no_btn = play_again_msg()

        mx, my = pygame.mouse.get_pos()
            
        if (event.type == pygame.MOUSEBUTTONDOWN):
                if is_clicked(yes_btn):
                    #reset game variables
                    screen = 'playing'
                    score, gas, score_added, enemies, play_x, play_y, pos, coins_ls, p1 = reset_game()

                    pygame.time.delay(100)
                elif is_clicked(no_btn):
                    screen = 'leaderboard'
                    pygame.time.delay(200)
    

    #display leaderbaord for 10 seconds then exit the game
    if screen == 'leaderboard':
             
        with open("ScoreBoard.txt", "r+", encoding = 'utf-8') as s:
            scores = s.read().split('\n')
            l = 5
            if len(scores)<5:
                l = len(scores)
            for i in range(l):
                for x in range(len(high_scores)):
                    if int(scores[i]) < high_scores[0]:
                        scores.insert(i, high_scores[0])
                        scores.remove(scores[-1])
                        high_scores.remove(high_scores[0])
                        
        with open('ScoreBoard.txt', 'r+', encoding = 'utf-8') as s:
            s.truncate(0)
            for i in scores:
                s.write(str(i) + '\n')
                
        msgs = ["1st: ", "2nd: ", "3rd: ", "4th: ", "5th: "]
        pygame.draw.rect(windowSurface, BLACK, pygame.Rect(50, 50, 700, 500))
        msg_scores = 'Leaderboard'
        text_scores = videoGameFont.render(msg_scores, True, WHITE, BLACK)
        text_scoresRect = text_scores.get_rect()
        text_scoresRect.centerx = 400
        text_scoresRect.bottom = 150
        windowSurface.blit(text_scores, text_scoresRect)
        for i in range(len(msgs)):
            msg = msgs[i] + str(scores[i])
            text = videoGameFont.render(msg, True, WHITE, BLACK)
            textRect = text.get_rect(center = (400, 200 + i*50))
            windowSurface.blit(text, textRect)
            pygame.display.update()
            dt = fpsClock.tick(FPS)
        gameover = True
        pygame.time.delay(4000)


    full_screen()
    pygame.display.update()
    dt = fpsClock.tick(FPS)
        
pygame.quit()
sys.exit()