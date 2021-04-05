from agents import Rabbit, Wolf, rabbits_alive, wolves_alive
import numpy as np
from settings import *
import matplotlib.pyplot as plt

def plot_ecosystem(t):
    rabbit_position = np.array([rabbit.position for rabbit in rabbits_alive])
    wolves_position = np.array([wolf.position for wolf in wolves_alive])
    
    fig, ax = plt.subplots()
    if len(rabbit_position > 0):
        ax.plot(rabbit_position[:,0], rabbit_position[:,1], 'bo')

    if len(wolves_position > 0 ):
        ax.plot(wolves_position[:,0], wolves_position[:,1], 'ro')
    ax.set_xlim([0, L])
    ax.set_ylim([0, L])

    plt.savefig('./time_step{}.png'.format(t))

# Generate the agents and distribuite them randomly over the domain
for _ in range(Nr):
    position = np.random.uniform(0, L, size=(1, 2)).flatten()
    rabbits_alive.append(Rabbit(position))

for _ in range(Nw):
    position = np.random.uniform(0, L, size=(1, 2)).flatten()
    wolves_alive.append(Wolf(position))

# Used for plotting system state
rab_alive_in_time = [Nr] 
wolf_alive_in_time = [Nw]

# TODO check this! change into two for loops, one for each agent
for t in range(0, T):
    if t % 100 == 0:
        plot_ecosystem(t)
    # animals = np.random.permutation(rabbits_alive + wolves_alive)
    i = j =0
    animals = rabbits_alive + wolves_alive
    n = len(animals)
    # the amount of animals is changing at each iteration
    
        
    while i < Nw:
# for animal in animals:
        wolf = wolves_alive[i]
        if wolf.alive:
            wolf.move()
        elif not wolf.alive:
            # print('Killing animal: ', animal.race)
            wolves_alive.remove(wolf)
        Nw = len(wolves_alive)
        i += 1
        
    while j < Nr:
        rabbit = rabbits_alive[j]
        if rabbit.alive:
            rabbit.move()
        elif not rabbit.alive:
            # print('Killing animal: ', animal.race)
                rabbits_alive.remove(rabbit)
        Nr = len(rabbits_alive)
        j += 1
        animals = rabbits_alive + wolves_alive
        n = len(animals)
        
    rab_alive_in_time.append(len(rabbits_alive))
    wolf_alive_in_time.append(len(wolves_alive))


# print('Wolves alive in time:')
# print(wolf_alive_in_time)
# print('Rabbits alive in time:')
# print(rab_alive_in_time)

# plot evolution of the system
fig, ax1 = plt.subplots(nrows=1, ncols=1) # two axes on figure

t = np.arange(T+1)
ax1.plot()
ax1.plot(t, rab_alive_in_time, 'bo')
ax1.plot(t, wolf_alive_in_time, 'r-')
ax1.legend(['Rabbits', 'Wolves'])
plt.title('Animals alive at each timestep')
plt.xlabel('Time')
plt.ylabel('Animals alive')
plt.savefig('./plot.png')