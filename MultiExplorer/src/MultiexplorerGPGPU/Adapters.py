# -*- coding: utf-8 -*-
import json, time
import os
import sys
import re
from typing import Dict, Union, Any, Optional
from xml.dom import minidom
from xml.etree import ElementTree
from MultiExplorer.src.MultiexplorerGPGPU.AllowedValues import PredictedModels, Applications
from MultiExplorer.src.Infrastructure.ExecutionFlow import Adapter
from MultiExplorer.src.Infrastructure.Inputs import Input, InputGroup, InputType
from MultiExplorer.src.config import PATH_REPO, PATH_RUNDIR
from .DS_DSE.metric import *
from sklearn import metrics


importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/DS_DSE/nsga2/'
sys.path.insert(0, importPath)
importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/DS_DSE/'
sys.path.insert(0, importPath)
importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/DS_DSE/brute_force/'
sys.path.insert(0, importPath)
importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/PerformanceExploration/GPGPU'
sys.path.insert(0, importPath)

from GPGPU import GPGPU
from DS_DSE.Nsga2Main import Nsga2Main
from DsDseBruteForce import DsDseBruteForce


projectFolder = None


class GPGPUSimulatorAdapter(Adapter):
    
    def __init__(self):
        Adapter.__init__(self)

        self.set_inputs([
            InputGroup({
                'label': None,
                'key': 'settings',
                "inputs": [
                    InputGroup({
                        'label': "Model Settings",
                        'key': "model_settings",
                        "inputs": [
                            Input({
                                "label" : "Model",
                                "key" : "model_name",
                                "is_user_input" : True,
                                "required" : True,
                                "allowed_values" : PredictedModels.get_dict(),
                            }),
                            Input({
                                "label" : "Application",
                                "key" : "app",
                                "is_user_input" : True,
                                "required" : True,
                                "allowed_values" : Applications.get_dict()
                            }),
                        ]
                    })
                ]
            })
        ])

        self.inFile = None

        self.inJson = None
        
        self.simTool = None

        self.dirListB4 = os.listdir(PATH_REPO)
        
        self.presentable_results = None    

    def execute(self):
        
        print('\n'*3 + '-'*20 + 'Simulation' + '-'*20)
        self.prepare()
        self.sim_execute()
        self.project_folder()
        self.change_json_in_project_folder()
        self.check_results()
        self.register_simulation_results()
        print('\n'*3)

    def prepare(self):
        global jsonLocation

        self.inFile = PredictedModels.get_json_path(self.inputs['settings']["model_settings"]['model_name'])
        jsonLocation = self.inFile

        with open(self.inFile) as data_file:
            self.inJson = json.load(data_file)

        self.simTool = GPGPU(input=self.inputs['settings'], jsonFile=self.inFile, app=Applications.get_model(self.inputs['settings']["model_settings"]['app']))

    def sim_execute(self):
        self.simTool.parse()
        self.simTool.execute() 

    def project_folder(self):
        global projectFolder

        path = PATH_RUNDIR + '/Multiexplorer_GPGPU/'
        dirs = [f for f in os.listdir(PATH_RUNDIR + '/Multiexplorer_GPGPU/') if os.path.isdir(os.path.join(path, f))]
        sorted_dirs = sorted(dirs, key=lambda d: os.path.getctime(os.path.join(path, d)), reverse=True)
        projectFolder = path + sorted_dirs[0]

    def change_json_in_project_folder(self):
        dirs = os.listdir(projectFolder)
        json_dirs = [x for x in dirs if x.endswith(".json")]

        if len(json_dirs) == 1:
            json_path = projectFolder + '/' + json_dirs[0]
        else:
            raise Exception("More than one .json in project folder")
        
        gui_data = self.inputs['settings'].get_dict()
        
        with open(json_path) as data_file:
            json_data = json.load(data_file)
            
        json_data['Preferences']['application'] = Applications.get_model(gui_data['app'])
        json_data['Preferences']['project_name'] = PredictedModels.get_model(gui_data['model_name']) + '_' + Applications.get_model(gui_data['app'])

        with open(json_path, 'w') as data_file:
            json.dump(json_data, data_file, sort_keys=True, indent=4)


    def check_results(self):
        global projectFolder

        path_output = projectFolder + '/output/BFSOutput.txt'
        path_err = projectFolder + '/output/BFSstderr.txt'
        gpgpusim_first_finished_text = "GPGPU-Sim: *** exit detected ***"
        gpgpusim_second_finished_text = "----------------------------END-of-Interconnect-DETAILS-------------------------\n"

        try:
            with open(path_output) as output_file:
                output_content = output_file.readlines()

            with open(path_err) as err_file:
                err_content = err_file.readlines()

            if output_content and not err_content and output_content[-1].strip() == gpgpusim_first_finished_text and \
                gpgpusim_second_finished_text in output_content:
                print("GPGPU-Sim finished running")
            else:
                raise Exception("GPGPU-Sim failed while running")

        except IOError:
            raise Exception("No GPGPU-Sim output found")


    def register_simulation_results(self):
        global projectFolder

        path = projectFolder + '/output/BFSOutput.txt'

        try:
            with open(path) as simulation_file:
                
                simulation_output = simulation_file.readlines()

                output_length = len(simulation_output)

                gpgpusim__text = "----------------------------END-of-Interconnect-DETAILS-------------------------\n"

                i = 1
                while(simulation_output[-i] != gpgpusim__text):
                    i += 1

                simulation_output = "".join(simulation_output[output_length - i:])

                sim_time = int(re.search(r"gpgpu_simulation_time = .* \((\d+) sec\)", simulation_output).group(1))
                sim_instructions_rate = int(re.search(r"gpgpu_simulation_rate = (\d+) \(inst/sec\)", simulation_output).group(1))
                sim_cycles_rate = int(re.search(r"gpgpu_simulation_rate = (\d+) \(cycle/sec\)", simulation_output).group(1))


            self.presentable_results = {
                'simulation_time': sim_time,
                'simulation_instructions_rate' : sim_instructions_rate,
                'simulation_cycles_rate': sim_cycles_rate
            }

        except IOError:
            raise "No GPGPU-Sim output found"


    def get_results(self):
        return self.presentable_results


class DSEAdapter(Adapter):

    def __init__(self):
        
        Adapter.__init__(self)

        self.set_inputs([
            InputGroup({
                'label': None,
                'key': 'settings',
                "inputs": [
                    InputGroup({
                        'label': "DSE Settings",
                        'key': 'dse_settings',
                        "inputs": [
                            Input({
                                'label': 'Run brute force aswell',
                                'key': 'run_brute_force',
                                "is_user_input": True,
                                "required": False,
                                'type': InputType.Checkbutton,
                                'value': True,
                            })
                        ]
                    }),
                    InputGroup({
                        'label': "Exploration Space",
                        'key': 'exploration_space',
                        'inputs': [
                            Input({
                                'label': 'GPU Cores for design',
                                'key': 'gpu_cores_for_design',
                                "is_user_input": True,
                                "required": True,
                                'type': InputType.IntegerRange,
                                'min_val': 1,
                                'max_val': 31,
                            }),
                            Input({
                                'label': 'Original Cores for design',
                                'key': 'original_cores_for_design',
                                "is_user_input": True,
                                "required": True,
                                "type": InputType.IntegerRange,
                                "min_val": 1,
                                "max_val": 32,
                            })
                        ],
                    }),
                    InputGroup({
                        'label': "Constraints",
                        'key': 'constraints',
                        'inputs': [
                            Input({
                                'label': 'Maximum Power Density',
                                'unit': 'V/mm²',
                                'key': 'maximum_power_density',
                                'type': InputType.Float,
                                "is_user_input": True,
                                "required": True,
                                "default_value":0.3
                            }),
                            Input({
                                'label': 'Maximum Area',
                                'unit': 'mm²',
                                'key': 'maximum_area',
                                'type': InputType.Float,
                                "is_user_input": True,
                                "required": True,
                                "default_value":200
                            }),
                        ],
                    }),
                    InputGroup({
                        'label': "NSGA-II Parameters",
                        'key': 'nsga_parameters',
                        'inputs': [
                            Input({
                                'label': 'Crossing Rate',
                                'unit': '%',
                                'key': 'mutation_strength',
                                'type': InputType.Float,
                                "is_user_input": True,
                                "required": True,
                                "default_value": 50.0,
                            }),
                            Input({
                                'label': 'Mutation Rate',
                                'unit': '%',
                                'key': 'mutation_rate',
                                'type': InputType.Float,
                                "is_user_input": True,
                                "required": True,
                                "default_value": 99.0,
                            }),
                            Input({
                                'label': 'Population Size',
                                'key': 'num_of_individuals',
                                'type': InputType.Integer,
                                "is_user_input": True,
                                "required": True,
                                "default_value": 10
                            }),
                            Input({
                                'label': 'Number of Generations',
                                'key': 'num_of_generations',
                                'type': InputType.Integer,
                                "is_user_input": True,
                                "required": True,
                                "default_value": 2
                            }),
                        ],
                    })
                ]
            })
        ])

        self.inFile = None
        
        self.inJson = None

        self.presentable_results = None

        self.brute_force = None

        self.nsga = None

        self.original_core = None


    def execute(self):
        
        print('-'*20 + 'DSE' + '-'*20)

        self.prepare()

        mod_json_path = self.change_json_in_project_folder()
        #mod_json_path = self.inJson
        
        
        if self.inputs['settings']['dse_settings']['run_brute_force']:
            self.dseBruteForce(mod_json_path)

        self.dse(mod_json_path)
        
        self.register_results() # nsga

        if self.inputs['settings']['dse_settings']['run_brute_force']: # arrumar depois
            self.register_brute_force_results() #bruteforce

        #print(self.presentable_results)

        print('\n'*3)

    def prepare(self):
        self.inFile = jsonLocation
    
        with open(self.inFile) as data_file:
            self.inJson = json.load(data_file)


    def change_json_in_project_folder(self):
        dirs = os.listdir(projectFolder)
        json_dirs = [x for x in dirs if x.endswith(".json")]

        if len(json_dirs) == 1:
            json_path = projectFolder + '/' + json_dirs[0]
        else:
            raise Exception("More than one .json in project folder")
        
        gui_data = self.inputs['settings'].get_dict()
        

        with open(json_path) as data_file:
            json_data = json.load(data_file)
   
        json_data['DSE']['ExplorationSpace']['ip_cores_for_design'][0] = gui_data['gpu_cores_for_design'][0]
        json_data['DSE']['ExplorationSpace']['ip_cores_for_design'][1] = gui_data['gpu_cores_for_design'][1]
        json_data['DSE']['ExplorationSpace']['original_cores_for_design'][0] = gui_data['original_cores_for_design'][0]
        json_data['DSE']['ExplorationSpace']['original_cores_for_design'][1] = gui_data['original_cores_for_design'][1]
        json_data['DSE']['Constraints']['maximum_powerDensity'] = gui_data['maximum_power_density']
        json_data['DSE']['Constraints']['maximum_area'] = gui_data['maximum_area']
        json_data['DSE']['Constraints']['application'] = json_data['Preferences']['application']

        with open(json_path, 'w') as data_file:
            json.dump(json_data, data_file, sort_keys=True, indent=4)

        return json_path

    def dse(self, json_project_folder):
        start = time.time()
        self.nsga = Nsga2Main(projectFolder, json_project_folder, self.inputs['settings'])
        print("DSE NSGA2: OK") 
        end = time.time()
        print("The time of execution of NSGA program is :", end-start)

    def dseBruteForce(self, json_project_folder):
        neg_mean_absolute_percentage_scorer = metrics.make_scorer(mean_absolute_percentage_error, greater_is_better=False)
        start = time.time()
        self.brute_force = DsDseBruteForce(projectFolder, pathCSV=json_project_folder)
        end = time.time()
        print("DSE Brute Force: OK")
        print("The time of execution of BF program is :", end-start)

    def register_results(self):
        results = {}

        try:
            population_results = json.load(open(projectFolder + "/populationResults.json"))
            results['population_results'] = population_results
        except IOError:
            results['population_results'] = None

        try: # nao ajustado !!!
            #dse_settings = json.load(open(self.get_output_path() + "/dse_settings.json"))
            #orig_core = dse_settings['processor'] + '_' + dse_settings['technology']
            orig_core = self.inJson["General_Modeling"]["model_name"] + '_' + self.inJson["General_Modeling"]["power"]["technology_node"] + 'nm'
            self.original_core = orig_core
        except IOError:
            orig_core = None

        self.results = results

        self.presentable_results = {
            'solutions': {},
            'performance_simulation' : {},
            'solution_status': {}
        }

        if self.brute_force:
            simulation_inputs = self.brute_force.inputDict['parameters']
            orig_core_performance = self.brute_force.preditor.performance_core_original
        else:
            simulation_inputs = self.nsga.inputDict['parameters']
            orig_core_performance = self.nsga.preditor.performance_core_original
        
        pow_density = float(simulation_inputs["power_orig"][0])/float(simulation_inputs["area_orig"][0])

        #arrumar
        self.presentable_results['performance_simulation'] = {
            'performance': [orig_core_performance, orig_core_performance],
            'power_density': [pow_density, pow_density]
        }

        for s in results['population_results']:
            solution = results['population_results'][s]
            
            title = (
                str(solution['amount_original_cores'])
                + "x " + orig_core
                + " & " + str(solution['amount_ip_cores'])
                + "x " + solution['core_ip']['id']
            )
            self.presentable_results['solutions'][title] = {
                'title': title,
                'nbr_ip_cores': solution['amount_ip_cores'],
                'nbr_orig_cores': solution['amount_original_cores'],
                'ip_core': solution['core_ip']['id'],
                'orig_core': orig_core,
                'total_nbr_cores': solution['amount_ip_cores'] + solution['amount_original_cores'],
                'total_area': solution['Results']['total_area'],
                'performance': abs(float(solution['Results']['performance_pred'])),
                'power_density': solution['Results']['total_power_density']
            }

    def get_results(self):
        return self.presentable_results
    
    def register_brute_force_results(self):
        if not self.brute_force:
            return
        
        solutions = self.brute_force.viable_solutions
        self.presentable_results['solution_status'] = {'is_viable': True}

        if not solutions:
            solutions = self.brute_force.all_solutions
            self.presentable_results['solution_status'] = {'is_viable': False}

        self.presentable_results['brute_force_solutions'] = {}
        
        for solution in solutions:
            title = (
                str(solution['amount_orig_core'])
                + "x " + self.original_core
                + " & " + str(solution['amount_ip_core'])
                + "x " + solution['ip_core']['id']
            )
            self.presentable_results['brute_force_solutions'][title] = {
                'title': title,
                'nbr_ip_cores': solution["amount_ip_core"],
                'nbr_orig_cores': solution["amount_orig_core"],
                'ip_core': solution["ip_core"]["id"],
                'orig_core': self.original_core,
                'total_nbr_cores': solution["amount_ip_core"] + solution["amount_orig_core"],
                'total_area': round(float(solution["area"]), 2),
                'performance': round(float(solution["performancePred"]), 2),
                'power_density': round(float(solution["powerDensity"]), 2)
            }
        
            
