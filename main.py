import os
from datetime import datetime, timedelta
import time
from multiprocessing import Pool
import multiprocessing
from cyclic_tests import expPyBaMM


os.chdir(os.path.dirname(os.path.realpath(__file__)))

parent_dir = os.path.dirname(os.path.realpath(__file__))

setData = \
{
    4 : {
            "disRate":[0.4, 0.5, 0.6, 0.75, 0.8, 1, 1.2, 1.5, 1.6, 1.75],
            "time":30
        },
    5 : {
            "disRate":[4/15, 1/3, 0.4, 0.5, 8/15, 2/3, 0.8, 1, 16/15, 7/6],
            "time":45
        },
    6 : {
            "disRate":[0.2, 0.25, 0.3, 0.375, 0.4, 0.5, 0.6, 0.75, 0.8, 0.875],
            "time":60
        },
    7 : {
            "disRate":[0.16, 0.2, 0.24, 0.3, 0.32, 0.4, 0.48, 0.6, 0.64, 0.7],
            "time":75
        },
    8 : {
            "disRate":[2/15, 1/6, 0.2, 0.25, 4/15, 1/3, 0.4, 0.5, 8/15, 7/12],
            "time":90
        },

}

expData = {4 : 0.1, 5 : 0.5, 6 : 0.75, 7 : 1}
restData = [0, 0.5, 1, 1.5, 2]
tempData = [0, 25, 50]

class ExperimentData:
    def __init__(self):
        self.exp = None
        self.tempC = None
        self.rest = None
        self.set = None
        self.disrate = None
        self.duration = None
        self.dir = None

def log(message, name = "log"):
    log = open( os.path.join(parent_dir, f"{name}.txt"), "a" )
    now = datetime.now().strftime("%d-%B-%Y, %H:%M:%S.%f")

    log.write(
        f"\n{now} {message}\
        \n"
    )
    log.close()

def call_experiment(e: ExperimentData):
    a = f"expPyBaMM is called for:\nExp-{e.exp} Temp-{e.tempC} Rest-{e.rest} Set is {e.set}\n"
    b = f"expPyBaMM is called for: Exp-{e.exp}, Temp-{e.tempC}, Rest-{e.rest}, Set is {e.set}, Discharge rate is {e.disrate}, duration is {e.duration}"
    
    start_t = time.perf_counter()
    log(f"********** Workign directory changed to {e.dir} **********")
    os.chdir(e.dir)
    print(a)
    log(b)

    end_t = time.perf_counter()
    exp_duration = end_t - start_t
    c = f"expPyBaMM is complete for: Exp-{e.exp}, Temp-{e.tempC}, Rest-{e.rest}, Set is {e.set}, Discharge rate is {e.disrate}, duration is {e.duration} and it took {str(timedelta(seconds=exp_duration))} (H:M:S:s) to complete"
    log(c)

def prepare_experiment(performExperiments):
    list_of_exp = []
    log("==================================================================================================")
    log(f"Number of CPU cores: {multiprocessing.cpu_count()}")  
    log(f"Number of pool workers: {multiprocessing.current_process().pool._processes}")
    log(f"Number of pool workers: {pool._processes}") 
    for performExp in performExperiments:
        for e in performExp["Exp"] : 
            for r in performExp["rest"]:
                for s in performExp["set"]:
                    for t in performExp["Temp"]: 

                        sData = setData[s]
                        d = sData["disRate"]
                        duration = sData["time"]

                        dir = os.path.join(parent_dir, f"Exp-{e}", f"{t} deg", "Variable rest periods",f"{r}hr rest", f"Set-{s}")
                        os.makedirs(dir, exist_ok=True)

                        for i in d:
                            e1 = ExperimentData()
                            e1.exp = e
                            e1.tempC = t
                            e1.rest = r
                            e1.set = s
                            e1.disrate = i
                            e1.duration = duration
                            e1.dir = dir

                            list_of_exp.append(e1)

    results = pool.imap(call_experiment, list_of_exp)

    for z in results:
        print(z)
        
def main():
    performExp = [5] # Write all the experiments to perform in this list
    performExp_with_temperatures = [0,25,50] # Write all the temperature in this list
    performExp_with_rest = [2]
    performExp_with_sets = [4]


    for e in performExp : 
        for r in performExp_with_rest:
            for s in performExp_with_sets:
                for t in performExp_with_temperatures: 
                    prepare_experiment(e,t,r,s)
                log(f"Experiment {e} completed for Temperature {t} deg C and rest {r} hour.", "overall")

if __name__ == "__main__":  
    pool = Pool(processes = 15)
    main()