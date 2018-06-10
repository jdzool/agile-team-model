#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jondowning

SimPy Simulation for estimating the time to complete an agile project 

Possible variables 
-- Size of different teams
-- Pace of work 
-- Length of epics 
"""

def run_model(input_abstraction): 

    import simpy
    import numpy.random as random 
    import numpy as np
    import json
    import pickle
    import os

    size_ba, size_data_ba, size_data_eng, size_qa = input_abstraction

    class Team(simpy.Resource):
        """A team consistents of a number of workers (``` num_workers ```). 
        Additional workers aid the speed with which epics are completed. 
        
        Each worker has a work rate (``` work_rate ```) which is the rate
        at which tickets can be completed by that team. 
        
        The total work rate for each team is calculated from 
        `` num_workers ``` *  ``` work_rate ``` 

        Tickets are request time from workers. When time is found, they
        can start the processes and wait for it to finish (which
        takes ``PROCESS_TIME`` units).

        """
        def __init__(self, env, num_workers, work_rate, name):
            self.env = env
            # We consider the team a resource,
            # each worker is not a resource otherwise: 
            #self.workers = simpy.Resource(env, num_workers) 
            super().__init__(env)
            self.queue_length = [] 
            self.team_capacity = []       
            self.num_workers = num_workers
            self.work_rate = work_rate
            self.name = name
                
        def process(self, ticket, epic_size):
            """The processes. It takes a ``ticket`` and processes it"""
            process_time = epic_size / (self.num_workers * self.work_rate)
            yield self.env.timeout(process_time)

            
        def request(self, *args, **kwargs):
            self.team_capacity.append((self._env.now, self.capacity))
            self.queue_length.append((self._env.now, len(self.queue)))
            return super().request(*args, **kwargs)

            
        def release(self, *args, **kwargs):
            self.team_capacity.append((self._env.now, self.capacity))
            self.queue_length.append((self._env.now, len(self.queue)))
            return super().release(*args, **kwargs)

        
    def epic(env, name, epic_size, team_list, data_dict):
        """Each epic has a ``name`` and a size ```epic_size```
        it arrives at a processor ```team``` 

        It then starts the process, waits for it to finish then is passed
        on to the next processor until completed 
        """

        # Settup a dictionary to aggregate data 
        if name not in data_dict:
            data_dict[name] = {}
            data_dict[name]['arrives'] = []
            data_dict[name]['enters'] = []
            data_dict[name]['leaves'] = []
        
        for team in team_list: 
            data_dict[name]['arrives'].append((team.name, env.now))
            print('%s arrives at the %s at time %.2f' % (name, team.name, env.now))
            with team.request() as req:
                
                yield req
                data_dict[name]['enters'].append((team.name, env.now))
                print('%s enters the %s at time %.2f' % (name, team.name, env.now))
                
                yield env.process(team.process(name, epic_size))
                data_dict[name]['leaves'].append((team.name, env.now))
                print('%s leaves the %s at %.2f' % (name, team.name, env.now))
        

    data_headers = ['name', 'arrives_ba', 'arrives_data_ba', \
                    'arrives_data_eng', 'arrives_qa', 'arrives_handover']

    # Unsure how else to access these variables (use global for now)
    global data_dict               
    data_dict = {}

    # Setup and start the simulation
    print('Process Flow')

    # Initialise environmnet 
    env = simpy.Environment()

    """
    Need to setup our flow 
    1) define teams
    team --> env, num_workers, work_rate (in epics per week), name 
    Start with a more or less balanced team (1 epic per 2 weeks / sprint) 
    """

    ba = Team(env, size_ba, 0.5, 'BA team') # 1 epic per 2 weeks
    data_ba = Team(env, size_data_ba, 0.2,'Data BA team') # 1 epic per 2 weeks
    data_engineering = Team(env, size_data_eng, 0.33, 'Data Engineering team') # 1 epic per 1 week
    qa = Team(env, size_qa, 0.5, 'Data QA team') # 1 epic per 1 week

    # 2) Define the order of the teams 
    team_list = [ba, data_ba, data_engineering, qa, data_ba]

    # 3) Create backlog
    epic_list = []

    for i in range(10):
        # Could make epics random lengths (or not!)
        # epic_size = random.uniform(1,6)
        epic_size = 2
        epic_list.append(epic_size)
        env.process(epic(env, 'Epic %d' % i, epic_size, team_list, data_dict))

    # Define length of simulation 
    # Length is not important -- simulation will stop when backlog is empty 
    years = 3

    # Execute!
    env.run(until=years*52)

    # Save data out
    output_dir = "./data/"

    # Calculate cost 
    # Find time when team is finished 
    last_epic = sorted(list(data_dict.keys()))[-1]
    team, last_time = map(list, zip(*data_dict[last_epic]['leaves']))
    last_time = max(last_time)
    
    team_size = np.sum([ba.num_workers,
                        data_ba.num_workers,
                        data_engineering.num_workers,
                        qa.num_workers])
    
    cost = team_size*last_time*5*1000

    # minimise queue lengths -- maximise value? 
    total_queue = []
    for team in team_list:
        team,queue = map(list, zip(*team.queue_length))   
        total_queue.append(np.sum(queue))
    total_queue = np.sum(total_queue)
    
    cost_per_epic = cost / len(data_dict.keys()) 
    queue_penality = total_queue*100
    
    loss_function = cost_per_epic + queue_penality
    
    print('%s epics were processed' %(int(''.join(filter(str.isdigit, last_epic)))+1))
    print('The final time is: %.2d weeks' %last_time)
    print('The cost per epic is: £%.2d K' %(cost_per_epic/1000))
    print('The queue penality is: £%.2d K' %(queue_penality/1000))
    print('The loss function is: £%.2d K' %(loss_function/1000))
    print('\n')
    print('The team size is: %s' %team_size)
    print('There are %s BAs' %ba.num_workers)
    print('There are %s Data BAs' %data_ba.num_workers)
    print('There are %s Data Engineers' %data_engineering.num_workers)
    print('There are %s Data QAs' %qa.num_workers)
    
    g_cost_per_epic.append(cost_per_epic/1000)
    g_final_time.append(last_time)
    g_team_size.append(team_size)
    g_amount_ba.append(ba.num_workers)
    g_amount_dba.append(data_ba.num_workers)
    g_amount_data_eng.append(data_engineering.num_workers)
    g_amount_qa.append(qa.num_workers)

    # Plots:
    from plots import plots_queue_len, plot_epic_progress

    plots_queue_len(data_dict, team_list, ba, data_ba, data_engineering, qa, )
    plot_epic_progress(data_dict, ba, data_ba, data_engineering, qa, path_out)

    return loss_function

