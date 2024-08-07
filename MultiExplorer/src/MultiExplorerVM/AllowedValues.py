# -*- coding: utf-8 -*-

import json
from enum import Enum
from os.path import exists
from ..config import PATH_INPUTS

PATH_VM = PATH_INPUTS + '/VM/'

"""
Modelos - c5, m5 e r5
Aplicações - 0 a 26

C5 - define o valor do mips
c5.24large - define price, coresVM e memory
c5.24large-18 - define a aplicação

Informações necessárias para executar no cloudsim:
mips, coreVM e memory
instructions for design(aplicação), 
cores cloudlet for design

Depois de executar o cloudlet calcula o tempo e devolve
o custo é o tempo que o cloudsim devolveu vezes o preço 
que vem no modelo

Inicialmente, colocar apenas a VM c5 
e as aplicações de 0 a 3

?
Em qual arquivo que eu posso encontrar onde muda na
interface gráfica?
"""

class Simulators(Enum):
    Cloudsim = 1

    @staticmethod
    def belongs(value): return value in set(item.value for item in Simulators)

    @staticmethod
    def get_label(value):
        if value == Simulators.Cloudsim:
            return "Cloudsim Simulator"

        raise ValueError("Value does not corresponds to a known simulator.")


class PredictedModels(Enum):
    m5n_ = 0
    m5n_x = 1
    m5n_2x = 2
    m5n_4x = 3
    m5n_8x = 4
    m5n_12x = 5
    m5n_24x = 6

    m5dn_ = 7
    m5dn_x = 8
    m5dn_2x = 9
    m5dn_24x = 10

    c5_ = 11
    c5_x = 12
    c5_2x = 13
    c5_4x = 14
    c5_9x = 15
    c5_12x = 16
    c5_18x = 17
    c5_24x = 18

    c5n_ = 19
    c5n_x = 20
    c5n_2x = 21
    c5n_4x = 22
    c5n_9x = 23
    c5n_18x = 24

    r5_ = 25
    r5_x = 26
    r5_2x = 27
    r5_4x = 28
    r5_8x = 29
    r5_12x = 30
    r5_24x = 31

    @staticmethod
    def load_configs():
        path = PATH_VM + 'vm.json'

        if not exists(path):
            raise OSError('File %s doesn\'t exist' % (path))

        with open(path) as config_file:
            config_json_data = json.load(config_file)
        return config_json_data["ipcores"]

    @staticmethod
    def belongs(value):
         return value in set(item.value for item in PredictedModels)

    @staticmethod
    def get_label(value):  
        for config in PredictedModels.load_configs():
            if config["id"].startswith(value.name.replace('_', '.')):
                return config["id"]

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_dict():
        return {
            PredictedModels.m5n_.value: PredictedModels.get_label(PredictedModels.m5n_),
            PredictedModels.m5n_x.value: PredictedModels.get_label(PredictedModels.m5n_x),
            PredictedModels.m5n_2x.value: PredictedModels.get_label(PredictedModels.m5n_2x),
            PredictedModels.m5n_4x.value: PredictedModels.get_label(PredictedModels.m5n_4x),
            PredictedModels.m5n_8x.value: PredictedModels.get_label(PredictedModels.m5n_8x),
            PredictedModels.m5n_12x.value: PredictedModels.get_label(PredictedModels.m5n_12x),
            PredictedModels.m5n_24x.value: PredictedModels.get_label(PredictedModels.m5n_24x),
            PredictedModels.m5dn_.value: PredictedModels.get_label(PredictedModels.m5dn_),
            PredictedModels.m5dn_x.value: PredictedModels.get_label(PredictedModels.m5dn_x),
            PredictedModels.m5dn_2x.value: PredictedModels.get_label(PredictedModels.m5dn_2x),
            PredictedModels.m5dn_24x.value: PredictedModels.get_label(PredictedModels.m5dn_24x),
            PredictedModels.c5_.value: PredictedModels.get_label(PredictedModels.c5_),
            PredictedModels.c5_x.value: PredictedModels.get_label(PredictedModels.c5_x),
            PredictedModels.c5_2x.value: PredictedModels.get_label(PredictedModels.c5_2x),
            PredictedModels.c5_4x.value: PredictedModels.get_label(PredictedModels.c5_4x),
            PredictedModels.c5_9x.value: PredictedModels.get_label(PredictedModels.c5_9x),
            PredictedModels.c5_12x.value: PredictedModels.get_label(PredictedModels.c5_12x),
            PredictedModels.c5_18x.value: PredictedModels.get_label(PredictedModels.c5_18x),
            PredictedModels.c5_24x.value: PredictedModels.get_label(PredictedModels.c5_24x),
            PredictedModels.c5n_.value: PredictedModels.get_label(PredictedModels.c5n_),
            PredictedModels.c5n_x.value: PredictedModels.get_label(PredictedModels.c5n_x),
            PredictedModels.c5n_2x.value: PredictedModels.get_label(PredictedModels.c5n_2x),
            PredictedModels.c5n_4x.value: PredictedModels.get_label(PredictedModels.c5n_4x),
            PredictedModels.c5n_9x.value: PredictedModels.get_label(PredictedModels.c5n_9x),
            PredictedModels.c5n_18x.value: PredictedModels.get_label(PredictedModels.c5n_18x),
            PredictedModels.r5_.value: PredictedModels.get_label(PredictedModels.r5_),
            PredictedModels.r5_x.value: PredictedModels.get_label(PredictedModels.r5_x),
            PredictedModels.r5_2x.value: PredictedModels.get_label(PredictedModels.r5_2x),
            PredictedModels.r5_4x.value: PredictedModels.get_label(PredictedModels.r5_4x),
            PredictedModels.r5_8x.value: PredictedModels.get_label(PredictedModels.r5_8x),
            PredictedModels.r5_12x.value: PredictedModels.get_label(PredictedModels.r5_12x),
            PredictedModels.r5_24x.value: PredictedModels.get_label(PredictedModels.r5_24x),
        }

    @staticmethod
    def get_model_name(value):
        return PredictedModels.get_dict()[value]

    @staticmethod
    def get_model_id(value):
        for config in PredictedModels.load_configs():
            if config["id"].startswith(PredictedModels.get_model_name(value).replace('_', '.')):
                return config["id"]
            
        raise ValueError("Value does not corresponds to a known predicted core.")        

    @staticmethod
    def get_mips(value):
        for config in PredictedModels.load_configs():
            if config["id"].startswith(PredictedModels.get_model_name(value).replace('_', '.')):
                return config["mips"]
            
        raise ValueError("Value does not corresponds to a known predicted core.")
    
    @staticmethod
    def get_coresVM(value):
        for config in PredictedModels.load_configs():
            if config["id"].startswith(PredictedModels.get_model_name(value).replace('_', '.')):
                return config["coresVM"]
    
        raise ValueError("Value does not corresponds to a known predicted core.")
    
    @staticmethod
    def get_price(value):
        for config in PredictedModels.load_configs():
            if config["id"].startswith(PredictedModels.get_model_name(value).replace('_', '.')):
                return config["price"]
    
        raise ValueError("Value does not corresponds to a known predicted core.")
    
    @staticmethod
    def get_memory(value):
        for config in PredictedModels.load_configs():
            if config["id"].startswith(PredictedModels.get_model_name(value).replace('_', '.')):
                return config["memory"]

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_network(value):
        for config in PredictedModels.load_configs():
            if config["id"].startswith(PredictedModels.get_model_name(value).replace('_', '.')):
                return config["network"]

        raise ValueError("Value does not corresponds to a known predicted core.")


class PredictedApplications(Enum):
    EPS = 0
    EPW = 1
    EPA = 2
    EPB = 3
    EPC = 4
    EPD = 5
    EPE = 6
    FTS = 7
    FTW = 8
    FTA = 9
    FTB = 10
    FTC = 11
    MGS = 12
    MGW = 13
    MGA = 14
    MGB = 15
    MGC = 16
    ISS = 17
    ISW = 18
    ISA = 19
    ISB = 20
    ISC = 21
    CGS = 22
    CGW = 23
    CGA = 24
    CGB = 25
    CGC = 26

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in PredictedApplications)

    @staticmethod
    def get_label(value):
        if value == PredictedApplications.EPS:
            return "EP-S"
        if value == PredictedApplications.EPW:
            return "EP-W"
        if value == PredictedApplications.EPA:
            return "EP-A"
        if value == PredictedApplications.EPB:
            return "EP-B"
        if value == PredictedApplications.EPC:
            return "EP-C"
        if value == PredictedApplications.EPD:
            return "EP-D"
        if value == PredictedApplications.EPE:
            return "EP-E"
        if value == PredictedApplications.FTS:
            return "FT-S"
        if value == PredictedApplications.FTW:
            return "FT-W"
        if value == PredictedApplications.FTA:
            return "FT-A"
        if value == PredictedApplications.FTB:
            return "FT-B"
        if value == PredictedApplications.FTC:
            return "FT-C"
        if value == PredictedApplications.MGS:
            return "MG-S"
        if value == PredictedApplications.MGW:
            return "MG-W"
        if value == PredictedApplications.MGA:
            return "MG-A"
        if value == PredictedApplications.MGB:
            return "MG-B"
        if value == PredictedApplications.MGC:
            return "MG-C"
        if value == PredictedApplications.ISS:
            return "IS-S"
        if value == PredictedApplications.ISW:
            return "IS-W"
        if value == PredictedApplications.ISA:
            return "IS-A"
        if value == PredictedApplications.ISB:
            return "IS-B"
        if value == PredictedApplications.ISC:
            return "IS-C"
        if value == PredictedApplications.CGS:
            return "CG-S"
        if value == PredictedApplications.CGW:
            return "CG-W"
        if value == PredictedApplications.CGA:
            return "CG-A"
        if value == PredictedApplications.CGB:
            return "CG-B"
        if value == PredictedApplications.CGC:
            return "CG-C"
        

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_dict():
        return {
            PredictedApplications.EPS.value: PredictedApplications.get_label(PredictedApplications.EPS),
            PredictedApplications.EPW.value: PredictedApplications.get_label(PredictedApplications.EPW),
            PredictedApplications.EPA.value: PredictedApplications.get_label(PredictedApplications.EPA),
            PredictedApplications.EPB.value: PredictedApplications.get_label(PredictedApplications.EPB),
            PredictedApplications.EPC.value: PredictedApplications.get_label(PredictedApplications.EPC),
            PredictedApplications.EPD.value: PredictedApplications.get_label(PredictedApplications.EPD),
            PredictedApplications.EPE.value: PredictedApplications.get_label(PredictedApplications.EPE),
            PredictedApplications.FTS.value: PredictedApplications.get_label(PredictedApplications.FTS),
            PredictedApplications.FTW.value: PredictedApplications.get_label(PredictedApplications.FTW),
            PredictedApplications.FTA.value: PredictedApplications.get_label(PredictedApplications.FTA),
            PredictedApplications.FTB.value: PredictedApplications.get_label(PredictedApplications.FTB),
            PredictedApplications.FTC.value: PredictedApplications.get_label(PredictedApplications.FTC),
            PredictedApplications.MGS.value: PredictedApplications.get_label(PredictedApplications.MGS),
            PredictedApplications.MGW.value: PredictedApplications.get_label(PredictedApplications.MGW),
            PredictedApplications.MGA.value: PredictedApplications.get_label(PredictedApplications.MGA),
            PredictedApplications.MGB.value: PredictedApplications.get_label(PredictedApplications.MGB),
            PredictedApplications.MGC.value: PredictedApplications.get_label(PredictedApplications.MGC),
            PredictedApplications.ISS.value: PredictedApplications.get_label(PredictedApplications.ISS),
            PredictedApplications.ISW.value: PredictedApplications.get_label(PredictedApplications.ISW),
            PredictedApplications.ISA.value: PredictedApplications.get_label(PredictedApplications.ISA),
            PredictedApplications.ISB.value: PredictedApplications.get_label(PredictedApplications.ISB),
            PredictedApplications.ISC.value: PredictedApplications.get_label(PredictedApplications.ISC),
            PredictedApplications.CGS.value: PredictedApplications.get_label(PredictedApplications.CGS),
            PredictedApplications.CGW.value: PredictedApplications.get_label(PredictedApplications.CGW),
            PredictedApplications.CGA.value: PredictedApplications.get_label(PredictedApplications.CGA),
            PredictedApplications.CGB.value: PredictedApplications.get_label(PredictedApplications.CGB),
            PredictedApplications.CGC.value: PredictedApplications.get_label(PredictedApplications.CGC),
        }
        
    @staticmethod
    def load_configs():
        path = PATH_VM + 'apps.json'
        with open(path) as config_file:
            config_json_data = json.load(config_file)
        return config_json_data

    @staticmethod
    def get_instructions_for_design(value):
        app_name = PredictedApplications.get_dict()[value]
        app_data = PredictedApplications.load_configs()

        return app_data[app_name]
        