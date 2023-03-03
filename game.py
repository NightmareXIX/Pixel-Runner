import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walks = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.player_animation_idx = 0

        self.jump_sound = pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.5)

        self.image = self.player_walks[self.player_animation_idx]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def animate_player(self):
        self.player_animation_idx += 0.1
        if self.player_animation_idx >= len(self.player_walks):
            self.player_animation_idx = 0
        # jump
        if self.rect.bottom < 300: self.image = player_jump
        # walk
        else: self.image = self.player_walks[int(self.player_animation_idx)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate_player()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type=='snail':
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300
        else:
            fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210

        self.frame_idx = 0
        self.image = self.frames[self.frame_idx]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
        self.obstacles = []

    def animate_obstacle(self):
        self.frame_idx += 0.1
        if self.frame_idx >= len(self.frames):
            self.frame_idx = 0
        self.image = self.frames[int(self.frame_idx)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animate_obstacle()
        self.rect.x -= 7
        self.destroy()


def get_time(x):
    current_time = int((pygame.time.get_ticks() - x) / 1000)
    score_surf = text.render(f'{current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_generator(rect_list):
    if rect_list:
        for rt in rect_list:
            rt.x -= 5
            if rt.bottom == 300:
                screen.blit(snail_surf, rt)
            else:
                screen.blit(fly_surf, rt)

        rect_list = [rt for rt in rect_list if rt.x >= -100]
        return rect_list
    else:
        return []


def collide(player, rect_list):
    if rect_list:
        for rt in rect_list:
            if player.colliderect(rt):
                global game_active
                game_active = False


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle, False):
        obstacle.empty()
        return False
    else: return True


def player_animation():
    global player_surf, player_idx
    player_idx += 0.1
    if player_idx >= len(player_walks):
        player_idx = 0
    # jump
    if player_rect.bottom < 300:
        player_surf = player_jump
    # walk
    else:
        player_surf = player_walks[int(player_idx)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
# set title of window
pygame.display.set_caption("Runner")
# set fps of while loop
clock = pygame.time.Clock()
start_time = 0
score = 0

# Sprite: Player
player = pygame.sprite.GroupSingle()
player.add(Player())

# Sprite: Obstacles
obstacle = pygame.sprite.Group()

# import font
text = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
# import sound
game_sound = pygame.mixer.Sound('audio/music.wav')
game_sound.play(loops=-1)

# import surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()

ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_rect = ground_surface.get_rect(topleft=(0, 300))

# score_surf = text.render('Score', False, '#2b2859')
# score_rect = score_surf.get_rect(center = (400, 50))

play_surf = text.render('Play', False, '#2b2859')
play_rect = play_surf.get_rect(center=(400, 70))

title = text.render('Pixel  Runner', False, '#2b2859')
title_rect = title.get_rect(midtop=(400, 10))

# Snail
snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_idx = 0
snail_surf = snail_frames[snail_idx]

# Fly
fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_idx = 0
fly_surf = fly_frames[fly_idx]

obstacle_rect_list = []

# Player
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_walks = [player_walk_1, player_walk_2]
player_idx = 0

player_surf = player_walks[player_idx]
player_rect = player_surf.get_rect(midbottom=(70, 300))
gravity = 0

player_stand = pygame.image.load('graphics/Player/player_stand.png')
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# Instructions
ins1 = text.render('Press SPACE to start/JUMP', False, '#2b2859')
ins1_surf = ins1.get_rect(center=(400, 360))

# user event
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1700)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 500)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

while True:
    for event in pygame.event.get():
        # close window
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                if player_rect.collidepoint(event.pos):
                    gravity = -20
            if event.type == pygame.KEYDOWN and player_rect.bottom == 300:
                if event.key == pygame.K_SPACE:
                    gravity = -20
            if event.type == obstacle_timer:
                obstacle.add(Obstacle(choice(['fly', 'snail', 'snail'])))
                # if randint(0, 2):
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomleft=(randint(900, 1100), 300)))
                #     obstacle.add(Obstacle('snail'))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomleft=(randint(1000, 1200), 210)))
                #     obstacle.add(Obstacle('fly'))
            if event.type == snail_timer:
                if snail_idx: snail_idx = 0
                else: snail_idx = 1
                snail_surf = snail_frames[snail_idx]

            if event.type == fly_timer:
                if fly_idx: fly_idx = 0
                else: fly_idx = 1
                fly_surf = fly_frames[fly_idx]

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    game_active = True
                    start_time = pygame.time.get_ticks()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()


    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, ground_rect)
    if game_active:
        score = get_time(start_time)
        # place surfaces
        # pygame.draw.rect(screen, (45, 170, 204), score_rect)
        # pygame.draw.line(screen, 'Red', (0, 0), pygame.mouse.get_pos(), 10)
        # screen.blit(score_surf, score_rect)

        # snail_rect.left -= 5
        # if snail_rect.right <= 0: snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)
        # obstacle_rect_list = obstacle_generator(obstacle_rect_list)

        # Player
        # gravity += 1
        # player_rect.y += gravity
        # if player_rect.bottom >= 300: player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf, player_rect)

        # Sprite player
        player.draw(screen)
        player.update()
        # Sprite obstacle
        obstacle.draw(screen)
        obstacle.update()



        # Collision
        game_active = collision_sprite()
        # collide(player_rect, obstacle_rect_list)

        # enemy collision
        # if snail_rect.colliderect(player_rect):
        #     game_active = False

    else:
        # start screen
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        # display info
        if score:
            play_surf = text.render(f'Score: {score}', False, '#2b2859')
            play_rect = play_surf.get_rect(center=(400, 70))
        # border for play button
        pygame.draw.rect(screen, '#8c8db8', pygame.transform.rotozoom(play_surf, 0, 1.3).get_rect(center=(400, 70)),
                         border_radius=5)
        screen.blit(play_surf, play_rect)
        screen.blit(title, title_rect)
        screen.blit(ins1, ins1_surf)

        # Reset values
        player_rect.midbottom = (70, 300)
        gravity = 0
        obstacle_rect_list.clear()

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #    print('jump')
    #
    # collision detect
    # if player_rect.colliderect(snail_rect):
    #    print(player_rect.center, snail_rect.center)
    #
    #    mouse_pos = pygame.mouse.get_pos()
    #    if player_rect.collidepoint(mouse_pos):
    #        print('collision')

    pygame.display.update()
    clock.tick(60)
