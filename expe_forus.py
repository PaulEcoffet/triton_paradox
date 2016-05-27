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
source = 'stim/Sounds_press'


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
    #random.shuffle(stim)
    return stim

def gen_all_stim(nb, notes, intervals):
    stim = []
    for note in notes:
        for interval in intervals:
            stim.extend([(note, (note + interval) % 12)] * nb)
    #random.shuffle(stim)
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
        sound = sounds[notes[stim[i]]]
        pygame.display.flip()
        sound.play()
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < 300:
            pygame.time.wait(15)
        sound.stop()
        window.fill(black)
        #txt = font.render(str(pygame.time.get_ticks() - start), True, white)
        #window.blit(txt, pos)
        pygame.display.flip()
        if i == 0:  # If first then wait (interstim)
            pygame.time.wait(100)

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
    window = pygame.display.set_mode([0, 0], pl.FULLSCREEN)
    pygame.mouse.set_visible(False)
    sounds = get_sounds(source)
    font = pygame.font.SysFont('sans', 40)


    with open('results/for_us/'+str(int(time.time()))+'_'+subject+'.csv', 'w') as f:
    ###########
    # PHASE 1 #
    ###########
    
        window.fill(black)
        blabla = font.render("Appuyer sur 'f' si l'intervalle est descendant, sur 'j' s'il est montant", True, white)
        valid = font.render("Veuillez appuyer sur entree quand vous etes pret", True, white)
        pos_bla = blabla.get_rect(midbottom=window.get_rect().center)
        pos_valid = valid.get_rect(midtop=window.get_rect().center)
        window.blit(blabla, pos_bla)
        window.blit(valid, pos_valid)
        pygame.display.flip()
        pygame.event.get() # clear buffer
        next_step = False
        while not next_step:
            e = pygame.event.wait()
            if e.type == pl.KEYDOWN and e.key == pl.K_RETURN:
                next_step = True

        cond = '1'
        stims1 = gen_stim(nb_stim_per_interval, [1, 2, 3, 4, 8, 9, 10, 11]) #24
        stims2 = gen_all_stim(4, list(range(12)), [5, 6, 7])  #108
        all_stims=stims1+stims2
        random.shuffle(all_stims)
        nb_stim=len(all_stims)  #132
        print ('subject', 'cond', 'note1', 'note2', 'resp', 'rt', sep=',', file=f)
        i=0
        for stim in all_stims:
            i=i+1
            resp, rt = do_trial(stim, window, sounds)
            if resp == 'Quit':
                raise Exception()
            print (subject, cond, stim[0], stim[1], resp, rt, file=f, sep=',')
            if i == nb_stim/3+1:
                valid = font.render("Ptite pause, appuyez sur entree quand vous etes pret", True, white)
                pos_valid = valid.get_rect(midtop=window.get_rect().center)
                window.blit(valid, pos_valid)
                pygame.display.flip()
                pygame.event.get() # clear buffer
                next_step = False
                while not next_step:
                    e = pygame.event.wait()
                    if e.type == pl.KEYDOWN and e.key == pl.K_RETURN:
                        next_step = True
                i=0

    ###########
    # PHASE 2 #
    ###########
        
##        for phase in [2,3]:
##            valid = font.render("Ptite pause, appuyez sur entree quand vous etes pret", True, white)
##            pos_valid = valid.get_rect(midtop=window.get_rect().center)
##            window.blit(valid, pos_valid)
##            pygame.display.flip()
##            pygame.event.get() # clear buffer
##            next_step = False
##            while not next_step:
##                e = pygame.event.wait()
##                if e.type == pl.KEYDOWN and e.key == pl.K_RETURN:
##                    next_step = True
##            cond = str(phase)
##            random.shuffle(stims)
##            for stim in stims:
##                resp, rt = do_trial(stim, window, sounds)
##                if resp == 'Quit':
##                    raise Exception()
##                print (subject, cond, stim[0], stim[1], resp, rt, file=f, sep=',')

try:
    expe()
finally:
    pygame.quit()
