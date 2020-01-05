# Side Scrolling Shooter Game
# Mahi Rahman, Son Tran, Sebastien Olife, Daniel Nguyen, Tejas Amrale, Peter Sorial, Spandan Kolapkar
# Version 1.0.0

import pygame, sys, random, time, os, math
from pygame.locals import *
import assets.modules.text as text
from assets.modules.variables import *
from assets.modules.sprites import *
from assets.modules.tilemap import *
import assets.modules.pygame_textinput as pygame_textinput

pygame.init()
fps = pygame.time.Clock()
pygame.display.set_caption('Star Invaders')
pygame.display.set_icon(pygame.image.load("assets/favicon.ico"))
pygame.mixer.music.set_volume(0.6)
pygame.mouse.set_visible(0)

global screen
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
display = pygame.Surface((400,250))

#Text
def get_text_width(text,spacing):
    global font_dat
    width = 0
    for char in text:
        if char in font_dat:
            width += font_dat[char][0] + spacing
    return width

font_dat = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
          'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
          '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
          '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
          '(':[2],')':[2],'/':[3],'_':[5],'=':[3],'\\':[3],'[':[2],']':[2],'*':[3],'"':[3],'<':[3],'>':[3],';':[1]}
font = text.generate_font('assets/font.png',font_dat,5,8,(248,248,248))
font_select = text.generate_font('assets/font.png',font_dat,5,8,(160,239,120))

#Variables
global up_key, down_key, select_key
up_key = 273
down_key = 274
select_key = 120

class menu_background(object):
    def __init__(self):
        self.particles = []
        self.timer = 0
        self.color_options = [(0,0,35)]
    def render(self,surface):
        surface.fill((0,0,10))
        self.timer += 1
        if self.timer > 20:
            self.timer = 0
            c = random.choice(self.color_options)
            x = random.randint(0,400)
            for i in range(1):
                self.particles.append([x,-10-i*2.5,c,8-i])
        for particle in self.particles:
            pygame.draw.circle(surface,particle[2],(int(particle[0]-math.sin(particle[1]/4500)*10),int(particle[1])),particle[3])
            particle[1] += 2.5
            if particle[0] > 400:
                self.particles.remove(particle)

#Main-Menu
def menu():
    bg = menu_background()
    logo = pygame.image.load('assets/images/logo.png')
    menu_options = ['Play','Highscores','Settings','Credits','Quit']
    menu_choice = 0
    in_menu = True

    pygame.mixer.music.load('assets/audio/mainmenu.wav')
    pygame.mixer.music.play(-1)

    while in_menu:
        bg.render(display)

        display.blit(logo,(56,20))
        text.show_text('Default Controls: Arrow Keys + X',2,240,1,9999,font,display)

        n = 0
        for option in menu_options:
            if menu_choice == n:
                text.show_text('> ' + option,200-int(get_text_width(option,1)/2)-5,100+n*20,1,9999,font_select,display)
            else:
                text.show_text(option,200-int(get_text_width(option,1)/2),100+n*20,1,9999,font,display)
            n += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == up_key:
                    menu_choice -= 1
                    if menu_choice < 0:
                        menu_choice = len(menu_options)-1
                if event.key == down_key:
                    menu_choice += 1
                    if menu_choice >= len(menu_options):
                        menu_choice = 0
                if event.key == select_key:
                    choice = menu_options[menu_choice]
                    if choice == 'Quit':
                        pygame.quit()
                        sys.exit()
                    if choice == 'Play':
                        game = Game()  #pygame will initialize here
                        while True: #While pygame is initialize
                            #pg.display.set_mode((0, 0), pg.FULLSCREEN)
                            pg.mouse.set_visible(False)
                            pg.mixer.music.load('assets/audio/level1.wav')
                            pg.mixer.music.play(-1)
                            game.new()
                            game.run()
                            if game.win:
                                game.you_win()
                            else:
                                game.game_over()
                    if choice == 'Highscores':
                        highscores()
                    if choice == 'Credits':
                        credits()
                    if choice == 'Settings':
                        settings()

        screen.blit(pygame.transform.scale(display,(WIDTH,HEIGHT)),(0,0))
        pygame.display.update()
        fps.tick(60)

#Highscores
def highscores():
    bg = menu_background()
    in_highscores = True
    while in_highscores:
        bg.render(display)

        with open("assets/raw_highscores.txt", "r") as array:
            leaderboard = []
            for line in array:
                leaderboard.append(line.split())
                leaderboard.sort(key=lambda i: int(i[1]), reverse=True)

        with open("assets/highscores.txt", "w+") as f:
            for NAME,SCORE in leaderboard:
                f.write(f'{NAME} - {SCORE} Points\n')

        f = open("assets/highscores.txt", "r")
        scores = f.read()

        text.show_text('LEADERBOARD',180,20,1,9999,font,display)
        text.show_text(scores,165,50,1,9999,font,display)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                in_highscores = False

        screen.blit(pygame.transform.scale(display,(WIDTH,HEIGHT)),(0,0))
        pygame.display.update()
        fps.tick(60)

#Settings
def settings():
    bg = menu_background()
    menu_options = ['Display Settings','Volume','Back']
    menu_choice = 0
    in_settings = True
    while in_settings:
        bg.render(display)

        n = 0
        for option in menu_options:
            if menu_choice == n:
                text.show_text('> ' + option,200-int(get_text_width(option,1)/2)-5,100+n*20,1,9999,font_select,display)
            else:
                text.show_text(option,200-int(get_text_width(option,1)/2),100+n*20,1,9999,font,display)
            n += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == up_key:
                    menu_choice -= 1
                    if menu_choice < 0:
                        menu_choice = len(menu_options)-1
                if event.key == down_key:
                    menu_choice += 1
                    if menu_choice >= len(menu_options):
                        menu_choice = 0
                if event.key == select_key:
                    choice = menu_options[menu_choice]
                    if choice == 'Display Settings':
                        display_config()
                    if choice == 'Volume':
                        volume()
                    if choice == 'Back':
                        in_settings = False
                if event.key == K_ESCAPE:
                    in_settings = False
        screen.blit(pygame.transform.scale(display,(WIDTH,HEIGHT)),(0,0))
        pygame.display.update()
        fps.tick(60)

def display_config():
    global WIDTH,HEIGHT,screen
    bg = menu_background()
    menu_options = ['Windowed','Fullscreen','Back']
    menu_choice = 0
    in_config = True
    while in_config:
        bg.render(display)

        n = 0
        for option in menu_options:
            if menu_choice == n:
                text.show_text('> ' + option,200-int(get_text_width(option,1)/2)-5,100+n*20,1,9999,font_select,display)
            else:
                text.show_text(option,200-int(get_text_width(option,1)/2),100+n*20,1,9999,font,display)
            n += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == up_key:
                    menu_choice -= 1
                    if menu_choice < 0:
                        menu_choice = len(menu_options)-1
                if event.key == down_key:
                    menu_choice += 1
                    if menu_choice >= len(menu_options):
                        menu_choice = 0
                if event.key == select_key:
                    choice = menu_options[menu_choice]
                    if choice == 'Windowed':
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    if choice == 'Fullscreen':
                        screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
                    if choice == 'Back':
                        in_config = False
                if event.key == K_ESCAPE:
                    in_config = False
        screen.blit(pygame.transform.scale(display,(WIDTH,HEIGHT)),(0,0))
        pygame.display.update()
        fps.tick(60)

def volume():
    bg = menu_background()
    menu_options = ['100/','75/','50/','25/','0/','Back']
    menu_choice = 0
    in_volume = True
    while in_volume:
        bg.render(display)

        n = 0
        for option in menu_options:
            if menu_choice == n:
                text.show_text('> ' + option,200-int(get_text_width(option,1)/2)-5,75+n*20,1,9999,font_select,display)
            else:
                text.show_text(option,200-int(get_text_width(option,1)/2),75+n*20,1,9999,font,display)
            n += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == up_key:
                    menu_choice -= 1
                    if menu_choice < 0:
                        menu_choice = len(menu_options)-1
                if event.key == down_key:
                    menu_choice += 1
                    if menu_choice >= len(menu_options):
                        menu_choice = 0
                if event.key == select_key:
                    choice = menu_options[menu_choice]
                    if choice == '100/':
                        pygame.mixer.music.set_volume(1)
                    if choice == '75/':
                        pygame.mixer.music.set_volume(0.75)
                    if choice == '50/':
                        pygame.mixer.music.set_volume(0.5)
                    if choice == '25/':
                        pygame.mixer.music.set_volume(0.25)
                    if choice == '0/':
                        pygame.mixer.music.set_volume(0)
                    if choice == 'Back':
                        in_volume = False
                if event.key == K_ESCAPE:
                    in_volume = False
        screen.blit(pygame.transform.scale(display,(WIDTH,HEIGHT)),(0,0))
        pygame.display.update()
        fps.tick(60)

#Credits
def credits():
    bg = menu_background()
    in_credits = True
    credits_dat = 'Star Invaders Level Design and Game Code by:\n\nMahi Rahman\nSon Tran\nDaniel Nguyen\nSebastien Olife\nTejas Amrale\nPeter Sorial\nSpandan Kolapkar\n\nWritten In - Python 3.7 and Pygame\nTools - Photoshop CS6, bfxr.net, Tiled Editor, Pytmx'
    while in_credits:
        bg.render(display)
        text.show_text(credits_dat,4,4,1,9999,font,display)
        text.show_text('(c) 2019, MFHS',4,240,1,9999,font,display)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                in_credits = False
        screen.blit(pygame.transform.scale(display,(WIDTH,HEIGHT)),(0,0))
        pygame.display.update()
        fps.tick(60)

#HUD For Player
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

#Main Game Class
class Game:
    def __init__(self):     #Variables are initialized
        #fps = pygame.time.Clock()
        self.particles = []
        self.timer = 0
        self.color_options = [(0,0,35)]
        self.font_name = pygame.font.match_font('8bit')
        self.load_data()

    #Loads Sounds and Text Font and Bullet Sprites
    def load_data(self):
        self.pixel_font = ('assets/8bit.ttf')
        self.bullet_img_R = pygame.image.load('assets/images/bullet_R.png').convert_alpha()
        self.bullet_img_R = pygame.transform.scale(self.bullet_img_R, (17, 8))
        self.bullet_img_L = pygame.image.load('assets/images/bullet_L.png').convert_alpha()
        self.bullet_img_L = pygame.transform.scale(self.bullet_img_L, (17, 8))
        self.bullet_mob = pygame.image.load('assets/images/alien_projectile.png').convert_alpha()
        self.bullet_mob = pygame.transform.scale(self.bullet_mob, (17, 8))

        self.effects_sound = {}
        for type in EFFECTS_SOUND:
            self.effects_sound[type] = pygame.mixer.Sound('assets/audio/'+EFFECTS_SOUND[type])
        self.shoot_sound = {}
        for audio in SHOOT_SOUND:
            self.shoot_sound[audio] = pygame.mixer.Sound('assets/audio/'+SHOOT_SOUND[audio])
        self.enemy_hurt = {}
        for audio in ENEMY_HURT:
            self.enemy_hurt[audio] = pygame.mixer.Sound('assets/audio/'+ENEMY_HURT[audio])
        self.player_jump = {}
        for audio in PLAYER_JUMP:
            self.player_jump[audio] = pygame.mixer.Sound('assets/audio/'+PLAYER_JUMP[audio])
        self.player_hurt = {}
        for audio in PLAYER_HURT:
            self.player_hurt[audio] = pygame.mixer.Sound('assets/audio/'+PLAYER_HURT[audio])
        self.enemy_morph = {}
        for audio in ENEMY_MORPH:
            self.enemy_morph[audio] = pygame.mixer.Sound('assets/audio/'+ENEMY_MORPH[audio])
        self.coin = {}
        for audio in COIN:
            self.coin[audio] = pygame.mixer.Sound('assets/audio/'+COIN[audio])

    #Initialize variables and sets up tilemap
    def new(self):
        self.score = 0
        self.score2 = 0
        self.playersalive = 0
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.invis_wall = pygame.sprite.Group()
        self.win_game = pygame.sprite.Group()
        self.mob_small_1 = pygame.sprite.Group()
        self.mob_small_2 = pygame.sprite.Group()
        self.mob_bullets = pygame.sprite.Group()
        self.mob_flying = pygame.sprite.Group()
        self.mob_big = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.spike = pygame.sprite.Group()
        self.map = TiledMap('assets/levels/lvl_1.tmx')
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.fall_death = pygame.sprite.Group()
        self.boundary = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bullets2 = pygame.sprite.Group()
        for tile_object in self.map.tmxdata.objects:    #FOR loop to render all objects and bitmap graphics in the tiled map (TMX)
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'player2':
                self.player2 = Player2(self, tile_object.x, tile_object.y)
            if tile_object.name == 'enemy':
                Mob_small_1(self, obj_center.x, obj_center.y)
            if tile_object.name == 'flying':
                Mob_flying(self, obj_center.x, obj_center.y)
            if tile_object.name in ['health']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name in ['coin']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'invis_wall':
                Invis_wall(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'boundary':
                Boundary(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'death':
                Fall(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'spike':
                Spike(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'win_area':
                Win_area(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False

    #Main Game Loop
    def run(self):
        self.playing = True
        self.win = False
        while self.playing and not self.win:
            self.dt = fps.tick(60)/1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    #Updates Camera and Sprites
    def update(self):
        if self.win or not self.playing:
            textinput.update(events)
            # Blit its surface onto the screen
            screen.blit(textinput.get_surface(), (10, 10))
            pygame.display.update()
            fps.tick(60)

        self.all_sprites.update()
        if self.player.alive and self.player2.alive:
            self.camera.update(self.player)
        elif self.player.alive and not self.player2.alive:
            self.camera.update(self.player)
        elif not self.player.alive and self.player2.alive:
            self.camera.update(self.player2)

        if self.player.collision: #if player 1 collision is enabled
            hits = pygame.sprite.spritecollide(self.player, self.items, False, collide_hit_rect)
            for hit in hits:
                if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                    hit.kill()
                    self.effects_sound['collect'].play()
                    self.player.add_health(20)
                elif hit.type == 'coin':
                    hit.kill()
                    self.coin['coin'].play()
                    self.score += 5

            hits = pygame.sprite.spritecollide(self.player, self.spike, False, collide_hit_rect)
            for hit in hits:
                if self.player.vel.x > 0:
                    self.player.vel.x -= 10
                    self.player.pos.x -= 10
                    self.player.vel.y -= 3
                elif self.player.vel.x < 0:
                    self.player.vel.x += 10
                    self.player.pos.x += 10
                    self.player.vel.y -= 3
                elif self.player.jumping and self.player.vel.x > 0:
                    self.player.pos.x -= 10
                    self.player.vel = vec(-5, -10)
                elif self.player.jumping and self.player.vel.x < 0:
                    self.player.pos.x += 10
                    self.player.vel = vec(5, -10)

                if self.player.vel.y < -5:
                    self.player.vel.y = -5

                self.player.health -= 5
                if self.player.health <= 0:
                    self.player.alive = False
                self.player_hurt['player_hurt'].play()
                self.player.hit()

            hits = pygame.sprite.spritecollide(self.player, self.mob_small_1, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt['player_hurt'].play()
                self.score -= 5
                self.player.health -= MOB_DAMAGE
                if self.player.health <= 0:
                    self.player.alive = False
                if self.player.alive:
                    self.player.hit()
                self.player.knockback(hit)

            hits = pygame.sprite.spritecollide(self.player, self.mob_small_2, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt['player_hurt'].play()
                self.score -= 5
                self.player.health -= MOB_DAMAGE
                if self.player.health <= 0:
                    self.player.alive = False
                if self.player.alive:
                    self.player.hit()
                self.player.knockback(hit)


            hits = pygame.sprite.spritecollide(self.player, self.mob_big, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt['player_hurt'].play()
                self.score -= 5
                self.player.health -= 20
                if self.player.health <= 0:
                    self.player.alive = False
                if self.player.alive:
                    self.player.hit()
                self.player.knockback(hit)

            hits = pygame.sprite.spritecollide(self.player, self.mob_bullets, False, collide_hit_rect)
            for hit in hits:
                hit.kill()
                self.player_hurt['player_hurt'].play()
                self.score -= 1
                self.player.health -= 5
                if self.player.health <= 0:
                    self.player.alive = False
                if self.player.alive:
                    self.player.hit()

            hits = pygame.sprite.spritecollide(self.player, self.mob_flying, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt['player_hurt'].play()
                self.score -= 5
                self.player.health -= 5
                if self.player.health <= 0:
                    self.player.alive = False
                self.player.hit()
                self.player.knockback(hit)

        if self.player2.collision:  #if player 2 collision is enabled
            hits = pygame.sprite.spritecollide(self.player2, self.items, False, collide_hit_rect)
            for hit in hits:
                if hit.type == 'health' and self.player2.health < PLAYER_HEALTH:
                    hit.kill()
                    self.effects_sound['collect'].play()
                    self.player2.add_health(20)
                elif hit.type == 'coin':
                    hit.kill()
                    self.coin['coin'].play()
                    self.score2 += 5

            hits = pygame.sprite.spritecollide(self.player2, self.spike, False, collide_hit_rect)
            for hit in hits:
                if self.player2.vel.x > 0:
                    self.player2.vel.x -= 10
                    self.player2.pos.x -= 10
                    self.player2.vel.y -= 3
                elif self.player2.vel.x < 0:
                    self.player2.vel.x += 10
                    self.player2.pos.x += 10
                    self.player2.vel.y -= 3
                elif self.player2.jumping and self.player2.vel.x > 0:
                    self.player2.pos.x -= 10
                    self.player2.vel = vec(-5, -10)
                elif self.player2.jumping and self.player2.vel.x < 0:
                    self.player2.pos.x += 10
                    self.player2.vel = vec(5, -10)

                if self.player2.vel.y < -5:
                    self.player2.vel.y = -5

                self.player2.health -= 5
                if self.player2.health <= 0:
                    self.player2.alive = False
                self.player_hurt['player_hurt'].play()
                self.player2.hit()

            hits = pygame.sprite.spritecollide(self.player2, self.mob_small_1, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt['player_hurt'].play()
                self.score2 -= 5
                self.player2.health -= MOB_DAMAGE
                if self.player2.health <= 0:
                    self.player2.alive = False
                if self.player2.alive:
                    self.player2.hit()
                self.player2.knockback(hit)

            hits = pygame.sprite.spritecollide(self.player2, self.mob_small_2, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt['player_hurt'].play()
                self.score2 -= 5
                self.player2.health -= MOB_DAMAGE
                if self.player2.health <= 0:
                    self.player2.alive = False
                if self.player2.alive:
                    self.player2.hit()
                self.player2.knockback(hit)

            hits = pygame.sprite.spritecollide(self.player2, self.mob_big, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt['player_hurt'].play()
                self.score2 -= 5
                self.player2.health -= 20
                if self.player2.health <= 0:
                    self.player2.alive = False
                if self.player2.alive:
                    self.player2.hit()
                self.player2.knockback(hit)


            hits = pygame.sprite.spritecollide(self.player2, self.mob_flying, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt['player_hurt'].play()
                self.score2 -= 5
                self.player2.health -= 5
                if self.player2.health <= 0:
                    self.player2.alive = False
                if self.player2.alive:
                    self.player2.hit()
                self.player2.knockback(hit)


            hits = pygame.sprite.spritecollide(self.player2, self.mob_bullets, False, collide_hit_rect)
            for hit in hits:
                hit.kill()
                self.player_hurt['player_hurt'].play()
                self.score2 -= 1
                self.player2.health -= 5
                if self.player2.health <= 0:
                    self.player2.alive = False
                if self.player2.alive:
                    self.player2.hit()
        else:
            pass

        #Bullet Collisions to Mobs
        hits = pygame.sprite.groupcollide(self.mob_small_1, self.bullets2, False, True)
        for hit in hits:
            self.enemy_hurt['enemy_hurt'].play()
            self.score2 += 1
            hit.health -= BULLET_DAMAGE
            if hit.health <= 0:
                hit.kill()
                self.score2 += 10
                chance = random.randint(1,4)
                if chance == 1:
                    self.enemy_morph['morph'].play()
                    Mob_Big(self, hit.pos.x, hit.pos.y, hit.facing)
                else:
                    pass

        hits = pygame.sprite.groupcollide(self.mob_small_1, self.bullets, False, True)
        for hit in hits:
            self.enemy_hurt['enemy_hurt'].play()
            self.score += 1
            hit.health -= BULLET_DAMAGE
            if hit.health <= 0:
                hit.kill()
                self.score += 10
                chance = random.randint(1,4)
                if chance == 1:
                    self.enemy_morph['morph'].play()
                    Mob_Big(self, hit.pos.x, hit.pos.y, hit.facing)
                else:
                    pass

        hits = pygame.sprite.groupcollide(self.mob_small_2, self.bullets2, False, True)
        for hit in hits:
            self.enemy_hurt['enemy_hurt'].play()
            self.score2 += 1
            hit.health -= BULLET_DAMAGE
            if hit.health <= 0:
                hit.kill()
                self.score2 += 10

        hits = pygame.sprite.groupcollide(self.mob_small_2, self.bullets, False, True)
        for hit in hits:
            self.enemy_hurt['enemy_hurt'].play()
            self.score += 1
            hit.health -= BULLET_DAMAGE
            if hit.health <= 0:
                hit.kill()
                self.score += 10

        hits = pygame.sprite.groupcollide(self.mob_flying, self.bullets, False, True)
        for hit in hits:
            self.enemy_hurt['enemy_hurt'].play()
            self.score += 2
            hit.health -= BULLET_DAMAGE
            if hit.health <= 0:
                hit.kill()
                self.score += 15
                self.enemy_morph['morph'].play()
                Mob_small_2(self, hit.pos.x, hit.pos.y, hit.facing)

        hits = pygame.sprite.groupcollide(self.mob_flying, self.bullets2, False, True)
        for hit in hits:
            self.enemy_hurt['enemy_hurt'].play()
            self.score2 += 2
            hit.health -= BULLET_DAMAGE
            if hit.health <= 0:
                hit.kill()
                self.score2 += 15
                self.enemy_morph['morph'].play()
                Mob_small_2(self, hit.pos.x, hit.pos.y, hit.facing)

        hits = pygame.sprite.groupcollide(self.mob_big, self.bullets2, False, True)
        for hit in hits:
            self.enemy_hurt['enemy_hurt'].play()
            self.score2 += 3
            hit.health -= BULLET_DAMAGE
            if hit.health <= 0:
                hit.kill()
                self.score2 += 30

        hits = pygame.sprite.groupcollide(self.mob_big, self.bullets, False, True)
        for hit in hits:
            self.enemy_hurt['enemy_hurt'].play()
            self.score += 3
            hit.health -= BULLET_DAMAGE
            if hit.health <= 0:
                hit.kill()
                self.score += 30

        if self.score < 0:
            self.score = 0

        if self.score2 < 0:
            self.score2 = 0

        out_of_map = pygame.sprite.spritecollide(self.player, self.fall_death, False)
        out_of_map2 = pygame.sprite.spritecollide(self.player2, self.fall_death, False)

        if out_of_map:
            self.player.health -= 100
            self.player.alive = False

        if out_of_map2:
            self.player2.health -= 100
            self.player2.alive = False

        if self.playersalive == 2:
            self.playing = False

        #Player 1 and 2 when level is finished displays WIN
        win1 = pygame.sprite.spritecollide(self.player, self.win_game, False)
        win2 = pygame.sprite.spritecollide(self.player2, self.win_game, False)
        if self.player.alive and not self.player2.alive:
            if win1:
                self.win = True
        elif not self.player.alive and self.player2.alive:
            if win2:
                self.win = True
        elif self.player.alive and self.player2.alive:
            if win1 and win2:
                self.win = True

    def draw(self):
        screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pygame.draw.rect(screen, RED, self.camera.apply_rect(sprite.hit_rect), 1)
                pygame.draw.rect(screen, GREEN, self.camera.apply_rect(sprite.rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pygame.draw.rect(screen, RED, self.camera.apply_rect(wall.rect), 1)
            for item in self.items:
                pygame.draw.rect(screen, RED, self.camera.apply_rect(item.rect), 1)
            for spike in self.spike:
                pygame.draw.rect(screen, RED, self.camera.apply_rect(spike.rect), 1)
            for item in self.bullets:
                pygame.draw.rect(screen, RED, self.camera.apply_rect(item.rect), 1)

        #HUD
        draw_player_health(screen, 10, 10, self.player.health / PLAYER_HEALTH)
        draw_player_health(screen, 350, 10, self.player2.health / PLAYER_HEALTH)

        if self.paused:
            self.display = pygame.Surface((self.map.width, self.map.height))
            self.draw_text("PAUSE", self.pixel_font,65, WHITE, WIDTH/2, HEIGHT/2, align="center")

        #Display player 1's score
        self.draw_text("SCORE:" + str(self.score), self.pixel_font,15, WHITE, WIDTH/6.5, 37, align="center")

        #Displaye player 2's score
        self.draw_text("SCORE:" + str(self.score2), self.pixel_font,15, WHITE, WIDTH/1.2, 37, align="center")

        #Enemy counter
        self.draw_text('ALIENS: {}'.format(len(self.mob_small_1) + len(self.mob_big) + len(self.mob_flying) + len(self.mob_small_2)), self.pixel_font, 15, WHITE, WIDTH/2, 15, align="center")
        pygame.display.flip()

    def draw_text(self, text, font_name, size, color, x, y, align="center"):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "center":
            text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)

    #Key presses
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                if event.key == pygame.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pygame.K_UP:
                    self.player2.jump()
                if event.key == pygame.K_w:
                    self.player.jump()
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_o:
                    print(self.player.vel)

    def you_win(self):
        enter = True
        while enter:
            player1name = pygame_textinput.TextInput(font_family = "assets/8bit.ttf", antialias = False)
            enter1 = True
            if self.score > 0:
                while enter1:
                    screen.fill((60,179,113))
                    events = pygame.event.get()
                    self.draw_text("enter player 1 name", self.pixel_font, 35, WHITE, int(WIDTH/2), int(HEIGHT/2)-50, align="center")
                    screen.blit(player1name.get_surface(), (int(WIDTH/2)-35, int(HEIGHT/2)))

                    if player1name.update(events):
                        pass

                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                enter1 = False

                    pygame.display.update()
                    fps.tick(60)
            else:
                enter1 = False

            player2name = pygame_textinput.TextInput(font_family = "assets/8bit.ttf", antialias = False)
            enter2 = True
            if self.score2 > 0:
                while enter2:
                    screen.fill((60,179,113))
                    events = pygame.event.get()
                    self.draw_text("enter player 2 name", self.pixel_font, 35, WHITE, int(WIDTH/2), int(HEIGHT/2)-50, align="center")
                    screen.blit(player2name.get_surface(), (int(WIDTH/2)-35, int(HEIGHT/2)))

                    if player2name.update(events):
                        pass

                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                enter2 = False

                    pygame.display.update()
                    fps.tick(60)
            else:
                enter1 = False
            enter = False

        screen.fill((60,179,113))

        if self.score > 0 and self.score2 > 0:
            highscore = {player1name.get_text(): self.score, player2name.get_text(): self.score2}
        if self.score > 0 and self.score2 == 0:
            highscore = {player1name.get_text(): self.score}
        if self.score == 0 and self.score2 > 0:
            highscore = {player2name.get_text(): self.score2}

        if self.score > 0  or self.score2 > 0:
            for NAME, SCORE in highscore.items():
                f = open("assets/raw_highscores.txt", "a")
                f.write(str(NAME) + ' ' + str(SCORE) + '\n')
                f.close()

        self.draw_text("You Win!", self.pixel_font, 80, YELLOW, WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("press ENTER to restart", self.pixel_font, 30, WHITE,WIDTH / 2, HEIGHT * 3 / 4.5, align="center")
        self.draw_text("or ESCAPE to go to main menu", self.pixel_font, 30, WHITE,WIDTH / 2, HEIGHT * 3 / 4, align="center")

        self.draw_text(player1name.get_text(), self.pixel_font,25, WHITE, WIDTH/3, 40, align="center")
        self.draw_text(str(self.score), self.pixel_font,25, WHITE, WIDTH/3, 60, align="center")

        self.draw_text(player2name.get_text(), self.pixel_font,25, WHITE, WIDTH/1.5, 40, align="center")
        self.draw_text(str(self.score2), self.pixel_font,25, WHITE, WIDTH/1.5, 60, align="center")

        pygame.display.flip()
        self.wait_for_key()

    def game_over(self):
        enter = True
        while enter:
            player1name = pygame_textinput.TextInput(font_family = "assets/8bit.ttf", antialias = False)
            enter1 = True
            if self.score > 0:
                while enter1:
                    screen.fill((110, 0, 0))
                    events = pygame.event.get()
                    self.draw_text("enter player 1 name", self.pixel_font, 35, WHITE, int(WIDTH/2), int(HEIGHT/2)-50, align="center")
                    screen.blit(player1name.get_surface(), (int(WIDTH/2)-35, int(HEIGHT/2)))

                    if player1name.update(events):
                        pass

                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                enter1 = False

                    pygame.display.update()
                    fps.tick(60)
            else:
                enter1 = False

            player2name = pygame_textinput.TextInput(font_family = "assets/8bit.ttf", antialias = False)
            enter2 = True
            if self.score2 > 0:
                while enter2:
                    screen.fill((110, 0, 0))
                    events = pygame.event.get()
                    self.draw_text("enter player 2 name", self.pixel_font, 35, WHITE, int(WIDTH/2), int(HEIGHT/2)-50, align="center")
                    screen.blit(player2name.get_surface(), (int(WIDTH/2)-35, int(HEIGHT/2)))

                    if player2name.update(events):
                        pass

                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                enter2 = False

                    pygame.display.update()
                    fps.tick(60)
            else:
                enter1 = False
            enter = False

        screen.fill((0, 0, 0))

        if self.score > 0 and self.score2 > 0:
            highscore = {player1name.get_text(): self.score, player2name.get_text(): self.score2}
        if self.score > 0 and self.score2 == 0:
            highscore = {player1name.get_text(): self.score}
        if self.score == 0 and self.score2 > 0:
            highscore = {player2name.get_text(): self.score2}

        if self.score > 0  or self.score2 > 0:
            for NAME, SCORE in highscore.items():
                f = open("assets/raw_highscores.txt", "a")
                f.write(str(NAME) + ' ' + str(SCORE) + '\n')
                f.close()

        self.draw_text("GAME OVER!", self.pixel_font, 80, RED,WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("press ENTER to restart", self.pixel_font, 30, WHITE,WIDTH / 2, HEIGHT * 3 / 4.5, align="center")
        self.draw_text("or ESCAPE to go to main menu", self.pixel_font, 30, WHITE,WIDTH / 2, HEIGHT * 3 / 4, align="center")

        self.draw_text(player1name.get_text(), self.pixel_font,25, WHITE, WIDTH/3, 40, align="center")
        self.draw_text(str(self.score), self.pixel_font,25, WHITE, WIDTH/3, 60, align="center")

        self.draw_text(player2name.get_text(), self.pixel_font,25, WHITE, WIDTH/1.5, 40, align="center")
        self.draw_text(str(self.score2), self.pixel_font,25, WHITE, WIDTH/1.5, 60, align="center")

        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pygame.event.wait()
        waiting = True
        while waiting:
            fps.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                    if event.key == pygame.K_ESCAPE:
                        menu()

    def render(self,surface):
        surface.fill((0,0,10))
        self.timer += 1
        if self.timer > 20:
            self.timer = 0
            c = random.choice(self.color_options)
            x = random.randint(0,400)
            for i in range(1):
                self.particles.append([x,-10-i*2.5,c,8-i])
        for particle in self.particles:
            pygame.draw.circle(surface,particle[2],(int(particle[0]-math.sin(particle[1]/4500)*10),int(particle[1])),particle[3])
            particle[1] += 2.5
            if particle[0] > 400:
                self.particles.remove(particle)

menu()