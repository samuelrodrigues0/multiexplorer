# -*- coding: UTF-8 -*-
import json, os, sys
import csv
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')
from InOut import InOut
from DbSelector import DbSelector
#from PerformancePredictor import PerformancePredictor
from PerformanceGPUPredictor import PerformanceGPUPredictor

class DsDseBruteForce(object):

    """Main Class"""

    def __init__(self, projectFolder, pathCSV):

        path_db=DbSelector(inputName=pathCSV).select_db()
        
        self.inputDict= InOut(projectFolder, inputName=pathCSV).makeInputDict()
        
        self.preditor= InOut(projectFolder, inputName=pathCSV).performancePreditor()
        
        self.db = json.loads(open(path_db).read())
        
        self.path_all_csv = projectFolder + "/brute_force_all_solutions.csv"
        
        self.path_viable_csv = projectFolder + "/brute_force_viable_solutions.csv"
        
        self.all_solutions = [] # plataformas que obedecem a restricao de area 
        
        self.viable_solutions = [] # plataformas que obedecem a restrição de area e tem performance maxima
        
        self.projectFolder = projectFolder
        
        #self.multiexplorerInputDict= InOut(projectFolder, inputName=pathCSV).getInputFile()
        
        self.combinations()        
        
        self.output_csv(self.path_all_csv)
        
        self.output_csv(self.path_viable_csv, True)


    def combinations(self):
        combinationList=[]

        def is_viable(parameters):
            #power density and total área, are restrictions
            if parameters[1] <= self.inputDict["restrictions"]["total_area"] and parameters[0] <= self.inputDict["restrictions"]["power_density"]:
                return True
            else:
                return False


        for amount_orig_core in range(self.inputDict["parameters"]["amount_original_cores"][0], self.inputDict["parameters"]["amount_original_cores"][1]+1):
            for amount_ip_core in range(self.inputDict["parameters"]["amount_ip_cores"][0], self.inputDict["parameters"]["amount_ip_cores"][1]+1):
                for ip_core in self.db["ipcores"]:
                    parameters= self.calculateParameters(amount_orig_core, amount_ip_core, ip_core)
                    #print(parameters)
                    processor = ip_core["id"]
                    ipCoreName= processor.split("_")[0]
                    #processor = ""
                    #if ip_core["id"] == "ARM_A53_22nm":
                    #    processor = "arm53"
                    #if ip_core["id"] == "ARM_A57_22nm":
                    #    processor = "arm57"
                    #if ip_core["id"] == "Atom_Silvermont_22nm":
                    #    processor = "atom"
                    #if ip_core["id"] == "Quark_x1000_32nm":
                    #    processor = "quark"
                    #if ip_core["id"] == "Smithfield_90nm":
                    #    processor = "smithfield"

                    """ performancePred = PerformanceGPUPredictor(
                        ipCoreName,
                        amount_ip_core,
                        amount_orig_core,                        
                        self.multiexplorerInputDict
                    ).getResults() """
                    performancePred = self.preditor.getResultsNSGA(
                        ipCoreName,
                        amount_ip_core,
                        amount_orig_core
                        )
                    

                    _dict={"amount_orig_core":amount_orig_core, "amount_ip_core":amount_ip_core, "ip_core":ip_core,"powerDensity":str(round(float(parameters[0]), 3)),"area":parameters[1], "performance":parameters[2], "performancePred":performancePred} 
                    self.all_solutions.append(_dict)   
                    if is_viable(parameters):
                        self.viable_solutions.append(_dict)


    def calculateParameters(self, amount_original, amount_ip, ip_core):
        
        orig_power = float(self.inputDict["parameters"]["power_orig"][1])

        orig_area = float(self.inputDict["parameters"]["area_orig"][1])

        orig_perf = float(self.inputDict["parameters"]["performance_orig"][1])

        total_power = float(amount_original * orig_power + amount_ip * ip_core["pow"])

        total_area = float(amount_original * orig_area + amount_ip * ip_core["area"])

        power_density = float(total_power) / float(total_area)

        total_performance = float(amount_original * orig_perf + amount_ip * ip_core["perf"])

        return power_density, total_area, total_performance


    def output_csv(self, path, viable_only=False):

        csv_file = open(path, "w")

        csv_writer= csv.writer(csv_file)

        header = (
            'total_area', 'total_performance', 'performance_pred', 'total_power_density',
            'id_ip_core', 'amount_ip_cores', 'performance ip', 'power ip', 'area_ip',
            'amount_original_cores', 'performance_orig', 'power_orig', 'area orig'
        )
        
        csv_writer.writerow(header)

        if viable_only:
            solutions = self.viable_solutions
        else:
            solutions = self.all_solutions

        for solution in solutions:
           
           #_dict={"amount_orig_core":amount_orig_core, "amount_ip_core":amount_ip_core, "ip_core":ip_core,"powerDensity":parameters[0],"area":parameters[1], "performance":parameters[2]}

            csv_writer.writerow([
                str(round(solution["area"], 2)),
                str(round(solution["performance"], 2)),
                solution["performancePred"],
                solution["powerDensity"],
                solution["ip_core"]["id"],
                solution["amount_ip_core"],
                solution["ip_core"]["perf"],
                solution["ip_core"]["pow"],
                solution["ip_core"]["area"],
                solution["amount_orig_core"],
                self.inputDict["parameters"]["performance_orig"][1],
                self.inputDict["parameters"]["power_orig"][1],
                self.inputDict["parameters"]["area_orig"][1]
            ])

        csv_file.close()

        
if __name__ == "__main__":
    objDse = DsDseBruteForce()
