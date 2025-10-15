from pyuvm import *
from modules.driver import NOCDriver
from modules.monitor import NOCMonitor
from modules.scoreboard import NOCScoreboard
from modules.helper import NOCHelper
class NOCEnv(uvm_env):
    def connect_phase(self):
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
        self.monitor.ap.connect(self.scoreboard.result_export)#monitor analysis port is connected to result
        self.driver.ap.connect(self.scoreboard.cmd_export)#driver analysis port connected to cmd
        self.helper=NOCHelper()
    def build_phase(self):
        super().build_phase()
        self.sequencer = uvm_sequencer("sequencer", self)
        self.driver = NOCDriver("driver", self)
        self.monitor=NOCMonitor("monitor",self)
        self.scoreboard = NOCScoreboard("scoreboard", self)
