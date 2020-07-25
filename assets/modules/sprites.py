#Created and maintained by Mahi Rahman and Son Tran

import pygame
import random
from assets.modules.tilemap import collide_hit_rect
from os import path
import pytweening as tween
from itertools import chain
PLAYER_HEALTH = 200

def wallCollide(sprite, group, direction):
    if direction == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if direction == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, direction, playernum):
        self.groups = game.all_sprites, game.__dict__['bullets%d' % playernum]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if direction == -1:
            self.image = game.bullet_player
        else:
            self.image = pygame.transform.rotate(game.bullet_player, 180)
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 17, 8)
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(pos)
        self.rect.center = pos
        self.vel = pygame.math.Vector2(direction * 7, 0)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > 1000:
            self.kill()
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()

class MobBullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, direction, angle):
        self.groups = game.all_sprites, game.mob_bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_mob
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 17, 8)
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(pos)
        self.rect.center = pos
        self.vel = direction * 2
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > 5000:
            self.kill()
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, playerid, left, right, shoot):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        self.current_frame = 0
        self.last_update = 0
        self.death_anim = 0
        self.death_time = 0
        self.last_shot = 0
        
        self.playerid = playerid
        self.loadImages(self.playerid)
        self.image = self.idle_frame[0] 
        
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 30, 45)
        self.hit_rect.center = self.rect.center
        
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(x, y)
        
        self.health = PLAYER_HEALTH
        self.acc = pygame.math.Vector2(0, 0)
        self.direction = 1 #1 == left, -1 == right

        self.left = left
        self.right = right
        self.shoot = shoot

        self.control = True
        self.alive = True
        self.collision = True
        self.running = False
        self.jumping = False
        self.shooting = False
        self.damaged = False

    def loadImages(self, playerid):
        self.idle_frame = []
        self.shoot_frame = []
        self.death_frame = []
        self.run_frame = []
        self.jump_frame = []

        i = 1
        while i <= 4:     
            self.idle_frame.append(pygame.transform.scale(pygame.image.load('assets/sprites/player/' + str(playerid) + '/idle/idle_' + str(i) + '.png').convert_alpha(), (64, 64)))
            self.shoot_frame.append(pygame.transform.scale(pygame.image.load('assets/sprites/player/' + str(playerid) + '/shoot/shoot_' + str(i) + '.png').convert_alpha(), (64, 64)))
            i += 1

        i = 1
        while i <= 8:
            self.death_frame.append(pygame.transform.scale(pygame.image.load('assets/sprites/player/' + str(playerid) + '/death/death_' + str(i) + '.png').convert_alpha(), (64, 64)))
            i += 1

        i = 1
        while i <= 14:
            self.run_frame.append(pygame.transform.scale(pygame.image.load('assets/sprites/player/' + str(playerid) + '/run/run_' + str(i) + '.png').convert_alpha(), (64, 64)))
            i += 1

        self.jump_frame.append(pygame.transform.scale(pygame.image.load('assets/sprites/player/' + str(playerid) + '/jump/jump.png').convert_alpha(), (64, 64)))

    def setKeys(self, left, right, shoot):
        if self.control:
            keys = pygame.key.get_pressed()
            
            if keys[left]:
                self.acc.x = -0.5
                self.direction = -1

            if keys[right]:
                self.acc.x = 0.5
                self.direction = 1
                
            #if keys[leap]:
                #self.jump()

##            for event in pygame.event.get():
##                if event.type == pygame.QUIT:
##                    self.quit()
##                if event.type == pygame.KEYDOWN:
##                  if event.key == leap:
##                     self.jump()
                
            if keys[shoot]:
                currenttick = pygame.time.get_ticks()
                if currenttick - self.last_shot > 150:
                    self.last_shot = currenttick
                    if self.running:
                        pos = self.pos + pygame.math.Vector2(32 * self.direction, 5)
                    else:
                        pos = self.pos + pygame.math.Vector2(32 * self.direction, -10)
                    Bullet(self.game, pos, self.direction, self.playerid)
                    self.game.shoot.play()
                    self.shooting = True

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain([i for i in range(40, 255, 25)] * 2)

    def knockback(self, hit):
        if self.jumping:
            if self.direction == 1:
                self.vel += pygame.math.Vector2(-8, -5)
            else:
                self.vel += pygame.math.Vector2(8, -5)

            if self.vel.y < -5:
                self.vel.y = -5

        elif hit.direction == -1 and self.direction == 1:
            self.pos += pygame.math.Vector2(-30, 0)
            self.vel += pygame.math.Vector2(-8, -5)
            
        elif hit.direction == -1 and self.direction == -1 and not self.running:
            self.pos += pygame.math.Vector2(-30, 0)
            self.vel += pygame.math.Vector2(-8, -5)
            
        elif hit.direction == 1 and self.direction == 1 and self.running:
            self.pos += pygame.math.Vector2(-30, 0)
            self.vel += pygame.math.Vector2(-8, -5)

        elif hit.direction == 1 and self.direction == -1:
            self.pos += pygame.math.Vector2(30, 0)
            self.vel += pygame.math.Vector2(8, -5)
            
        elif hit.direction == 1 and self.direction == 1 and not self.running:
            self.pos += pygame.math.Vector2(30, 0)
            self.vel += pygame.math.Vector2(8, -5)

        elif hit.direction == -1 and self.direction == -1 and self.running:
            self.pos += pygame.math.Vector2(30, 0)
            self.vel += pygame.math.Vector2(8, -5)

    def update(self):
        self.animate()
        self.acc = pygame.math.Vector2(0, 0.5)
        self.setKeys(self.left, self.right, self.shoot)
        
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags = pygame.BLEND_RGBA_MULT)
            except:
                self.damaged = False
                self.loadImages(self.playerid)

        self.rect = self.image.get_rect()
        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        
        if abs(self.vel.x) < 0.2:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        wallCollide(self, self.game.walls, 'x')
        wallCollide(self, self.game.boundary, 'x')
        self.hit_rect.centery = self.pos.y
        wallCollide(self, self.game.walls, 'y')
        wallCollide(self, self.game.boundary, 'y')
        self.rect.center = self.hit_rect.center
        self.death()

    def addHealth(self, amount):

        #Takes <amount> as a parameter which indicates the amount of health player will gain.
        #Checks if player health does not go over the maximum health.
        
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def animate(self):
        currenttick = pygame.time.get_ticks()

        if self.vel.x != 0:
            self.running = True
        else:
            self.running = False

        if self.vel.y != 0:
            self.jumping = True
        else:
            self.jumping = False

        if self.alive:
            if not self.running and not self.shooting:
                
                if currenttick - self.last_update > 350:
                    self.last_update = currenttick
                    
                    if self.direction == -1:
                        self.current_frame = (self.current_frame + 1) % len(self.idle_frame)
                        self.image = self.idle_frame[self.current_frame]
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.idle_frame)
                        self.image = pygame.transform.flip(self.idle_frame[self.current_frame], True, False)
                    self.rect = self.image.get_rect()

            elif self.running:
                if currenttick - self.last_update > 200:
                    self.last_update = currenttick
                    if self.direction == -1:
                        self.current_frame = (self.current_frame + 1) % len(self.run_frame)
                        self.image = self.run_frame[self.current_frame]
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.run_frame)
                        self.image = pygame.transform.flip(self.run_frame[self.current_frame], True, False)
                    self.rect = self.image.get_rect()

            elif self.shooting:
                if currenttick - self.last_update > 150:
                    self.last_update = currenttick
                    if self.direction == -1:
                        self.current_frame = (self.current_frame + 1) % len(self.shoot_frame)
                        self.image = self.shoot_frame[self.current_frame]
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.shoot_frame)
                        self.image = pygame.transform.flip(self.shoot_frame[self.current_frame], True, False)
                    self.rect = self.image.get_rect()
                self.shooting = False

            if self.jumping:
                if currenttick - self.last_update > 150:
                    self.last_update = currenttick
                    if self.direction == -1:
                        self.current_frame = (self.current_frame + 1) % len(self.jump_frame)
                        self.image = self.jump_frame[self.current_frame]
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.jump_frame)
                        self.image = pygame.transform.flip(self.jump_frame[self.current_frame], True, False)

    def jump(self):
        if self.alive:
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.game.__dict__['jump_%d' % self.playerid].play()
                self.vel.y = -8.5

    def death(self):
        if not self.alive:
            self.control = False
            self.collision = False
            currenttick = pygame.time.get_ticks()
            if currenttick - self.death_time > 150:
                self.death_time = currenttick
                if self.direction == -1:
                    self.death_anim = (self.death_anim + 1) % len(self.death_frame)
                    self.image = self.death_frame[self.death_anim]
                else:
                    self.death_anim = (self.death_anim + 1) % len(self.death_frame)
                    self.image = pygame.transform.flip(self.death_frame[self.death_anim], True, False)
                self.rect = self.image.get_rect()

            if self.death_anim >= 7:
                self.hit_rect = pygame.Rect(0, 0, 0, 0)
                self.shooting = False
                self.game.playersalive += 1
                self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y, mobtype, mobhealth, spritex, spritey, framespeed, acceleration, detect_wall_range):
        self.mobtype = mobtype
        self.groups = game.all_sprites, game.__dict__['mob_%s' % self.mobtype]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        self.current_frame = 0
        self.last_update = 0
        self.spritex = spritex
        self.spritey = spritey
        self.acceleration = acceleration
        self.detect_wall_range = detect_wall_range

        self.loadImages()
        self.image = self.walk_frame[0]
        self.health_bars = self.image.copy()
        self.rect = self.image.get_rect()
        self.framespeed = framespeed
        self.hit_rect = pygame.Rect(0, 0, 24, 36).copy()
        self.hit_rect.center = self.rect.center
        
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        
        self.rect.center = self.pos
        self.health = mobhealth
        self.HEALTH = mobhealth
        self.direction = 1

    def loadImages(self):
        self.walk_frame = []

        i = 1
        while i <= 4:
            self.walk_frame.append(pygame.transform.scale(pygame.image.load('assets/sprites/enemy/' + self.mobtype + '/run_' + str(i) + '.png').convert_alpha(), (self.spritex, self.spritey)))
            i += 1

    def animate(self):
        currenttick = pygame.time.get_ticks()

        if currenttick - self.last_update > self.framespeed:
            self.last_update = currenttick
            if self.direction == -1:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame)
                self.image = self.walk_frame[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame)
                self.image = pygame.transform.flip(self.walk_frame[self.current_frame], True, False)
            self.rect = self.image.get_rect()

    def update(self):
        self.drawHealth()
        self.animate()
        self.position()
        self.moving()

        self.hit_rect.centerx = self.pos.x
        wallCollide(self, self.game.invis_wall, 'x')
        self.hit_rect.centery = self.pos.y
        wallCollide(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def position(self):
        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

    def moving(self):
        self.acc = pygame.math.Vector2(self.acceleration * self.direction, 0.5)
        self.rect.centerx += self.detect_wall_range * self.direction
        hits = pygame.sprite.spritecollide(self, self.game.invis_wall, False)
        self.rect.centerx -= self.detect_wall_range * self.direction
        if hits:
            self.direction = self.direction * - 1

    def drawHealth(self):
        if self.health > int(self.HEALTH/1.5):
            self.col = (0, 255, 0)
        elif self.health > int(self.HEALTH/3):
            self.col = (255, 255, 0)
        else:
            self.col = (255, 0, 0)
        width = int(self.rect.width * self.health / self.HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 2)
        if self.health < self.HEALTH:
            pygame.draw.rect(self.image, self.col, self.health_bar)
            self.loadImages()

class MobFlying(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob_flying
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.loadImages()
        self.image = self.walk_frame[0]
        self.health_bars = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 24, 30).copy()
        self.hit_rect.center = self.rect.center
        
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        
        self.rect.center = self.pos
        self.rot = 0
        self.health = 150
        self.direction = 1
        self.last_shot = 0
        self.wobble = 0
        
        self.target = game.player
        self.target2 = game.player2
        self.fix = True

    def loadImages(self):
        self.walk_frame = []

        i = 1
        while i <= 4:
            self.walk_frame.append(pygame.transform.scale(pygame.image.load('assets/sprites/enemy/med/run_' + str(i) + '.png').convert_alpha(), (24, 36)))
            i += 1

    def animate(self):
        currenttick = pygame.time.get_ticks()

        if currenttick - self.last_update > 200:
            self.last_update = currenttick
            if self.direction == -1:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame)
                self.image = self.walk_frame[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame)
                self.image = pygame.transform.flip(self.walk_frame[self.current_frame], True, False)
            self.rect = self.image.get_rect()

    def update(self):
        self.drawHealth()
        self.animate()
        target_dist = self.target.pos - self.pos
        target_dist2 = self.target2.pos - self.pos

        if target_dist.length_squared() < 150**2 and target_dist2.length_squared() < 150**2:
            if self.target.alive and self.target2.alive:
                if target_dist.length_squared() < target_dist2.length_squared():
                    self.chase("1")
                elif target_dist2.length_squared() < target_dist.length_squared():
                    self.chase("2")
            elif self.target.alive and not self.target2.alive:
                self.chase("1")
            elif not self.target.alive and self.target2.alive:
                self.chase("2")

        elif target_dist.length_squared() < 150**2 and target_dist2.length_squared() > 150**2:
            if self.target.alive:
                self.chase("1")
            else:
                self.moving()
                self.position()

        elif target_dist2.length_squared() < 150**2 and target_dist.length_squared() > 150**2:
            if self.target2.alive:
                self.chase("2")
            else:
                self.moving()
                self.position()

        else:
            self.moving()
            self.position()

        self.hit_rect.centerx = self.pos.x
        wallCollide(self, self.game.invis_wall, 'x')
        self.hit_rect.centery = self.pos.y
        wallCollide(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def position(self):
        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

    def chase(self, player_num):
        if player_num == "1":
            self.rot = (self.game.player.pos - self.pos).angle_to(pygame.math.Vector2(1, 0))
            if self.game.player.pos.x - self.pos.x < 0:
                self.direction = -1
            else:
                self.direction = 1
        else:
            self.rot = (self.game.player2.pos - self.pos).angle_to(pygame.math.Vector2(1, 0))
            if self.game.player2.pos.x - self.pos.x < 0:
                self.direction = -1
            else:
                self.direction = 1

        self.rect.center = self.pos
        self.acc = pygame.math.Vector2(50, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.shoot()
        self.fix = False

    def moving(self):
        self.rot = 0
        if not self.fix:
            self.vel.x = 0
            self.fix = True

        if self.vel.y != 0.2 and self.vel.y != -0.2:
            self.vel.y = 0.2
        currenttick = pygame.time.get_ticks()

        if currenttick - self.wobble > 750 and self.vel.y == -0.2:
            self.wobble = currenttick
            self.vel.y = 0.2
        elif currenttick - self.wobble > 750 and self.vel.y == 0.2:
            self.wobble = currenttick
            self.vel.y = -0.2

        self.acc = pygame.math.Vector2(0.15 * self.direction, 0)

        self.rect.centerx += 2 * self.direction
        hits = pygame.sprite.spritecollide(self, self.game.invis_wall, False)
        self.rect.centerx -= 2 * self.direction
        if hits:
            self.direction = self.direction * -1

    def drawHealth(self):
        if self.health > 120:
            self.col = (0, 255, 0)
        elif self.health > 50:
            self.col = (255, 255, 0)
        else:
            self.col = (255, 0, 0)
        width = int(self.rect.width * self.health / 150)
        self.health_bar = pygame.Rect(0, 0, width, 2)
        if self.health < 150:
            pygame.draw.rect(self.image, self.col, self.health_bar)
            self.loadImages()

    def shoot(self):
        currenttick = pygame.time.get_ticks()
        if currenttick - self.last_shot > 2500:
            self.last_shot = currenttick
            MobBullet(self.game, self.pos, pygame.math.Vector2(1, 0), 0)
            MobBullet(self.game, self.pos, pygame.math.Vector2(0, -1), 90)
            MobBullet(self.game, self.pos, pygame.math.Vector2(-1, 0), 180)
            MobBullet(self.game, self.pos, pygame.math.Vector2(0, 1), 270)

class MobCharge(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob_charge
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.loadImages()
        self.image = self.walk_frame[0]
        self.health_bars = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 24, 30).copy()
        self.hit_rect.center = self.rect.center
        
        self.pos = pygame.math.Vector2(x, y)
        self.rect.center = self.pos
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        
        self.target = game.player
        self.target2 = game.player2

        self.charging = False
        self.chargesequence = False
        
        self.health = 100
        self.detected = 0
        self.direction = 1
        self.charge_time = 0
        self.round = 1

    def loadImages(self):
        self.walk_frame = []

        i = 1
        while i <= 4:           
            self.walk_frame.append(pygame.transform.scale(pygame.image.load('assets/sprites/enemy/low/run_' + str(i) + '.png').convert_alpha(), (24, 36)))
            i += 1

    def animate(self):
        currenttick = pygame.time.get_ticks()
        if self.charging:
            anim_speed = 50
        else:
            anim_speed = 200

        if currenttick - self.last_update > anim_speed:
            self.last_update = currenttick
            if self.direction == -1:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame)
                self.image = self.walk_frame[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame)
                self.image = pygame.transform.flip(self.walk_frame[self.current_frame], True, False)
            self.rect = self.image.get_rect()

    def update(self):
        self.drawHealth()
        target_dist = self.target.pos - self.pos
        target2_dist = self.target2.pos - self.pos

        if not self.charging and self.detected == 0 and not self.chargesequence:
            self.animate()
            self.position()
            self.moving(0.2)

        if target_dist.length_squared() < 150**2 and not self.charging and self.detected == 0 and not self.chargesequence:
            self.detected = 1

        elif target2_dist.length_squared() < 150**2 and not self.charging and self.detected == 0 and not self.chargesequence:
            self.detected = 1

        if self.detected == 1 and not self.charging and not self.chargesequence:
            self.step = 0
            self.charge_counter = 0

            if self.target.pos.x - self.pos.x <= 0:
                self.direction = -1
            else:
                self.direction = 1

            self.chargesequence = True

        elif self.detected == 1 and not self.charging and self.chargesequence:
            time = pygame.time.get_ticks()
            self.animate()
            self.vel.x = 0
            if self.charge_counter != 3:
                self.position()
                self.acc.x = 0
                if time - self.step > 200:
                    self.chargeMotion()
                    self.step = time
                    self.charge_counter += 1
            else:
                self.charge_counter = 0
                self.charging = True

        elif self.detected == 1 and self.charging and self.chargesequence:
            self.charge_time = pygame.time.get_ticks()
            if self.charge_time <= int(10000*self.round):
                self.animate()
                self.position()
                self.moving(0.5)
            else:
                self.round += 1
                self.detected = 0
                self.chargesequence = False
                self.charging = False

        self.hit_rect.centerx = self.pos.x
        wallCollide(self, self.game.invis_wall, 'x')
        self.hit_rect.centery = self.pos.y
        wallCollide(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def position(self):
        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

    def chargeMotion(self):
        self.acc = pygame.math.Vector2(-0.5 * self.direction, 0.5)
        self.rect.centerx -=2 * self.direction
        hits = pygame.sprite.spritecollide(self, self.game.invis_wall, False)
        self.rect.centerx +=2 * self.direction
        if hits:
            self.acc = pygame.math.Vector2(0, 0.5)

    def moving(self, acceleration):
        self.acc = pygame.math.Vector2(acceleration * self.direction, 0.5)
        self.rect.centerx += 2 * self.direction
        hits = pygame.sprite.spritecollide(self, self.game.invis_wall, False)
        self.rect.centerx -= 2 * self.direction
        if hits:
            self.direction = self.direction * -1

    def drawHealth(self):
        if self.health > 60:
            self.col = (0, 255, 0)
        elif self.health > 30:
            self.col = (255, 255, 0)
        else:
            self.col = (255, 0, 0)
        width = int(self.rect.width * self.health / 100)
        self.health_bar = pygame.Rect(0, 0, width, 2)
        if self.health < 100:
            pygame.draw.rect(self.image, self.col, self.health_bar)
            self.loadImages()
            
class TileObject(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h, obj_type):
        self.groups = game.__dict__['%s' % obj_type]
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Item(pygame.sprite.Sprite):
    def __init__(self, game, pos, obj_type):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        self.load_image()
        self.image = self.item_images[obj_type]
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 20, 17)
        self.hit_rect.center = self.rect.center
        
        self.obj_type = obj_type
        self.pos = pos
        self.rect.center = pos
        self.step = 0
        self.direction = 1

    def update(self):
        offset = 5 * (tween.easeInOutSine(self.step / 11) - 0.5)
        self.rect.centery = self.pos.y + offset * self.direction
        self.step += 0.4
        if self.step > 10:
            self.step = 0
            self.direction *= -1

    def load_image(self):
        self.item_images = {}
        self.item_images.update(health = pygame.image.load('assets/images/chicken.png').convert_alpha())
        self.item_images.update(coin = pygame.image.load('assets/images/coin.png').convert_alpha())
