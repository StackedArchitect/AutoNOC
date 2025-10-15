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
from time import time
import os
#importing the uvm testbench modules
from modules.helper import NOCHelper
from modules.sequence import NOCSequence
from modules.environment import NOCEnv

# Figure 6: Setting up logging using the logger variable
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



row=8
column=8
@pyuvm.test()
class test(uvm_test):

    def build_phase(self):
        #change the below parameter to change the test bench
        self.helper=NOCHelper(row,column,1,huristic="DE")
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
        self.drop_objection()

@pyuvm.test()
class test(uvm_test):

    def build_phase(self):
        #change the below parameter to change the test bench
        self.helper=NOCHelper(row,column,1,huristic="GA")
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
        self.drop_objection()

@pyuvm.test()
class test(uvm_test):

    def build_phase(self):
        #change the below parameter to change the test bench
        self.helper=NOCHelper(row,column,1,huristic="PSO")
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
        self.drop_objection()
