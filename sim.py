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

def simulation(arrival_rate, service_rate, simulation_time, number_of_queues):
    jobs = 0 # Number of jobs that have arrived
    done = 0 # Number of jobs that have been completed
    waiting_time = 0 # Mean waiting time of the jobs in the queue
    time_in_system = 0 # Time that the jobs spend in the system
    arrival_times = poisson_random_variable(number_of_queues * arrival_rate, simulation_time) # Generate Poisson arrival times
    queue_free_time = np.zeros(number_of_queues) # Vector storing the time when the queue is free for each queue
    
    elapsed_time = time.time() # Timer to measure the elapsed time of the simulation for testing purposes
    while True:
        # Creating a progress bar
        print(f"\rRemaining Jobs: {len(arrival_times)}", end="") # always ends with 1, but it is not a problem! 

        arrival_time = arrival_times.pop(0) # Get the first job arrival time from the list
        jobs += 1

        # Uniformly choose a queue
        queue_index = random.randint(0, number_of_queues-1)
        # print(f"\nQueue Index: {queue_index} -> Arrival Time: {arrival_time}")

        if service_rate >= 0:
            job_time = exponential_random_variable(service_rate) # Create a job with exponential service time
        else:
            job_time = 1 # Create a job with fixed service time (1 second)
        
        # Update the queue free time
        if queue_free_time[queue_index] < arrival_time:
            queue_free_time[queue_index] = arrival_time + job_time
            if queue_free_time[queue_index] <= simulation_time:
                waiting_time += 0
                time_in_system += job_time
                done += 1
        else:
            queue_free_time[queue_index] += job_time
            if queue_free_time[queue_index] <= simulation_time:
                waiting_time += queue_free_time[queue_index] - arrival_time - job_time
                time_in_system += queue_free_time[queue_index] - arrival_time
                done += 1

        if len(arrival_times) == 0: # Arrival list is empty
            break # Stop the simulation when all jobs have been processed
    
    
    print('\n' + '='*50) 
    # print(queue_free_time)
    print(f"-> Lambda = {arrival_rate}")

    if service_rate >= 0:
        print(f"-> Mu = {service_rate}")
    else:
        print(f"-> Mu = 1 (Fixed Service Time)")
    
    print(f"Number of jobs arrived: {jobs}")
    print(f"Number of jobs completed: {done}")
    print(f"Mean waiting time: {waiting_time/done}")
    print(f"Mean time in the system: {time_in_system/done}")
    print(f"Elapsed Time: {time.time() - elapsed_time}")
    print('='*50)

    return time_in_system/done, waiting_time/done

if __name__ == "__main__":
    arrival_rate_list = [0.5, 0.8, 0.9, 0.99] # lambda
    service_rate = 1 # mu
    simulation_time = 10000 # 10000 seconds
    number_of_queues = 100 # Number of M/M/1 FIFO queues

    result = []
    for arrival_rate in arrival_rate_list:
        result.append(simulation(arrival_rate, service_rate, simulation_time, number_of_queues))

    # Second exercise with fixed service rate
    service_rate = -1 # mu = 1s (Fixed)
    result_1 = []
    for arrival_rate in arrival_rate_list:
        result_1.append(simulation(arrival_rate, service_rate, simulation_time, number_of_queues))

    print("Simulation Finished!")

    # Plotting
    plt.plot(arrival_rate_list, [r[0] for r in result], label='Mean Time in System', color = 'blue', marker='o')
    plt.plot(arrival_rate_list, [r[0] for r in result_1], label='Mean Time in System (Fixed Service Time)', color = 'green', marker='o')
    plt.title('Mean Time in System')
    plt.xlabel('Arrival Rate(Lambda)')
    plt.ylabel('Time(s)')
    plt.legend()
    plt.grid()
    plt.show()
