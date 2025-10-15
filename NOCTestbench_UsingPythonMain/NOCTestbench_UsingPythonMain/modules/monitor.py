import cocotb
from cocotb.triggers import Timer, ClockCycles, FallingEdge, RisingEdge
from cocotb.clock import Clock
from logging import info, info,fatal,warning
from logging.handlers import WatchedFileHandler
import random
import pyuvm
from pyuvm import *
from pyuvm import ConfigDB
from cocotb.result import TestSuccess

from modules.helper import NOCHelper
from modules.transaction_objects import NOCTransaction,NOCTransaction_list

class NOCMonitor(uvm_monitor):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.helper=NOCHelper()
        self.ap= uvm_analysis_port("ap",self)
    async def run_phase(self):
        key={}
        current={}
        for i in self.helper.Data_Out_Ports:
            current[i]=[]
            key[i]=None
        while True:
            await FallingEdge(self.helper.dut.clk)
            for i in self.helper.Data_Out_Ports:
            
                current[i]=hex(int(str(getattr(getattr(self.helper.dut,i),"value")),2))
                if current[i] == "0x60000000":#reset state ingoning
                    if key[i] is not None:
                        warning(f"An incomplete Transaction encountered-->{str(key[i])}")
                        self.helper.incomplete_transactions+=1
                        key[i]=None

                elif current[i][:6] in ["0x2000","0x2800","0x3000","0x3800"]:#header flit is detected
                    #self.result[i]in
                    key[i]=NOCTransaction()
                    key[i].header_flit=current[i]
                    
                elif current[i] == "0x40000000":#tailer flit is detected
                    try:
                        key[i].tailer_flit=current[i]
                        key[i].time=cocotb.utils.get_sim_time('ns')#for gathering time
                    except Exception as e:
                        warning("A tailer flit is encountered witout the header and payload")
                    self.ap.write(key[i])
                    info("\033[93m"+f"monitor recorded={str(key[i])}"+"\033[0m")
                    key[i]=None

                    
                else:
                    #print(f"we are decieveing data key[{i}]={key[i]} current[{i}]={current[i]}")
                    if key[i] is None:
                        warning("None encountered during payload flit. Header flit is missing")
                        continue
                    if key[i].payload_flit1 is None:
                        key[i].payload_flit1=current[i]
                    elif key[i].payload_flit1 != current[i]:
                        key[i].payload_flit2=current[i]
                    else :
                        continue
   
