#Created by Mahi Rahman and Son Tran

import pygame
import random
from assets.modules.tilemap import collide_hit_rect
from os import path
import pytweening as tween
from itertools import chain
PLAYER_HEALTH = 200

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if dir == 1:
            self.image = game.bullet_img_R
        else:
            self.image = game.bullet_img_L
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 17, 8)
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(pos)
        self.rect.center = pos
        self.vel = pygame.math.Vector2(dir * 7, 0)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > 1000:
            self.kill()
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()

class Bullet2(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if dir == 1:
            self.image = game.bullet_img_R
        else:
            self.image = game.bullet_img_L
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 17, 8)
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(pos)
        self.rect.center = pos
        self.vel = pygame.math.Vector2(dir * 7, 0)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > 1000:
            self.kill()
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()

class Mob_Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir, angle):
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
        self.vel = dir * 2
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > 5000:
            self.kill()
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.death_anim = 0
        self.control = True
        self.load_images()
        self.image = self.standing_frame_R[0]
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 30, 45)
        self.hit_rect.center = self.rect.center
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(x, y)
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.acc = pygame.math.Vector2(0, 0)
        self.running = False
        self.jumping = False
        self.dir = 1
        self.last_shot = 0
        self.damaged = False
        self.shooting = False
        self.alive = True
        self.collision = True
        self.death_time = 0

    def load_images(self):
        self.standing_frame_R = []
        self.standing_frame_L = []
        self.run_frame_R = []
        self.run_frame_L = []
        self.shoot_frame_R = []
        self.shoot_frame_L = []
        self.death_frame_L = []
        self.death_frame_R = []
        self.jump_frame_L = []
        self.jump_frame_R = []

        i = 1
        while i <= 4:
            frame_R_IDLE = pygame.image.load('assets/sprites/player/1/idle/R_idle_' + str(i) + '.png').convert_alpha()
            frame_L_IDLE = pygame.image.load('assets/sprites/player/1/idle/L_idle_' + str(i) + '.png').convert_alpha()
            frame_R_SHOOT = pygame.image.load('assets/sprites/player/1/shoot/R_shoot_' + str(i) + '.png').convert_alpha()
            frame_L_SHOOT = pygame.image.load('assets/sprites/player/1/shoot/L_shoot_' + str(i) + '.png').convert_alpha()
            frame_R_IDLE = pygame.transform.scale(frame_R_IDLE, (64, 64))
            frame_L_IDLE = pygame.transform.scale(frame_L_IDLE, (64, 64))
            frame_L_SHOOT = pygame.transform.scale(frame_L_SHOOT, (64, 64))
            frame_R_SHOOT = pygame.transform.scale(frame_R_SHOOT, (64, 64))
            i = i + 1
            self.standing_frame_R.append(frame_R_IDLE)
            self.standing_frame_L.append(frame_L_IDLE)
            self.shoot_frame_R.append(frame_R_SHOOT)
            self.shoot_frame_L.append(frame_L_SHOOT)

        i = 1
        while i <= 8:
            frame_L_DEATH = pygame.image.load('assets/sprites/player/1/death/L_death_' + str(i) + '.png').convert_alpha()
            frame_R_DEATH = pygame.image.load('assets/sprites/player/1/death/R_death_' + str(i) + '.png').convert_alpha()
            frame_L_DEATH = pygame.transform.scale(frame_L_DEATH, (64, 64))
            frame_R_DEATH = pygame.transform.scale(frame_R_DEATH, (64, 64))
            i = i + 1
            self.death_frame_L.append(frame_L_DEATH)
            self.death_frame_R.append(frame_R_DEATH)

        i = 1
        while i <= 14:
            frame_R_RUN = pygame.image.load('assets/sprites/player/1/run/R_run_' + str(i) + '.png').convert_alpha()
            frame_L_RUN = pygame.image.load('assets/sprites/player/1/run/L_run_' + str(i) + '.png').convert_alpha()
            frame_R_RUN = pygame.transform.scale(frame_R_RUN, (64, 64))
            frame_L_RUN = pygame.transform.scale(frame_L_RUN, (64, 64))
            i = i + 1
            self.run_frame_R.append(frame_R_RUN)
            self.run_frame_L.append(frame_L_RUN)

        frame = pygame.image.load('assets/sprites/player/1/jump/L_jump.png').convert_alpha()
        frame = pygame.transform.scale(frame, (64, 64))
        self.jump_frame_L.append(frame)

        frame = pygame.image.load('assets/sprites/player/1/jump/R_jump.png').convert_alpha()
        frame = pygame.transform.scale(frame, (64, 64))
        self.jump_frame_R.append(frame)

    def get_keys(self):
        if self.control:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                self.acc.x = 0.5
                self.dir = 1
            if keys[pygame.K_a]:
                self.acc.x = -0.5
                self.dir = -1
            if keys[pygame.K_SPACE]:
                now = pygame.time.get_ticks()
                if now - self.last_shot > 150:
                    self.last_shot = now
                    if self.running:
                        pos = self.pos + pygame.math.Vector2(32 * self.dir, 5)
                    else:
                        pos = self.pos + pygame.math.Vector2(32 * self.dir, -10)
                    Bullet(self.game, pos, self.dir)
                    self.game.shoot.play()
                    self.shooting = True
        else:
            pass

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain([i for i in range(40, 255, 25)] * 2)

    def knockback(self, hit):
        if self.jumping:
            if self.dir == 1:
                self.vel += pygame.math.Vector2(-8, -5)
            else:
                self.vel += pygame.math.Vector2(8, -5)

            if self.vel.y < -5:
                self.vel.y = -5

        elif hit.dir == -1 and self.dir == 1: #dir == 1,-1 is right,left
            self.pos += pygame.math.Vector2(-30, 0)
            self.vel += pygame.math.Vector2(-8, -5)
        elif hit.dir == -1 and self.dir == -1 and not self.running:
            self.pos += pygame.math.Vector2(-30, 0)
            self.vel += pygame.math.Vector2(-8, -5)
        elif hit.dir == 1 and self.dir == 1 and self.running:
            self.pos += pygame.math.Vector2(-30, 0)
            self.vel += pygame.math.Vector2(-8, -5)
        elif hit.dir == -1 and self.dir == -1 and self.running:
            self.pos += pygame.math.Vector2(30, 0)
            self.vel += pygame.math.Vector2(8, -5)
        elif hit.dir == 1 and self.dir == 1 and not self.running:
            self.pos += pygame.math.Vector2(30, 0)
            self.vel += pygame.math.Vector2(8, -5)
        elif hit.dir == 1 and self.dir == -1:
            self.pos += pygame.math.Vector2(30, 0)
            self.vel += pygame.math.Vector2(8, -5)

    def knockback_charge(self, hit):
        if self.jumping:
            if self.dir == 1 and hit.dir == -1:
                self.vel += pygame.math.Vector2(-8, -5)
            elif self.dir == 1 and hit.dir == 1:
                self.vel += pygame.math.Vector2(-8, -5)
            elif self.dir == -1 and hit.dir == 1:
                self.vel += pygame.math.Vector2(8, -5)
            elif self.dir == -1 and hit.dir == -1:
                self.vel += pygame.math.Vector2(8, -5)

            if self.vel.y < -5:
                self.vel.y = -5

        elif hit.dir == -1 and self.dir == 1: #dir == 1,-1 is right,left
            self.pos += pygame.math.Vector2(-30, -2)
            self.vel += pygame.math.Vector2(-13, -7)
        elif hit.dir == -1 and self.dir == -1 and not self.running:
            self.pos += pygame.math.Vector2(-30, -2)
            self.vel += pygame.math.Vector2(-13, -7)
        elif hit.dir == -1 and self.dir == -1 and self.running:
            self.pos += pygame.math.Vector2(30, -2)
            self.vel += pygame.math.Vector2(13, -7)
        elif hit.dir == 1 and self.dir == 1 and self.running:
            self.pos += pygame.math.Vector2(-30, -2)
            self.vel += pygame.math.Vector2(-13, -7)
        elif hit.dir == 1 and self.dir == 1 and not self.running:
            self.pos += pygame.math.Vector2(30, -2)
            self.vel += pygame.math.Vector2(13, -7)
        elif hit.dir == 1 and self.dir == -1:
            self.pos += pygame.math.Vector2(30, -2)
            self.vel += pygame.math.Vector2(13, -7)

    def update(self):
        self.animate()
        self.acc = pygame.math.Vector2(0, 0.5)
        self.get_keys()
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pygame.BLEND_RGBA_MULT)
            except:
                self.damaged = False
                self.load_images()
        self.rect = self.image.get_rect()
        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        if abs(self.vel.x) < 0.2:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.boundary, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        collide_with_walls(self, self.game.boundary, 'y')
        self.rect.center = self.hit_rect.center
        self.death()

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def animate(self):
        now = pygame.time.get_ticks()

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
                if now - self.last_update > 350:
                    self.last_update = now
                    if self.dir == 1:
                        self.current_frame = (self.current_frame + 1) % len(self.standing_frame_R)
                        self.image = self.standing_frame_R[self.current_frame]
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.standing_frame_L)
                        self.image = self.standing_frame_L[self.current_frame]
                    self.rect = self.image.get_rect()
            elif self.running:
                if now - self.last_update > 200:
                    self.last_update = now
                    if self.dir == 1:
                        self.current_frame = (self.current_frame + 1) % len(self.run_frame_R)
                        self.image = self.run_frame_R[self.current_frame]
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.run_frame_L)
                        self.image = self.run_frame_L[self.current_frame]
                    self.rect = self.image.get_rect()
            elif self.shooting:
                if now - self.last_update > 150:
                    self.last_update = now
                    if self.dir == 1:
                        self.current_frame = (self.current_frame + 1) % len(self.shoot_frame_R)
                        self.image = self.shoot_frame_R[self.current_frame]
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.shoot_frame_L)
                        self.image = self.shoot_frame_L[self.current_frame]
                    self.rect = self.image.get_rect()
                self.shooting = False

            if self.jumping:
                if now - self.last_update > 150:
                    self.last_update = now
                    if self.dir == 1:
                        self.current_frame = (self.current_frame + 1) % len(self.jump_frame_R)
                        self.image = self.jump_frame_R[self.current_frame]
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.jump_frame_L)
                        self.image = self.jump_frame_L[self.current_frame]

    def jump(self):
        if self.alive:
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.game.jump_1.play()
                self.vel.y = -8.5

    def death(self):
        if not self.alive:
            self.control = False
            self.collision = False
            now = pygame.time.get_ticks()
            if now - self.death_time > 150:
                self.death_time = now
                if self.dir == 1:
                    self.death_anim = (self.death_anim + 1) % len(self.death_frame_R)
                    self.image = self.death_frame_R[self.death_anim]
                else:
                    self.death_anim = (self.death_anim + 1) % len(self.death_frame_L)
                    self.image = self.death_frame_L[self.death_anim]
                self.rect = self.image.get_rect()

            if self.death_anim >= 7:
                self.hit_rect = pygame.Rect(0, 0, 0, 0)
                self.shooting = False
                self.game.playersalive += 1
                self.kill()

class Player2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.death_anim = 0
        self.control = True
        self.load_images()
        self.image = self.standing_frame_R[0]
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 30, 45)
        self.hit_rect.center = self.rect.center
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(x, y)
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.acc = pygame.math.Vector2(0, 0)
        self.dir = 1
        self.running = False
        self.jumping = False
        self.shooting = False
        self.damaged = False
        self.alive = True
        self.collision = True
        self.death_time = 0

    def load_images(self):
        self.standing_frame_R = []
        self.standing_frame_L = []
        self.run_frame_R = []
        self.run_frame_L = []
        self.shoot_frame_R = []
        self.shoot_frame_L = []
        self.death_frame_L = []
        self.death_frame_R = []
        self.jump_frame_L = []
        self.jump_frame_R = []

        i = 1
        while i <= 4:
            frame_R_IDLE = pygame.image.load('assets/sprites/player/2/idle/R_idle_' + str(i) + '.png').convert_alpha()
            frame_L_IDLE = pygame.image.load('assets/sprites/player/2/idle/L_idle_' + str(i) + '.png').convert_alpha()
            frame_R_SHOOT = pygame.image.load('assets/sprites/player/2/shoot/R_shoot_' + str(i) + '.png').convert_alpha()
            frame_L_SHOOT = pygame.image.load('assets/sprites/player/2/shoot/L_shoot_' + str(i) + '.png').convert_alpha()
            frame_R_IDLE = pygame.transform.scale(frame_R_IDLE, (64, 64))
            frame_L_IDLE = pygame.transform.scale(frame_L_IDLE, (64, 64))
            frame_L_SHOOT = pygame.transform.scale(frame_L_SHOOT, (64, 64))
            frame_R_SHOOT = pygame.transform.scale(frame_R_SHOOT, (64, 64))
            i = i + 1
            self.standing_frame_R.append(frame_R_IDLE)
            self.standing_frame_L.append(frame_L_IDLE)
            self.shoot_frame_R.append(frame_R_SHOOT)
            self.shoot_frame_L.append(frame_L_SHOOT)

        i = 1
        while i <= 8:
            frame_L_DEATH = pygame.image.load('assets/sprites/player/2/death/L_death_' + str(i) + '.png').convert_alpha()
            frame_R_DEATH = pygame.image.load('assets/sprites/player/2/death/R_death_' + str(i) + '.png').convert_alpha()
            frame_L_DEATH = pygame.transform.scale(frame_L_DEATH, (64, 64))
            frame_R_DEATH = pygame.transform.scale(frame_R_DEATH, (64, 64))
            i = i + 1
            self.death_frame_L.append(frame_L_DEATH)
            self.death_frame_R.append(frame_R_DEATH)

        i = 1
        while i <= 14:
            frame_R_RUN = pygame.image.load('assets/sprites/player/2/run/R_run_' + str(i) + '.png').convert_alpha()
            frame_L_RUN = pygame.image.load('assets/sprites/player/2/run/L_run_' + str(i) + '.png').convert_alpha()
            frame_R_RUN = pygame.transform.scale(frame_R_RUN, (64, 64))
            frame_L_RUN = pygame.transform.scale(frame_L_RUN, (64, 64))
            i = i + 1
            self.run_frame_R.append(frame_R_RUN)
            self.run_frame_L.append(frame_L_RUN)

        frame = pygame.image.load('assets/sprites/player/2/jump/L_jump.png').convert_alpha()
        frame = pygame.transform.scale(frame, (64, 64))
        self.jump_frame_L.append(frame)

        frame = pygame.image.load('assets/sprites/player/2/jump/R_jump.png').convert_alpha()
        frame = pygame.transform.scale(frame, (64, 64))
        self.jump_frame_R.append(frame)

    def get_keys(self):
        if self.control:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.acc.x = 0.5
                self.dir = 1
            if keys[pygame.K_LEFT]:
                self.acc.x = -0.5
                self.dir = -1
            if keys[pygame.K_RETURN]:
                now = pygame.time.get_ticks()
                if now - self.last_shot > 150:
                    self.last_shot = now
                    if self.running:
                        pos = self.pos + pygame.math.Vector2(32 * self.dir, 5)
                    else:
                        pos = self.pos + pygame.math.Vector2(32 * self.dir, -10)
                    Bullet2(self.game, pos, self.dir)
                    self.game.shoot.play()
                    self.shooting = True

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain([i for i in range(40, 255, 25)] * 2)

    def knockback(self, hit):
        if self.jumping:
            if self.dir == 1:
                self.vel += pygame.math.Vector2(-8, -5)
            else:
                self.vel += pygame.math.Vector2(8, -5)

            if self.vel.y < -5:
                self.vel.y = -5

        elif hit.dir == -1 and self.dir == 1: #dir == 1,-1 is right,left
            self.pos += pygame.math.Vector2(-30, 0)
            self.vel += pygame.math.Vector2(-8, -5)
        elif hit.dir == -1 and self.dir == -1 and not self.running:
            self.pos += pygame.math.Vector2(-30, 0)
            self.vel += pygame.math.Vector2(-8, -5)
        elif hit.dir == 1 and self.dir == 1 and self.running:
            self.pos += pygame.math.Vector2(-30, 0)
            self.vel += pygame.math.Vector2(-8, -5)
        elif hit.dir == -1 and self.dir == -1 and self.running:
            self.pos += pygame.math.Vector2(30, 0)
            self.vel += pygame.math.Vector2(8, -5)
        elif hit.dir == 1 and self.dir == 1 and not self.running:
            self.pos += pygame.math.Vector2(30, 0)
            self.vel += pygame.math.Vector2(8, -5)
        elif hit.dir == 1 and self.dir == -1:
            self.pos += pygame.math.Vector2(30, 0)
            self.vel += pygame.math.Vector2(8, -5)

    def knockback_charge(self, hit):
        if self.jumping:
            if self.dir == 1 and hit.dir == -1:
                self.vel += pygame.math.Vector2(-8, -5)
            elif self.dir == 1 and hit.dir == 1:
                self.vel += pygame.math.Vector2(-8, -5)
            elif self.dir == -1 and hit.dir == 1:
                self.vel += pygame.math.Vector2(8, -5)
            elif self.dir == -1 and hit.dir == -1:
                self.vel += pygame.math.Vector2(8, -5)

            if self.vel.y < -5:
                self.vel.y = -5

        elif hit.dir == -1 and self.dir == 1: #dir == 1,-1 is right,left
            self.pos += pygame.math.Vector2(-30, -2)
            self.vel += pygame.math.Vector2(-13, -7)
        elif hit.dir == -1 and self.dir == -1 and not self.running:
            self.pos += pygame.math.Vector2(-30, -2)
            self.vel += pygame.math.Vector2(-13, -7)
        elif hit.dir == -1 and self.dir == -1 and self.running:
            self.pos += pygame.math.Vector2(30, -2)
            self.vel += pygame.math.Vector2(13, -7)
        elif hit.dir == 1 and self.dir == 1 and self.running:
            self.pos += pygame.math.Vector2(-30, -2)
            self.vel += pygame.math.Vector2(-13, -7)
        elif hit.dir == 1 and self.dir == 1 and not self.running:
            self.pos += pygame.math.Vector2(30, -2)
            self.vel += pygame.math.Vector2(13, -7)
        elif hit.dir == 1 and self.dir == -1:
            self.pos += pygame.math.Vector2(30, -2)
            self.vel += pygame.math.Vector2(13, -7)

    def update(self):
        self.animate()
        self.acc = pygame.math.Vector2(0, 0.5)
        self.get_keys()
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pygame.BLEND_RGBA_MULT)
            except:
                self.damaged = False
                self.load_images()
        self.rect = self.image.get_rect()
        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        if abs(self.vel.x) < 0.2:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.boundary, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        collide_with_walls(self, self.game.boundary, 'y')
        self.rect.center = self.hit_rect.center
        self.death()

    def animate(self):
        now = pygame.time.get_ticks()

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
                if now - self.last_update > 350:
                    self.last_update = now
                    if self.dir == 1:
                        self.current_frame = (self.current_frame + 1) % len(self.standing_frame_R)
                        self.image = self.standing_frame_R[self.current_frame]
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.standing_frame_L)
                        self.image = self.standing_frame_L[self.current_frame]
                    self.rect = self.image.get_rect()
            elif self.running:
                if now - self.last_update > 200:
                    self.last_update = now
                    if self.dir == 1:
                        self.current_frame = (self.current_frame + 1) % len(self.run_frame_R)
                        self.image = self.run_frame_R[self.current_frame]
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.run_frame_L)
                        self.image = self.run_frame_L[self.current_frame]
                    self.rect = self.image.get_rect()
            elif self.shooting:
                if now - self.last_update > 150:
                    self.last_update = now
                    if self.dir == 1:
                        self.current_frame = (self.current_frame + 1) % len(self.shoot_frame_R)
                        self.image = self.shoot_frame_R[self.current_frame]
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.shoot_frame_L)
                        self.image = self.shoot_frame_L[self.current_frame]
                    self.rect = self.image.get_rect()
                self.shooting = False

            if self.jumping:
                if now - self.last_update > 150:
                    self.last_update = now
                    if self.dir == 1:
                        self.current_frame = (self.current_frame + 1) % len(self.jump_frame_R)
                        self.image = self.jump_frame_R[self.current_frame]
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.jump_frame_L)
                        self.image = self.jump_frame_L[self.current_frame]

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def jump(self):
        if self.alive:
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.game.jump_2.play()
                self.vel.y = -8.5

    def death(self):
        if not self.alive:
            self.control = False
            self.collision = False
            now = pygame.time.get_ticks()
            if now - self.death_time > 150:
                self.death_time = now
                if self.dir == 1:
                    self.death_anim = (self.death_anim + 1) % len(self.death_frame_R)
                    self.image = self.death_frame_R[self.death_anim]
                else:
                    self.death_anim = (self.death_anim + 1) % len(self.death_frame_L)
                    self.image = self.death_frame_L[self.death_anim]
                self.rect = self.image.get_rect()

            if self.death_anim >= 7:
                self.hit_rect = pygame.Rect(0, 0, 0, 0)
                self.shooting = False
                self.game.playersalive += 1
                self.kill()

class Mob_small(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob_small
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.walk_frame_L[0]
        self.health_bars = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 24, 36).copy()
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.rect.center = self.pos
        self.health = 100
        self.dir = -1
        self.alive = True

    def load_images(self):
        self.walk_frame_R = []
        self.walk_frame_L = []

        i = 1
        while i <= 4:
            frame_R = pygame.image.load('assets/sprites/enemy/low/1/R_run_' + str(i) + '.png').convert_alpha()
            frame_R = pygame.transform.scale(frame_R, (24, 36))
            frame_L = pygame.image.load('assets/sprites/enemy/low/1/L_run_' + str(i) + '.png').convert_alpha()
            frame_L = pygame.transform.scale(frame_L, (24, 36))
            i = i + 1
            self.walk_frame_R.append(frame_R)
            self.walk_frame_L.append(frame_L)

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now
            if self.dir == -1:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_L)
                self.image = self.walk_frame_L[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_R)
                self.image = self.walk_frame_R[self.current_frame]
            self.rect = self.image.get_rect()

    def update(self):
        self.draw_health()
        self.animate()
        self.movement_equation()
        self.moving()

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.invis_wall, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def movement_equation(self):
        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

    def moving(self):
        self.acc = pygame.math.Vector2(0.2 * self.dir, 0.5)
        self.rect.centerx += 2 * self.dir
        hits2 = pygame.sprite.spritecollide(self, self.game.invis_wall, False)
        self.rect.centerx -= 2 * self.dir
        if hits2:
            self.dir = self.dir * -1

    def draw_health(self):
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
            self.load_images()

class Mob_Big(pygame.sprite.Sprite):
    def __init__(self, game, x, y, facing):
        self.game = game
        self.groups = game.all_sprites, game.mob_big
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.walk_frame_L[0]
        self.health_bars = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 24, 36).copy()
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.rect.center = self.pos
        self.dir = 1
        self.health = 300
        self.alive = True

    def load_images(self):
        self.walk_frame_R = []
        self.walk_frame_L = []

        i = 1
        while i <= 4:
            frame_R = pygame.image.load('assets/sprites/enemy/high/R_run_' + str(i) + '.png').convert_alpha()
            frame_R = pygame.transform.scale(frame_R, (36, 48))
            frame_L = pygame.image.load('assets/sprites/enemy/high/L_run_' + str(i) + '.png').convert_alpha()
            frame_L = pygame.transform.scale(frame_L, (36, 48))
            i = i + 1
            self.walk_frame_R.append(frame_R)
            self.walk_frame_L.append(frame_L)

    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 80:
            self.last_update = now
            if self.dir == -1:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_L)
                self.image = self.walk_frame_L[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_R)
                self.image = self.walk_frame_R[self.current_frame]
            self.rect = self.image.get_rect()

    def update(self):
        self.draw_health()
        self.animate()
        self.movement_equation()
        self.moving()
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.invis_wall, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()

    def movement_equation(self):
        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

    def moving(self):
        self.acc = pygame.math.Vector2(0.4 * self.dir, 0.5)
        self.rect.centerx += 5 * self.dir
        hits2 = pygame.sprite.spritecollide(self, self.game.invis_wall, False)
        self.rect.centerx -= 5 * self.dir
        if hits2:
            self.dir = self.dir * -1

    def draw_health(self):
        if self.health > 200:
            self.col = (0, 255, 0)
        elif self.health > 100:
            self.col = (255, 255, 0)
        else:
            self.col = (255, 0, 0)
        width = int(self.rect.width * self.health / 300)
        self.health_bar = pygame.Rect(0, 0, width, -5)
        if self.health < 300:
            pygame.draw.rect(self.image, self.col, self.health_bar)
            self.load_images()

class Mob_flying(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob_flying
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.walk_frame_L[0]
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
        self.target = game.player
        self.target2 = game.player2
        self.alive = True
        self.dir = 1
        self.facing = False
        self.last_shot = 0
        self.wobble = 0
        self.fix = True

    def load_images(self):
        self.walk_frame_R = []
        self.walk_frame_L = []

        i = 1
        while i <= 4:
            frame_R = pygame.image.load('assets/sprites/enemy/med/R_run_' + str(i) + '.png').convert_alpha()
            frame_R = pygame.transform.scale(frame_R, (24, 36))
            frame_L = pygame.image.load('assets/sprites/enemy/med/L_run_' + str(i) + '.png').convert_alpha()
            frame_L = pygame.transform.scale(frame_L, (24, 36))
            i = i + 1
            self.walk_frame_R.append(frame_R)
            self.walk_frame_L.append(frame_L)

    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 200:
            self.last_update = now
            if self.dir == -1:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_L)
                self.image = self.walk_frame_L[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_R)
                self.image = self.walk_frame_R[self.current_frame]
            self.rect = self.image.get_rect()

    def update(self):
        self.draw_health()
        self.animate()
        target_dist = self.target.pos - self.pos
        target_dist2 = self.target2.pos - self.pos

        if target_dist.length_squared() < 150**2 and target_dist2.length_squared() < 150**2:
            if self.target.alive and self.target2.alive:
                if target_dist.length_squared() < target_dist2.length_squared():
                    self.chase_player("1")
                elif target_dist2.length_squared() < target_dist.length_squared():
                    self.chase_player("2")
            elif self.target.alive and not self.target2.alive:
                self.chase_player("1")
            elif not self.target.alive and self.target2.alive:
                self.chase_player("2")
            else:
                pass

        elif target_dist.length_squared() < 150**2 and target_dist2.length_squared() > 150**2:
            if self.target.alive:
                self.chase_player("1")
            else:
                self.moving()
                self.movement_equation()

        elif target_dist2.length_squared() < 150**2 and target_dist.length_squared() > 150**2:
            if self.target2.alive:
                self.chase_player("2")
            else:
                self.moving()
                self.movement_equation()

        else:
            self.moving()
            self.movement_equation()

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.invis_wall, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def movement_equation(self):
        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

    def chase_player(self, player_num):
        if player_num == "1":
            self.rot = (self.game.player.pos - self.pos).angle_to(pygame.math.Vector2(1, 0))
            if self.game.player.pos.x - self.pos.x < 0:
                self.dir = -1
            else:
                self.dir = 1
        else:
            self.rot = (self.game.player2.pos - self.pos).angle_to(pygame.math.Vector2(1, 0))
            if self.game.player2.pos.x - self.pos.x < 0:
                self.dir = -1
            else:
                self.dir = 1

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
        now = pygame.time.get_ticks()

        if now - self.wobble > 750 and self.vel.y == -0.2:
            self.wobble = now
            self.vel.y = 0.2
        elif now - self.wobble > 750 and self.vel.y == 0.2:
            self.wobble = now
            self.vel.y = -0.2

        self.acc = pygame.math.Vector2(0.15 * self.dir, 0)

        self.rect.centerx += 2 * self.dir
        hits2 = pygame.sprite.spritecollide(self, self.game.invis_wall, False)
        self.rect.centerx -= 2 * self.dir
        if hits2:
            self.dir = self.dir * -1

    def draw_health(self):
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
            self.load_images()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > 2500:
            self.last_shot = now
            angle = 180
            dir = pygame.math.Vector2(-1, 0)
            Mob_Bullet(self.game, self.pos, dir, angle)
            angle = 0
            dir = pygame.math.Vector2(1, 0)
            Mob_Bullet(self.game, self.pos, dir, angle)
            angle = 90
            dir = pygame.math.Vector2(0, -1)
            Mob_Bullet(self.game, self.pos, dir, angle)
            angle = 270
            dir = pygame.math.Vector2(0, 1)
            Mob_Bullet(self.game, self.pos, dir, angle)

class Mob_charge(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob_charge
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.walk_frame_L[0]
        self.health_bars = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 24, 30).copy()
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.rect.center = self.pos
        self.health = 100
        self.target = game.player
        self.target2 = game.player2
        self.dir = 1
        self.alive = True
        self.facing = False
        self.charging = False
        self.chargesequence = False
        self.detected = False
        self.charge_time = 0
        self.round = 1

    def load_images(self):
        self.walk_frame_R = []
        self.walk_frame_L = []

        i = 1
        while i <= 4:
            frame_R = pygame.image.load('assets/sprites/enemy/low/2/R_run_' + str(i) + '.png').convert_alpha()
            frame_R = pygame.transform.scale(frame_R, (24, 36))
            frame_L = pygame.image.load('assets/sprites/enemy/low/2/L_run_' + str(i) + '.png').convert_alpha()
            frame_L = pygame.transform.scale(frame_L, (24, 36))
            i = i + 1
            self.walk_frame_L.append(frame_L)
            self.walk_frame_R.append(frame_R)

    def animate(self):
        now = pygame.time.get_ticks()
        if self.charging:
            anim_speed = 50
        else:
            anim_speed = 200


        if now - self.last_update > anim_speed:
            self.last_update = now
            if self.dir == -1:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_L)
                self.image = self.walk_frame_L[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_R)
                self.image = self.walk_frame_R[self.current_frame]
            self.rect = self.image.get_rect()

    def update(self):
        self.draw_health()
        target_dist = self.target.pos - self.pos
        target2_dist = self.target2.pos - self.pos

        if not self.charging and not self.detected and not self.chargesequence:
            self.animate()
            self.movement_equation()
            self.moving()

        if target_dist.length_squared() < 150**2 and not self.charging and not self.detected and not self.chargesequence:
            self.detected = True

        elif target2_dist.length_squared() < 150**2 and not self.charging and not self.detected and not self.chargesequence:
            self.detected = True

        if self.detected and not self.charging and not self.chargesequence:
            self.step = 0
            self.charge_counter = 0

            if self.target.pos.x - self.pos.x <= 0:
                self.dir = -1
            else:
                self.dir = 1

            self.chargesequence = True

        elif self.detected and not self.charging and self.chargesequence:
            time = pygame.time.get_ticks()
            self.animate()
            self.vel.x = 0
            if self.charge_counter != 10:
                self.movement_equation()
                self.acc.x = 0
                if time - self.step > 200:
                    self.charge_motion()
                    self.step = time
                    self.charge_counter += 1
            else:
                self.charge_counter = 0
                self.charging = True

        elif self.detected and self.charging and self.chargesequence:
            self.charge_time = pygame.time.get_ticks()
            if self.charge_time <= int(10000*self.round):
                self.animate()
                self.movement_equation()
                self.chargeaccel()
            else:
                self.round += 1
                self.detected = False
                self.chargesequence = False
                self.charging = False

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.invis_wall, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def movement_equation(self):
        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos


    def charge_motion(self):
        self.acc = pygame.math.Vector2(-0.2 * self.dir, 0.5)
        self.rect.centerx -=2 * self.dir
        hits2 = pygame.sprite.spritecollide(self, self.game.invis_wall, False)
        self.rect.centerx +=2 * self.dir
        if hits2:
            self.acc = pygame.math.Vector2(0, 0.5)

    def moving(self):
        self.acc = pygame.math.Vector2(0.2 * self.dir, 0.5)
        self.rect.centerx += 2 * self.dir
        hits = pygame.sprite.spritecollide(self, self.game.invis_wall, False)
        self.rect.centerx -= 2 * self.dir
        if hits:
            self.dir = self.dir * -1


    def chargeaccel(self):
        self.acc = pygame.math.Vector2(0.5 * self.dir, 0.5)
        self.rect.centerx +=2 * self.dir
        hits2 = pygame.sprite.spritecollide(self, self.game.invis_wall, False)
        self.rect.centerx -=2 * self.dir
        if hits2:
            self.dir = self.dir * -1


    def draw_health(self):
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
            self.load_images()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Spike(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.spike
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Fall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.fall_death
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Boundary(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.boundary
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Invis_wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.invis_wall
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Win_area(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.win_game
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Item(pygame.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_image()
        self.image = self.item_images[type]
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 20, 17)
        self.hit_rect.center = self.rect.center
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        offset = 5 * (self.tween(self.step / 11) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += 0.4
        if self.step > 10:
            self.step = 0
            self.dir *= -1

    def load_image(self):
        chicken = {'health': 'assets/images/chicken.png'}
        coin = {'coin': 'assets/images/coin.png'}
        self.item_images = {}
        for item in chicken:
            self.item_images[item] = pygame.image.load(chicken[item]).convert_alpha()
        for item in coin:
            self.item_images[item] = pygame.image.load(coin[item]).convert_alpha()
