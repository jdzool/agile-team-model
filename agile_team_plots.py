"""
@author: jondowning

"""

import pickle
import json 

with open('data.json', 'r') as fp:
    data = json.load(fp)
    
with open('parrot.pkl', 'rb') as f:
    mynewlist = pickle.load(f)

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

cost_per_epic = cost / len(data_dict.keys())

print('%s epics were processed' %(int(''.join(filter(str.isdigit, last_epic)))+1))
print('The final time is: %.2d weeks' %last_time)
print('The cost per epic is: £%.2d K' %(cost_per_epic/1000))
print('The team size in: %s' %team_size)


# plots! 
import matplotlib.pyplot as plt
from collections import OrderedDict

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
plt.savefig('queues.png', dpi=400)

# This doesn't work -- capacity is always 1     
#plt.figure()    
#for team in team_list:
#    x,y = map(list, zip(*team.team_capacity))
#    plt.plot(x,y,label=team.name)
#    plt.legend()
#    plt.xlabel('Time (weeks)')
#    plt.ylabel('Capcity (epics)')
#    plt.tight_layout()

# flatten data_dict per 

import pandas as pd 

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
plt.savefig('team_list.png', dpi=400)

plt.show()
            
#            
#    plt.plot(x,y,label=team.name)
#    plt.legend()
#    plt.xlabel('Time (weeks)')
#    plt.ylabel('Capcity (epics)')
#    plt.tight_layout()
#   

