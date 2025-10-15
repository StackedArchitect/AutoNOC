

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
from queue import Queue


from modules.helper import NOCHelper
from modules.transaction_objects import NOCTransaction_list,NOCTransaction

class NOCDriver(uvm_driver):
    def __init__(self, name="NOCDriver", parent=None):
        super().__init__(name, parent)
        self.helper = NOCHelper()
        self.ap = uvm_analysis_port("ap", self) 
        info("noc driver is initialed")
        self.dut=cocotb.top
    async def run_phase(self):
        """
        In run phase , the driver wait for the transaction's
        from sequencer , and when it recieved it will apply these value to the dut
        This driver is capable to handle both list of transactions and a single transaction
        """
        await self.helper.clockClockGeneration()
        await self.helper.clrAndReset()
        info(f"Sending to the Noc")
        while True:
            transaction = await self.seq_item_port.get_next_item()
            if isinstance(transaction, NOCTransaction_list):
                await self.multiple_flit_driver(transaction)#have to change this to make the code work with single
                self.seq_item_port.item_done()
                              #I think you will have to change the code in sequnce module to make it work
                transaction.time=cocotb.utils.get_sim_time('ns')#for performance analysis
                info(f"time = {transaction.time}")
                info(f"sent--->{str(transaction)}")
            else:
                await self.single_flit_driver(transaction)
                self.seq_item_port.item_done()


    async def multiple_flit_driver(self,transactionList:list):
        """
        This fucntion takes a list of transanactions and 
        drive the dut. All the flits are applied at the same time paralelly
        with out any time delay
        """
        for i in range(4):
            # warning(f"i={i}")
            for transaction in transactionList.transactionList:     
                #lines for auto-noc         
                source_row_column=str(transaction.header_flit[6:8])
                source_row=int(source_row_column[0])
                source_column=int(source_row_column[1])
                port = getattr(self.dut, f"data_in_core[{source_row}][{source_column}]")
                #lines for auto noc
                
                if i==0:
                    setattr(port, "value", int(transaction.header_flit, 16))  # sending the header flit
                    # warning(f"setting header value header ={transaction.header_flit} port={self.helper.Data_In_Ports[source]}")
                elif i==1:
                    setattr(port, "value", int(transaction.payload_flit1, 16))  # sending the payload flit1
                    # warning(f"setting payload value payload1 ={transaction.payload_flit1} header={transaction.header_flit} {self.helper.Data_In_Ports[source]}")
                elif i==2:
                    setattr(port, "value", int(transaction.payload_flit2, 16))  # sending the payload flit1
                    # warning(f"setting payload value payload2 ={transaction.payload_flit2} header={transaction.header_flit} {self.helper.Data_In_Ports[source]}")
                else:
                    setattr(port, "value", int(transaction.tailer_flit, 16))  # sending the tailer flit
                    transaction.time=cocotb.utils.get_sim_time('ns')#for gathering time
                    info(f"time = {transaction.time}")
                    info(f"sent--->{str(transaction)}")
                    await ClockCycles(self.dut.clk, 6, rising=False)
                    setattr(port, "value", 0x7fffffff)
                    self.ap.write(transaction)
                    self.helper.send_transactions+=1
                    # warning(f"setting tailer flit i={i}  header={transaction.header_flit} {self.helper.Data_In_Ports[source]}")
            await ClockCycles(self.dut.clk, 6, rising=False)


    async def single_flit_driver(self, transaction):
        """
        This fucntion takes only one flit and apply the flits to the noc
        """

        source_row_column=str(transaction.header_flit[6:8])
        #lines for auto-Noc
        source_row=int(source_row_column[0])
        source_column=int(source_row_column[1])
        port = getattr(self.dut, f"data_in_core[{source_row}][{source_column}]")
        #lines for auto NOC
        
            
        setattr(port, "value", int(transaction.header_flit, 16))  # sending the header flit
        await ClockCycles(self.dut.clk, 6, rising=False)
        setattr(port, "value", int(transaction.payload_flit1, 16))  # sending the payload flit1
        await ClockCycles(self.dut.clk, 6, rising=False)
        setattr(port, "value", int(transaction.payload_flit2, 16))  # sending the payload flit2
        await ClockCycles(self.dut.clk, 6, rising=False)
        setattr(port, "value", int(transaction.tailer_flit, 16))  # sending the tailer flit
        await ClockCycles(self.dut.clk, 10, rising=False)
        self.ap.write(transaction)  
        self.helper.send_transactions+=1
        transaction.time=cocotb.utils.get_sim_time('ns')#for gathering time
        info(f"time = {transaction.time}")
        info(f"sent--->{str(transaction)}")
    

    def final_phase(self):
        return super().final_phase()
