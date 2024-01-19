from MultiExplorer.src.Infrastructure.Events import Event
from MultiExplorer.src.Infrastructure.ExecutionFlow import Step
from MultiExplorer.src.MultiexplorerGPGPU.Adapters import GPGPUSimulatorAdapter, DSEAdapter
from MultiExplorer.src.MultiexplorerGPGPU.Presenters import NSGAPresenter, GPGPUSimPresenter

class GPGPUSimulationStep(Step):
    
    def get_results(self):
        return self.adapter.get_results()


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                GPGPUSimulationStep,
                cls
            ).__new__(cls)

        return cls.instance


    def __init__(self):
        super(GPGPUSimulationStep, self).__init__()

        self.adapter = GPGPUSimulatorAdapter()

    @staticmethod
    def has_user_input():
        return True

    @staticmethod
    def get_label():
        return 'Simulation'

    @staticmethod
    def has_user_input():
        return True


    def get_user_inputs(self):
        return self.adapter.get_user_inputs()


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


    def get_presenter(self):
        return GPGPUSimPresenter()


class DSEStep(Step):
    
    def get_results(self):
        return self.adapter.get_results()


    def get_presenter(self):
        return NSGAPresenter()


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                DSEStep,
                cls
            ).__new__(cls)

        return cls.instance


    def __init__(self):
        super(DSEStep, self).__init__()

        self.adapter = DSEAdapter()


    @staticmethod
    def get_label(): 
        return 'DSE'

    @staticmethod
    def has_user_input(): 
        return True


    def get_user_inputs(self): 
        return self.adapter.get_user_inputs()


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

