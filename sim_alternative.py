# Simulation for a M/M/1 FIFO queue with Poisson arrivals and exponential service times
# Exercice 8.27 from Upfal and Mitzenmacher book of Probability and Computing
# Second simulation with service times, instead being exponentially distributed with mean 1 second, they are always exactly 1 second

# Poisons arrivals with rate lambda < 1 [0.5; 0.8; 0.9; 0.99]
# Exponential service times with rate mu = 1 (seconds)
# Simulation time = 10000 seconds
# # Number of M/M/1 FIFO queues = 100

import math
import random
import numpy as np
import matplotlib.pyplot as plt
import time


def exponential_random_variable(rate):
    return -math.log(random.uniform(0,1)) / rate # Inverse of the CDF of the exponential distribution
    # return random.expovariate(rate) # Python built-in function for exponential random variable


def poisson_random_variable(rate, simulation_time):
    # Generate Poisson random variable using exponential random variables
    # Poisson random variable is the sum of exponential random variables with rate lambda
    t = 0
    time = []
    while t < simulation_time:
        t += exponential_random_variable(rate)
        time.append(t)
    if time[len(time)-1] > simulation_time: # Remove the last element if it is greater than 10000
        return time[:-1]
    return time


if __name__ == "__main__":
    arrival_rate_list = [0.5, 0.8, 0.9, 0.99] # lambda
    service_rate = 1 # mu
    simulation_time = 10000 # 10000 seconds
    number_of_queues = 100 # Number of M/M/1 FIFO queues
    done = 0 # Number of jobs that have been completed

    for arrival_rate in arrival_rate_list:

        arrival_times = poisson_random_variable(number_of_queues * arrival_rate, simulation_time) # Generate Poisson arrival times

        queue_free_time = np.zeros(number_of_queues) # Vector storing the time when the queue is free for each queue
        
        elapsed_time = time.time() # Timer to measure the elapsed time of the simulation for testing purposes

        while True:
            # Creating a progress bar
            print(f"\rRemaining Jobs: {len(arrival_times)}", end="")

            arrival_time = arrival_times.pop(0) # Get the first job arrival time from the list

            # Uniformly choose a queue
            queue_index = random.randint(0, number_of_queues-1)

            job_time = 1 # Service time is always 1 second
            
            # Update the queue free time

            if queue_free_time[queue_index] < arrival_time:
                queue_free_time[queue_index] = arrival_time + job_time
            else:
                queue_free_time[queue_index] += job_time

            if queue_free_time[queue_index] > simulation_time:
                pass # Ignoring job on this queue (Another servers can be available)
            else:
                done += 1

            if len(arrival_times) == 0: # Arrival list is empty
                break # Stop the simulation when all jobs have been processed

        print('\n' + '='*50) 
        print(f"-> Lambda = {arrival_rate}")
        print(f"-> Mu = {service_rate}")
        print(f"Number of jobs completed: {done}")
        print(f"{done/simulation_time} jobs per second")
        print(f"Average Time in the system per job: {simulation_time/done} seconds")
        print(f"Elapsed time in simulation: {time.time() - elapsed_time} seconds")


    print("Simulation finished!")

# Test: Why the results are the same comparing to sim_alternative.py?
