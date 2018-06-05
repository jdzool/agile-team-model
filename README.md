# agile-team-model

Discrete Event Simulation of an Agile Data Team (SimPy)

This is a model which attempts to simulate at a basic level the movement of tasks through various teams on a scrum board. The outputs are learnings related to the
- Theory of constraints: For example relating to the topics covered in The Goal (https://en.wikipedia.org/wiki/The_Goal_(novel)) 


A team consistents of a number of workers (``` num_workers ```). Additional workers aid the speed with which epics are completed. 

Each worker has a work rate (``` work_rate ```) which is the rate at which tickets can be completed by that team. 

The total work rate for each team is calculated from ``` num_workers ``` *  ``` work_rate ``` 

Tickets are request time from workers. When time is found, they can start the processes and wait for it to finish (which takes ``process_time`` units).