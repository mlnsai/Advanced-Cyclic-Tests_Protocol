import pybamm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from os import system, name 
from time import sleep 
import os
from pybamm import Parameter, constants, exp

def clear(): 
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 
sleep(2) 
clear() 


def expPyBaMM(charRate, discharRate, tempC, rest, setNum, duration, dir):
    os.chdir(dir)


    model = pybamm.lithium_ion.SPMe({"thermal": "lumped", "SEI":"solvent-diffusion limited", "SEI porosity change" : "true", "lithium plating": "reversible"})
    parameter_values = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Chen2020_plating)
    parameter_values.update({"Ambient temperature [K]": tempC + 273.15}) 
    parameter_values.update({"Initial temperature [K]": tempC + 273.15})
    tempK = tempC + 273.15
    def sd_diffusivity(T_amb):
        D_sd = 2.5e-22
        EaD = 4000
        arrhenius = exp(EaD / constants.R * (1 / 298.15 - 1 / T_amb))
        return D_sd * arrhenius
    parameter_values.update({"Outer SEI solvent diffusivity [m2.s-1]":sd_diffusivity(tempK)})

    if rest == 0:
        exp4 = [( f"Discharge at {discharRate}C for {duration} minutes",
                    f"Charge at {charRate}C until 4.2V",
                    "Hold at 4.2V for 2 hours"
                )]*500
    else:
        exp4 = [( f"Discharge at {discharRate}C for {duration} minutes",
            f"Rest for {rest} hours", 
            f"Charge at {charRate}C until 4.2V",
            "Hold at 4.2V for 2 hours",
            f"Rest for {rest} hours"
        )]*500



    experiment = pybamm.Experiment(exp4)

    sim = pybamm.Simulation(model, experiment=experiment, parameter_values=parameter_values)
    sol = sim.solve()


    cyclearr = sol.summary_variables["Cycle number"]
    L1 = sol.summary_variables["Loss of lithium inventory [%]"]
    L2 = sol.summary_variables["Loss of lithium to SEI [mol]"]
    L3 = sol.summary_variables["Loss of lithium to lithium plating [mol]"]


    df = pd.DataFrame({  "Cycle number":cyclearr,
                        "Loss of lithium inventory [%]" : L1,
                        "Loss of lithium to SEI [mol]" : L2,
                        "Loss of lithium to lithium plating [mol]" : L3,

                        })
    name = f"Charge_{charRate}C_Discharge_{discharRate}C_{tempC}_deg_rest_{rest}hr_Set{setNum}"
    print(os.getcwd())
    df.to_csv(f"{name}_Summary.csv", index= False)
    sol = sim.solution
    sol.save_data(f"{name}.csv", ["Time [h]", "Current [A]", 
                                                            "Terminal voltage [V]",
                                                            "Discharge capacity [A.h]",
                                                            "X-averaged cell temperature [K]", 
                                                            "Ambient temperature [K]", 
                                                            "Loss of lithium to SEI [mol]",
                                                            "Loss of lithium to lithium plating [mol]" ,
                                                            "Loss of lithium inventory [%]" 
                                                        ], to_format="csv")                                                        
    
    return name

