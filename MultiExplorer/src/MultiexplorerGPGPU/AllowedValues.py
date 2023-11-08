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
    armA53 = 3
    armA57 = 4
    atom = 5
    quark = 6
    smithfield = 7

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in PredictedModels)

    @staticmethod
    def get_label(value):
        if value == PredictedModels.gtx480:
            return "GTX 480"
        if value == PredictedModels.titanx:
            return "Titan X"
        if value == PredictedModels.armA53:
            return "armA53"
        if value == PredictedModels.armA57:
            return "armA57"
        if value == PredictedModels.atom:
            return "Atom"
        if value == PredictedModels.quark:
            return "Quark"
        if value == PredictedModels.smithfield:
            return "Smithfield"


        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_dict():
        return {
            PredictedModels.gtx480.value: PredictedModels.get_label(PredictedModels.gtx480),
            PredictedModels.titanx.value: PredictedModels.get_label(PredictedModels.titanx),
            PredictedModels.armA53.value: PredictedModels.get_label(PredictedModels.armA53),
            PredictedModels.armA57.value: PredictedModels.get_label(PredictedModels.armA57),
            PredictedModels.atom.value: PredictedModels.get_label(PredictedModels.atom),
            PredictedModels.quark.value: PredictedModels.get_label(PredictedModels.quark),
            PredictedModels.quark.value: PredictedModels.get_label(PredictedModels.quark),
        }
    
    @staticmethod
    def get_model(value):
        # type: (int) -> str
        if value == PredictedModels.gtx480.value:
            return "gtx480"
        elif value == PredictedModels.titanx.value:
            return "titanx"
        elif value == PredictedModels.armA53.value:
            return "armA53"
        elif value == PredictedModels.armA57.value:
            return "armA57"
        elif value == PredictedModels.atom.value:
            return "atom"
        elif value == PredictedModels.quark.value:
            return "quark"
        elif value == PredictedModels.smithfield.value:
            return "smithfield"

        raise ValueError("Value does not corresponds to a known predicted core.")
    
    @staticmethod
    def get_json_path(value):
        if value == PredictedModels.gtx480.value:
            return PATH_INPUTS + "/gtx480.json"
        elif value == PredictedModels.titanx.value:
            return PATH_INPUTS + "/titanx.json"
        elif value == PredictedModels.armA53.value:
            return PATH_INPUTS + "/armA53.json"
        elif value == PredictedModels.armA57.value:
            return PATH_INPUTS + "/armA57.json"
        elif value == PredictedModels.atom.value:
            return PATH_INPUTS + "/atom.json"
        elif value == PredictedModels.quark.value:
            return PATH_INPUTS + "/quark.json"
        elif value == PredictedModels.smithfield.value:
            return PATH_INPUTS + "/smithfield.json"

        raise ValueError("Can't find default input json file for unknown/unpredicted cores.")
    
    @staticmethod
    def get_sim_tool(value):
        
        if value == PredictedModels.gtx480.value or value == PredictedModels.titanx.value:
            return "gpgpusim"
        else:
            return "sniper" 

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
        if value == Applications.bfs.value:
            return "bfs"
        elif value == Applications.clock.value:
            return "clock"
        if value == Applications.dwt2d.value:
            return "dwt2d"
        elif value == Applications.hotspot.value:
            return "hotspot"
        if value == Applications.needle.value:
            return "needle"
        elif value == Applications.nn.value:
            return "nn"
        if value == Applications.vectorAdd.value:
            return "vectorAdd"

        raise ValueError("Value does not corresponds to a known predicted core.")