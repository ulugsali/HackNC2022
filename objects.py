import pygame, sys
import const
from pygame.locals import *

class Wall:
    rect: pygame.Rect
    def __init__(self, wall_x: int, wall_y: int, height: int, width: int) -> None:
        surf = pygame.image.load(const.PILL).convert()
        self.surf = pygame.transform.scale(surf, (const.OBS_SIZE, const.OBS_SIZE))
        self.surf.set_colorkey(const.WHITE, RLEACCEL)
        self.rect = pygame.Rect(wall_x, wall_y, width, height)

class Player:
    vel_x: int
    vel_y: int
    is_flipped: bool = False

    def __init__(self) -> None:
        surface = pygame.image.load(const.PLAYER_FILENAME).convert()
        self.surf = pygame.transform.scale(surface, (80, 80))
        self.surf.set_colorkey((const.WHITE), RLEACCEL)
        self.rect = self.surf.get_rect(center = (50, 50))
        self.vel_x = 0
        self.vel_y = 0

    def update(self, pressed_keys) -> None:
        if self.vel_y == 0 and (pressed_keys[K_s] or pressed_keys[K_DOWN]):
            self.vel_y += const.JUMP
        if self.vel_y == 0 and (pressed_keys[K_w] or pressed_keys[K_UP]):
            self.vel_y -= const.JUMP
        if pressed_keys[K_a] or pressed_keys[K_LEFT]:
            self.vel_x -= const.MOVEMENT
            if self.is_flipped is False:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.is_flipped = True
        if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
            self.vel_x += const.MOVEMENT
            if self.is_flipped is True:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.is_flipped = False
        
        if self.rect.centerx > const.WIDTH:
            self.rect.centerx = const.WIDTH - 5
            self.vel_x = -5
        elif self.rect.centerx < 0:
            self.vel_x = 5
            self.rect.centerx = 5
        elif self.rect.centery < 0:
            self.vel_y = 0
            self.rect.centery = 5
    
    def collide(self, walls) -> bool:
        for wall in walls:
            if wall.rect.colliderect(self.rect):
                return True
            return False

class Background:
    x: int
    y: int
    reverse: bool = False
    def __init__(self) -> None:
        surface = pygame.image.load(const.BACKGROUND_FILENAME).convert()
        self.surf = pygame.transform.scale(surface, (const.WIDTH * 2, const.HEIGHT))
        
        # Set the x and y to start at 0
        self.x = 0
        self.y = 0

    def render(self, screen):
        screen.blit(self.surf, (self.x, self.y))

    def update(self, timer: int):
        self.x -= 20
        if self.x <= -640:
            self.x = 0
            if self.reverse is False:
                surface = pygame.image.load(const.BACKGROUND_FILENAME1).convert()
                self.surf = pygame.transform.scale(surface, (const.WIDTH * 2, const.HEIGHT))
                self.reverse = True
            else:
                surface = pygame.image.load(const.BACKGROUND_FILENAME).convert()
                self.surf = pygame.transform.scale(surface, (const.WIDTH * 2, const.HEIGHT))
                self.reverse = False

class Loser:
    
    def __init__(self, player: Player) -> None:
            self.surf = pygame.image.load(const.KIM).convert()
            self.surf = pygame.transform.scale(self.surf, (200, 200)) 
            self.rect = self.surf.get_rect(center = (player.rect.centerx, player.rect.centery))   

class Score:

    def __init__(self, timer: int) -> None:
        pygame.font.init()
        self.my_font = pygame.font.SysFont(None, 30)
        self.text_surface = self.my_font.render(f'{timer*60} points', True, const.BLACK)
        self.font_rect = self.text_surface.get_rect(center=(const.WIDTH/2, const.HEIGHT-40))

    def end(self, timer: int) -> None:
        self.text_surface = self.my_font.render(f'You scored {timer * 60} points!', True, const.BLACK)
        self.font_rect = self.text_surface.get_rect(center=(const.WIDTH/2, const.HEIGHT-40))

    def restart(self) -> None:
        self.text_surface = self.my_font.render(f'To close, press escape, to restart press any other key.', True, const.BLACK)
        self.font_rect = self.text_surface.get_rect(center=(const.WIDTH/2, const.HEIGHT-20))
    
    def highscore(self) -> None:
        self.text_surface = self.my_font.render(f'New High Score! Congrats!', True, const.BLACK)
        self.font_rect = self.text_surface.get_rect(center=(const.WIDTH/2, const.HEIGHT-60))

    def lower_score(self, highscore: int) -> None:
        self.text_surface = self.my_font.render(f'The highscore is: {highscore}', True, const.BLACK)
        self.font_rect = self.text_surface.get_rect(center=(const.WIDTH/2, const.HEIGHT-60))