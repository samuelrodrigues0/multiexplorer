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

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in PredictedModels)

    @staticmethod
    def get_label(value):
        if value == PredictedModels.gtx480:
            return "GTX_480"
        if value == PredictedModels.titanx:
            return "Titan_X"

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_dict():
        return {
            PredictedModels.gtx480.value: PredictedModels.get_label(PredictedModels.gtx480),
            PredictedModels.titanx.value: PredictedModels.get_label(PredictedModels.titanx)
        }
    
    @staticmethod
    def get_model(value):
        # type: (int) -> str
        if value == PredictedModels.gtx480.value:
            return "GTX480"
        elif value == PredictedModels.titanx.value:
            return "TITANX"

        raise ValueError("Value does not corresponds to a known predicted core.")
    
    @staticmethod
    def get_json_path(value):
        if value == PredictedModels.gtx480.value:
            return PATH_INPUTS + "/gtx480.json"
        elif value == PredictedModels.titanx.value:
            return PATH_INPUTS + "/titanx.json"

        raise ValueError("Can't find default input json file for unknown/unpredicted cores.")
    
    @staticmethod
    def get_sim_tool(value):
        
        if value == PredictedModels.gtx480.value or value == PredictedModels.titanx.value:
            return "gpgpusim"

        #raise ValueError("Can't find default input json file for unknown/unpredicted cores.")


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
    

class Technology_configs(Enum):
    nm22 = 1
    nm32 = 2
    nm45 = 3
    nm90 = 4

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in Technology_configs)

    @staticmethod
    def get_label(value):
        if value == Technology_configs.nm22:
            return "22nm"
        if value == Technology_configs.nm32:
            return "32nm"
        if value == Technology_configs.nm45:
            return "45nm"
        if value == Technology_configs.nm90:
            return "90nm"

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_dict():
        return {
            Technology_configs.nm22.value: Technology_configs.get_label(Technology_configs.nm22),
            Technology_configs.nm32.value: Technology_configs.get_label(Technology_configs.nm32),
            Technology_configs.nm45.value: Technology_configs.get_label(Technology_configs.nm45),
            Technology_configs.nm90.value: Technology_configs.get_label(Technology_configs.nm90)

        }
    
    @staticmethod
    def get_model(value):
        # type: (int) -> str
        if value == Technology_configs.nm22.value:
            return "22"
        elif value == Technology_configs.nm32.value:
            return "32"
        elif value == Technology_configs.nm45.value:
            return "45"
        elif value == Technology_configs.nm90.value:
            return "90"

        raise ValueError("Value does not corresponds to a known predicted core.")
    

class Db_app(Enum):
    clock = 1
    asyncAPI = 2
    all = 3

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in Db_app)

    @staticmethod
    def get_label(value):
        if value == Db_app.clock:
            return "clock"
        if value == Db_app.asyncAPI:
            return "asyncAPI"
        #if value == Db_app.all:
         #   return "all"

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_dict():
        return {
            Db_app.clock.value: Db_app.get_label(Db_app.clock),
            Db_app.asyncAPI.value: Db_app.get_label(Db_app.asyncAPI),
            #Db_app.all.value: Db_app.get_label(Db_app.all),

        }
    
    @staticmethod
    def get_model(value):
        # type: (int) -> str
        if value == Db_app.clock.value:
            return "clock"
        elif value == Db_app.asyncAPI.value:
            return "asyncAPI"
        #elif value == Db_app.all.value:
        #    return "all"

        raise ValueError("Value does not corresponds to a known predicted core.")