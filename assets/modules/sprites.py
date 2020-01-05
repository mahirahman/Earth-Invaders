import pygame as pg
import random
from assets.modules.variables import *
from assets.modules.tilemap import collide_hit_rect
from os import path
import pytweening as tween
from itertools import chain
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, facing_R):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if facing_R:
            self.image = game.bullet_img_R
        else:
            self.image = game.bullet_img_L
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 17, 8)
        self.hit_rect.center = self.rect.center
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()

class Bullet2(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, facing_R):
        self.groups = game.all_sprites, game.bullets2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if facing_R:
            self.image = game.bullet_img_R
        else:
            self.image = game.bullet_img_L
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 17, 8)
        self.hit_rect.center = self.rect.center
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()

class Mob_Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, angle):
        self.groups = game.all_sprites, game.mob_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_mob
        self.image = pg.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 17, 8)
        self.hit_rect.center = self.rect.center
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * MOB_BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > MOB_BULLET_LIFETIME:
            self.kill()
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.death_anim = 0
        self.control = True
        self.load_images()
        self.image = self.standing_frame_R[0]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.acc = vec(0, 0)
        self.running = False
        self.jumping = False
        self.facing_R = True
        self.last_shot = 0
        self.damaged = False
        self.shooting = False
        self.alive = True
        self.collision = True
        self.death_time = 0

    def load_images(self):
        self.standing_frame_R = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/player/1/idle/R_idle_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.standing_frame_R.append(frame)

        self.standing_frame_L = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/player/1/idle/L_idle_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.standing_frame_L.append(frame)


        self.run_frame_R = []

        i = 1
        while i <= 14:
            frame = pg.image.load('assets/sprites/player/1/run/R_run_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.run_frame_R.append(frame)

        self.run_frame_L = []

        i = 1
        while i <= 14:
            frame = pg.image.load('assets/sprites/player/1/run/L_run_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.run_frame_L.append(frame)

        self.shoot_frame_R = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/player/1/shoot/R_shoot_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.shoot_frame_R.append(frame)

        self.shoot_frame_L = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/player/1/shoot/L_shoot_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.shoot_frame_L.append(frame)

        self.death_frame_L = []

        i = 1
        while i <= 8:
            frame = pg.image.load('assets/sprites/player/1/death/L_death_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.death_frame_L.append(frame)

        self.death_frame_R = []

        i = 1
        while i <= 8:
            frame = pg.image.load('assets/sprites/player/1/death/R_death_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.death_frame_R.append(frame)

        self.jump_frame_L = []
        frame = pg.image.load('assets/sprites/player/1/jump/L_jump.png').convert_alpha()
        frame = pg.transform.scale(frame, (64, 64))
        self.jump_frame_L.append(frame)

        self.jump_frame_R = []
        frame = pg.image.load('assets/sprites/player/1/jump/R_jump.png').convert_alpha()
        frame = pg.transform.scale(frame, (64, 64))
        self.jump_frame_R.append(frame)

    def get_keys(self):
        if self.control:
            keys = pg.key.get_pressed()
            if keys[pg.K_d]:
                self.acc.x = PLAYER_ACC
                self.facing_R = True
            if keys[pg.K_a]:
                self.acc.x = -PLAYER_ACC
                self.facing_R = False
            if keys[pg.K_SPACE]:
                now = pg.time.get_ticks()
                if self.running and self.shooting:
                    if now - self.last_shot > BULLET_RATE:
                        self.last_shot = now
                        if self.facing_R:
                            pos = self.pos + BARREL_OFFSET_RUN_R
                            dir = vec(1,0)
                            Bullet(self.game, pos, dir, self.facing_R)
                            self.game.shoot_sound['shoot'].play()
                            self.shooting = True
                        else:
                            pos = self.pos + BARREL_OFFSET_RUN_L
                            dir = vec(-1,0)
                            Bullet(self.game, pos, dir, self.facing_R)
                            self.game.shoot_sound['shoot'].play()
                            self.shooting = True
                else:
                    if now - self.last_shot > BULLET_RATE:
                        self.last_shot = now
                        if self.facing_R:
                            pos = self.pos + BARREL_OFFSET_R
                            dir = vec(1, 0)
                            Bullet(self.game, pos, dir, self.facing_R)
                            self.game.shoot_sound['shoot'].play()
                            self.shooting = True
                        else:
                            pos = self.pos + BARREL_OFFSET_L
                            dir = vec(-1, 0)
                            Bullet(self.game, pos, dir, self.facing_R)
                            self.game.shoot_sound['shoot'].play()
                            self.shooting = True
        else:
            pass

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 2)

    def knockback(self, hit):
        if self.jumping:
            if self.facing_R and hit.facing:
                self.vel += vec(-8, -5)
            elif self.facing_R and not hit.facing:
                self.vel += vec(-8, -5)
            elif not self.facing_R and not hit.facing:
                self.vel += vec(8, -5)
            elif not self.facing_R and hit.facing:
                self.vel += vec(8, -5)

            if self.vel.y < -5:
                self.vel.y = -5

        elif hit.facing and self.facing_R: #hit.facing = left, not hit.facing = right, facing_R = right, not facing_R = left
            self.pos += vec(-MOB_KNOCKBACK, 0)
        elif hit.facing and not self.facing_R and not self.running:
            self.pos += vec(-MOB_KNOCKBACK, 0)
        elif hit.facing and not self.facing_R and self.running:
            self.pos += vec(MOB_KNOCKBACK, 0)
        elif not hit.facing and self.facing_R and self.running:
            self.pos += vec(-MOB_KNOCKBACK, 0)
        elif not hit.facing and self.facing_R and not self.running:
            self.pos += vec(MOB_KNOCKBACK, 0)
        elif not hit.facing and not self.facing_R:
            self.pos += vec(MOB_KNOCKBACK, 0)

    def update(self):
        self.animate()
        self.acc = vec(0, 0.5)
        self.get_keys()
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
                self.load_images()
        self.rect = self.image.get_rect()
        self.acc.x += self.vel.x * PLAYER_FRICTION
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
        now = pg.time.get_ticks()

        if self.vel.x != 0:
            self.running = True
        else:
            self.running = False

        if self.vel.y != 0:
            self.jumping = True
        else:
            self.jumping = False

        if self.alive:
            if self.facing_R:
                if not self.running and not self.shooting:
                    if now - self.last_update > 350:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.standing_frame_R)
                        self.image = self.standing_frame_R[self.current_frame]
                        self.rect = self.image.get_rect()
                elif self.running:
                    if now - self.last_update > 200:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.run_frame_R)
                        self.image = self.run_frame_R[self.current_frame]
                        self.rect = self.image.get_rect()
                elif self.shooting:
                    if now - self.last_update > 150:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.shoot_frame_R)
                        self.image = self.shoot_frame_R[self.current_frame]
                        self.rect = self.image.get_rect()
                    self.shooting = False

            else:
                if not self.running and not self.shooting:
                    if now - self.last_update > 350:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.standing_frame_L)
                        self.image = self.standing_frame_L[self.current_frame]
                        self.rect = self.image.get_rect()
                elif self.running:
                    if now - self.last_update > 200:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.run_frame_L)
                        self.image = self.run_frame_L[self.current_frame]
                elif self.shooting:
                    if now - self.last_update > 150:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.shoot_frame_L)
                        self.image = self.shoot_frame_L[self.current_frame]
                        self.rect = self.image.get_rect()
                    self.shooting = False

            if self.jumping:
                if self.facing_R:
                    if now - self.last_update > 150:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.jump_frame_R)
                        self.image = self.jump_frame_R[self.current_frame]
                else:
                    if now - self.last_update > 150:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.jump_frame_L)
                        self.image = self.jump_frame_L[self.current_frame]
        else:
            pass

    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.game.player_jump['jump'].play()
            self.vel.y = -10

    def death(self):
        if not self.alive:
            self.control = False
            self.collision = False
            now = pg.time.get_ticks()
            if self.facing_R:
                if now - self.death_time > 150:
                    self.death_time = now
                    self.death_anim = (self.death_anim + 1) % len(self.death_frame_R)
                    self.image = self.death_frame_R[self.death_anim]
                    self.rect = self.image.get_rect()

            elif not self.facing_R:
                if now - self.death_time > 150:
                    self.death_time = now
                    self.death_anim = (self.death_anim + 1) % len(self.death_frame_L)
                    self.image = self.death_frame_L[self.death_anim]
                    self.rect = self.image.get_rect()

            if self.death_anim >= 7:
                self.hit_rect = pg.Rect(0, 0, 0, 0)
                self.shooting = False
                self.game.playersalive += 1
                self.kill()


class Player2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.death_anim = 0
        self.control = True
        self.load_images()
        self.image = self.standing_frame_R[0]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT2
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.acc = vec(0, 0)
        self.running = False
        self.jumping = False
        self.facing_R = True
        self.shooting = False
        self.damaged = False
        self.alive = True
        self.collision = True
        self.death_time = 0

    def load_images(self):
        self.standing_frame_R = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/player/2/idle/R_idle_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.standing_frame_R.append(frame)

        self.standing_frame_L = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/player/2/idle/L_idle_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.standing_frame_L.append(frame)


        self.run_frame_R = []

        i = 1
        while i <= 14:
            frame = pg.image.load('assets/sprites/player/2/run/R_run_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.run_frame_R.append(frame)

        self.run_frame_L = []

        i = 1
        while i <= 14:
            frame = pg.image.load('assets/sprites/player/2/run/L_run_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.run_frame_L.append(frame)

        self.shoot_frame_R = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/player/2/shoot/R_shoot_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.shoot_frame_R.append(frame)

        self.shoot_frame_L = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/player/2/shoot/L_shoot_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.shoot_frame_L.append(frame)

        self.death_frame_L = []

        i = 1
        while i <= 8:
            frame = pg.image.load('assets/sprites/player/2/death/L_death_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.death_frame_L.append(frame)

        self.death_frame_R = []

        i = 1
        while i <= 8:
            frame = pg.image.load('assets/sprites/player/2/death/R_death_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (64, 64))
            i = i + 1
            self.death_frame_R.append(frame)

        self.jump_frame_L = []
        frame = pg.image.load('assets/sprites/player/2/jump/L_jump.png').convert_alpha()
        frame = pg.transform.scale(frame, (64, 64))
        self.jump_frame_L.append(frame)

        self.jump_frame_R = []
        frame = pg.image.load('assets/sprites/player/2/jump/R_jump.png').convert_alpha()
        frame = pg.transform.scale(frame, (64, 64))
        self.jump_frame_R.append(frame)

    def get_keys(self):
        self.rot_speed = 0
        if self.control:
            keys = pg.key.get_pressed()
            if keys[pg.K_RIGHT]:
                self.acc.x = PLAYER_ACC
                self.facing_R = True
            if keys[pg.K_LEFT]:
                self.acc.x = -PLAYER_ACC
                self.facing_R = False
            if keys[pg.K_RETURN]:
                now = pg.time.get_ticks()
                if self.running and self.shooting:
                    if now - self.last_shot > BULLET_RATE:
                        self.last_shot = now
                        if self.facing_R:
                            pos = self.pos + BARREL_OFFSET_RUN_R
                            dir = vec(1,0)
                            Bullet2(self.game, pos, dir, self.facing_R)
                            self.game.shoot_sound['shoot'].play()
                            self.shooting = True
                        else:
                            pos = self.pos + BARREL_OFFSET_RUN_L
                            dir = vec(-1,0)
                            Bullet2(self.game, pos, dir, self.facing_R)
                            self.game.shoot_sound['shoot'].play()
                            self.shooting = True
                else:
                    if now - self.last_shot > BULLET_RATE:
                        self.last_shot = now
                        if self.facing_R:
                            pos = self.pos + BARREL_OFFSET_R
                            dir = vec(1, 0)
                            Bullet2(self.game, pos, dir, self.facing_R)
                            self.game.shoot_sound['shoot'].play()
                            self.shooting = True
                        else:
                            pos = self.pos + BARREL_OFFSET_L
                            dir = vec(-1, 0)
                            Bullet2(self.game, pos, dir, self.facing_R)
                            self.game.shoot_sound['shoot'].play()
                            self.shooting = True

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 2)

    def knockback(self, hit):
        if self.jumping:
            if self.facing_R:
                self.vel += vec(-3, -5)
            else:
                self.vel += vec(3, -5)

            if self.vel.y < -5:
                self.vel.y = -5

        elif hit.facing and self.facing_R: #hit.facing = left, not hit.facing = right, facing_R = right, not facing_R = left
            self.pos += vec(-MOB_KNOCKBACK, 0)
        elif hit.facing and not self.facing_R and not self.running:
            self.pos += vec(-MOB_KNOCKBACK, 0)
        elif hit.facing and not self.facing_R and self.running:
            self.pos += vec(MOB_KNOCKBACK, 0)
        elif not hit.facing and self.facing_R and self.running:
            self.pos += vec(-MOB_KNOCKBACK, 0)
        elif not hit.facing and self.facing_R and not self.running:
            self.pos += vec(MOB_KNOCKBACK, 0)
        elif not hit.facing and not self.facing_R:
            self.pos += vec(MOB_KNOCKBACK, 0)

    def update(self):
        self.animate()
        self.acc = vec(0, 0.5)
        self.get_keys()
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
                self.load_images()
        self.rect = self.image.get_rect()
        self.acc.x += self.vel.x * PLAYER_FRICTION
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
        now = pg.time.get_ticks()

        if self.vel.x != 0:
            self.running = True
        else:
            self.running = False

        if self.vel.y != 0:
            self.jumping = True
        else:
            self.jumping = False

        if self.alive:
            if self.facing_R:
                if not self.running and not self.shooting:
                    if now - self.last_update > 350:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.standing_frame_R)
                        self.image = self.standing_frame_R[self.current_frame]
                        self.rect = self.image.get_rect()
                elif self.running:
                    if now - self.last_update > 200:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.run_frame_R)
                        self.image = self.run_frame_R[self.current_frame]
                        self.rect = self.image.get_rect()
                elif self.shooting:
                    if now - self.last_update > 150:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.shoot_frame_R)
                        self.image = self.shoot_frame_R[self.current_frame]
                        self.rect = self.image.get_rect()
                    self.shooting = False

            else:
                if not self.running and not self.shooting:
                    if now - self.last_update > 350:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.standing_frame_L)
                        self.image = self.standing_frame_L[self.current_frame]
                        self.rect = self.image.get_rect()
                elif self.running:
                    if now - self.last_update > 200:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.run_frame_L)
                        self.image = self.run_frame_L[self.current_frame]
                elif self.shooting:
                    if now - self.last_update > 150:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.shoot_frame_L)
                        self.image = self.shoot_frame_L[self.current_frame]
                        self.rect = self.image.get_rect()
                    self.shooting = False

            if self.jumping:
                if self.facing_R:
                    if now - self.last_update > 150:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.jump_frame_R)
                        self.image = self.jump_frame_R[self.current_frame]
                else:
                    if now - self.last_update > 150:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.jump_frame_L)
                        self.image = self.jump_frame_L[self.current_frame]
        else:
            pass

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def jump(self):
        self.rect.x += 1
        self.rect.y -= 1
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.x -= 1
        self.rect.y += 1
        if hits:
            self.vel.y = -10
            self.game.player_jump['jump'].play()

    def death(self):
        if not self.alive:
            self.control = False
            self.collision = False
            now = pg.time.get_ticks()
            if self.facing_R:
                if now - self.death_time > 150:
                    self.death_time = now
                    self.death_anim = (self.death_anim + 1) % len(self.death_frame_R)
                    self.image = self.death_frame_R[self.death_anim]
                    self.rect = self.image.get_rect()

            elif not self.facing_R:
                if now - self.death_time > 150:
                    self.death_time = now
                    self.death_anim = (self.death_anim + 1) % len(self.death_frame_L)
                    self.image = self.death_frame_L[self.death_anim]
                    self.rect = self.image.get_rect()

            if self.death_anim >= 7:
                self.hit_rect = pg.Rect(0, 0, 0, 0)
                self.shooting = False
                self.game.playersalive += 1
                self.kill()

class Mob_small_1(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob_small_1
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.walk_frame_L[0]
        self.health_bars = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.target = game.player
        self.target2 = game.player2
        self.alive = True
        self.facing = False
        self.col = GREEN

    def load_images(self):
        self.walk_frame_R = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/enemy/low/1/R_run_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (24, 36))
            i = i + 1
            self.walk_frame_R.append(frame)

        self.walk_frame_L = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/enemy/low/1/L_run_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (24, 36))
            i = i + 1
            self.walk_frame_L.append(frame)

    def animate(self):
        now = pg.time.get_ticks()
        if self.facing:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_L)
                self.image = self.walk_frame_L[self.current_frame]
                self.rect = self.image.get_rect()
        else:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_R)
                self.image = self.walk_frame_R[self.current_frame]
                self.rect = self.image.get_rect()

    def update(self):
        self.draw_health()
        self.animate()
        target_dist = self.target.pos - self.pos
        target2_dist = self.target2.pos - self.pos
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.moving()

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.invis_wall, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def moving(self):
        if not self.facing:
            self.acc = vec(0.2, 0.5)
            self.rect.centerx +=2
            hits2 = pg.sprite.spritecollide(self, self.game.invis_wall, False)
            self.rect.centerx -=2
            if hits2:
                self.facing = True

        else:
            self.acc = vec(-0.2, 0.5)
            self.rect.centerx -= 2
            hits = pg.sprite.spritecollide(self, self.game.invis_wall, False)
            self.rect.centerx += 2
            if hits:
                self.facing = False

    def draw_health(self):
        if self.health > 60:
            self.col = GREEN
        elif self.health > 30:
            self.col = YELLOW
        else:
            self.col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 2)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, self.col, self.health_bar)
            self.load_images()

class Mob_small_2(pg.sprite.Sprite):
    def __init__(self, game, x, y, facing):
        self.groups = game.all_sprites, game.mob_small_2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.walk_frame_L[0]
        self.health_bars = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.target = game.player
        self.target2 = game.player2
        self.alive = True
        self.facing = facing
        self.col = GREEN

    def load_images(self):
        self.walk_frame_R = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/enemy/low/2/R_run_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (24, 36))
            i = i + 1
            self.walk_frame_R.append(frame)

        self.walk_frame_L = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/enemy/low/2/L_run_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (24, 36))
            i = i + 1
            self.walk_frame_L.append(frame)

    def animate(self):
        now = pg.time.get_ticks()
        if self.facing:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_L)
                self.image = self.walk_frame_L[self.current_frame]
                self.rect = self.image.get_rect()
        else:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_R)
                self.image = self.walk_frame_R[self.current_frame]
                self.rect = self.image.get_rect()

    def update(self):
        self.draw_health()
        self.animate()
        target_dist = self.target.pos - self.pos
        target2_dist = self.target2.pos - self.pos
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.moving()

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.invis_wall, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def moving(self):
        if not self.facing:
            self.acc = vec(0.2, 0.5)
            self.rect.centerx +=2
            hits2 = pg.sprite.spritecollide(self, self.game.invis_wall, False)
            self.rect.centerx -=2
            if hits2:
                self.facing = True

        else:
            self.acc = vec(-0.2, 0.5)
            self.rect.centerx -= 2
            hits = pg.sprite.spritecollide(self, self.game.invis_wall, False)
            self.rect.centerx += 2
            if hits:
                self.facing = False

    def draw_health(self):
        if self.health > 60:
            self.col = GREEN
        elif self.health > 30:
            self.col = YELLOW
        else:
            self.col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 2)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, self.col, self.health_bar)
            self.load_images()

class Mob_Big(pg.sprite.Sprite):
    def __init__(self, game, x, y, facing):
        self.game = game
        self.groups = game.all_sprites, game.mob_big
        pg.sprite.Sprite.__init__(self, self.groups)
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.walk_frame_L[0]
        self.health_bars = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_BIG_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = 300
        self.target = game.player
        self.target2 = game.player2
        self.alive = True
        self.facing = facing
        self.col = GREEN

    def load_images(self):
        self.walk_frame_R = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/enemy/high/R_run_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (36, 48))
            i = i + 1
            self.walk_frame_R.append(frame)

        self.walk_frame_L = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/enemy/high/L_run_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (36, 48))
            i = i + 1
            self.walk_frame_L.append(frame)

    def animate(self):
        now = pg.time.get_ticks()
        if self.facing:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_L)
                self.image = self.walk_frame_L[self.current_frame]
                self.rect = self.image.get_rect()
        else:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_R)
                self.image = self.walk_frame_R[self.current_frame]
                self.rect = self.image.get_rect()

    def update(self):
        self.draw_health()
        self.animate()
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.moving()

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.invis_wall, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            self.kill()

    def moving(self):
        if not self.facing:
            self.acc = vec(0.1, 0.5)
            self.rect.centerx +=2
            hits2 = pg.sprite.spritecollide(self, self.game.invis_wall, False)
            self.rect.centerx -=2
            if hits2:
                self.facing = True

        else:
            self.acc = vec(-0.1, 0.5)
            self.rect.centerx -= 2
            hits = pg.sprite.spritecollide(self, self.game.invis_wall, False)
            self.rect.centerx += 2
            if hits:
                self.facing = False

    def draw_health(self):
        if self.health > 200:
            self.col = GREEN
        elif self.health > 100:
            self.col = YELLOW
        else:
            self.col = RED
        width = int(self.rect.width * self.health / 300)
        self.health_bar = pg.Rect(0, 0, width, -5)
        if self.health < 300:
            pg.draw.rect(self.image, self.col, self.health_bar)
            self.load_images()

class Mob_flying(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob_flying
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.walk_frame_L[0]
        self.health_bars = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_FLYING_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = 150
        self.target = game.player
        self.target2 = game.player2
        self.alive = True
        self.facing = False
        self.col = GREEN
        self.last_shot = 0
        self.wobble = 0
        self.fix = True

    def load_images(self):
        self.walk_frame_R = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/enemy/med/R_run_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (24, 36))
            i = i + 1
            self.walk_frame_R.append(frame)

        self.walk_frame_L = []

        i = 1
        while i <= 4:
            frame = pg.image.load('assets/sprites/enemy/med/L_run_' + str(i) + '.png').convert_alpha()
            frame = pg.transform.scale(frame, (24, 36))
            i = i + 1
            self.walk_frame_L.append(frame)

    def animate(self):
        now = pg.time.get_ticks()
        if self.facing:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_L)
                self.image = self.walk_frame_L[self.current_frame]
                self.rect = self.image.get_rect()
        else:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frame_R)
                self.image = self.walk_frame_R[self.current_frame]
                self.rect = self.image.get_rect()

    def update(self):
        self.draw_health()
        self.animate()
        target_dist = self.target.pos - self.pos
        target_dist2 = self.target2.pos - self.pos
        if self.target.alive and self.target2.alive:
            if target_dist.length_squared() < DETECT_RADIUS**2 and target_dist2.length_squared() < DETECT_RADIUS**2:
                if target_dist.length_squared() < target_dist2.length_squared():
                    self.chase_player1()
                elif target_dist2.length_squared() < target_dist.length_squared():
                    self.chase_player2()
                if self.vel.x > 0:
                    self.facing = False
                else:
                    self.facing = True

            elif target_dist.length_squared() < DETECT_RADIUS**2:
                self.chase_player1()
                if self.vel.x > 0:
                    self.facing = False
                else:
                    self.facing = True

            elif target_dist2.length_squared() < DETECT_RADIUS**2:
                self.chase_player2()
                if self.vel.x > 0:
                    self.facing = False
                else:
                    self.facing = True

            elif target_dist.length_squared() > DETECT_RADIUS**2 and target_dist2.length_squared() > DETECT_RADIUS**2:
                self.moving()
                self.acc.x += self.vel.x * PLAYER_FRICTION
                self.vel += self.acc
                self.pos += self.vel + 0.5 * self.acc
                self.pos += self.vel * self.game.dt
                self.rect.center = self.pos

        elif self.target.alive and not self.target2.alive:
            if target_dist.length_squared() < DETECT_RADIUS**2:
                self.chase_player1()
                if self.vel.x > 0:
                    self.facing = False
                else:
                    self.facing = True

            elif target_dist.length_squared() > DETECT_RADIUS**2:
                self.moving()
                self.acc.x += self.vel.x * PLAYER_FRICTION
                self.vel += self.acc
                self.pos += self.vel + 0.5 * self.acc
                self.pos += self.vel * self.game.dt
                self.rect.center = self.pos

        elif not self.target.alive and self.target2.alive:
            if target_dist2.length_squared() < DETECT_RADIUS**2:
                self.chase_player2()
                if self.vel.x > 0:
                    self.facing = False
                else:
                    self.facing = True

            elif target_dist2.length_squared() > DETECT_RADIUS**2:
                self.moving()
                self.acc.x += self.vel.x * PLAYER_FRICTION
                self.vel += self.acc
                self.pos += self.vel + 0.5 * self.acc
                self.pos += self.vel * self.game.dt
                self.rect.center = self.pos

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.invis_wall, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def chase_player1(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.rect.center = self.pos
        self.acc = vec(50, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.shoot()
        self.fix = False

    def chase_player2(self):
        self.rot = (self.game.player2.pos - self.pos).angle_to(vec(1, 0))
        self.rect.center = self.pos
        self.acc = vec(50, 0).rotate(-self.rot)
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
        now = pg.time.get_ticks()

        if not self.facing:
            if now - self.wobble > 750 and self.vel.y == -0.2:
                self.wobble = now
                self.vel.y = 0.2
            elif now - self.wobble > 750 and self.vel.y == 0.2:
                self.wobble = now
                self.vel.y = -0.2

            self.acc = vec(0.15, 0)
            self.rect.centerx +=2
            hits2 = pg.sprite.spritecollide(self, self.game.invis_wall, False)
            self.rect.centerx -=2
            if hits2:
                self.facing = True

        else:
            if now - self.wobble > 750 and self.vel.y == -0.2:
                self.wobble = now
                self.vel.y = 0.2
            elif now - self.wobble > 750 and self.vel.y == 0.2:
                self.wobble = now
                self.vel.y = -0.2

            self.acc = vec(-0.15, 0)
            self.rect.centerx -= 2
            hits = pg.sprite.spritecollide(self, self.game.invis_wall, False)
            self.rect.centerx += 2
            if hits:
                self.facing = False

    def draw_health(self):
        if self.health > 120:
            self.col = GREEN
        elif self.health > 50:
            self.col = YELLOW
        else:
            self.col = RED
        width = int(self.rect.width * self.health / 150)
        self.health_bar = pg.Rect(0, 0, width, 2)
        if self.health < 150:
            pg.draw.rect(self.image, self.col, self.health_bar)
            self.load_images()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > MOB_BULLET_RATE:
            self.last_shot = now
            pos = self.pos
            angle = 180
            dir = vec(-1, 0)
            Mob_Bullet(self.game, pos, dir, angle)
            angle = 0
            dir = vec(1, 0)
            Mob_Bullet(self.game, pos, dir, angle)
            angle = 90
            dir = vec(0, -1)
            Mob_Bullet(self.game, pos, dir, angle)
            angle = 270
            dir = vec(0, 1)
            Mob_Bullet(self.game, pos, dir, angle)

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Spike(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.spike
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Fall(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.fall_death
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Boundary(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.boundary
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Invis_wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.invis_wall
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Win_area(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.win_game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_image()
        self.image = self.item_images[type]
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 20, 17)
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
            self.item_images[item] = pg.image.load(chicken[item]).convert_alpha()
        for item in coin:
            self.item_images[item] = pg.image.load(coin[item]).convert_alpha()