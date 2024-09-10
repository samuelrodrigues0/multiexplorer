import os
import tkMessageBox
from ..config import PATH_RUNDIR
from ..Infrastructure.Events import Event
from Steps import CloudSimStep, NSGAIIDSEStep
from ..Infrastructure.ExecutionFlow import ExecutionFlow
from Presenters import BruteForceTablePresenter, NSGATablePresenter, CloudSimPresenter, NSGAPresenter, BruteForcePresenter

class MultiExplorerVMExecutionFlow(ExecutionFlow):
    
    @staticmethod
    def get_info():
        return (
            "This workflow enables the configuration of virtual machines based on user requirements and application constraints. \n"
            + "MultiExplorer-VM utilizes CloudSim as the cloud simulation platform. \n"
            + "The design space exploration (DSE) is conducted using an NSGA2-based algorithm. \n"
            + "In the current version, MultiExplorer-VM also incorporates a brute-force algorithm to explore all viable design alternatives. \n"
            + "The brute-force approach serves as a validation step for our DSE methodology."
        )

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                MultiExplorerVMExecutionFlow,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        super(MultiExplorerVMExecutionFlow, self).__init__()

        self.steps = [
            CloudSimStep(),
            NSGAIIDSEStep()
        ]

    @staticmethod
    def get_label():
        return 'MultiExplorer Virtual Machines'

    def get_output_path(self):
        return (
                PATH_RUNDIR
                + "/" + MultiExplorerVMExecutionFlow.get_label().replace(' ', '_')
        )
    
    def setup_dirs(self):
        output_path = self.get_output_path()

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        nbr_of_dirs = len(next(os.walk(output_path))[1])

        nbr_of_dirs = nbr_of_dirs & 63

        output_path = output_path + "/" + "{:02d}".format(nbr_of_dirs)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        for step in self.steps:
            step.set_output_path(output_path)

    def execute(self):
        self.setup_dirs()

        ExecutionFlow.execute(self)

    def get_results(self):
        return {
            "cloudsim": self.steps[0].get_results(),
            "dsdse": self.steps[1].get_results()
        }
    
    def get_presenters(self):
        return [
            NSGATablePresenter(),
            NSGAPresenter(),
            BruteForceTablePresenter(),
            BruteForcePresenter(),
            CloudSimPresenter()
        ]
    
    def handle_step_failure(self, step):
        tkMessageBox.showerror(
            "Execution Failure",
            "The " + step.get_label() + " Step execution wasn't successful. " + str(step.execution_exception)
        )

        self.fire(Event.FLOW_EXECUTION_FAILED)

    def finish(self):
        self.fire(Event.FLOW_EXECUTION_ENDED)
