#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jondowning

Optimisation 

"""

from scipy.optimize import minimize
from skopt import gp_minimize

def agile_des(input_abstraction):
    
    import simpy
    import numpy.random as random 
    import numpy as np
    import matplotlib.pyplot as plt
    from collections import OrderedDict
    import pandas as pd 
    import os

    

    
    class Team(simpy.Resource):
        """A team consistents of a number of workers (``` NUM_WORKERS ```). 
        Additional workers aid the speed with which epics are completed. 
        
        Each team has a work rate (``` WORK_RATE ```) which is the rate
        at which tickets can be completed. 
    
        Tickets are request time from workers when they got one, they
        can start the processes and wait for it to finish (which
        takes ``PROCESS_TIME`` minutes).
    
        """
        def __init__(self, env, num_workers, work_rate, name):
            self.env = env
            #self.workers = simpy.Resource(env, num_workers) # Each worker is not a resource
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
    
    global data_dict               
    data_dict = {}
          
    def epic(env, name, epic_size, team_list, data_dict):
        """Each epic has a ``name`` and a size ```epic_size```
        it arrives at a processor ```team``` 
    
        It then starts the process, waits for it to finish then is passed
        on to the next processor until complete 
        
        """
    
        if name not in data_dict:
            data_dict[name] = {}
            data_dict[name]['arrives'] = []
            data_dict[name]['enters'] = []
            data_dict[name]['leaves'] = []
        
    #    print('%s arrives at %.2f.' % (name, env.now))
    #    with team.workers.request() as request:
    #        yield request
    #
    ##        team.data[name].append(env.now)
    #        print('%s enters the process at %.2f.' % (name, env.now))
    #        yield env.process(team.process(name))
    #        
    ##        team.data[name].append(env.now)    
        
        for team in team_list: 
            data_dict[name]['arrives'].append((team.name, env.now))
            #print('%s arrives at the %s at time %.2f.' % (name, team.name, env.now))
            with team.request() as req:
                
                yield req
                data_dict[name]['enters'].append((team.name, env.now))
                #print('%s enters the %s at time %.2f.' % (name, team.name, env.now))
                
                yield env.process(team.process(name, epic_size))
                data_dict[name]['leaves'].append((team.name, env.now))
                #print('%s leaves the %s at %.2f.' % (name, team.name, env.now))
    
    # Setup and start the simulation
    print('Process Flow')
    # random.seed(RANDOM_SEED)  # This helps reproducing the results
    
    env = simpy.Environment()
    # env, num_workers, work_rate -- in epics per week 
    
    print(input_abstraction)

    ba = Team(env, input_abstraction[0], 0.5, 'BA team') # 1 epic per 2 weeks
    data_ba = Team(env, input_abstraction[1], 0.2,'Data BA team') # 1 epic per 2 weeks
    data_engineering = Team(env, input_abstraction[2], 0.33, 'Data Engineering team') # 1 epic per 1 week
    qa = Team(env, input_abstraction[3], 0.5, 'Data QA team') # 1 epic per 1 week
    #handover = Team(env, 1, 0.2, 'Handover team') # 1 epic per 2 weeks
    
    team_list = [ba, data_ba, data_engineering, qa, data_ba]
    
    epic_list = []
    
    for i in range(10):
        #epic_size = random.uniform(1,6)
        epic_size = 2
        epic_list.append(epic_size)
        env.process(epic(env, 'Epic %d' % i, epic_size, team_list, data_dict))
    
    # Execute!
    years = 5
    
    env.run(until=years*52)
    
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

    

    
    # plots! 
    
    team_names = [ba.name, data_ba.name, data_engineering.name, qa.name]
    colours = ['r','g','b','m']
    team_name_colour = dict(zip(team_names,colours))
    
    plt.figure(figsize=(10,8)) 
    for team in team_list:
        x,y = map(list, zip(*team.queue_length))
        plt.plot(x,y, team_name_colour[team.name], label=team.name)
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        
        plt.xlabel('Time (weeks)')
        plt.ylabel('Queue length (epics)')
        plt.tight_layout()
    plt.savefig('./queues/' + time_str + '_queues.png', dpi=400)
    
    
    team_names_all = []
    time_enters_all = []
    time_exits_all = []
    key_name_all = []
    
    for epic in data_dict.keys(): 
        team_names, time_enters = map(list, zip(*data_dict[epic]['enters']))
        team_names, time_exits = map(list, zip(*data_dict[epic]['leaves']))
        key_name = [epic]*len(team_names)
        
        key_name_all.append(key_name)
        team_names_all.append(team_names)
        time_enters_all.append(time_enters)
        time_exits_all.append(time_exits)
    
    key_name_all = [item for sublist in key_name_all for item in sublist]
    team_names_all = [item for sublist in team_names_all for item in sublist]
    time_enters_all = [item for sublist in time_enters_all for item in sublist]
    time_exits_all = [item for sublist in time_exits_all for item in sublist]
        
    df_data = pd.DataFrame(data = list(zip(key_name_all,
                                           team_names_all, 
                                           time_enters_all, 
                                           time_exits_all)), 
                           columns = ['epic', 'team','time_enter','time_exit'])
    
    df_data['id'] = df_data['epic'].apply(lambda x: int(''.join(filter(str.isdigit, x))))
    
    
    fig, ax = plt.subplots(figsize=(10,8))
    for team_name in team_names:
        tmp = df_data[(df_data.team == team_name)]
        for i in range(0,len(tmp)):
            tmp2 = tmp[['id','time_enter','time_exit']].iloc[i].tolist()
            x = [tmp2[1], tmp2[2]]
            y = [tmp2[0], tmp2[0]]
            ax.plot(x, y, team_name_colour[team_name], label = team_name)
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.xlabel('Time (weeks)')
        plt.ylabel('Epic (#)')
    plt.savefig('./team_list/' + time_str + '_team_list.png', dpi=400)
    
    return loss_function
            
#res = minimize(agile_des, input_abstraction, method='BFGS',\
#                options={'disp': True})








