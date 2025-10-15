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
from random import randint
from math import ceil
import os #for the file path name
from modules.helper import NOCHelper
from modules.transaction_objects import NOCTransaction_list,NOCTransaction
from modules.huristic_DE import *
from modules.huristic_PSO import *
from modules.huristic_GA import *

class NOCSequence(uvm_sequence):
    def __init__(self, name="uvm_sequence"):
        super().__init__(name)
        self.data={}
        self.helper = NOCHelper()
        self.cov=self.generate_filename()
        self.cov.write("No.of packets,coverage\n")
        self.coverage=0

    def generate_filename(self):
        """Generates a unique filename based on row and column values."""
        base_filename = f"coverage_report_{self.helper.row}X{self.helper.column}_{self.helper.huristic}"
        suffix = ""
        i = 1
        while True:
            filename = f"{base_filename}{suffix}.csv"
            if not os.path.exists(filename):
                return open(filename,"w")
            suffix = f"({i})"
            i += 1

    async def body(self):
        parallel_transactions=1 #random.randint(1,self.helper.size)
        transaction_list=[]
        count=0;
        # for i in range(self.helper.number_of_iterations):
        while(self.coverage<1):
            source_destination_gen = self.generate_source_destination()
            info(f"source={source_destination_gen} len={len(source_destination_gen)}")
            for i in source_destination_gen:
                source_node,destination_node=i#getting source node we are geenrating the transaction
                transaction=self.generate_transaction(source_node,destination_node)
                transaction_key=source_node+destination_node
                count=count+1
                self.helper.all_transactions[transaction_key]+=1
                self.coverage=self.calculate_coverage()
                self.cov.write(f"{count} ,{round(self.coverage*100,2)}\n")
                # await self.start_item(transaction)
                # await self.finish_item(transaction)
        self.cov.close()

    def calculate_coverage(self):
        source_coverage=sum([self.helper.source_coverage[keys]>0 for keys in self.helper.source_coverage])
        destination_coverage=sum([self.helper.destination_coverage[keys]>0 for keys in self.helper.destination_coverage])
        cross_coverage=sum([self.helper.all_transactions[keys]>0 for keys in self.helper.all_transactions])
        return (cross_coverage)/(self.helper.total_coverage)

    def generate_source_destination(self):
        row=self.helper.row
        column=self.helper.column
        print(f"self.helper.huristic --------------------------->{self.helper.huristic }")
        if self.helper.huristic =="DE":
            traffic= generate_source_destination_DE(row,column)
        elif self.helper.huristic=="PSO":
            traffic=source_destination_generator_pos(row,column)
        elif self.helper.huristic=="GA":
            traffic=source_destination_generator_GA(row,column)
        else:
            print("Generating the randim Traffic");
            traffic=self.generate_random_source_and_node()
        return traffic
    def generate_random_source_and_node(self):
        traffic=[]
        for i in range(1):
            while True:
                source=format(randint(0,self.helper.row),'04b')+format(randint(0,self.helper.column),'04b')
                destination=format(randint(0,self.helper.row),'04b')+format(randint(0,self.helper.column),'04b')
                if source!=destination: break
            traffic.append([source,destination])
            self.helper.source_coverage[source]+=1
            self.helper.destination_coverage[destination]+=1
        return traffic
    def generate_transaction(self, source_node, destination_node):
        transaction = NOCTransaction()
        transaction.header_flit = hex(int(self.generate_header_flit(source=source_node, destination=destination_node), 2))
        payload_flit1, payload_flit2 = self.generate_payload_flit()
        transaction.payload_flit1 = hex(int(payload_flit1, 2))
        transaction.payload_flit2 = hex(int(payload_flit2, 2))
        transaction.tailer_flit = hex(int("01011000000000000000000000000000", 2))
        return transaction

    def generate_header_flit(self, source, destination):
        headerCode = "0" + "01" + "11" + "000" + "0000" + "0000"  # we assumed vsID is equal 11 for all the data transmissions
        flit = headerCode + source + destination
        assert len(flit) == 32, f"The flit size is not 32"
        return flit

    def generate_payload_flit(self):
        #
        initial = ["00011100", "00011011"]
        #initial = [ "00000000",  "00000000"]
        payload = [0, 0]
        data = random.randrange(0, 16777215)
        data = bin(data)[2:]
        data1 = random.randrange(0, 16777215)
        data1 = bin(data1)[2:]
        if len(data) < 24:
            data = "0" * (24 - len(data)) + data
        if len(data1) < 24:
            data1 = "0" * (24 - len(data1)) + data1
        payload[0] = initial[0] + data
        payload[1] = initial[1] + data1
        assert len(payload[0]) ==32 and len(payload[1])==32,f"payload flit len is not equal to 32"
        return payload
