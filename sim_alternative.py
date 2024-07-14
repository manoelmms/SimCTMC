# Simulation for a M/M/1 FIFO queue with Poisson arrivals and exponential service times
# Exercice 8.27 from Upfal and Mitzenmacher book of Probability and Computing

# Poisons arrivals with rate lambda < 1 [0.5; 0.8; 0.9; 0.99]
# Exponential service times with rate mu = 1 (seconds)
# Simulation time = 10000 seconds
# # Number of M/M/1 FIFO queues = 100

import math
import random
import numpy as np
import matplotlib.pyplot as plt

# https://introcs.cs.princeton.edu/python/43stack/mm1queue.py 

def exponential_random_variable(rate):
    return -math.log(random.uniform(0,1)) / rate # Inverse of the CDF of the exponential distribution
    # return random.expovariate(rate) # Python built-in function for exponential random variable


def simulation(arrival_rate, service_rate, sim_time):
    next_arrival = exponential_random_variable(arrival_rate)
    next_service = next_arrival + exponential_random_variable(service_rate)
    time = 0

    while True:



if __name__ == "__main__":
    arrival_rate = 0.9 # lambda
    service_rate = 1 # mu
    simulation_time = 10000
    number_of_queues = 1
    t = 0
    done = 0

    arrival_times = poisson_random_variable(number_of_queues * arrival_rate, simulation_time)
    # print(arrival_times)
    queue_time = np.zeros(number_of_queues)
    

    while True:
        arrival_time = arrival_times.pop(0) # Get the first element of the list # 1s -> 4

        # Uniformly choose a queue
        queue_index = random.randint(0, number_of_queues-1)
        job_time = exponential_random_variable(service_rate)
        
        #tempo q o ultimo job saiu - o tempo que eu cheguei = 25 - 15 = 10
        between_time = queue_time[queue_index] - arrival_time # FIXME
        if between_time < 0:
            between_time = 0
        #queue_time[queue_index] = waiting_time + job_time
        # t = 2, e = 1, [3.25], T = (3.25 - 2 + 1), [3.25 + T]
        #2 * 3.25 - arrival + job_time
        
        queue_time[queue_index] = queue_time[queue_index] + between_time + job_time

        #t = queue_time[queue_index]

        #print(queue_time[queue_index])
        print(f"({queue_index}, {queue_time[queue_index]}, {arrival_time}, {job_time}, {between_time})")
        #1° fila -> 9998.2 + 3, 2° -> 9998.5 + 1

        if queue_time[queue_index] <= simulation_time:
            done+=1
        if arrival_times == []:
            break
    # print(simulation_time)
    print(done)
    print(done/simulation_time)
    print(simulation_time/done)