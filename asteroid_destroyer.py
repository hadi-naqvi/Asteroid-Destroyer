# Date: November 5th, 2019
# Author: Hadi Naqvi
# Description: Asteroid Destroyer Game

# Module imports
import pygame, sys, random, time
pygame.init()

# Framerate/clock setup
Clock = pygame.time.Clock()
FPS = 60

# Screen setup
window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Asteroid Destroyer By Hadi")

# Importing graphics and sounds
font = pygame.font.SysFont('Callibri', 40)
shooter_img = pygame.image.load('shooter.png')
bullet_img = pygame.image.load('bullet.png')
asteroid_img = pygame.image.load('asteroid.png')
explosion_img = [pygame.image.load('explosion0.png'), pygame.image.load('explosion1.png'), pygame.image.load('explosion2.png'), pygame.image.load('explosion3.png'), pygame.image.load('explosion4.png'), pygame.image.load('explosion5.png'), pygame.image.load('explosion6.png'), pygame.image.load('explosion7.png'), pygame.image.load('explosion8.png'), pygame.image.load('explosion9.png')]
background_img = pygame.image.load('background.jpg')
explosion_sound = pygame.mixer.Sound('explosion.wav')
shot_sound = pygame.mixer.Sound('shot.wav')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

# Essential variables needed for game
directions = (-1, 1) # -1 for left and 1 for right
x_speeds = (0.25, 0.5, 0.75, 1)
shoot_cooldown = 0
game_running = True
score = 0
wave = 1

# Classes for shooter, bullets and asteroids
class Shooter(object):
    def __init__(self, x, y, width, height, sprite):
        self.health = 10
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 15
        self.sprite = sprite
    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))

class Bullet(object):
    def __init__(self, x, y, width, height, sprite):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.sprite = sprite
    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))
    def move(self):
        self.y -= self.speed

class Asteroid(object):
    def __init__(self, x, y, width, height, x_speed, y_speed, direction, sprite):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.direction = direction
        self.sprite = sprite
    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))
    def move(self):
        self.x += self.x_speed * self.direction
        self.y += self.y_speed
    def explode(self):
        explosions.append(Explosion(self.x, self.y))

class Explosion(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.explosion_count = 0

# Updates the screen and objects
def update_screen(window):
    # Background and text
    window.blit(background_img, (0, 0))
    window.blit(font.render("Asteroid Destroyer", 1, (255, 128, 255)), (window_width - 270, 20))
    window.blit(font.render("Score: {}".format(score), 1, (255, 255, 255)), (window_width - 150, 50))
    window.blit(font.render("Wave: {}".format(int(wave)), 1, (255, 255, 255)), (window_width - 150, 80))
    window.blit(font.render("HP: {}/{}".format(round(player.health, 1), 10), 1, (255, 255, 255)), (player.x, player.y + 120))

    # Objects on screen
    player.draw(window)
    pygame.draw.rect(window, (255, 0, 0), (player.x, player.y + 100, 100, 15))
    pygame.draw.rect(window, (0, 255, 0), (player.x, player.y + 100, player.health * 10, 15))
    for asteroid in asteroids:
        asteroid.move()
        asteroid.draw(window)
    for bullet in bullets:
        bullet.move()
        bullet.draw(window)
    for explosion in explosions:
        window.blit(explosion_img[round(explosion.explosion_count // 1)], (explosion.x, explosion.y))
        explosion.explosion_count += 0.25
    
    # Updates screen
    pygame.display.update()

# Outputs a message upon losing the game and then closes the game
def lose():
    window.blit(font.render("You lose!", 1, (255, 0, 0)), (window_width / 2, window_height / 2))
    pygame.display.update()
    time.sleep(3)

# Objects on screen
player = Shooter(window_width / 2, window_height - 150, 100, 281, shooter_img)
bullets = []
asteroids = []
explosions = []

# Main game loop
while game_running:
    Clock.tick(FPS)
    # Allows the player to close the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            game_running = False
    
    # Cooldown on shooting
    if shoot_cooldown < 3:
        shoot_cooldown += 1
    elif shoot_cooldown >= 3:
        shoot_cooldown = 0
    
    # Removes explosion animation after completion
    for explosion in explosions:
        if explosion.explosion_count > 9:
            explosions.pop(explosions.index(explosion))
    
    # Detects user input
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT] and player.x >= 0:
        player.x -= player.speed
    if keys_pressed[pygame.K_RIGHT] and player.x + player.width <= window_width:
        player.x += player.speed
    if keys_pressed[pygame.K_SPACE] and len(bullets) < wave and shoot_cooldown == 0:
        bullets.append(Bullet(player.x + player.width / 2 - 10, player.y, 20, 20, bullet_img))
        shot_sound.play()
    
    # Spawns in asteroids
    while len(asteroids) < wave and shoot_cooldown == 0:
        asteroids.append(Asteroid(random.randint(0 + 100, window_width - 100), 0, 90, 96, random.choice(x_speeds), random.randint(1, 3), random.choice(directions), asteroid_img))
    
    # Collision detection
    # Checks if asteroid hits any borderes of the screen
    for asteroid in asteroids:
        if asteroid.x <= 0 or asteroid.x + asteroid.width >= window_width:
            asteroid.explode()
            asteroids.pop(asteroids.index(asteroid))
            explosion_sound.play()
            if 0 < player.health < 11:
                player.health -= 1
        elif asteroid.y >= window_height - 150:
            asteroid.explode()
            asteroids.pop(asteroids.index(asteroid))
            explosion_sound.play()
            if 0 < player.health < 11:
                player.health -= 1
        else:
            # Checks if any bullets are hitting the asteroids
            for bullet in bullets:
                if asteroid.x <= bullet.x <= asteroid.x + asteroid.width and asteroid.y <= bullet.y <= asteroid.y + asteroid.height:
                    asteroid.explode()
                    asteroids.pop(asteroids.index(asteroid))
                    bullets.pop(bullets.index(bullet))
                    explosion_sound.play()
                    if 0 < player.health < 9.9 and wave < 5:
                        player.health += 0.1
                    wave += 0.02
                    score += 2
    # Checks if bullets have reached border of screen
    for bullet in bullets:
        if bullet.y <= 0:
            bullets.pop(bullets.index(bullet))
    # Game ends if player's health is below or equal to 0
    if player.health <= 0:
        lose()
        pygame.quit()
        sys.exit()
        game_running = False
    update_screen(window)