import pygame

pygame.init()


def background_sound():
    pygame.mixer.music.load('resources/background.wav')
    pygame.mixer.music.play(-1)


def explosion_sound():
    pygame.mixer.Sound('resources/explosion.wav').play()


def bullet_sound():
    pygame.mixer.Sound('resources/bullet.wav').play()
