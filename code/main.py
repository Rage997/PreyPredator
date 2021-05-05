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
    rabbits_alive.append(Rabbit(position, age=np.random.randint(TR_d)))

for _ in range(Nw):
    position = np.random.uniform(0, L, size=(1, 2)).flatten()
    wolves_alive.append(Wolf(position, age=np.random.randint(TR_d)))

# Used for plotting system state
rab_alive_in_time = [Nr] 
wolf_alive_in_time = [Nw]

# TODO check this! change into two for loops, one for each agent
for t in range(0, T):
    animals = np.random.permutation(rabbits_alive + wolves_alive)
    for animal in animals:
        if animal.alive:
            animal.move()
    
        elif not animal.alive:
            # print('Killing animal: ', animal.race)
            if animal.race == "Wolf":
                wolves_alive.remove(animal)
            elif animal.race == "Rabbit":
                rabbits_alive.remove(animal)
            else:
                raise ValueError('Unknown animal race')
    Nr, Nw = len(rabbits_alive), len(wolves_alive)
    # print(Nr, Nw)
    rab_alive_in_time.append(Nr)
    wolf_alive_in_time.append(Nw)
    
    # ------ Uncomment if you want to plot the system ----
    # if t % 250 == 0:
    #     plot_ecosystem(t)

print('Wolves alive in time:')
print(wolf_alive_in_time[500:])
print('Rabbits alive in time:')
print(rab_alive_in_time[500:])

# plot evolution of the system
fig, ax1 = plt.subplots(nrows=1, ncols=1) # two axes on figure

t = np.arange(T+1)
ax1.plot()
ax1.plot(t, rab_alive_in_time, 'bo')
ax1.plot(t, wolf_alive_in_time, 'r-')
ax1.set_yscale('log')
ax1.legend(['Rabbits', 'Wolves'])
plt.title('Animals alive at each timestep')
plt.xlabel('Time')
plt.ylabel('Animals alive')
plt.savefig('./plot.png')