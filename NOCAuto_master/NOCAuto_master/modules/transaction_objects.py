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

class NOCTransaction_list(uvm_sequence_item):
    def __init__(self, TransactionList=[],name="NOCTransaction_list"):
        super().__init__(name)
        self.transactionList=TransactionList
    def __str__(self):
        s=""
        for i in self.transactionList:
            s+=f"\n{str(i)}"
        return s
    def __len__(self):
        return len(self.transactionList)

class NOCTransaction(uvm_sequence_item):
    def __init__(self, name="NOCTransaction"):
        super().__init__(name)
        self.header_flit = None
        self.tailer_flit = None
        self.payload_flit1 = None
        self.payload_flit2 = None
        self.time=None

    def __str__(self) -> str:
        return f"Header: {self.header_flit}, Payload1: {self.payload_flit1}, Payload2: {self.payload_flit2}, Tailer: {self.tailer_flit}, time={self.time}"

    def __eq__(self, other) -> bool:
        if not isinstance(other,NOCTransaction):
            print(f"chutiya both operators should belong to NOCTransaction Class")
            return False
        else:
            try:
                is_header_same=(self.header_flit[-4:] == other.header_flit[-4:])
                is_payload1_same=(self.payload_flit1[-6:]==other.payload_flit1[-6:])
                is_payload2_same=(self.payload_flit2[-6:]==other.payload_flit2[-6:])
                return is_header_same and is_payload1_same and is_payload2_same
            except Exception as e:
                fatal(f"An empty data riceved exception={e}")
            return True
    #this is the sequencer code that sends the data sequentially convering all the data paths
    # async def body(self):
    #     self.helper = NOCHelper()
    #     await self.helper.clockClockGeneration()
    #     await self.helper.clrAndReset()
    #     for source_node in self.helper.routerId:
    #         for destination_node in self.helper.routerId:
    #             if source_node != destination_node:
    #                 transaction = self.generate_transaction(source_node=source_node, destination_node=destination_node)
    #                 self.data[source_node+destination_node]=transaction
    #                 await self.start_item(transaction)
    #                 await self.finish_item(transaction)
            # while True:
            # if len(self.helper.all_transactions)<1:
            #     break
            # source_node,destination_node=self.generate_source_destination()
            # transaction=self.generate_transaction(source_node,destination_node)
            # transaction_key=source_node+destination_node
            # if transaction_key in self.helper.all_transactions:
            #     self.helper.all_transactions.remove(transaction_key)
            #     await self.start_item(transaction)
            #     await self.finish_item(transaction)
