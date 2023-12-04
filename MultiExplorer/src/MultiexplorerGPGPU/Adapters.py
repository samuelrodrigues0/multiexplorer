# -*- coding: utf-8 -*-
import json, time
import os
import sys
import re
from typing import Dict, Union, Any, Optional
from xml.dom import minidom
from xml.etree import ElementTree
from MultiExplorer.src.MultiexplorerGPGPU.AllowedValues import PredictedModels, Applications, Configs
from MultiExplorer.src.Infrastructure.ExecutionFlow import Adapter
from MultiExplorer.src.Infrastructure.Inputs import Input, InputGroup, InputType
from MultiExplorer.src.config import PATH_PRED_VM
from MultiExplorer.src.config import PATH_REPO, PATH_RUNDIR
from MultiExplorer.src.metric import *
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


class GPGPUSimulatorAdapter(Adapter):
    
    def __init__(self):
        Adapter.__init__(self)

        self.set_inputs([
            InputGroup({
                'label': "Settings",
                'key': 'Settings',
                "inputs": [
                    Input({
                        "label" : "Model",
                        "key" : "model",
                        "is_user_input" : True,
                        "required" : True,
                        "allowed_values" : PredictedModels.get_dict(),
                    }),
                    Input({
                        "label" : "Application",
                        "key" : "app",
                        "is_user_input" : True,
                        "required" : False,
                        "allowed_values" : Applications.get_dict()
                    })
                ]
            }),
        ])

        self.inFile = None

        self.inJson = None
        
        self.simTool = None

        self.dirListB4 = os.listdir(PATH_REPO)
        
        #self.folderOldSimul = None
    

    def execute(self):
        self.prepare()
        self.sim_execute()
        self.project_folder()


    def prepare(self):
        
        global jsonLocation

        self.inFile = PredictedModels.get_json_path(self.inputs['Settings']['model'])
        jsonLocation = self.inFile

        with open(self.inFile) as data_file:
            self.inJson = json.load(data_file)
            
        self.simTool = GPGPU(self.inFile, app=Applications.get_model(self.inputs['Settings']['app']))



    def sim_execute(self):
        self.simTool.parse()
        self.simTool.execute()
        self.simTool.convertResults()
 

    def project_folder(self):

        global projectFolder

        path = PATH_RUNDIR + '/Multiexplorer_GPGPU/'
        dirs = [f for f in os.listdir(PATH_RUNDIR + '/Multiexplorer_GPGPU/') if os.path.isdir(os.path.join(path, f))]
        sorted_dirs = sorted(dirs, key=lambda d: os.path.getctime(os.path.join(path, d)), reverse=True)
        projectFolder = path + sorted_dirs[0]

        """if PredictedModels.get_sim_tool(self.inputs['Settings']['model']) == "gpgpusim":
                for f in os.listdir(PATH_RUNDIR + '/Multiexplorer_GPGPU/'):
                    if f.startswith(self.inJson['Preferences']['project_name']):
                        projectFolder=os.path.join("rundir/Multiexplorer_GPGPU/", f)
                        break  """


class DSEAdapter(Adapter):

    def __init__(self):
        Adapter.__init__(self)

        self.set_inputs([
            InputGroup({
                'label': "DSE Settings",
                'key': 'dse_Settings',
                "inputs": [
                    Input({
                        'label': 'Run brute force aswell',
                        'key': 'run_brute_force',
                        "is_user_input": True,
                        "required": False,
                        'type': InputType.Checkbutton,
                        'value': True,
                    }),
                    Input({
                        "label" : "DSE Config",
                        "key" : "dse_config",
                        "is_user_input" : True,
                        "required" : False,
                        "allowed_values" : Configs.get_dict()
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
                        "required": False,
                        'type': InputType.IntegerRange,
                        'min_val': 1,
                        'max_val': 31,
                    }),
                    Input({
                        'label': 'Original Cores for design',
                        'key': 'original_cores_for_design',
                        "is_user_input": True,
                        "required": False,
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
                        "default_value":1
                    }),
                    Input({
                        'label': 'Maximum Area',
                        'unit': 'mm²',
                        'key': 'maximum_area',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                        "default_value":1
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
                        "default_value": 10.0,
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
                        "default_value": 150
                    }),
                ],
            })
        ])

        self.dse_engine = None

        self.inFile = None
        self.inJson = None


    def execute(self):
        self.prepare()

        #self.dseBruteForce()

        self.dse()


    def prepare(self):
        
        self.inFile = jsonLocation
    
        with open(self.inFile) as data_file:
            self.inJson = json.load(data_file)


    def dse(self):

        if self.inJson['Preferences']['DSE']:
            start = time.time()
            print('RAPAZ... ', self.inFile)
            Nsga2Main(projectFolder)
            print("DSE NSGA2: OK") 
            end = time.time()
            print("The time of execution of NSGA program is :", end-start)
            #self.suggestedArchitecture()

    def dseBruteForce(self):

        neg_mean_absolute_percentage_scorer = metrics.make_scorer(mean_absolute_percentage_error, greater_is_better=False)
        if self.inJson['Preferences']['DSE']:
            start = time.time()
            print('\n\n')
            print("DseBruteFORCE:")
            print('\n\n')
            print("JSON FILE: ", self.inFile)
            print("PROJECT FOLDER: ", projectFolder)
            DsDseBruteForce(projectFolder, pathCSV=self.inFile)
            end = time.time()
            print("DSE Brute Force: OK")
            print("The time of execution of BF program is :", end-start)

