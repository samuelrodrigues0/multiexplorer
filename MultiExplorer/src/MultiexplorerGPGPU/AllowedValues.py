# -*- coding: utf-8 -*-

from enum import Enum

from MultiExplorer.src.config import PATH_INPUTS


class Simulators(Enum):
    
    GPGPUSim = 1

    @staticmethod
    def belongs(value): return value in set(item.value for item in Simulators)

    @staticmethod
    def get_label(value):
        if value == Simulators.GPGPUSim:
            return "GPGPU Simulator"

        raise ValueError("Value does not corresponds to a known simulator.")


class PredictedModels(Enum):
    gtx480 = 1
    titanx = 2
    gk110 = 3
    qv100 = 4
    rtx2060 = 5
    titanv = 6

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in PredictedModels)

    @staticmethod
    def get_label(value):
        
        if value == PredictedModels.gtx480:
            return "GTX_480"
        elif value == PredictedModels.titanx:
            return "Titan_X"
        elif value == PredictedModels.gk110:
            return "GK_110"
        elif value == PredictedModels.qv100:
            return "QV_100"
        elif value == PredictedModels.rtx2060:
            return "RTX_2060"
        elif value == PredictedModels.titanv:
            return "Titan_V"

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_dict():
        
        return {
            PredictedModels.gtx480.value: PredictedModels.get_label(PredictedModels.gtx480),
            PredictedModels.titanx.value: PredictedModels.get_label(PredictedModels.titanx),
            #PredictedModels.gk110.value: PredictedModels.get_label(PredictedModels.gk110),
            PredictedModels.qv100.value: PredictedModels.get_label(PredictedModels.qv100),
            PredictedModels.rtx2060.value: PredictedModels.get_label(PredictedModels.rtx2060),
            PredictedModels.titanv.value: PredictedModels.get_label(PredictedModels.titanv)
        }
    
    @staticmethod
    def get_model(value):
        
        # type: (int) -> str
        if value == PredictedModels.gtx480.value:
            return "GTX480"
        elif value == PredictedModels.titanx.value:
            return "TITANX"
        elif value == PredictedModels.gk110.value:
            return "GK110"
        elif value == PredictedModels.qv100.value:
            return "QV100"
        elif value == PredictedModels.rtx2060.value:
            return "RTX2060"
        elif value == PredictedModels.titanv.value:
            return "TITANV"

        raise ValueError("Value does not corresponds to a known predicted core.")
    
    @staticmethod
    def get_json_path(value):
        
        if value == PredictedModels.gtx480.value:
            return PATH_INPUTS + "/GPUs/gtx480.json"
        elif value == PredictedModels.titanx.value:
            return PATH_INPUTS + "/GPUs/titanx.json"
        elif value == PredictedModels.gk110.value:
            return PATH_INPUTS + "/GPUs/gk110.json"
        elif value == PredictedModels.qv100.value:
            return PATH_INPUTS + "/GPUs/qv100.json"
        elif value == PredictedModels.rtx2060.value:
            return PATH_INPUTS + "/GPUs/rtx2060.json"
        elif value == PredictedModels.titanv.value:
            return PATH_INPUTS + "/GPUs/titanv.json"

        raise ValueError("Can't find default input json file for unknown/unpredicted cores.")
    
    @staticmethod
    def get_sim_tool(value):  
        return "gpgpusim"


class Applications(Enum):
    asyncAPI = 1
    backprop = 2
    bfs = 3
    clock = 4
    dwt2d = 5
    hotspot = 6
    needle = 7 
    nn = 8
    vectorAdd = 9

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in Applications)

    @staticmethod
    def get_label(value):
        
        if value == Applications.asyncAPI:
            return "asyncAPI"
        if value == Applications.backprop:
            return "backprop"
        if value == Applications.bfs:
            return "bfs"
        if value == Applications.clock:
            return "clock"
        if value == Applications.dwt2d:
            return "dwt2d"
        if value == Applications.hotspot:
            return "hotspot"
        if value == Applications.needle:
            return "needle"
        if value == Applications.nn:
            return "nn"
        if value == Applications.vectorAdd:
            return "vectorAdd"

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_dict():
        
        return {
            Applications.asyncAPI.value: Applications.get_label(Applications.asyncAPI),
            Applications.backprop.value: Applications.get_label(Applications.backprop),
            Applications.bfs.value: Applications.get_label(Applications.bfs),
            Applications.clock.value: Applications.get_label(Applications.clock),
            Applications.dwt2d.value: Applications.get_label(Applications.dwt2d),
            Applications.hotspot.value: Applications.get_label(Applications.hotspot),
            Applications.needle.value: Applications.get_label(Applications.needle),
            Applications.nn.value: Applications.get_label(Applications.nn),
            Applications.vectorAdd.value: Applications.get_label(Applications.vectorAdd),
        }
    
    @staticmethod
    def get_model(value):
        
        # type: (int) -> str
        if value == Applications.asyncAPI.value:
            return "asyncAPI"
        elif value == Applications.backprop.value:
            return "backprop"
        elif value == Applications.bfs.value:
            return "bfs"
        elif value == Applications.clock.value:
            return "clock"
        elif value == Applications.dwt2d.value:
            return "dwt2d"
        elif value == Applications.hotspot.value:
            return "hotspot"
        elif value == Applications.needle.value:
            return "needle"
        elif value == Applications.nn.value:
            return "nn"
        elif value == Applications.vectorAdd.value:
            return "vectorAdd"

        raise ValueError("Value does not corresponds to a known predicted core.")

"""
Melhoria futura

class Configs(Enum):
    
    gpu_gpu = 1
    gpu_cpu = 2

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in Configs)

    @staticmethod
    def get_label(value):
        
        if value == Configs.gpu_gpu:
            return "gpu-gpu"
        if value == Configs.gpu_cpu:
            return "gpu-cpu"

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_dict():
        
        return {
            Configs.gpu_gpu.value: Configs.get_label(Configs.gpu_gpu),
            Configs.gpu_cpu.value: Configs.get_label(Configs.gpu_cpu),

        }
    
    @staticmethod
    def get_model(value):
       
        # type: (int) -> str
        if value == Configs.gpu_gpu.value:
            return "gpu-gpu"
        elif value == Configs.gpu_cpu.value:
            return "gpu-cpu"

        raise ValueError("Value does not corresponds to a known predicted core.")
"""