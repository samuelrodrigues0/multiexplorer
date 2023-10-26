import os
import tkMessageBox

from MultiExplorer.src.Infrastructure.Events import Event
from MultiExplorer.src.Infrastructure.ExecutionFlow import ExecutionFlow
#from MultiExplorer.src.config import PATH_RUNDIR

class MultiexplorerGPGPUExecutionFlow(ExecutionFlow):
    
    def __init__(self):
        pass

    @staticmethod
    def get_label():
        return 'GPGPU'
    
    