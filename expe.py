import pygame
import pygame.locals as pl

import random

white = (255, 255, 255)
black = (0, 0, 0)

notes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
nb_stim_per_interval = 3

def gen_stim(nb_per_interval):
    stim = []
    for i in range(1, 12):
        for j in range(nb_per_interval):
            note = random.randint(0, 11)
            next_note = (note + i) % 12
            stim.append((note, next_note))

    random.shuffle(stim)
    return stim

def do_trial(stim, window):
    font = pygame.font.SysFont('sans', 40)
    window.fill(black)
    pygame.draw.circle(window, white, window.get_rect().center, 4)
    pygame.display.flip()
    pygame.time.wait(1000)
    for i in range(2):
        window.fill(black)
        txt = font.render(notes[stim[i]], True, white)
        pos = txt.get_rect(center=window.get_rect().center)
        window.blit(txt, pos)
        pygame.display.flip()
        pygame.time.wait(1000)

    return 0, 1


def expe():
    pygame.init()
    window = pygame.display.set_mode([800, 600])
    stims = gen_stim(nb_stim_per_interval)
    for stim in stims[:2]:
        resp, rt = do_trial(stim, window)
try:
    expe()
finally:
    pygame.quit()
