from settings import *
import numpy as np
import random

rabbits_alive = []
wolves_alive = []

class Animal():
    def __init__(self, position, age=0):
        # self.age = np.random.randint(TR_d)
        self.age = age
        self.position = np.array(position)
        self.alive = True

    def get_direction(self):
        # Step lenght sampled from N(0, sigma)
        step_length = np.random.normal(0, sigma)
        # direction is chosen randomly from a random unit vector
        v = np.random.ranf(2)
        direction = v / np.linalg.norm(v)
        return step_length * direction
    
    def check_in_boundary(self):
        if self.position[0] > L:
                self.position[0] = self.position[0] - L
        elif self.position[0] < 0:
            self.position[0] = L - abs(self.position[0])

        if self.position[1] > L:
            self.position[1] = self.position[1] - L
        elif self.position[1] < 0:
            self.position[1] = L - abs(self.position[1])

    def die(self):
        # TODO better way to die???
        self.alive = False

class Rabbit(Animal):
    def __init__(self, position, age=0):
        self.race = 'Rabbit'
        super().__init__(position, age)

    def move(self):
        if not self.alive:
            return

        direction = self.get_direction()
        self.position = self.position + direction
        self.check_in_boundary()

        self.age += 1
        if self.age > TR_d:
            self.die()
        else:
            self.replicate()
       
    def replicate(self):
        if np.random.rand(1) < PR_r:
        # if np.random.binomial(1, PR_r):
            child = Rabbit(self.position)
            rabbits_alive.append(child)


class Wolf(Animal):
    def __init__(self, position, age=0):
        self.hunger = 0 # A wolf is hunger for its prey
        self.race = "Wolf"
        super().__init__(position, age)

    def move(self):
        if self.hunger >= TW_d:
            self.die()
        if not self.alive:
            return
        direction = self.get_direction()
        self.position = self.position + direction
        self.check_in_boundary()

        self.eat()
        # self.hunger += 1

    def find_prey(self):
        prey = []
        for rabbit in rabbits_alive:
            if np.linalg.norm(rabbit.position - self.position) <= r_c:
                if rabbit.alive: 
                    # additional check. There may be dead rabbits to be yet clean
                    prey.append(rabbit)
        return prey

    def eat(self):
        prey = self.find_prey()
        if len(prey) == 0:
            self.hunger += 1
            # return
        else:
            for rabbit in prey:
                if np.random.rand(1) < PW_e:
                # if np.random.binomial(1, PW_e):
                    self.hunger = 0
                    rabbit.alive = False
                    self.replicate()

    def replicate(self):
        if np.random.rand(1) < PR_w:
        # if np.random.binomial(1, PR_w):
            child = Wolf(self.position)
            wolves_alive.append(child)
    