# -*- coding: UTF-8 -*-

from nsga2.Evolution import Evolution
from nsga2.problems.model_dse import DS_DSE
from nsga2.problems.model_dse.Definitions import Definitions
from Plotter import Plotter
from DbSelector import DbSelector
import sys, json, os

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')

from InOut import InOut

class Nsga2Main(object):
    """Main Class"""

    def __init__(self, projectFolder, inputName, inputs):

        self.inputs_from_user = inputs.get_dict()

        #print "projectFolderNSGA2MAIN:" + projectFolder
        selector= DbSelector(inputName)
        self.bd=json.loads(open(selector.select_db()).read())
        dse_definitions = Definitions(projectFolder, inputName)
        plotter = Plotter(dse_definitions)
        #problem = DS_DSE(dse_definitions)
        #print "dse_definitions:" + str(dse_definitions)
        problem = DS_DSE(dse_definitions, projectFolder, inputName)
#       evolution = Evolution(problem, 5000, 10, projectFolder)
        #evolution = Evolution(problem, 100, 10, projectFolder, inputName)
        evolution = Evolution(problem, self.inputs_from_user["num_of_generations"], self.inputs_from_user["num_of_individuals"], projectFolder, inputName, self.inputs_from_user["mutation_rate"], self.inputs_from_user["mutation_strength"] )
        #evolution.register_on_new_generation(plotter.plot_population_best_front)
        evolution.register_on_new_generation(self.print_generation)
        #evolution.register_on_new_generation(print_metrics)
        #evolution.register_on_new_generation(collect_metrics)
        pareto_front = evolution.evolve()
        #output= InOut()
        output = InOut(projectFolder, inputName)
        self.preditor = output.performancePreditor()
        output.printResults(pareto_front,self.preditor )
        self.inputDict= output.makeInputDict()
        #plotter.plot_x_y(collected_metrics.keys(), map(lambda (hv, hvr): hvr, collected_metrics.values()), 'generation', 'HVR', 'HVR metric for ZDT3 problem', 'hvr-zdt3')
        
	
    def print_generation(self,population, generation_num):
	if(generation_num%100 == 0):        
		print("Generation: {}".format(generation_num))

    def print_metrics(self,population, generation_num):
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
