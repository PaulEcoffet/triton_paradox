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

def gen_stim(nb_per_interval, intervals_to_do):
    stim = []
    intervals = intervals_to_do * nb_per_interval
    note = random.randint(0, 11)
    note2 = (note + intervals[0]) % 12
    stim.append((note, note2))
    for interval in intervals[1:]:
        while note in stim[-1] or note2 in stim[-1]:  # On retire les notes si l'une d'entre elle était présente juste avant
            note = random.randint(0, 11)
            note2 = (note + interval) % 12
        stim.append((note, note2))
    random.shuffle(stim)
    return stim

def gen_all_stim(nb, notes, intervals):
    stim = []
    for note in notes:
        for interval in intervals:
            stim.extend([(note, (note + interval) % 12)] * nb)
    random.shuffle(stim)
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
        txt = font.render(notes[stim[i]], True, white)
        pos = txt.get_rect(center=window.get_rect().center)
        window.blit(txt, pos)
        sound = sounds[notes[stim[i]]]
        pygame.display.flip()
        sound.play()
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < 490:
            pygame.time.wait(15)
        sound.stop()
        window.fill(black)
        txt = font.render(str(pygame.time.get_ticks() - start), True, white)
        window.blit(txt, pos)
        pygame.display.flip()
        if i == 0:  # If first then wait (interstim)
            pygame.time.wait(300)

    rep = None
    start = pygame.time.get_ticks()
    pygame.event.get()
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
    #cond = raw_input("condition [f]: plat, [c]: cloche> ")
    #cond = 'c'  # TODO Implement different conditions
    pygame.mixer.pre_init(44100,-16,2, 1024)
    pygame.init()
    window = pygame.display.set_mode([400, 400])
    sounds = get_sounds(source)


    with open('results/'+subject+'_'+str(int(time.time()))+'.csv', 'w') as f:
    ###########
    # PHASE 1 #
    ###########
        cond = '1'
        stims = gen_stim(nb_stim_per_interval, [1, 2, 3, 4, 8, 9, 10, 11])
        print ('subject', 'cond', 'note1', 'note2', 'resp', 'rt', sep=',', file=f)
        for stim in stims:
            resp, rt = do_trial(stim, window, sounds)
            if resp == 'Quit':
                raise Exception()
            print (subject, cond, stim[0], stim[1], resp, rt, file=f, sep=',')

    ###########
    # PHASE 2 #
    ###########
        stims = gen_all_stim(3, list(range(12)), [5, 6, 7])
        for phase in [2,3]:
            cond = str(phase)
            random.shuffle(stims)
            for stim in stims:
                resp, rt = do_trial(stim, window, sounds)
                if resp == 'Quit':
                    raise Exception()
                print (subject, cond, stim[0], stim[1], resp, rt, file=f, sep=',')
try:
    expe()
finally:
    pygame.quit()
