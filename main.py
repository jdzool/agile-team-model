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

    # Initialise global variables 
    globals.initialise_variables()

    # Import run model 
    from agile_team_model import run_model, plots

    # Inputs 
    inputs = {
        'amount_of_epics': 10,
        'size_ba':1,
        'size_data_ba':2,
        'size_data_eng':3,
        'size_qa':1
        }
    
    # This is all setup: 

    # Delete 
    paths = ["./team_queue/", "./epic_progress/", "./data"]

    # Delete down the outputs folders
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)

    # All plots should be able to be created from data captured in global varibales
    g_cost_per_epic = []
    g_final_time = []
    g_team_size = []
    g_amount_ba = []
    g_amount_dba = []
    g_amount_data_eng = []
    g_amount_qa = []

    amount_of_epics = inputs['amount_of_epics']



    # For optimisation around team size:  
    input_abstraction = [inputs['size_ba'], inputs['size_data_ba'], \
        inputs['size_data_eng'], inputs['size_qa']]

    # Limitations on input_abstraction 
    dimensions = [(1,10),(1,10),(1,10),(1,10)]
 
    # Run the optimisation 
    res = gp_minimize(run_model.run_model, 
                    dimensions,                 
                    n_calls=40, 
                    x0=input_abstraction)

    # Plot the data out
    plot_convergence(res)

    plots.plot_cost_per_optimisation(g_cost_per_epic)
    plots.plot_cost_per_epic_weeks(g_cost_per_epic, g_final_time)
    plots.plot_team_shape(g_cost_per_epic, g_amount_ba, g_amount_dba, g_amount_data_eng, g_amount_qa)