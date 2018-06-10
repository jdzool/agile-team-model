"""
@author: jondowning

"""

def total_cost_calc(data_dict, ba, data_ba, data_engineering, qa): 
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


def plot_queue_len(data_dict, team_list, ba, data_ba, data_engineering, qa, path_out):
    import matplotlib.pyplot as plt
    from collections import OrderedDict
    import datetime 

    time_str = str(datetime.datetime.now())

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


def plot_epic_progress(data_dict, ba, data_ba, data_engineering, qa, path_out):
    import pandas as pd 
    import matplotlib.pyplot as plt
    from collections import OrderedDict
    import datetime 

    time_str = str(datetime.datetime.now())

    team_names_all = []
    time_enters_all = []
    time_exits_all = []
    key_name_all = []

    team_names = [ba.name, data_ba.name, data_engineering.name, qa.name]
    colours = ['r','g','b','m']
    team_name_colour = dict(zip(team_names,colours))

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


def plot_cost_per_optimisation(g_cost_per_epic):
    import numpy as np
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10,8))
    x = np.arange(0,len(g_cost_per_epic))
    ax.plot(x, g_cost_per_epic, 'r', label = 'Cost per epic')
    plt.xlabel('Iteration of optimisation')
    plt.ylabel('£ K')
    plt.legend()
    plt.savefig('Summary_cost_per_epic.png', dpi=400)

def plot_cost_per_epic_weeks(g_cost_per_epic, g_final_time):
    fig, ax = plt.subplots(figsize=(10,8))
    x = np.arange(0,len(g_cost_per_epic))
    ax.plot(x, g_final_time, 'r', label = 'Final time (weeks)')
    plt.xlabel('Iteration of optimisation')
    plt.ylabel('Weeks')
    plt.legend()
    plt.savefig('Summary_cost.png', dpi=400)

def plot_team_shape(g_cost_per_epic, g_amount_ba, g_amount_dba, g_amount_data_eng, g_amount_qa):
    fig, ax = plt.subplots(figsize=(10,8))
    x = np.arange(0,len(g_cost_per_epic))
    ax.plot(x, g_amount_ba, 'r', label = 'Amount of BAs')
    ax.plot(x, g_amount_dba, 'g', label = 'Amount of Data BAs')
    ax.plot(x, g_amount_data_eng, 'b', label = 'Amount of Data Engineers')
    ax.plot(x, g_amount_qa, 'm', label = 'Amount of QAs')
    plt.xlabel('Iteration of optimisation')
    plt.ylabel('Count')
    plt.legend()
    plt.savefig('Summary_team_shape.png', dpi=400)

            
