# -*- coding: UTF-8 -*-
import sys
import json
from InOutVM import InOut
from DbSelectorVM import DbSelector
from nsga2.Evolution import Evolution
from nsga2.problems.model_dse import DS_DSE
from nsga2.problems.model_dse.Definitions import Definitions


class Nsga2Main(object):
    """
    Main Class
    """
    def __init__(self, projectFolder, inputName, mutation_strength, mutation_rate, num_of_individuals, num_of_generations, prediction):
        print("projectFolderNSGA2MAIN:" + projectFolder)
        selector= DbSelector(inputName=inputName)
        self.bd=json.loads(open(selector.select_db()).read())
        dse_definitions = Definitions()
        problem = DS_DSE(dse_definitions, projectFolder, inputName, prediction)
        evolution = Evolution(problem, num_of_generations, num_of_individuals, mutation_strength, mutation_rate, projectFolder, prediction, inputName=inputName)
        evolution.register_on_new_generation(self.print_generation)
        pareto_front = evolution.evolve()
        output = InOut(projectFolder, inputName, prediction)
        output.printResults(pareto_front)
	
    def print_generation(self, population, generation_num):
        if generation_num%100 == 0:        
            print("Generation: {}".format(generation_num))

    def print_metrics(self, population, generation_num):
        pareto_front = population.fronts[0]
        metrics = ZDT3Metrics()
        hv = metrics.HV(pareto_front)
        hvr = metrics.HVR(pareto_front)
        print("HV: {}".format(hv))
        print("HVR: {}".format(hvr))

    collected_metrics = {}
    def collect_metrics(self,population, generation_num):
        pareto_front = population.fronts[0]
        metrics = ZDT3Metrics()
        hv = metrics.HV(pareto_front)
        hvr = metrics.HVR(pareto_front)
        collected_metrics[generation_num] = hv, hvr

    def get_db_lenght(self):
        return len(self.bd["ipcores"])


if __name__ == "__main__":
    nsga2Obj = Nsga2Main()
