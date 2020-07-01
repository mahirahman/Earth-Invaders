import pygame, sys, random, time, os, math
from pygame.locals import *
import assets.modules.text as text
from assets.modules.sprites import *
from assets.modules.tilemap import *
import assets.modules.pygame_textinput as pygame_textinput

pygame.init()
fps = pygame.time.Clock()
stars = []
pygame.display.set_caption('Earth Invaders')
pygame.display.set_icon(pygame.image.load("assets/favicon.ico"))
pygame.mixer.music.set_volume(0.6)
pygame.mouse.set_visible(0)
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

def bg_render(surface):
    surface.fill((9,10,15))

    for i in range(25):
        stars.append([random.randint(0, WIDTH), random.randint(0, HEIGHT)])
        pygame.draw.circle(screen, (200, 200, 200), stars[i], 2, 0)
        stars[i][0] -= 5
        if stars[i][0] < 0:
            stars[i][0] = WIDTH

    pygame.display.flip()
    fps.tick(60)

def menu():
    logo = pygame.image.load('assets/images/logo.png')
    menu_options = ['Play','Controls','Highscores','Settings','Credits','Quit']
    menu_choice = 0
    in_menu = True

    pygame.mixer.music.load('assets/audio/mainmenu.wav')
    pygame.mixer.music.play(-1)

    while in_menu:
        bg_render(display)
        display.blit(logo,(65,46))

        text.show_text('Menu Controls: Arrow Keys + Space',2,240,1,9999,font,display)

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
                if event.key == K_UP:
                    menu_choice -= 1
                    if menu_choice < 0:
                        menu_choice = len(menu_options)-1
                if event.key == K_DOWN:
                    menu_choice += 1
                    if menu_choice >= len(menu_options):
                        menu_choice = 0
                if event.key == K_SPACE:
                    choice = menu_options[menu_choice]
                    if choice == 'Play':
                        game = Game()
                        while True:
                            pygame.mouse.set_visible(False)
                            pygame.mixer.music.load('assets/audio/level1.wav')
                            pygame.mixer.music.play(-1)
                            game.new()
                            game.run()
                            if game.win:
                                game.you_win()
                            else:
                                game.game_over()
                    if choice == 'Controls':
                        controls()
                    if choice == 'Highscores':
                        highscores()
                    if choice == 'Credits':
                        credits()
                    if choice == 'Settings':
                        settings()
                    if choice == 'Quit':
                        pygame.quit()
                        sys.exit()

        screen.blit(pygame.transform.scale(display,(WIDTH,HEIGHT)),(0,0))
        pygame.display.flip()
        fps.tick(60)

def controls():
    in_controls = True
    while in_controls:
        bg_render(display)

        text.show_text('Press ESC to go back',2,240,1,9999,font,display)
        text_array = ['Use WASD and Space for Player 1','Use Arrow keys and Right Enter for Player 2','Press P to Pause']

        n = 0
        for list in text_array:
            text.show_text(list,200-int(get_text_width(list,2)/2),95+n*20,1,9999,font,display)
            n += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    in_controls = False
        screen.blit(pygame.transform.scale(display,(WIDTH,HEIGHT)),(0,0))
        pygame.display.flip()
        fps.tick(60)

def highscores():
    in_highscores = True
    while in_highscores:
        bg_render(display)

        text.show_text('Press ESC to go back',2,240,1,9999,font,display)

        with open("assets/highscores.txt", "r") as array:
            leaderboard = array.readlines()

        leaderboard = list(map(lambda line: tuple(line.split()), leaderboard))
        leaderboard.sort(key=lambda line: int(line[1]), reverse=True)
        leaderboard = list(map(lambda line: f"{line[0]} - {line[1]} Points\n", leaderboard))
        for n,score in enumerate(leaderboard):
            text.show_text(score,200-int(get_text_width(score,2)/2),50+n*20,1,9999,font,display)

        text.show_text('LEADERBOARD',200-int(get_text_width('LEADERBOARD',1)/2),20,1,9999,font,display)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    in_highscores = False

        screen.blit(pygame.transform.scale(display,(WIDTH,HEIGHT)),(0,0))
        pygame.display.flip()
        fps.tick(60)

def settings():
    menu_options = ['Display Settings','Volume','Back']
    menu_choice = 0
    in_settings = True
    while in_settings:
        bg_render(display)

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
                if event.key == K_UP:
                    menu_choice -= 1
                    if menu_choice < 0:
                        menu_choice = len(menu_options)-1
                if event.key == K_DOWN:
                    menu_choice += 1
                    if menu_choice >= len(menu_options):
                        menu_choice = 0
                if event.key == K_SPACE:
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
        pygame.display.flip()
        fps.tick(60)

def display_config():
    global WIDTH,HEIGHT,screen
    menu_options = ['Windowed','Fullscreen','Back']
    menu_choice = 0
    in_config = True
    while in_config:
        bg_render(display)

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
                if event.key == K_UP:
                    menu_choice -= 1
                    if menu_choice < 0:
                        menu_choice = len(menu_options)-1
                if event.key == K_DOWN:
                    menu_choice += 1
                    if menu_choice >= len(menu_options):
                        menu_choice = 0
                if event.key == K_SPACE:
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
        pygame.display.flip()
        fps.tick(60)

def volume():
    menu_options = ['100/','75/','50/','25/','0/','Back']
    menu_choice = 0
    in_volume = True
    while in_volume:
        bg_render(display)

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
                if event.key == K_UP:
                    menu_choice -= 1
                    if menu_choice < 0:
                        menu_choice = len(menu_options)-1
                if event.key == K_DOWN:
                    menu_choice += 1
                    if menu_choice >= len(menu_options):
                        menu_choice = 0
                if event.key == K_SPACE:
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
        pygame.display.flip()
        fps.tick(60)

def credits():
    in_credits = True
    while in_credits:
        bg_render(display)

        text.show_text('Press ESC to go back',2,240,1,9999,font,display)
        credits_array = ['Mahi Rahman','Son Tran','Daniel Nguyen','Tejas Amrale','Peter Sorial','Spandan Kolapkar']

        n = 0
        for names in credits_array:
            text.show_text(names,200-int(get_text_width(names,1)/2),70+n*20,1,9999,font,display)
            n += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    in_credits = False

        screen.blit(pygame.transform.scale(display,(WIDTH,HEIGHT)),(0,0))
        pygame.display.flip()
        fps.tick(60)

class Game:

    def __init__(self):
        self.font_name = pygame.font.match_font('8bit')
        pygame.font.init()
        self.font = pygame.font.Font('assets/8bit.ttf', 60)
        self.opx = 2
        self.osurf = 0
        self.tsurf = 0
        self.load_data()

    #Loads Sounds and Text Font and Bullet Sprites
    def load_data(self):
        self.pixel_font = ('assets/8bit.ttf')
        self.bullet_img_R = pygame.image.load('assets/images/bullet_R.png').convert_alpha()
        self.bullet_img_R = pygame.transform.scale(self.bullet_img_R, (12, 5))
        self.bullet_img_L = pygame.image.load('assets/images/bullet_L.png').convert_alpha()
        self.bullet_img_L = pygame.transform.scale(self.bullet_img_L, (12, 5))
        self.bullet_mob = pygame.image.load('assets/images/alien_projectile.png').convert_alpha()
        self.bullet_mob = pygame.transform.scale(self.bullet_mob, (17, 8))

        self.coin = pygame.mixer.Sound("assets/audio/coin.wav")
        self.enemy_hurt = pygame.mixer.Sound("assets/audio/enemy_hurt.wav")
        self.health = pygame.mixer.Sound("assets/audio/health.wav")
        self.jump_1 = pygame.mixer.Sound("assets/audio/jump_1.wav")
        self.jump_2 = pygame.mixer.Sound("assets/audio/jump_2.wav")
        self.morph = pygame.mixer.Sound("assets/audio/morph.wav")
        self.player_hurt = pygame.mixer.Sound("assets/audio/player_hurt.wav")
        self.shoot = pygame.mixer.Sound("assets/audio/shoot.wav")

        self.healthbar_0 = pygame.image.load('assets/sprites/health/0.png')
        self.healthbar_1 = pygame.image.load('assets/sprites/health/1.png')
        self.healthbar_2 = pygame.image.load('assets/sprites/health/2.png')
        self.healthbar_3 = pygame.image.load('assets/sprites/health/3.png')
        self.healthbar_4 = pygame.image.load('assets/sprites/health/4.png')
        self.healthbar_5 = pygame.image.load('assets/sprites/health/5.png')
        self.healthbar_6 = pygame.image.load('assets/sprites/health/6.png')
        self.healthbar_7 = pygame.image.load('assets/sprites/health/7.png')
        self.healthbar_8 = pygame.image.load('assets/sprites/health/8.png')
        self.healthbar_9 = pygame.image.load('assets/sprites/health/9.png')
        self.healthbar_10 = pygame.image.load('assets/sprites/health/10.png')
        self.healthbar_11 = pygame.image.load('assets/sprites/health/11.png')
        self.healthbar_12 = pygame.image.load('assets/sprites/health/12.png')
        self.healthbar_13 = pygame.image.load('assets/sprites/health/13.png')
        self.healthbar_14 = pygame.image.load('assets/sprites/health/14.png')
        self.healthbar_15 = pygame.image.load('assets/sprites/health/15.png')
        self.healthbar_16 = pygame.image.load('assets/sprites/health/16.png')
        self.healthbar_17 = pygame.image.load('assets/sprites/health/17.png')
        self.healthbar_18 = pygame.image.load('assets/sprites/health/18.png')
        self.healthbar_19 = pygame.image.load('assets/sprites/health/19.png')
        self.healthbar_20 = pygame.image.load('assets/sprites/health/20.png')

    #HUD For Player
    def draw_player_health(self, x, y, percent, playerid):

        if percent < 0:
            percent = 0

        if percent > 0.95:
            health_icon = self.healthbar_20
        elif percent > 0.9:
            health_icon = self.healthbar_19
        elif percent > 0.85:
            health_icon = self.healthbar_18
        elif percent > 0.8:
            health_icon = self.healthbar_17
        elif percent > 0.75:
            health_icon = self.healthbar_16
        elif percent > 0.7:
            health_icon = self.healthbar_15
        elif percent > 0.65:
            health_icon = self.healthbar_14
        elif percent > 0.6:
            health_icon = self.healthbar_13
        elif percent > 0.55:
            health_icon = self.healthbar_12
        elif percent > 0.5:
            health_icon = self.healthbar_11
        elif percent > 0.45:
            health_icon = self.healthbar_10
        elif percent > 0.4:
            health_icon = self.healthbar_9
        elif percent > 0.35:
            health_icon = self.healthbar_8
        elif percent > 0.3:
            health_icon = self.healthbar_7
        elif percent > 0.25:
            health_icon = self.healthbar_6
        elif percent > 0.2:
            health_icon = self.healthbar_5
        elif percent > 0.15:
            health_icon = self.healthbar_4
        elif percent > 0.1:
            health_icon = self.healthbar_3
        elif percent > 0.05:
            health_icon = self.healthbar_2
        elif percent > 0:
            health_icon = self.healthbar_1
        else:
            health_icon = self.healthbar_0

        health_scaled = pygame.transform.scale(health_icon, (170, 44))
        if playerid == 2:
            health_scaled = pygame.transform.flip(health_scaled, True, False)
        screen.blit(health_scaled,(x, y))

    #Initialize variables and sets up tilemap
    def new(self):
        self.score = 0
        self.score2 = 0
        self.playersalive = 0
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.invis_wall = pygame.sprite.Group()
        self.win_game = pygame.sprite.Group()
        self.mob_small = pygame.sprite.Group()
        self.mob_bullets = pygame.sprite.Group()
        self.mob_flying = pygame.sprite.Group()
        self.mob_charge = pygame.sprite.Group()
        self.mob_big = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.spike = pygame.sprite.Group()
        self.map = TiledMap('assets/levels/level1.tmx')
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.fall_death = pygame.sprite.Group()
        self.boundary = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bullets2 = pygame.sprite.Group()
        for tile_object in self.map.tmxdata.objects:    #FOR loop to render all objects and bitmap graphics in the tiled map (TMX)
            obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'player2':
                self.player2 = Player2(self, tile_object.x, tile_object.y)
            if tile_object.name == 'enemy':
                Mob_small(self, obj_center.x, obj_center.y)
            if tile_object.name == 'flying':
                Mob_flying(self, obj_center.x, obj_center.y)
            if tile_object.name == 'charge':
                Mob_charge(self,obj_center.x, obj_center.y)
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
            screen.blit(textinput.get_surface(), (10, 10))
            pygame.display.flip()
            fps.tick(60)

        self.all_sprites.update()
        if self.player.alive and self.player2.alive:
            self.camera.update(self.player)
        elif self.player.alive and not self.player2.alive:
            self.camera.update(self.player)
        elif not self.player.alive and self.player2.alive:
            self.camera.update(self.player2)

        if self.player.collision:
            hits = pygame.sprite.spritecollide(self.player, self.items, False, collide_hit_rect)
            for hit in hits:
                if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                    hit.kill()
                    self.health.play()
                    self.player.add_health(20)
                elif hit.type == 'coin':
                    hit.kill()
                    self.coin.play()
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
                    self.player.vel = pygame.math.Vector2(-5, -10)
                elif self.player.jumping and self.player.vel.x < 0:
                    self.player.pos.x += 10
                    self.player.vel = pygame.math.Vector2(5, -10)

                if self.player.vel.y < -5:
                    self.player.vel.y = -5

                self.player.health -= 5
                if self.player.health <= 0:
                    self.player.alive = False
                self.player_hurt.play()
                self.player.hit()

            hits = pygame.sprite.spritecollide(self.player, self.mob_small, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt.play()
                self.score -= 5
                self.player.health -= 10
                if self.player.health <= 0:
                    self.player.alive = False
                if self.player.alive:
                    self.player.hit()
                self.player.knockback(hit)

            hits = pygame.sprite.spritecollide(self.player, self.mob_big, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt.play()
                self.score -= 5
                self.player.health -= 20
                if self.player.health <= 0:
                    self.player.alive = False
                if self.player.alive:
                    self.player.hit()
                self.player.knockback(hit)

            hits = pygame.sprite.spritecollide(self.player, self.mob_flying, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt.play()
                self.score -= 5
                self.player.health -= 10
                if self.player.health <= 0:
                    self.player.alive = False
                self.player.hit()
                self.player.knockback(hit)

            hits = pygame.sprite.spritecollide(self.player, self.mob_charge, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt.play()
                self.score -= 5
                self.player.health -= 10
                if self.player.health <= 0:
                    self.player.alive = False
                if hit.charging:
                    self.player.knockback_charge(hit)
                else:
                    self.player.knockback(hit)
                self.player.hit()

            hits = pygame.sprite.spritecollide(self.player, self.mob_bullets, False, collide_hit_rect)
            for hit in hits:
                hit.kill()
                self.player_hurt.play()
                self.score -= 1
                self.player.health -= 10
                if self.player.health <= 0:
                    self.player.alive = False
                if self.player.alive:
                    self.player.hit()


        if self.player2.collision:
            hits = pygame.sprite.spritecollide(self.player2, self.items, False, collide_hit_rect)
            for hit in hits:
                if hit.type == 'health' and self.player2.health < PLAYER_HEALTH:
                    hit.kill()
                    self.health.play()
                    self.player2.add_health(20)
                elif hit.type == 'coin':
                    hit.kill()
                    self.coin.play()
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
                    self.player2.vel = pygame.math.Vector2(-5, -10)
                elif self.player2.jumping and self.player2.vel.x < 0:
                    self.player2.pos.x += 10
                    self.player2.vel = pygame.math.Vector2(5, -10)

                if self.player2.vel.y < -5:
                    self.player2.vel.y = -5

                self.player2.health -= 5
                if self.player2.health <= 0:
                    self.player2.alive = False
                self.player_hurt.play()
                self.player2.hit()

            hits = pygame.sprite.spritecollide(self.player2, self.mob_small, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt.play()
                self.score2 -= 5
                self.player2.health -= 10
                if self.player2.health <= 0:
                    self.player2.alive = False
                if self.player2.alive:
                    self.player2.hit()
                self.player2.knockback(hit)

            hits = pygame.sprite.spritecollide(self.player2, self.mob_big, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt.play()
                self.score2 -= 5
                self.player2.health -= 20
                if self.player2.health <= 0:
                    self.player2.alive = False
                if self.player2.alive:
                    self.player2.hit()
                self.player2.knockback(hit)

            hits = pygame.sprite.spritecollide(self.player2, self.mob_flying, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt.play()
                self.score2 -= 5
                self.player2.health -= 10
                if self.player2.health <= 0:
                    self.player2.alive = False
                if self.player2.alive:
                    self.player2.hit()
                self.player2.knockback(hit)

            hits = pygame.sprite.spritecollide(self.player2, self.mob_charge, False, collide_hit_rect)
            for hit in hits:
                self.player_hurt.play()
                self.score2 -= 5
                self.player2.health -= 10
                if self.player2.health <= 0:
                    self.player2.alive = False
                if hit.charging:
                    self.player2.knockback_charge(hit)
                else:
                    self.player2.knockback(hit)
                self.player2.hit()

            hits = pygame.sprite.spritecollide(self.player2, self.mob_bullets, False, collide_hit_rect)
            for hit in hits:
                hit.kill()
                self.player_hurt.play()
                self.score2 -= 1
                self.player2.health -= 10
                if self.player2.health <= 0:
                    self.player2.alive = False
                if self.player2.alive:
                    self.player2.hit()

        #Bullet Collisions to Mobs
        hits = pygame.sprite.groupcollide(self.mob_small, self.bullets2, False, True)
        for hit in hits:
            self.enemy_hurt.play()
            self.score2 += 1
            hit.health -= 10
            if hit.health <= 0:
                hit.kill()
                self.score2 += 10
                chance = random.randint(0,9)
                if chance == 0:
                    self.morph.play()
                    Mob_Big(self, hit.pos.x, hit.pos.y, hit.facing)
                else:
                    pass

        hits = pygame.sprite.groupcollide(self.mob_small, self.bullets, False, True)
        for hit in hits:
            self.enemy_hurt.play()
            self.score += 1
            hit.health -= 10
            if hit.health <= 0:
                hit.kill()
                self.score += 10
                chance = random.randint(0,9)
                if chance == 0:
                    self.morph.play()
                    Mob_Big(self, hit.pos.x, hit.pos.y, hit.facing)
                else:
                    pass

        hits = pygame.sprite.groupcollide(self.mob_flying, self.bullets, False, True)
        for hit in hits:
            self.enemy_hurt.play()
            self.score += 2
            hit.health -= 10
            if hit.health <= 0:
                hit.kill()
                self.score += 15

        hits = pygame.sprite.groupcollide(self.mob_flying, self.bullets2, False, True)
        for hit in hits:
            self.enemy_hurt.play()
            self.score2 += 2
            hit.health -= 10
            if hit.health <= 0:
                hit.kill()
                self.score2 += 15

        hits = pygame.sprite.groupcollide(self.mob_big, self.bullets2, False, True)
        for hit in hits:
            self.enemy_hurt.play()
            self.score2 += 3
            hit.health -= 10
            if hit.health <= 0:
                hit.kill()
                self.score2 += 30

        hits = pygame.sprite.groupcollide(self.mob_big, self.bullets, False, True)
        for hit in hits:
            self.enemy_hurt.play()
            self.score += 3
            hit.health -= 10
            if hit.health <= 0:
                hit.kill()
                self.score += 30

        hits = pygame.sprite.groupcollide(self.mob_charge, self.bullets, False, True)
        for hit in hits:
            self.enemy_hurt.play()
            self.score += 5
            hit.health -= 10
            if hit.health <= 0:
                hit.kill()
                self.score += 40

        hits = pygame.sprite.groupcollide(self.mob_charge, self.bullets2, False, True)
        for hit in hits:
            self.enemy_hurt.play()
            self.score2 += 5
            hit.health -= 10
            if hit.health <= 0:
                hit.kill()
                self.score2 += 40

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

        #HUD
        self.draw_player_health(5, 5, self.player.health / PLAYER_HEALTH, 1)
        self.draw_player_health(337, 5, self.player2.health / PLAYER_HEALTH, 2)

        #Display player 1's score
        self.draw_text("SCORE:" + str(self.score), self.pixel_font,15, (255, 255, 255), 100, 41, align="center")

        #Display player 2's score
        self.draw_text("SCORE:" + str(self.score2), self.pixel_font,15, (255, 255, 255), 410, 41, align="center")

        #Enemy counter
        self.draw_text('ALIENS: {}'.format(len(self.mob_small) + len(self.mob_big) + len(self.mob_flying) + len(self.mob_charge)), self.pixel_font, 15, (255, 255, 255), WIDTH/2, 15, align="center")

        if self.paused:
            self.display = pygame.Surface((self.map.width, self.map.height))
            self.draw_pause_text("Player 1: Use WASD to move and Space to shoot", self.pixel_font,15, (255, 255, 255), WIDTH/2, HEIGHT/2-90, align="center")
            self.draw_pause_text("Player 2: Use Arrow keys to move and Right Enter to shoot", self.pixel_font,15, (255, 255, 255), WIDTH/2, HEIGHT/2-70, align="center")
            self.draw_pause_text("PAUSE", self.pixel_font,65, (255, 255, 255), WIDTH/2, HEIGHT/2, align="center")
            self.draw_pause_text("Press P to unpause", self.pixel_font,15, (255, 255, 255), WIDTH/2, HEIGHT/2+25, align="center")
            self.draw_pause_text("Press ESC to go back to main menu", self.pixel_font,15, (255, 255, 255), WIDTH/2, HEIGHT/2+90, align="center")


        pygame.display.flip()

    def _circlepoints(self,r):
        r = int(round(r))
        x, y, e = r, 0, 1 - r
        points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        return points

    def getsurf(self,pause_text,color):
        return self.font.render(pause_text, True, color).convert_alpha()

    def draw_text(self, text, font_name, size, color, x, y, align="center"):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if align == "center":
            text_rect.center = (x, y)

        screen.blit(text_surface, text_rect)

    def draw_pause_text(self, text, font_name, size, color, x, y, align="center"):
        font = pygame.font.Font(font_name, size)

        self.osurf = font.render(text, True, (0, 0, 0, 0))
        self.tsurf = font.render(text, True, (255, 255, 255, 0))
        self.osurf_rect = self.osurf.get_rect()
        self.tsurf_rect = self.tsurf.get_rect()
        if align == "center":
            self.osurf_rect.center = (x, y)
            self.tsurf_rect.center = (x, y)

        for offset, blendmax in [(0, False), (300, True)]:
            for dx, dy in self._circlepoints(self.opx):
                if blendmax:
                    screen.blit(self.osurf, (dx + x, dy + y), None, pygame.BLEND_RGBA_MAX)
                else:
                    screen.blit(self.osurf, (dx + x, dy + y))
            screen.blit(self.tsurf, (x, y))

    #Key presses
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                if event.key == pygame.K_UP:
                    self.player2.jump()
                if event.key == pygame.K_w:
                    self.player.jump()
                if event.key == pygame.K_p:
                    self.paused = not self.paused

    def you_win(self):
        enter = True
        while enter:
            player1name = pygame_textinput.TextInput(font_family = "assets/8bit.ttf", antialias = False)
            enter1 = True
            while enter1:
                screen.fill((60,179,113))
                events = pygame.event.get()
                self.draw_text("enter player 1 name", self.pixel_font, 35, (255, 255, 255), int(WIDTH/2), int(HEIGHT/2)-50, align="center")
                screen.blit(player1name.get_surface(), (int(WIDTH/2)-35, int(HEIGHT/2)))

                if player1name.update(events):
                    pass

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            enter1 = False

                pygame.display.flip()
                fps.tick(60)

            player2name = pygame_textinput.TextInput(font_family = "assets/8bit.ttf", antialias = False)
            enter2 = True
            while enter2:
                screen.fill((60,179,113))
                events = pygame.event.get()
                self.draw_text("enter player 2 name", self.pixel_font, 35, (255, 255, 255), int(WIDTH/2), int(HEIGHT/2)-50, align="center")
                screen.blit(player2name.get_surface(), (int(WIDTH/2)-35, int(HEIGHT/2)))

                if player2name.update(events):
                    pass

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            enter2 = False

                pygame.display.flip()
                fps.tick(60)

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
                f = open("assets/highscores.txt", "a")
                f.write(str(NAME) + ' ' + str(SCORE) + '\n')
                f.close()

        self.draw_text("You Win!", self.pixel_font, 80, (255, 255, 0), WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("press ENTER to restart", self.pixel_font, 30, (255, 255, 255),WIDTH / 2, HEIGHT * 3 / 4.5, align="center")
        self.draw_text("or ESCAPE to go to main menu", self.pixel_font, 30, (255, 255, 255),WIDTH / 2, HEIGHT * 3 / 4, align="center")

        self.draw_text(player1name.get_text(), self.pixel_font,25, (255, 255, 255), WIDTH/3, 40, align="center")
        self.draw_text(str(self.score), self.pixel_font,25, (255, 255, 255), WIDTH/3, 60, align="center")

        self.draw_text(player2name.get_text(), self.pixel_font,25, (255, 255, 255), WIDTH/1.5, 40, align="center")
        self.draw_text(str(self.score2), self.pixel_font,25, (255, 255, 255), WIDTH/1.5, 60, align="center")

        pygame.display.flip()
        self.wait_for_key()

    def game_over(self):
        enter = True
        while enter:
            player1name = pygame_textinput.TextInput(font_family = "assets/8bit.ttf", antialias = False)
            enter1 = True
            while enter1:
                screen.fill((110, 0, 0))
                events = pygame.event.get()
                self.draw_text("enter player 1 name", self.pixel_font, 35, (255, 255, 255), int(WIDTH/2), int(HEIGHT/2)-50, align="center")
                screen.blit(player1name.get_surface(), (int(WIDTH/2)-35, int(HEIGHT/2)))

                if player1name.update(events):
                    pass

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            enter1 = False

                pygame.display.flip()
                fps.tick(60)

            player2name = pygame_textinput.TextInput(font_family = "assets/8bit.ttf", antialias = False)
            enter2 = True
            while enter2:
                screen.fill((110, 0, 0))
                events = pygame.event.get()
                self.draw_text("enter player 2 name", self.pixel_font, 35, (255, 255, 255), int(WIDTH/2), int(HEIGHT/2)-50, align="center")
                screen.blit(player2name.get_surface(), (int(WIDTH/2)-35, int(HEIGHT/2)))

                if player2name.update(events):
                    pass

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            enter2 = False

                pygame.display.flip()
                fps.tick(60)
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
                f = open("assets/highscores.txt", "a")
                f.write(str(NAME) + ' ' + str(SCORE) + '\n')
                f.close()

        self.draw_text("GAME OVER!", self.pixel_font, 80, (255, 0, 0),WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("press ENTER to restart", self.pixel_font, 30, (255, 255, 255),WIDTH / 2, HEIGHT * 3 / 4.5, align="center")
        self.draw_text("or ESCAPE to go to main menu", self.pixel_font, 30, (255, 255, 255),WIDTH / 2, HEIGHT * 3 / 4, align="center")

        self.draw_text(player1name.get_text(), self.pixel_font,25, (255, 255, 255), WIDTH/3, 40, align="center")
        self.draw_text(str(self.score), self.pixel_font,25, (255, 255, 255), WIDTH/3, 60, align="center")

        self.draw_text(player2name.get_text(), self.pixel_font,25, (255, 255, 255), WIDTH/1.5, 40, align="center")
        self.draw_text(str(self.score2), self.pixel_font,25, (255, 255, 255), WIDTH/1.5, 60, align="center")

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

menu()
