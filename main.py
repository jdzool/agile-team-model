"""
@author: jondowning
"""

if __name__ == "__main__":

    # Still to explore -- different optimisation methods 
    from agile_team_model import globals  
    from skopt import gp_minimize 
    from skopt.plots import plot_convergence
    import os
    import shutil

    # Import model module  
    from agile_team_model import run_model, plots

    # Initialise global variables 
    globals.initialise_variables()

    # Inputs 
    inputs = {
        'amount_of_epics': 10,
        'size_ba':1,
        'size_data_ba':2,
        'size_data_eng':3,
        'size_qa':1
        }
    
    # This is all setup: 

    # Define output folders  
    paths = ["./team_queue/", "./epic_progress/", "./data"]

    # Delete down the outputs folders
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)

    # All plots should be able to be created from data captured in global varibales
    globals.g_cost_per_epic = []
    globals.g_final_time = []
    globals.g_team_size = []
    globals.g_amount_ba = []
    globals.g_amount_dba = []
    globals.g_amount_data_eng = []
    globals.g_amount_qa = []
    globals.amount_of_epics = inputs['amount_of_epics']



    # For optimisation around team size:  
    input_abstraction = [inputs['size_ba'], inputs['size_data_ba'], \
        inputs['size_data_eng'], inputs['size_qa']]

    # Limitations on input_abstraction 
    dimensions = [(1,6),(1,6),(1,6),(1,6)]
 
    # Run the optimisation 
    res = gp_minimize(run_model.run_model, 
                    dimensions,                 
                    n_calls=15, 
                    x0=input_abstraction)

    # Plot the data out
    plot_convergence(res)

    plots.plot_cost_per_optimisation(globals.g_cost_per_epic)
    plots.plot_cost_per_epic_weeks(globals.g_cost_per_epic, globals.g_final_time)
    plots.plot_team_shape(globals.g_cost_per_epic, globals.g_amount_ba, \
                                globals.g_amount_dba, globals.g_amount_data_eng, globals.g_amount_qa)

    # TODO -- could dump data into data folder 
    # TODO use data output as for standard test