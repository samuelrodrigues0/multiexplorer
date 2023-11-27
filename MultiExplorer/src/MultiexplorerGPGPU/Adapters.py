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
from MultiExplorer.src.config import PATH_PRED_VM
from MultiExplorer.src.config import PATH_REPO, PATH_RUNDIR
from MultiExplorer.src.metric import *
from sklearn import metrics

"""importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/PerformanceExploration/Multi2Sim'
sys.path.insert(0, importPath)
importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/PerformanceExploration/Sniper'
sys.path.insert(0, importPath)
importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/PhysicalExploration/McPAT'
sys.path.insert(0, importPath)
importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/PerformanceExploration/MPSoCBench'
sys.path.insert(0, importPath)"""
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
#from Multi2Sim import Multi2Sim
#from Sniper import Sniper
#from MPSoCBench import MPSoCBench
#from McPAT import McPAT
from DS_DSE import Nsga2Main
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
                        "label" : "Application (GPU-ONLY)",
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


    def prepare(self):
        
        global jsonLocation

        self.inFile = PredictedModels.get_json_path(self.inputs['Settings']['model'])
        jsonLocation = self.inFile
        print(self.inFile, jsonLocation)

        with open(self.inFile) as data_file:
            self.inJson = json.load(data_file)
            
        def multi2sim():
            path = importPath + '/PerformanceExploration/Multi2Sim/'
            self.simTool = Multi2Sim(
                self.inFile, "paramMap.json", "PerformanceMap_new.json")
            pass

        def sniper():
            #print self.inJson['Preferences']['application']
            self.simTool = Sniper(self.inFile, self.inJson['Preferences']['application'])
            pass
        def gpgpusim():
            self.simTool = GPGPU(self.inFile, app=Applications.get_model(self.inputs['Settings']['app']))
            pass
        def mpsocbench():
            self.simTool = MPSoCBench(
                self.inFile, "paramMap.json", "PerformanceMap_new.json")
            pass

        eval(PredictedModels.get_sim_tool(self.inputs['Settings']['model']) + '()')

        self.project_folder()


    def sim_execute(self):
        self.simTool.parse()
        self.simTool.execute()
        self.simTool.convertResults()
 

    def project_folder(self):

        global projectFolder
        if PredictedModels.get_sim_tool(self.inputs['Settings']['model']) =="gpgpusim":
                for f in os.listdir(PATH_RUNDIR + '/Multiexplorer_GPGPU/'):
                    if f.startswith(self.inJson['Preferences']['project_name']):
                        projectFolder=os.path.join("rundir/Multiexplorer_GPGPU/", f)
                        break  


class DSEAdapter(Adapter):

    def __init__(self):
        Adapter.__init__(self)

        self.set_inputs([
            InputGroup({
                'label': "Exploration Space",
                'key': 'exploration_space',
                'inputs': [
                    Input({
                        'label': 'Ip Cores for design',
                        'key': 'ip_cores_for_design',
                        "is_user_input": True,
                        "required": False,
                        'type': InputType.IntegerRange,
                        'min_val': 1,
                        'max_val': 31,
                    }),
                    Input({
                        'label': 'Original Cores for desing',
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
        ])

        self.dse_engine = None

        self.inFile = None
        self.inJson = None



    def execute(self):
        self.prepare()

        self.dseBruteForce()

        #self.dse()


    def prepare(self):
        
        self.inFile = jsonLocation
    
        with open(self.inFile) as data_file:
            self.inJson = json.load(data_file)



    def dse(self):

        if self.inJson['Preferences']['DSE']:
            start = time.time()
            Nsga2Main(projectFolder, pathCSV=self.inFile)
            print("DSE NSGA2: OK") 
            end = time.time()
            print("The time of execution of NSGA program is :", end-start)
            #self.suggestedArchitecture()

    def dseBruteForce(self):

        neg_mean_absolute_percentage_scorer = metrics.make_scorer(mean_absolute_percentage_error, greater_is_better=False)
        if self.inJson['Preferences']['DSE']:
            start = time.time()
            DsDseBruteForce(projectFolder, pathCSV=self.inFile)
            end = time.time()
            print("DSE Brute Force: OK")
            print("The time of execution of BF program is :", end-start)

