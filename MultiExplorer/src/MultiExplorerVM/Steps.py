import os
import sys
from Adapters import CloudsimAdapter, NsgaIIPredDSEAdapter
from ..Infrastructure.Events import Event
from ..Infrastructure.ExecutionFlow import Step
from Presenters import CloudSimPresenter, NSGAPresenter


class CloudSimStep(Step):

    def get_results(self):
        return self.adapter.get_results()
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                CloudSimStep,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        super(CloudSimStep, self).__init__()

        self.adapter = CloudsimAdapter() 

    @staticmethod
    def get_label():
        return 'Simulation'

    @staticmethod
    def has_user_input():
        return True

    def get_user_inputs(self):
        return self.adapter.get_user_inputs()
    
    def get_presenter(self):
        return CloudSimPresenter()

    def __execute__(self):
        self.execution_exception = None

        try:
            self.adapter.execute()
        except BaseException as exception:
            self.execution_exception = exception

    def __finish__(self):
        if self.execution_exception is None:
            self.fire(Event.STEP_EXECUTION_ENDED)
        else:
            self.fire(Event.STEP_EXECUTION_FAILED, self)

class NSGAIIDSEStep(Step):
    def get_results(self):
        return self.adapter.get_results()

    def get_presenter(self):
        return NSGAPresenter()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                NSGAIIDSEStep,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        super(NSGAIIDSEStep, self).__init__()

        self.adapter = NsgaIIPredDSEAdapter()

    @staticmethod
    def get_label(): return 'DSE'

    @staticmethod
    def has_user_input(): return True

    def get_user_inputs(self): return self.adapter.get_user_inputs()

    def __execute__(self):
        self.execution_exception = None

        try:
            self.adapter.execute()
        except BaseException as exception:
            self.execution_exception = exception

    def __finish__(self):
        if self.execution_exception is None:
            self.fire(Event.STEP_EXECUTION_ENDED)
        else:
            self.fire(Event.STEP_EXECUTION_FAILED, self)
