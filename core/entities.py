from random import randint, choice
import pygame
from pygame.locals import *
import numpy as np
from core.settings import SCREEN_SIZE
from core.states import (StateMachine, AntStateDelivering, AntStateExploring,
                         AntStateHunting, AntStateSeeking)


class GameEntity(object):

    def __init__(self, world, name, image):
        self.world = world
        self.name = name
        self.image = image
        self.location = np.array([0, 0])
        self.destination = np.array([0, 0])
        self.speed = 0
        self.brain = StateMachine()

    def render(self, surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))

    def process(self, time_passed):
        self.brain.think()

        if self.speed > 0 and any(self.location != self.destination):

            vec_to_destination = self.destination - self.location
            distance_to_destination = len(vec_to_destination)
            heading = np.sqrt((vec_to_destination**2).astype(int))/2

            travel_distance = min(
                distance_to_destination, time_passed * self.speed
            )
            new_location = self.location + (travel_distance * heading)

            if new_location[0] > SCREEN_SIZE[0]:
                new_location[0] = randint(1, SCREEN_SIZE[0]/2)

            if new_location[1] > SCREEN_SIZE[1]:
                new_location[0] = randint(1, SCREEN_SIZE[1]/2)

            self.location = new_location


class Spider(GameEntity):
    def __init__(self, world, image):
        super().__init__(world, 'spider', image)
        self.dead_image = pygame.transform.flip(image, 0, 1)
        self.health = 25
        self.speed = 0.5

    def bitten(self):
        self.health -= 1
        if self.health <= 0:
            self.speed = 0
            self.image = None

        self.speed = 0.2

    def render(self, surface):
        super().render(surface)

        x, y = self.location
        w, h = self.image.get_size()
        bar_x = x - 12
        bar_y = y + h/2
        surface.fill((255, 0, 0), (bar_x, bar_y, 25, 4))
        surface.fill((0, 255, 0), (bar_x, bar_y, self.health, 4))

    def process(self, time_passed):
        x, y = self.location
        x += randint(-1, 1)
        y += randint(-1, 1)

        max_x, max_y = SCREEN_SIZE

        if x > max_x:
            x = randint(1, max_x/2)

        if y > max_y:
            y = randint(1, max_y/2)

        self.location = np.array([x, y])

        super().process(time_passed)


class Leaf(GameEntity):
    def __init__(self, world, name, image):
        super().__init__(world, 'leaf', image)


class Ant(GameEntity):
    def __init__(self, world, name, image):
        super().__init__(world, 'ant', image)

        # Instancia os estados
        exploring_state = AntStateExploring(self)
        seeking_state = AntStateSeeking(self)
        delivering_state = AntStateDelivering(self)
        hunting_state = AntStateHunting(self)

        states = [
            exploring_state,
            seeking_state,
            delivering_state,
            hunting_state
        ]

        # Adiciona os estados ao cérebro
        for state in states:
            self.brain.add_state(state)

        self.carry_image = None
        self.speed = 0.6

    def carry(self, image):
        self.carry_image = image

    def drop(self, surface):
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()

            surface.blit(self.carry_image, (x-1, y-1))
            self.carry_image = None

    def render(self, surface):
        super().render(surface)

        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x-w, y-h/2))
