# Feito pelo Prof. Vinícius Gusmão Pereira de Sá

import numpy, random

VERBOSE = False

'''
  Samples from an exponential distribution with rate Lambda (average 1/Lambda).
'''
def exponential(Lambda):
  return -numpy.log(1-random.random())/Lambda

'''
  Simulates *n_servers* M/M/1 (or M/D/1) queues fed by Poisson processes with
  rate *Lambda* and exponential service time with rate *Mu* (or fixed time
  at 1/Mu). The total simulation time is given by the parameter *duration*.
  We actually run it for *duration + warm_up* seconds, where *warm_up* is
  the length of the transient phase, whose metrics might be discarded.

  Returns the empirical averages of job size and time in system,
  along with the average time in system obtained during the transient phase
  for didactic purposes.
'''
def test(Lambda, Mu, n_servers, duration, warm_up, fixed_job_size=False):

  # the only data structure we need
  next_time_server_idle = [0] * n_servers

  # variables for metrics (separate metrics for the transient phase)
  total_job_size = 0
  count_completed_jobs, count_completed_jobs_warm_up = 0, 0
  total_time_in_system, total_time_in_system_warm_up = 0, 0

  job_arrival = 0  # 1st arrival takes place at time 0, w.l.o.g.

  while job_arrival < warm_up + duration:
    job_size = 1/Mu if fixed_job_size else exponential(Mu)

    # picks a server uniformly at random
    chosen_server = random.randint(0, n_servers - 1)

    # if server is idle when the job arrives, it gets serviced immediately;
    # otherwise the service starts when the server would have become idle
    job_service_start = max(job_arrival, next_time_server_idle[chosen_server])
    job_service_end = job_service_start + job_size

    if VERBOSE:
      print("job_arrival =", job_arrival)
      print("job_size =", job_size)
      print("chosen_server=", chosen_server)
      print("next_time_server_idle =", next_time_server_idle[chosen_server])
      print("job_service_start =", job_service_start)
      print("job_service_end =", job_service_end)

    # updates the next time the server will become idle
    next_time_server_idle[chosen_server] = job_service_end

    # if not warming up and within the specified duration, register metrics
    if job_service_end < warm_up + duration:
      if job_service_start >= warm_up:  # metrics after the transient phase
        count_completed_jobs += 1
        total_time_in_system += job_service_end - job_arrival
        total_job_size += job_size
      else:  # metrics during the transient phase (for didactical purposes)
        count_completed_jobs_warm_up += 1
        total_time_in_system_warm_up += job_service_end - job_arrival

    # defines the next arrival time via a unified Poisson process
    job_arrival += exponential(Lambda * n_servers)

  return total_job_size/count_completed_jobs, \
         total_time_in_system/count_completed_jobs, \
         total_time_in_system_warm_up/count_completed_jobs_warm_up


# -----------
# main
# -----------

MU = 1
SERVER_COUNT = 100
DURATION = 10000
WARM_UP = 20000

for LAMBDA in (0.5, 0.8, 0.9, 0.99):
  print("--------------------------------\n")
  print("lambda =", LAMBDA)
  print("mu =", MU)
  print("transient phase =", WARM_UP)
  print("duration =", DURATION)
  print()

  results = test(LAMBDA, MU, SERVER_COUNT, DURATION, WARM_UP, False)
  print("M/M/1")
  print("average job size = %.4f" % results[0])
  print("average time in system (transient) = %.2f" % results[2])
  print("average time in system = %.2f" % results[1])
  print("theoretical E[T] = 1/(mu-lambda) = %.2f\n" %
        (1/(MU-LAMBDA)))

  results = test(LAMBDA, MU, SERVER_COUNT, DURATION, WARM_UP, True)
  print("M/D/1")
  print("constant job size = %.4f" % results[0])
  print("average time in system (transient) = %.2f" % results[2])
  print(f"average time in system = %.2f" % results[1])
  print("theoretical E[T] = 1/(mu) + rho/(2 mu(1-rho)) = %.2f\n" %
        (1/MU + (LAMBDA/MU)/(2*MU*(1-LAMBDA/MU))))
