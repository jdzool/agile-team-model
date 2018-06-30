#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jondowning

The best method to get data out of the system is to monitor
http://simpy.readthedocs.io/en/latest/topical_guides/monitoring.html

How is this different from using a global variable ? 
"""

import simpy

data = []

def car(env, name, bcs, driving_time, charge_duration):
    # Simulate driving to the BCS
    yield env.timeout(driving_time)
     # Request one of its charging spots
    data.append((name,env.now))
    print('%s arriving at %d' % (name, env.now))
    with bcs.request() as req:
        yield req
        # Charge the battery
        data.append((name,env.now))
        print('%s starting to charge at %s' % (name, env.now))
        
        yield env.timeout(charge_duration)
        data.append((name,env.now))
        print('%s leaving the bcs at %s' % (name, env.now))


env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2)

for i in range(4):
    env.process(car(env, 'Car %d' % i, bcs, i*2, 5))
    
env.run()