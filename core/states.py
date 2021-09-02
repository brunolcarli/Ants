"""
Define modelos de máquina de estado.
"""
from random import randint
import numpy as np
from core.settings import SCREEN_SIZE, NEST_SIZE, NEST_POSITION


class State(object):
    def __init__(self, name):
        self.name = name

    def do_actions(self):
        ...

    def check_conditions(self):
        ...

    def entry_actions(self):
        ...

    def exit_actions(self):
        ...


class StateMachine(object):
    def __init__(self):
        self.states = {}
        self.active_state = None

    def add_state(self, state):
        self.states[state.name] = state

    def think(self):
        if self.active_state is None:
            return

        self.active_state.do_actions()

        new_state = self.active_state.check_conditions()
        if new_state is not None:
            self.set_state(new_state)

    def set_state(self, new_state):
        if self.active_state is not None:
            self.active_state.exit_actions()

        self.active_state = self.states[new_state]
        self.active_state.entry_actions()


class AntStateExploring(State):
    def __init__(self, ant):
        super().__init__('exploring')
        self.ant = ant

    def random_destination(self):
        w, h = SCREEN_SIZE
        self.ant.destination = np.array([randint(0, w), randint(0, h)])

    def do_actions(self):
        if randint(1, 20) == 1:
            self.random_destination()

    def check_conditions(self):
        leaf = self.ant.world.get_close_entity('leaf', self.ant.location)
        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return 'seeking'

        spider = self.ant.world.get_close_entity(
            'spider',
            NEST_POSITION,
            NEST_SIZE
        )

        if spider is not None:
            distance = self.ant.location - spider.location
            if any(distance < 100.):
                self.ant.spider_id = spider.id
                return 'hunting'

    def entry_actions(self):
        self.ant.speed = 0.5
        self.random_destination()


class AntStateSeeking(State):
    def __init__(self, ant):
        super().__init__('seeking')
        self.ant = ant
        self.leaf_id = None

    def check_conditions(self):
        leaf = self.ant.world.get(self.ant.leaf_id)

        if leaf is None:
            return 'exploring'

        distance = self.ant.location - leaf.location
        if any(distance < 5):
            self.ant.carry(leaf.image)
            self.ant.world.remove_entity(leaf)
            return 'delivering'

    def entry_actions(self):
        leaf = self.ant.world.get(self.ant.leaf_id)

        if leaf is not None:
            self.ant.destination = leaf.location
            self.ant.speed = 0.6


class AntStateDelivering(State):
    def __init__(self, ant):
        super().__init__('delivering')
        self.ant = ant

    def check_conditions(self):
        # if Vector2(*NEST_POSITION).get_distance_to(self.ant.location) < NEST_SIZE:
        if any(np.array(NEST_POSITION) - self.ant.location < NEST_SIZE):
            if (randint(1, 10) == 1):
                self.ant.drop(self.ant.world.background)
                return 'exploring'

    def entry_actions(self):
        self.ant.speed = 0.2
        distance = np.array(NEST_POSITION) - self.ant.location
        step = randint(int(min(distance/2)+1), int(max(distance/2))+2)
        self.ant.location = self.ant.location + step


class AntStateHunting(State):
    def __init__(self, ant):
        super().__init__('hunting')
        self.ant = ant
        self.got_kill = False

    def do_actions(self):
        spider = self.ant.world.get(self.ant.spider_id)

        if spider is None:
            return

        self.ant.destination = spider.location
        distance = self.ant.location - spider.location
        if any(distance < 15):
            if randint(1, 5) == 1:
                spider.bitten()

            if spider.health <= 0:
                self.ant.carry(spider.image)
                self.ant.world.remove_entity(spider)
                self.got_kill = True

    def check_conditions(self):
        if self.got_kill:
            return 'delivering'

        spider = self.ant.world.get(self.ant.spider_id)
        if spider is None:
            return 'exploring'

        distance = spider.location - np.array(NEST_POSITION)
        if any(distance * 3):
            return 'exploring'

    def entry_actions(self):
        self.speed = 0.6

    def exit_actions(self):
        self.got_kill = False
