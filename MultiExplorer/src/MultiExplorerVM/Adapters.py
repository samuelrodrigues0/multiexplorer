# -*- coding: utf-8 -*-

import json
from os import listdir
from os.path import exists
from shutil import copyfile, move
from AllowedValues import PATH_VM
from AllowedValues import PredictedModels, PredictedApplications
from .DS_DSE.cloudsim.CloudSim import CloudSim
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
                        "unit": 'USD/h'
                    }),
                    Input({
                        'label': 'Maximum Time',
                        'key': 'maximum_time',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                        "unit": 'hours'
                    }),
                ]
            }),
            InputGroup({
                'label': 'Cores Cloud set',
                'key': 'corescloudset',
                "inputs": [
                    Input({
                        'label': 'Cores Cloudlet for design',
                        'key': 'corescloudlet_for_design',
                        "is_user_input": True,
                        "required": True,
                        'type': InputType.Integer,
                        'max_val': 32,
                    })
                ]
            })
        ])

        self.project_folder = None

        self.application_code = None

        self.input_json = PATH_VM + 'sketch.json'

        self.input_json_data = None

        self.cloudsim = None

        self.presentable_results = None

    def get_results(self):
        return self.presentable_results

    def execute(self):
        self.prepare()

        mips = self.input_json_data['General_Modeling']['mips']
        price = self.input_json_data['General_Modeling']['price']
        cores_vm = self.input_json_data['General_Modeling']['coresVM']
        memory = self.input_json_data['General_Modeling']['memory']
        cores_cloudlet_for_design = self.input_json_data['DSE']['ExplorationSpace']['corescloudlet_for_design']
        app = self.input_json_data['Preferences']['application']

        self.cloudsim = CloudSim(mips, 10000, memory, cores_vm, cores_cloudlet_for_design, app/1000000)
        time = self.cloudsim.getTime() # seconds
        time = float(time.replace(',', '.')) / 3600 # horas

        self.set_presentable_results(time, price)

    def set_presentable_results(self, time, price):
        self.presentable_results = {
            'original_time' : time,
            'original_price' : price
        }

    def prepare(self):
        self.project_folder = self.get_output_path()
        self.application_code = PredictedApplications.get_instructions_for_design(self.inputs['application']['application_vm'])
        self.copy_json_to_project_folder()
        self.change_json_parameters()
        self.get_json_data()

    def get_json_data(self):
        with open(self.input_json, 'r') as json_file:
            self.input_json_data = json.load(json_file)

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
            json_data['DSE']["ExplorationSpace"]['corescloudlet_for_design'] = int(self.inputs['corescloudset']['corescloudlet_for_design'])

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
                        'label': 'Predicted Output (Normally Calculated)',
                        'key': 'run_prediction',
                        "is_user_input": False,
                        "required": False,
                        'type': InputType.Checkbutton,
                        'value': False,
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
                        "default_value": 1.0,
                    }),
                    Input({
                        'label': 'Mutation Rate',
                        'unit': '%',
                        'key': 'mutation_rate',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                        "default_value": 90.0,
                    }),
                    Input({
                        'label': 'Population Size',
                        'key': 'num_of_individuals',
                        'type': InputType.Integer,
                        "is_user_input": True,
                        "required": True,
                        "default_value": 20
                    }),
                    Input({
                        'label': 'Number of Generations',
                        'key': 'num_of_generations',
                        'type': InputType.Integer,
                        "is_user_input": True,
                        "required": True,
                        "default_value": 50
                    }),
                ],
            })
        ])

        self.nsga = None

        self.brute_force = None

        self.project_folder = None

        self.input_json = None

        self.json_data = None
        
        self.original_core = None

        self.presentable_results = None

    def execute(self):
        self.prepare()
        
        if self.inputs['exploration_space']['run_brute_force']:
            self.dse_brute_force()
        
        self.dse()

        self.register_nsga_results()

        self.register_brute_force_results()

        self.ord_values()

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

            with open(self.input_json, 'w') as json_w:
                json.dump(json_data, json_w, indent=4)
        except OSError as err_message:
            raise OSError('Error from %s : %s' % (self.input_json, err_message))

    def get_json_data(self):
        with open(self.input_json) as json_file:
            self.json_data = json.load(json_file)

    def prepare(self):
        self.project_folder = self.get_output_path()
        self.input_json = self.get_input_json()    
        self.change_json_parameters()
        self.get_json_data()

    def dse(self):
        self.nsga = Nsga2Main ( 
                        self.project_folder,
                        self.input_json,
                        float(self.inputs['nsga_parameters']['mutation_strength'])/100,
                        float(self.inputs['nsga_parameters']['mutation_rate'])/100,
                        int(self.inputs['nsga_parameters']['num_of_individuals']),
                        int(self.inputs['nsga_parameters']['num_of_generations']),
                        self.inputs['exploration_space']['run_prediction']
                    )
        print("DSE NSGA2: OK")

    def dse_brute_force(self):
        self.brute_force = DsDseBruteForce(self.project_folder, self.input_json, self.inputs['exploration_space']['run_prediction'])
        print("DSE Brute Force: OK")

    def register_nsga_results(self):
        
        results = {}

        try:
            population_results = json.load(open(self.project_folder + "/populationResults.json"))
            results['population_results'] = population_results
        except IOError:
            results['population_results'] = None

        try:
            orig_core = self.json_data["General_Modeling"]["model_name"]
            self.original_core = orig_core
        except IOError:
            orig_core = None

        self.presentable_results = {
            'nsga_solutions': {}
        }


        for s in results['population_results']:
            solution = results['population_results'][s]

            title = (
                str(solution['amount_original_vm'])
                + "x " + self.original_core
                + " & " + str(solution['amount_sup_vm'])
                + "x " + solution['core_ip']['id']
            )
            self.presentable_results['nsga_solutions'][title] = {
                'title': title,
                'nbr_sup_core' : solution['amount_sup_vm'],
                'nbr_orig_core' : solution['amount_original_vm'],
                'ip_core' : solution['core_ip']['id'],  
                'ip' : solution['core_ip'],
                'orig_core' : self.original_core,
                'total_nbr_cores' : solution['amount_sup_vm'] + solution['amount_original_vm'],
                'total_cost' : solution['Results']['total_cost'],
                'total_time' : solution['Results']['total_time'],
                'cost_pred' : solution['Results']['cost_pred'],
                'time_pred' : solution['Results']['time_pred'] #* 3600,
            }

    def register_brute_force_results(self):
        
        if not self.brute_force:
            return

        assert self.presentable_results is not None, "register_nsga_results must be called first"
        
        self.presentable_results['brute_force_solutions'] = {}
        self.presentable_results['solution_status'] = {}

        solutions = self.brute_force.final_solution
        self.presentable_results['solution_status'] = {'is_viable': True}

        if not solutions:
            solutions = self.brute_force.first_solution
            self.presentable_results['solution_status'] = {'is_viable': False}
        
        for solution in solutions:

            title = (
                str(solution['amount_orig_vm'])
                + "x " + self.original_core
                + " & " + str(solution['amount_sup_vm'])
                + "x " + solution['ip_core']['id']
            )
            
            self.presentable_results['brute_force_solutions'][title] = {
                'title': title,
                'nbr_sup_core' : solution['amount_sup_vm'],
                'nbr_orig_core' : solution['amount_orig_vm'],
                'ip_core' : solution['ip_core']['id'],
                'ip' : solution['ip_core'],
                'orig_core' : self.original_core,
                'total_nbr_cores' : solution['amount_sup_vm'] + solution['amount_orig_vm'],
                'total_cost' : solution['cost'],
                'total_time' : solution['time'],
                'cost_pred' : solution['cost_pred'],
                'time_pred' : solution['time_pred']# * 3600,
            }

    def get_results(self):
        return self.presentable_results

    def ord_values(self):
        nsga_solutions = self.presentable_results['nsga_solutions']
        self.presentable_results['sorted_nsga'] = self.get_filtered_results(nsga_solutions)

        if 'brute_force_solutions' in self.presentable_results:
            brute_force_solutions = self.presentable_results['brute_force_solutions']
            self.presentable_results['sorted_bruteforce'] = self.get_filtered_results(brute_force_solutions)

    def get_filtered_results(self, solutions):
        sorted_solutions = [key for key, value in sorted(solutions.items(), key=lambda sol: float(sol[1]['time_pred']), reverse=True)]            
        filtered_sorted_solutions = []
        solutions_length = len(sorted_solutions)
        
        for i in range(solutions_length):
            if i == (solutions_length-1):
                if solutions[filtered_sorted_solutions[-1]]['time_pred'] != solutions[sorted_solutions[i]]['time_pred']:
                    filtered_sorted_solutions.append(sorted_solutions[i])
                break

            if solutions[sorted_solutions[i]]['time_pred'] != solutions[sorted_solutions[i+1]]['time_pred']:
                filtered_sorted_solutions.append(sorted_solutions[i])
            else:
                if solutions[sorted_solutions[i]]['cost_pred'] > solutions[sorted_solutions[i+1]]['cost_pred']:
                    continue
                else:
                    sorted_solutions[i+1] = sorted_solutions[i]

        filtered_sorted_solutions = filtered_sorted_solutions[:10]

        return filtered_sorted_solutions
