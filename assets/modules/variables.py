import pygame
pygame.init()
vec = pygame.math.Vector2

#Game

#WIDTH = 512
#HEIGHT = 400

WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#Player
PLAYER_HEALTH = 200
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_HIT_RECT = pygame.Rect(0, 0, 30, 45)
PLAYER_HIT_RECT2 = pygame.Rect(0, 0, 30, 45)
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
BARREL_OFFSET_R = vec(32, -10)
BARREL_OFFSET_L = vec(-32, -10)
BARREL_OFFSET_RUN_R = vec(32, 5)
BARREL_OFFSET_RUN_L = vec(-32, 5)
DAMAGE_ALPHA = [i for i in range(40, 255, 25)]

#Gun
BULLET_SPEED = 7
BULLET_LIFETIME = 1000
BULLET_RATE = 150
BULLET_DAMAGE = 10

#Sounds
ENEMY_HURT = {'enemy_hurt': 'enemy_hurt.wav'}
ENEMY_MORPH = {'morph': 'morph.wav'}
PLAYER_JUMP = {'jump': 'jump.wav'}
PLAYER_HURT = {'player_hurt': 'player_hurt.wav'}
SHOOT_SOUND = {'shoot': 'shoot.wav'}
EFFECTS_SOUND = {'collect': 'health.wav'}
COIN = {'coin': 'coin.wav'}

#Mob
MOB_SPEED = vec(0.2, 0.5)
MOB_HIT_RECT = pygame.Rect(0, 0, 24, 36)
MOB_CHARGE_HIT_RECT = pygame.Rect(0, 0, 24, 30)
MOB_BIG_HIT_RECT = pygame.Rect(0, 0, 24, 36)
MOB_FLYING_HIT_RECT = pygame.Rect(0, 0, 24, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 30
MOB_KNOCKBACK_CHARGE = 30
MOB_BULLET_RATE = 2500
MOB_BULLET_SPEED = 2
MOB_BULLET_LIFETIME = 5000
DETECT_RADIUS = 150
