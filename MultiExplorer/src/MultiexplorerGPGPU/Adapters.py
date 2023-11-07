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


class GPGPUSimulatorAdapter(Adapter):
    def __init__(self):
        Adapter.__init__(self)

        self.presenter = None

        self.set_inputs([
            InputGroup({
                'label': "Settings",
                'key': 'Settings',
                "inputs": [
                    Input({
                        "label" : "GPU Model",
                        "key" : "model_gpu",
                        "is_user_input" : True,
                        "required" : True,
                        "allowed_values" : PredictedModels.get_dict(),
                    })
                ]
            }),
        ])

        self.config = {}

        self.results = {}

        self.presentable_results = None

        self.use_benchmarks = True

        self.benchmark_size = None

        self.dse_settings_file_name = None

        self.cfg_path = None

        self.output_path = None


    def set_values_from_json(self, absolute_file_path):
        """
        This method reads a json file and sets the values of the inputs.
        """
        input_json = json.loads(open(absolute_file_path).read())


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
                        "required": True,
                        'type': InputType.IntegerRange,
                        'min_val': 1,
                        'max_val': 31,
                    }),
                    Input({
                        "label" : "Application",
                        "key" : "app",
                        "is_user_input" : True,
                        "required" : True,
                        "allowed_values" : Applications.get_dict()
                    }),
                    Input({
                        'label': 'Original Cores for desing',
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
                    }),
                    Input({
                        'label': 'Maximum Area',
                        'unit': 'mm²',
                        'key': 'maximum_area',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                    }),
                ],
            }),
        ])

        self.dse_engine = None

    def execute(self):
        self.prepare()

        self.dse_engine.run()

        self.register_results()
