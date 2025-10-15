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

class NOCHelper(metaclass=pyuvm.Singleton):
    """
    This class includes some common values and methodtotal_number_of_transactions
    that are usefull to all the components in the uvm testbench
    for  huristic valid inputs are  "POS" ,"DE","GA"  . If none of the values are given then it will assume the random generation.
    """
    def __init__(self, row=2, column=2,number_of_iterations=1,huristic="R"):
        self.number_of_iterations=number_of_iterations
        self.row = row
        self.column = column
        self.dut=cocotb.top
        self.size=row*column
        self.huristic=huristic
        self.Data_In_Ports = [f"data_in_core_r{i+1}" for i in range(self.row * self.column)]
        self.Data_Out_Ports = [f"data_out_core_r{i+1}" for i in range(self.row * self.column)]
        self.routerId = [f'{row:04b}{column:04b}' for row in range(self.row) for column in range(self.column)]
        self.all_transactions={}
        self.send_transactions=0
        self.incomplete_transactions=0
        self.total_coverage=0
        self.source_coverage={}
        self.destination_coverage={}
        for i in self.routerId:
            self.source_coverage[i]=0
            for j in self.routerId:
                self.destination_coverage[j]=0
                if i!=j:
                    self.all_transactions[i+j]=0
                    self.total_coverage+=1
        info("\033[93m"+f"rows={self.row} column={self.column} all={self.number_of_iterations} huristics= {huristic}"+"\033[0m")
        info("\033[93m"+f"all possible Transactions={self.all_transactions}"+"\033[0m")
        info("\033[93m"+f"all the routerId={self.routerId}"+"\033[0m")
        info("\033[93m"+f"data in ports={self.Data_In_Ports}"+"\033[0m")
        info("\033[93m"+f"data out ports={self.Data_Out_Ports}"+"\033[0m")

    async def clrAndReset(self):
        """
        This method will reset the NOC module and clear
        all the outputs.
        """
        info("\033[93m"+"inside clr reset"+"\033[0m")
        dut=self.dut
        dut.clr.value = 1
        await ClockCycles(dut.clk, 2)
        dut.clr.value = 0
        for i in self.Data_In_Ports:
            setattr(getattr(dut, i), "value", 0x7fffffff)
        await ClockCycles(dut.clk, 1)
        info("\033[93m"+"clear and reset is done"+"\033[0m")

    async def clockClockGeneration(self):
        """
        This method will start a clock with period of 20 micro seconds
        """
        info("\033[93m"+"inside the clock generation"+"\033[0m")
        clk = Clock(self.dut.clk, 10, units="us")
        cocotb.start_soon(clk.start())
        info("\033[93m"+"clock is created"+"\033[0m")
        info("\033[93m"+"inside the clock generation"+"\033[0m")
if __name__ =="main":
    print("just a helper class")
