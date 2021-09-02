"""
Define aspectos do ambiente.
"""
import numpy as np
import pygame
from core.settings import SCREEN_SIZE, NEST_POSITION, NEST_SIZE


class World(object):
    def __init__(self):
        self.entities = {}
        self.entity_id = 0

        # desenha o ambiente
        self.background = pygame.surface.Surface(SCREEN_SIZE).convert()  # TODO
        self.background.fill((255, 255, 255))
        pygame.draw.circle(
            self.background,
            (200, 255, 255),
            NEST_POSITION,
            int(NEST_SIZE)
        )

    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):
        del self.entities[entity.id]

    def get(self, entity_id):
        return self.entities.get(entity_id)

    def process(self, time_passed):
        time_passed_seconds = time_passed / 1000.0

        for entity in list(self.entities.values()):
            entity.process(time_passed_seconds)

    def render(self, surface):
        surface.blit(self.background, (0, 0))
        for entity in self.entities.values():
            entity.render(surface)

    def get_close_entity(self, name, location, e_range=100):
        location = np.array(location)

        for entity in list(self.entities.values()):
            if entity.name == name:
                distance = location - entity.location
                if any(distance < e_range):
                    return entity
