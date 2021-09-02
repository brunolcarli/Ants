"""
Define mecâncias de funcinamento.
"""
from random import randint, choice
import pygame
from pygame.locals import *
import numpy as np
from core.settings import SCREEN_SIZE, ANT_COUNT
from core.world import World
from core.entities import Ant, Leaf, Spider


def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

    world = World()
    w, h = SCREEN_SIZE
    clock = pygame.time.Clock()

    import os
    print(os.getcwd())

    ant_image = pygame.image.load('static/img/ant.png').convert_alpha()
    leaf_image = pygame.image.load('static/img/leaf.png').convert_alpha()
    spider_image = pygame.image.load('static/img/spider.png').convert_alpha()

    for _ in range(ANT_COUNT):
        ant = Ant(world, 'ant', ant_image)
        ant.location = np.array([randint(0, w/2), randint(0, h/2)])
        ant.brain.set_state('exploring')
        world.add_entity(ant)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

        time_passed = clock.tick(30)
        if choice([True, False]):
            leaf = Leaf(world, 'leaf', leaf_image)
            leaf.location = np.array([randint(0, w/2), randint(0, h/2)])
            world.add_entity(leaf)

        if randint(1, 25) == 1:
            spider = Spider(world, spider_image)
            spider.location = np.array([w-5, randint(0, h/2)])
            spider.destination = np.array([w+5, randint(0, h/2)])
            world.add_entity(spider)

        world.process(time_passed)
        world.render(screen)

        pygame.display.update()
