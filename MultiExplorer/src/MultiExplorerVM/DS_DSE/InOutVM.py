# -*- coding: UTF-8 -*-
import os
import re
import sys
import csv
import math
import json
from glob import glob
from pprint import pprint
from decimal import Decimal
from datetime import datetime
from DbSelectorVM import DbSelector
from JsonToCSV import JsonToCSV
from PerformancePredictorVM import PerformancePredictor
from MultiExplorer.src.config import PATH_RUNDIR


class InOut(object):
    """ 
    This class makes the interface between user entry and input of nsga, and also, makes de output of algorithm nsga.
    """
    def __init__(self, projectFolder, inputName, prediction):
        self.prediction = prediction
        self.projectFolder = projectFolder
        self.outputPath = ""
        self.inputName = inputName
        self.outputName = str(projectFolder)+"/populationResults.json"
        self.jsonFile = None
        self.objDict = {}
        self.inputDict = {}
        self.selector= DbSelector(inputName=self.inputName)
	
        self.menorTempo = 0
        self.menorCusto = 0
        self.tempo = 0
        self.custo = 0
        
        self.qntorig1 = 0
        self.qntsup1 = 0
        self.inst1 = 0
        self.cc1 = 0
        self.orig1 = 0
        self.sup1 = 0
        
        self.qntorig2 = 0
        self.qntsup2 = 0
        self.inst2 = 0
        self.cc2 = 0
        self.orig2 = 0
        self.sup2 = 0

    def totalTime(self, individual):
        amount_orig_vm = individual.features[0]
        amount_sup_vm = individual.features[1]

        instructions = individual.features[2]
        corescloudlet = individual.features[3]

        mips_orig = individual.features[4]["mips"]
        coresvm_orig = individual.features[4]["coresVM"]

        mips_sup = individual.features[5]["mips"]
        coresvm_sup = individual.features[5]["coresVM"]
        

        cores_cloudlet_orig = round(amount_orig_vm*coresvm_orig*corescloudlet/(coresvm_orig*amount_orig_vm+coresvm_sup*amount_sup_vm))
        cores_cloudlet_sup = corescloudlet - cores_cloudlet_orig

        instructions_orig = round(instructions*cores_cloudlet_orig/corescloudlet)
        instructions_sup = instructions - instructions_orig

        time_vm_orig = ((((instructions_orig/1000000)/amount_orig_vm)*(cores_cloudlet_orig/amount_orig_vm))/(mips_orig*coresvm_orig))/3600

        time_vm_sup = ((((instructions_sup/1000000)/amount_sup_vm)*(cores_cloudlet_sup/amount_sup_vm))/(mips_sup*coresvm_sup))/3600

        if time_vm_orig > time_vm_sup:
            totalTime = time_vm_orig
        else:
            totalTime = time_vm_sup

        return totalTime
        
    def totalCost(self, individual):
        amount_orig_vm = individual.features[0]
        amount_sup_vm = individual.features[1]

        instructions = individual.features[2]
        corescloudlet = individual.features[3]

        mips_orig = individual.features[4]["mips"]
        coresvm_orig = individual.features[4]["coresVM"]
        price_orig = individual.features[4]["price_orig"]

        mips_sup = individual.features[5]["mips"]
        coresvm_sup = individual.features[5]["coresVM"]
        price_sup = individual.features[5]["price"]
        

        cores_cloudlet_orig = round(amount_orig_vm*coresvm_orig*corescloudlet/(coresvm_orig*amount_orig_vm+coresvm_sup*amount_sup_vm))
        cores_cloudlet_sup = corescloudlet - cores_cloudlet_orig

        instructions_orig = round(instructions*cores_cloudlet_orig/corescloudlet)
        instructions_sup = instructions - instructions_orig

        time_vm_orig = ((((instructions_orig/1000000)/amount_orig_vm)*(cores_cloudlet_orig/amount_orig_vm))/(mips_orig*coresvm_orig))/3600
        
        if math.ceil(time_vm_orig) == 0:
            cost_vm_orig = 1*price_orig*amount_orig_vm
        else:
            cost_vm_orig = math.ceil(time_vm_orig)*price_orig*amount_orig_vm

        time_vm_sup = ((((instructions_sup/1000000)/amount_sup_vm)*(cores_cloudlet_sup/amount_sup_vm))/(mips_sup*coresvm_sup))/3600

        if math.ceil(time_vm_sup) == 0:
            cost_vm_sup = 1*price_sup*amount_sup_vm
        else:
            cost_vm_sup = math.ceil(time_vm_sup)*price_sup*amount_sup_vm

        totalCost = cost_vm_orig + cost_vm_sup

        return totalCost
        
    #método que imprime em um json e em uma planilha todos os indivíduos gerados no nsga
    def printResults(self, population):
        num = 0
        for individual in population:
            self.inserctInDict(individual, num)
            num = num+1
        self.writeResults()
        JsonToCSV(self.projectFolder).convertJSONToCSV()
        var2 = PATH_RUNDIR + "/MultiExplorer_VM/Resultados_menorTempo_menorCusto.csv"
        csv_data = open(var2, 'a')
        csvWriter = csv.writer(csv_data)
        result = str(self.menorTempo)
        list = []
        list.append(self.menorTempo)
        list.append(self.custo)
        list.append(self.qntorig1)
        list.append(self.orig1)
        list.append(self.qntsup1)
        list.append(self.sup1)
        list.append(self.inst1)
        list.append(self.cc1)
        
        csvWriter.writerow(list)
        
        list = []
        list.append(self.tempo)
        list.append(self.menorCusto)
        list.append(self.qntorig2)
        list.append(self.orig2)
        list.append(self.qntsup2)
        list.append(self.sup2)
        list.append(self.inst2)
        list.append(self.cc2)
        csvWriter.writerow(list)
        csv_data.close()
    
    #método responsável por criar um dicionário de saída, com as características dos indivíduos gerados pelo nsga 
    def inserctInDict(self, individual, num):
        self.objDict[num]={}
        #inserction of features
        self.objDict[num]["amount_original_vm"]= individual.features[0]
        self.objDict[num]["amount_sup_vm"]= individual.features[1]
        self.objDict[num]["instructions"]= individual.features[2]
        self.objDict[num]["corescloudlet"]= individual.features[3]
        self.objDict[num]["orig_vm"]= individual.features[4]
        self.objDict[num]["core_ip"]= individual.features[5]

        #metrics
        self.objDict[num]["Results"]={}
        #inserction of power_density and total_area
        time = self.totalTime(individual)
        self.objDict[num]["Results"]["total_time"]= "-"

        cost = self.totalCost(individual)
        self.objDict[num]["Results"]["total_cost"]= "-"


        if self.menorTempo == 0:
            self.menorTempo = time
            self.custo = cost
            self.qntorig1 = individual.features[0]
            self.qntsup1 = individual.features[1]
            self.inst1 = individual.features[2]
            self.cc1 = individual.features[3]
            self.orig1 = individual.features[4]["name"]
            self.sup1 = individual.features[5]["id"]
        
        if self.menorTempo > time:
            self.menorTempo = time
            self.custo = cost
            self.qntorig1 = individual.features[0]
            self.qntsup1 = individual.features[1]
            self.inst1 = individual.features[2]
            self.cc1 = individual.features[3]
            self.orig1 = individual.features[4]["name"]
            self.sup1 = individual.features[5]["id"]
        
        if self.menorCusto == 0:
            self.menorCusto = cost
            self.tempo = time
            self.qntorig2 = individual.features[0]
            self.qntsup2 = individual.features[1]
            self.inst2 = individual.features[2]
            self.cc2 = individual.features[3]
            self.orig2 = individual.features[4]["name"]
            self.sup2 = individual.features[5]["id"]
        
        if self.menorCusto > cost:
            self.menorCusto = cost
            self.tempo = time
            self.qntorig2 = individual.features[0]
            self.qntsup2 = individual.features[1]
            self.inst2 = individual.features[2]
            self.cc2 = individual.features[3]
            self.orig2 = individual.features[4]["name"]
            self.sup2 = individual.features[5]["id"]
		
        processor = individual.features[5]["id"]

        #################################################################################################################################################

        #print(individual.features)
        if self.prediction:
            preditor_original = PerformancePredictor(individual.features[4]['mips'], individual.features[4]['coresVM'],
                                                     individual.features[4]['price_orig'], individual.features[2],
                                                     individual.features[3], individual.features[0])
            
            amount_orig_vm = individual.features[0]
            amount_sup_vm = individual.features[1]

            time_orig_pred = float(preditor_original.getResultsTime()) * amount_orig_vm 
            cost_orig_pred = float(preditor_original.getResultsCost()) * amount_orig_vm  

            preditor_original = PerformancePredictor(individual.features[5]['mips'], individual.features[5]['coresVM'],
                                            individual.features[5]['price'], individual.features[2],
                                            individual.features[3], individual.features[1]) 
            
            time_sup_pred = float(preditor_original.getResultsTime()) * amount_sup_vm
            cost_sup_pred = float(preditor_original.getResultsCost()) * amount_sup_vm   

            time = time_orig_pred + time_sup_pred
            cost = cost_orig_pred + cost_sup_pred                                      

            #with open("/multiexplorer/MultiExplorer/src/MultiExplorerVM/resultado.txt", 'a') as results:
            #    if os.stat("/multiexplorer/MultiExplorer/src/MultiExplorerVM/resultado.txt").st_size == 0:
            #        results.write("{:^50} {:^19} {:^7} {:^27} {:^17}\n".format("CONFIG", "TIME", "COST", "PRED_TIME", "COST_TIME"))

            #    results.write("{:^50} {:^19} {:^7} {:^27} {:^17}\n".format("{}x {} & {}x {}".format(individual.features[0], individual.features[4]["name"],
            #                                                                            individual.features[1], individual.features[5]['id']),
            #                                                    time, cost, "{} ({} + {})".format(time_orig_pred+time_sup_pred, time_orig_pred, time_sup_pred), 
            #                                                    "{} ({} + {})".format(cost_orig_pred+cost_sup_pred, cost_orig_pred,cost_sup_pred)))

        #################################################################################################################################################

        self.objDict[num]["Results"]["time_pred"] = time
        self.objDict[num]["Results"]["cost_pred"] = cost


    def writeResults(self):
        jsonFile = open(self.outputPath+self.outputName, "w")
        jsonFile.write(json.dumps(self.objDict, indent= 4, sort_keys=True))
        jsonFile.close()
    
    # método responsável por extrair resultados de simulação uteis do desempenho como:
    # power density
    # area core
    # peak dynamic
    # core amount
    def readInputFromMcpat(self):
        mcpatDict = {}
        contArea = 0
        contPeakDynamic = 0
        contSubthresholdLeakage= 0
        contGateLeakage= 0
        linesMCPATFile = []

        with open(self.inputPathForMCPATFile) as inFile:
            for line in inFile:
                linesMCPATFile.append(line)

        for line in linesMCPATFile:
            if '*Power Density' in line:
                power_density_orig = line.split()[3]
               
            if 'Total Cores' in line:
                amount_original_cores = line.split()[2]

            if 'Core:' in line:
                area_orig = linesMCPATFile[linesMCPATFile.index(line)+1].split()[2]
                peak_dynamic = linesMCPATFile[linesMCPATFile.index(line)+2].split()[3]
                subthreshold_leakage = linesMCPATFile[linesMCPATFile.index(line)+3].split()[3]
                gate_leakage = linesMCPATFile[linesMCPATFile.index(line)+5].split()[3]


        mcpatDict["power_density_orig"] = round(float(power_density_orig), 3)
        mcpatDict["amount_original_cores"] = int(amount_original_cores)
        mcpatDict["area_orig"] = float(area_orig)
        mcpatDict["power_orig"] = round(float(peak_dynamic )+float(subthreshold_leakage)+float(gate_leakage), 3)
        mcpatDict["power_density_orig"] = round(float(0.0475), 3)

        return mcpatDict

    def readInputFromPerformanceSim(self):
        sniperDict = {}
        sniperDict["performance_orig"] = self.selector.get_performance_in_db()
        return sniperDict

    #faz o interfaceamento entre a Descrição de DSE passada pelo usuário, e o dicionário de entrada do algoritmo
    def makeInputDict(self):
        """
         Este método, ao final retornará um dicionário que será a entrada do nsga, como no modelo abaixo:
        
        {
            "parameters":{
                "amount_original_cores":[-,-],
                "area_orig":[-,-],
                "power_orig":[-,-],
                "performance_orig":[-,-],
                "amount_ip_cores":[-,-]
            },
            "restrictions":
            {
                "total_area":[-,-],
                "power_density":[-,-]
            }
        }
        
         amount original cores --> é a quantidade de cores originais que serão explorador no nsga
         area_orig --> é o tamanho de área do core original (este intervalo não vai variar, por exemplo
           se tivermos um processador com 100mm2 de área, o intervalo será de [100, 100])
         power_orig --> é a potência do core original
         performance_orig --> é a performance do core original, obtida através de algum simulador de performance, por exemplo, sniper ou multi2sim
         amount_ip_cores --> é a quantidade de cores ip, que serão acrescentados no projeto (cores ip, são cores diferentes do original)
        """

        def setDefault():
            print("-> default DSE input")
            parameters = {}
            restriction = {}

            mcpat = self.readInputFromMcpat()
            performanceSim = self.readInputFromPerformanceSim()

            parameters["amount_original_cores"] = [1 , mcpat["amount_original_cores"]]
            parameters["area_orig"] = [mcpat["area_orig"], mcpat["area_orig"]]
            parameters["power_orig"] = [mcpat["power_orig"], mcpat["power_orig"]]
            parameters["performance_orig"] = [performanceSim["performance_orig"], performanceSim["performance_orig"]]
            parameters["amount_ip_cores"] = [int(mcpat["amount_original_cores"])/2, int(mcpat["amount_original_cores"])*2]

            restriction["total_area"] = float(mcpat["area_orig"])*float(mcpat["amount_original_cores"])
            restriction["power_density"] = float(mcpat["power_orig"])/float(mcpat["area_orig"])  #para o força bruta

            self.inputDict["parameters"] = parameters
            self.inputDict["restrictions"] = restriction

            return self.inputDict

        def setInputDict(descriptionInput):
            parameters = {}
            restriction = {}

            parameters["model_name"]=descriptionInput["General_Modeling"]["model_name"]
            parameters["mips"]=descriptionInput["General_Modeling"]["mips"]
            parameters["coresVM"]=descriptionInput["General_Modeling"]["coresVM"]
            parameters["price_orig"]=descriptionInput["General_Modeling"]["price"]

	    
            time_orig = 0
            cost_orig = math.ceil(time_orig)*descriptionInput["General_Modeling"]["price"]

            parameters["time_orig"]=[float(time_orig), float(time_orig)]
            parameters["cost_orig"]=[float(cost_orig), float(cost_orig)]

            parameters["instructions"]= descriptionInput["DSE"]["ExplorationSpace"]["instructions_for_design"]
            parameters["corescloudlet"]= descriptionInput["DSE"]["ExplorationSpace"]["corescloudlet_for_design"]

            min_ip_core=descriptionInput["DSE"]["ExplorationSpace"]["sup_vm_for_design"][0]
            max_ip_core=descriptionInput["DSE"]["ExplorationSpace"]["sup_vm_for_design"][1]
            parameters["amount_sup_vm"] = [min_ip_core , max_ip_core]


            min_orig_core=descriptionInput["DSE"]["ExplorationSpace"]["original_vm_for_design"][0]
            max_orig_core=descriptionInput["DSE"]["ExplorationSpace"]["original_vm_for_design"][1]
            parameters["amount_original_vm"] = [min_orig_core , max_orig_core]
	    

            restriction["total_cost"] = descriptionInput["DSE"]["Constraints"]["maximum_cost"]
            restriction["total_time"] = descriptionInput["DSE"]["Constraints"]["maximum_time"] #para o força bruta

            self.inputDict["parameters"] = parameters
            self.inputDict["restrictions"] = restriction

            return self.inputDict

        descriptionInput = json.loads(open(self.inputName).read())
        
        # verificar se tem chave DSE, caso tenha, criar dicionário com o que o usuário passou no arquivo de entrada, caso contrário, 
        # criar deicionário com os valores defaults(valores defaults são valores baseados apenas nas saídas de simulação de desempenho e física)
        if descriptionInput.has_key("DSE"):
            return setInputDict(descriptionInput)
        else:
            return setDefault()


if __name__ == "__main__":
    obj = InOut()
    obj.readRangeFromIp()
    obj.readInputFromPerformanceSim()
    obj.readInputFromMcpat()
    obj.makeInputDict()
