# -*- coding: utf8 -*-

from __future__ import print_function

import time
import pygame
import pygame.locals as pl
import os.path


import random

white = (255, 255, 255)
black = (0, 0, 0)

notes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
nb_stim_per_interval = 3
source = 'stim/sounds_eb_30'


def get_sounds(source):
    sounds = dict()
    for note in notes:
        s = pygame.mixer.Sound(os.path.join(source, note + '.wav'))
        sounds[note] = s
    return sounds

def gen_stim(nb_per_interval):
    stim = []
    intervals = list(range(1, 12)) * nb_per_interval
    note = random.randint(0, 11)
    note2 = (note + intervals[0]) % 12
    stim.append((note, note2))
    for interval in intervals[1:]:
        while note in stim[-1] or note2 in stim[-1]:  # On retire les notes si l'une d'entre elle était présente juste avant
            note = random.randint(0, 11)
            note2 = (note + interval) % 12
        stim.append((note, note2))

    return stim

def do_trial(stim, window, sounds):
    ch = pygame.mixer.find_channel()
    font = pygame.font.SysFont('sans', 40)
    window.fill(black)
    pygame.draw.circle(window, white, window.get_rect().center, 4)
    pygame.display.flip()
    pygame.time.wait(1000)
    for i in range(2):
        window.fill(black)
        #txt = font.render(notes[stim[i]], True, white)
        #pos = txt.get_rect(center=window.get_rect().center)
        #window.blit(txt, pos)
        ch.play(sounds[notes[stim[i]]])
        pygame.display.flip()
        while ch.get_busy():
            pygame.time.delay(50)
        if i == 0:  # If first then wait (interstim)
            pygame.time.delay(300)

    rep = None
    start = pygame.time.get_ticks()
    while rep is None:
        event = pygame.event.wait()
        if event.type == pl.KEYDOWN:
            if event.unicode == 'f':
                rep = -1
            elif event.unicode == 'j':
                rep = 1
            elif event.key == pl.K_ESCAPE:
                return 'Quit', 0
    return rep, pygame.time.get_ticks() - start


def expe():
    subject = raw_input("subject> ")
    cond = raw_input("condition [f]: plat, [c]: cloche> ")
    cond = 'c'  # TODO Implement different conditions
    pygame.init()
    window = pygame.display.set_mode([0, 0], pl.FULLSCREEN)
    sounds = get_sounds(source)
    stims = gen_stim(nb_stim_per_interval)
    with open('results/'+subject+'_'+str(int(time.time()))+'.csv', 'w') as f:
        print ('subject', 'cond', 'note1', 'note2', 'resp', 'rt', sep=',', file=f)
        for stim in stims:
            resp, rt = do_trial(stim, window, sounds)
            if resp == 'Quit':
                break
            print (subject, cond, stim[0], stim[1], resp, rt, file=f, sep=',')
try:
    expe()
finally:
    pygame.quit()
