import cocotb
from cocotb.triggers import Timer, ClockCycles, FallingEdge, RisingEdge
from cocotb.clock import Clock
from logging import info, info,fatal,warning
from logging.handlers import WatchedFileHandler
import random
import pyuvm
from pyuvm import *
from time import time
import os
import json
#importing the uvm testbench modules
from modules.helper import NOCHelper
from modules.sequence import NOCSequence
from modules.environment import NOCEnv
from script import rewrite
# Figure 6: Setting up logging using the logger variable
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

data=open("config.json","r")
config=json.load(data)

row=int(config["row_value"])
column=int(config["row_value"])
algo = config["algorithm"]
t=config["Topology"]
info(f"row={row} column={column}")
rewrite(row,column,t)
@pyuvm.test()
class test(uvm_test):
    def build_phase(self):
        
        #change the below parameter to change the test bench
        self.helper=NOCHelper(row,column,1,huristic=algo)
        self.helper.algorithmic_parameters=config["algorithm_params"]
        self.env = NOCEnv("env", self)

    async def run_phase(self):
        t1=time()
        self.raise_objection()
        seq = NOCSequence.create("seq")
        await seq.start(self.env.sequencer)
        await Timer(10, "ms")
        t2=time()
        seq = NOCSequence.create
        print("\033[93m"+f"time taken ={t2-t1} seconds"+"\033[0m")
        #await ClockCycles(cocotb.top.clk,100)
        self.drop_objection()

