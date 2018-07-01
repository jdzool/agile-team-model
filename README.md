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
- A single run for a defined project size (```run_model_once_example.py```)
- Optimisation for team size (given defined cost function and project size) (```main.py```)

Default parameters: 

The current team consists of the following roles; BA, Data BA, Data Engineering, Data QA

The shape of our scrum board is: BA, Data BA, Data Engineering, Data QA, Data BA (validation / handover)

## Defined cost function 

Optimisation is conducted against a ```loss_function```. This was created using the ```cost_per_epic``` a value which considers the average cost of the team and time to complete an epic. A ```queue_penality``` is added to the  addition loss function KPI in order to penalise long queues being formed in the system. In this case the optimisation attempts to minimise the size of the ```loss_function```. 

## Optimisation

During optimisation two outputs are tracked: the size of the relative queues on each team (see example output: ```example_team_list_epic_progress.png```) and the time at which each team picks up each epic (see example output: ```example_team_list_epic_progress.png```). These graphics are created at each optimsiation step. 

The summary of outputs from the optimisation pass is show in the following images ```Summary_cost_per_epic.png```, ```Summary_team_shape.png```, ```Summary_total_time.png```. These graphics respectively give the user information on how optimisation has proceeded with respect to the total cost, the shape of the team (note: we optimising against our loss function) and the total time taken to complete all epics. Having information on the process of optimisation helps to give the user confidence optimisation has found a globally local solution. 

