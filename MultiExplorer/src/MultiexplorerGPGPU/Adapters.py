# -*- coding: utf-8 -*-
import json
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
from MultiExplorer.src.config import PATH_REPO

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
sys.path.insert(0, importPath)
importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/DS_DSE/nsga2/'
sys.path.insert(0, importPath)
importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/DS_DSE/'
sys.path.insert(0, importPath)
importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/DS_DSE/brute_force/'
sys.path.insert(0, importPath)"""
importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/PerformanceExploration/GPGPU'
sys.path.insert(0, importPath)

from GPGPU import GPGPU
#from Multi2Sim import Multi2Sim
#from Sniper import Sniper
#from MPSoCBench import MPSoCBench
#from McPAT import McPAT
#from DS_DSE import Nsga2Main
#from DS_DSE.brute_force import DsDseBruteForce


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
        self.simTool.parse()
        self.simTool.execute()
        self.simTool.convertResults()


    def prepare(self):
        
        self.inFile = self.inFile = PredictedModels.get_json_path(self.inputs['Settings']['model'])

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
                        "required": False,
                    }),
                    Input({
                        'label': 'Maximum Area',
                        'unit': 'mm²',
                        'key': 'maximum_area',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": False,
                    }),
                ],
            }),
        ])

        self.dse_engine = None

    def execute(self):
        self.prepare()

        #self.dse_engine.run()

        #self.register_results()


    def prepare(self):
        pass


