import os
import tkMessageBox
from Steps import GPGPUSimulationStep, DSEStep
from MultiExplorer.src.config import PATH_RUNDIR
from MultiExplorer.src.Infrastructure.Events import Event
from MultiExplorer.src.Infrastructure.ExecutionFlow import ExecutionFlow
from Presenters import BruteForceTablePresenter, NSGAPresenter, NSGATablePresenter, BruteForcePresenter, GPGPUSimPresenter

class MultiexplorerGPGPUExecutionFlow(ExecutionFlow):
    
    @staticmethod
    def get_info():
        return (
           "This flow allows for the design space exploration of GPU-based heterogeneous systems. " 
           + "The user begins by selecting the initial configuration and the application to be used. " 
           + "Next, power density and area constraints are specified. " 
           + "The performance of the initial configuration is gathered using the GPGPU-Sim simulator, " 
           + "while physical parameters are estimated with GPGPUWattch, a tool integrated into GPGPU-Sim. " 
           + "Finally, design space exploration is performed using either a genetic algorithm (NSGA-II) or brute force."
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
        return 'Multiexplorer GPUs'
    
    def get_output_path(self):
        return (
                PATH_RUNDIR
                + "/" + MultiexplorerGPGPUExecutionFlow.get_label().replace(' ', '_')
        )
    
    def setup_dirs(self):
        output_path = self.get_output_path()

        if not os.path.exists(output_path):
            os.makedirs(output_path)

    def execute(self):
        self.setup_dirs()
        ExecutionFlow.execute(self)

    def get_results(self):
        return {
            "gpgpusim": self.steps[0].get_results(),
            "dsdse": self.steps[1].get_results()
        }
    
    def get_presenters(self):
        return [
            NSGATablePresenter(),
            NSGAPresenter(),
            BruteForceTablePresenter(),
            BruteForcePresenter(),
            GPGPUSimPresenter(),
        ]

    def handle_step_failure(self, step):
        tkMessageBox.showerror(
            "Execution Failure",
            "The " + step.get_label() + " Step execution wasn't successful. " + str(step.execution_exception)
        )

        self.fire(Event.FLOW_EXECUTION_FAILED)

    def finish(self):
        self.fire(Event.FLOW_EXECUTION_ENDED)