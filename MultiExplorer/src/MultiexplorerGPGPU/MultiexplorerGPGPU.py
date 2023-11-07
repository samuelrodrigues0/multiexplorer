import os
import tkMessageBox

from MultiExplorer.src.Infrastructure.Events import Event
from MultiExplorer.src.Infrastructure.ExecutionFlow import ExecutionFlow
from Steps import GPGPUSimulationStep, DSEStep
from MultiExplorer.src.config import PATH_RUNDIR

class MultiexplorerGPGPUExecutionFlow(ExecutionFlow):
    
    @staticmethod
    def get_info():
        return (
            "Multiexplorer GPGPU"
        )
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                MultiexplorerGPGPUExecutionFlow,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        super(MultiexplorerGPGPUExecutionFlow, self).__init__()

        self.steps = [
            GPGPUSimulationStep(),
            DSEStep(),
        ]

    @staticmethod
    def get_label():
        return 'Multiexplorer GPGPU'
    
    def get_output_path(self):
        return (
                PATH_RUNDIR
                + "/" + MultiexplorerGPGPUExecutionFlow.get_label().replace(' ', '_')
        )
    
    def execute(self):
        
        ExecutionFlow.execute(self)

    def handle_step_failure(self, step):
        tkMessageBox.showerror(
            "Execution Failure",
            "The " + step.get_label() + " Step execution wasn't successful. " + str(step.execution_exception)
        )

        self.fire(Event.FLOW_EXECUTION_FAILED)

    def finish(self):
        self.fire(Event.FLOW_EXECUTION_ENDED)