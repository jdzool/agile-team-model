"""
@author: jondowning
"""


if __name__ == "__main__":

    # Still to explore -- different optimisation methods 
    from skopt import gp_minimize 
    from skopt.plots import plot_convergence

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
    
    global amount_of_epics
    amount_of_epics = inputs['amount_of_epics']

    # For optimisation around team size:  
    input_abstraction = [inputs['size_ba'], inputs['size_data_ba'], \
        inputs['size_data_eng'], inputs['size_qa']]

    # Limitations on input_abstraction 
    dimensions = [(1,10),(1,10),(1,10),(1,10)]

    # Output variables -- is there an easier method than using global variables? 
    global g_cost_per_epic
    global g_final_time
    global g_team_size
    global g_amount_ba
    global g_amount_dba
    global g_amount_data_eng
    global g_amount_qa

    # All plots should be able to be created from data captured in global varibales
    g_cost_per_epic = []
    g_final_time = []
    g_team_size = []
    g_amount_ba = []
    g_amount_dba = []
    g_amount_data_eng = []
    g_amount_qa = []

 
    # Run the optimisation 
    res = gp_minimize(run_model.agile_des, 
                    dimensions,                 
                    n_calls=40, 
                    x0=input_abstraction)

    # Plot the data out
    plot_convergence(res)

    plots.plot_cost_per_optimisation(g_cost_per_epic)
    plots.plot_cost_per_epic_weeks(g_cost_per_epic, g_final_time)
    plots.plot_team_shape(g_cost_per_epic, g_amount_ba, g_amount_dba, g_amount_data_eng, g_amount_qa)