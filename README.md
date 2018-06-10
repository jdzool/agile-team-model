# agile-team-model

### Discrete Event Simulation of an Agile Data Team (SimPy)

This is a model simulate at a basic level the movement of tasks through various teams on a scrum board. Tasks are simulated as discrete events (http://simpy.readthedocs.io/), which consume resources from teams as they move through a defined software engineering process. 

The outputs of this model are learnings related to:
- The optimal size and shape of a team, given a work rate for each subteam 
- Practical understanding and framing of constraint type problems within our team. Many ideas relate to the topics covered in The Goal (https://en.wikipedia.org/wiki/The_Goal_(novel)) 

## Concepts 
A team consistents of a number of workers (``` num_workers ```). Additional workers aid the speed with which epics are completed. 

Each worker has a work rate (``` work_rate ```) which is the rate at which tickets can be completed by that team. 

The total work rate for each team is calculated from ``` num_workers ``` *  ``` work_rate ``` 

Tickets are request time from workers. When time is found, they can start the processes and wait for it to finish (which takes ``process_time`` units).

## Running the code 

There are two methods to run the code 
- A single run for a defined project size 
- Optimisation for team size (given defined cost function and project size)

Default parameters: 

Our current team consists of the following role; BA, Data BA, Data Engineering, Data QA

The shape of our scrum board is BA, Data BA, Data Engineering, Data QA, Data BA (validation / handover)

## Defined cost function 


