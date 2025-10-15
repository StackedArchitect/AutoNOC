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
        self.dut=cocotb.top
    async def run_phase(self):
        key={}
        current={}
        for i in range(self.helper.row):
            for j in range(self.helper.column):
                current[f"{i}{j}"]=[]
                key[f"{i}{j}"]=None
        await FallingEdge(self.helper.dut.clr)
        while True:
            await FallingEdge(self.helper.dut.clk)
            #info("\n")
            for i in range(self.helper.row):
                for j in range(self.helper.column):
                    port = getattr(self.dut, f"data_in_core[{i}][{j}]")
                    current[f"{i}{j}"]=hex(int(str(getattr(port,"value")),2))
                    theta=hex(int(str(getattr(port,"value")),2))
                    #info(f"data_out_core[{i}][{j}] = {theta} type of theta ={type(theta)}")
                    if current[f"{i}{j}"] in ["0x60000000","0x7fffffff"]:#reset state ingoning
                        if key[f"{i}{j}"] is not None:
                            warning(f"An incomplete Transaction encountered-->{str(key[i])}")
                            self.helper.incomplete_transactions+=1
                            key[f"{i}{j}"]=None
                    elif current[f"{i}{j}"][:6] in ["0x2000","0x2800","0x3000","0x3800"]:#header flit is detected
                            #self.result[i]in
                            #info("Header Flit is detected")
                            key[f"{i}{j}"]=NOCTransaction()
                            key[f"{i}{j}"].header_flit=current[f"{i}{j}"]  
                    elif current[f"{i}{j}"] in ["0x40000000","0x58000000"]:#tailer flit is detected
                            try:
                                    key[f"{i}{j}"].tailer_flit=current[f"{i}{j}"]
                                    key[f"{i}{j}"].time=cocotb.utils.get_sim_time('ns')#for gathering time
                                    self.ap.write(key[f"{i}{j}"])
                                    temp=key[f"{i}{j}"]
                                    info(f"Monitor Recorded ={str(temp)} at {i}{j}")
                                    print()
                            except Exception as e:
                                    pass
                                #warning("A tailer flit is encountered witout the header and payload")
                            key[f"{i}{j}"]=None
                    else:
                                #info("Payloaf flit is detected")
                                if key[f"{i}{j}"] is None:
                                        warning(f"i={i} j={j} None encountered during payload flit. Header flit is missing")
                                        continue
                                if key[f"{i}{j}"].payload_flit1 is None:
                                        key[f"{i}{j}"].payload_flit1=current[f"{i}{j}"]
                                elif key[f"{i}{j}"].payload_flit1 != current[f"{i}{j}"]:
                                        key[f"{i}{j}"].payload_flit2=current[f"{i}{j}"]
                                else :
                                        continue

