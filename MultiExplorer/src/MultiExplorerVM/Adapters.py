# -*- coding: utf-8 -*-

import json
from os import listdir
from os.path import exists
from shutil import copyfile, move
from AllowedValues import PATH_VM
from AllowedValues import PredictedModels, PredictedApplications
from .DS_DSE.Nsga2MainVM import Nsga2Main
from ..Infrastructure.Inputs import Input, InputGroup, InputType
from ..Infrastructure.ExecutionFlow import Adapter
from .DS_DSE.brute_force.DsDseBruteForce import DsDseBruteForce


class CloudsimAdapter(Adapter):
   
    def __init__(self):
        Adapter.__init__(self)

        self.set_inputs([
            InputGroup({
                'label': "Application",
                'key': 'application',
                "inputs": [
                    Input({
                        "label" : "Model VM",
                        "key" : "model_vm",
                        "is_user_input" : True,
                        "required" : True,
                        "allowed_values" : PredictedModels.get_dict(),
                    }),
                    Input({
                        "label" : "Applicaton VM",
                        "key" : "application_vm",
                        "is_user_input" : True,
                        "required" : True,
                        "allowed_values" : PredictedApplications.get_dict(),
                    }),
                ]
            }),
            InputGroup({
                'label': "Constraints",
                'key': 'constraints',
                "inputs": [
                    Input({
                       'label': 'Maximum Cost',
                        'key': 'maximum_cost',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                    }),
                    Input({
                        'label': 'Maximum Time',
                        'key': 'maximum_time',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                    }),
                ]
            })
        ])

        self.project_folder = None

        self.application_code = None

        self.input_json = PATH_VM + 'sketch.json'

    def execute(self):
        self.prepare()

    def prepare(self):
        self.project_folder = self.get_output_path()
        self.application_code = PredictedApplications.get_instructions_for_design(self.inputs['application']['application_vm'])
        self.copy_json_to_project_folder()
        self.change_json_parameters()

    def copy_json_to_project_folder(self):
        destinated_json = self.create_project_folder_json()
        try:
            copyfile(self.input_json, destinated_json)
        except OSError as err_message:
            raise OSError('Error while copying %s to %s : %s' % (self.input_json, destinated_json, err_message))
        self.input_json = destinated_json
        
    def create_project_folder_json(self):
        path = self.project_folder + '/' + PredictedModels.get_model_name(self.inputs['application']["model_vm"]) + '.json'
        try:
            with open(path, 'w'):
                pass
        except OSError as err_message:
            raise OSError('Can\'t create %s : %s' % (path, err_message))

        return path

    def change_json_parameters(self):
        try:
            with open(self.input_json, 'r') as json_r:
                json_data = json.load(json_r)

            model = self.inputs['application']['model_vm']
            json_data['General_Modeling']['mips'] = PredictedModels.get_mips(model)
            json_data['General_Modeling']['price'] = PredictedModels.get_price(model)
            json_data['General_Modeling']['memory'] = PredictedModels.get_memory(model)
            json_data['General_Modeling']['coresVM'] = PredictedModels.get_coresVM(model)
            json_data['General_Modeling']['model_name'] = PredictedModels.get_model_id(model)
            json_data['Preferences']['application'] = self.application_code
            json_data['Preferences']['project_name'] = json_data['General_Modeling']['model_name'] + '-' + str(self.application_code)
            json_data['DSE']['Constraints']['maximum_cost'] = float(self.inputs['constraints']['maximum_cost'])
            json_data['DSE']['Constraints']['maximum_time'] = float(self.inputs['constraints']['maximum_time'])
            json_data['DSE']['ExplorationSpace']['instructions_for_design'] = self.application_code

            with open(self.input_json, 'w') as json_w:
                json.dump(json_data, json_w, indent=4)
                
        except OSError as err_message:
            raise OSError('Error from %s : %s' % (self.input_json, err_message))


class NsgaIIPredDSEAdapter(Adapter):

    def __init__(self):
        Adapter.__init__(self)

        self.set_inputs([
            InputGroup({
                'label': "Exploration Space",
                'key': 'exploration_space',
                'inputs': [
                    Input({
                        'label': 'Run brute force aswell',
                        'key': 'run_brute_force',
                        "is_user_input": True,
                        "required": False,
                        'type': InputType.Checkbutton,
                        'value': True,
                    }),
                    Input({
                        'label': 'Cores Cloudlet for design',
                        'key': 'corescloudlet_for_design',
                        "is_user_input": True,
                        "required": True,
                        'type': InputType.Integer,
                        'max_val': 32,
                    }),
                    Input({
                        'label': 'Original number VM for design',
                        'key': 'original_vm_for_design',
                        "is_user_input": True,
                        "required": True,
                        'type': InputType.IntegerRange,
                        'min_val': 1,
                        'max_val': 31,
                    }),
                    Input({
                        'label': 'Suplementar number VM for design',
                        'key': 'sup_vm_for_design',
                        "is_user_input": True,
                        "required": True,
                        "type": InputType.IntegerRange,
                        "min_val": 1,
                        "max_val": 32,
                    })
                ],
            }),
        ])

        self.dsdse = None

        self.brute_force = None

        self.project_folder = None

        self.input_json = None
        
    def execute(self):
        self.prepare()
        
        if self.inputs['exploration_space']['run_brute_force']:
            self.dseBruteForce()
        
        self.dse()

    def get_json_name(self):
        dir_names = listdir(self.project_folder)
        jsons = [dir for dir in dir_names if dir.endswith(".json")]
        
        assert len(jsons) != 0, "No input json in project folder"
        
        return jsons[0]
    
    def get_input_json(self):
        return self.project_folder + '/' + self.get_json_name()

    def change_json_parameters(self):
        try:
            with open(self.input_json) as json_r:
                json_data = json.load(json_r)
                
            json_data['DSE']['ExplorationSpace']['original_vm_for_design'][0] = int(self.inputs['exploration_space']['original_vm_for_design'][0])
            json_data['DSE']['ExplorationSpace']['original_vm_for_design'][1] = int(self.inputs['exploration_space']['original_vm_for_design'][1])
            json_data['DSE']['ExplorationSpace']['sup_vm_for_design'][0] = int(self.inputs['exploration_space']['sup_vm_for_design'][0])
            json_data['DSE']['ExplorationSpace']['sup_vm_for_design'][1] = int(self.inputs['exploration_space']['sup_vm_for_design'][1])
            json_data['DSE']["ExplorationSpace"]['corescloudlet_for_design'] = int(self.inputs['exploration_space']['corescloudlet_for_design'])

            with open(self.input_json, 'w') as json_w:
                json.dump(json_data, json_w, indent=4)
        except OSError as err_message:
            raise OSError('Error from %s : %s' % (self.input_json, err_message))
        
    def prepare(self):
        self.project_folder = self.get_output_path()
        self.input_json = self.get_input_json()    
        self.change_json_parameters()

    def dse(self):
        self.dse = Nsga2Main(self.project_folder, self.input_json)
        print ("DSE NSGA2: OK")

    def dseBruteForce(self):
        self.brute_force = DsDseBruteForce(self.project_folder, self.input_json)
        print ("DSE Brute Force: OK")
