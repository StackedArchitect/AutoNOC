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
import tabulate





from modules.helper import NOCHelper
              
class NOCScoreboard(uvm_scoreboard):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.score=0
        self.sucess=0
        self.missed=0
        self.helper=NOCHelper()
        self.expected_transactions = {}
        self.received_transactions = {}
        self.time_taken={}

        
    def build_phase(self):
        self.cmd_fifo=uvm_tlm_analysis_fifo("cmd_fifo",self)
        self.result_fifo=uvm_tlm_analysis_fifo("result_fifo",self)
        self.cmd_get_port=uvm_get_port("cmd_get_port",self)
        self.result_get_port=uvm_get_port("result_get_port",self)
        self.cmd_export=self.cmd_fifo.analysis_export
        self.result_export=self.result_fifo.analysis_export

    def connect_phase(self):
        self.cmd_get_port.connect(self.cmd_fifo.get_export)
        self.result_get_port.connect(self.result_fifo.get_export)


    def check_phase(self):
        while self.cmd_get_port.can_get():
            """
            get the all the values from the fifo and store it in a dictioanry
            """
            cmd_flit_success,cmd_flit_transaction=self.cmd_get_port.try_get()
            if cmd_flit_success:
                self.record_expected_transaction(cmd_flit_transaction)
            else:
                info(f"cmd_get failure transaction = {cmd_flit_transaction}")
        while self.result_get_port.can_get():
            """
            get the all the values from the result  fifo and comapre with 
            the dictionary  expected flits.
           """
            result_flit_success,result_flit_transaction=self.result_get_port.try_get()
            if result_flit_success:
                source_to_destination=result_flit_transaction.header_flit[6:]
                if source_to_destination in self.expected_transactions:
                    expected_flit_list=self.expected_transactions[source_to_destination]
                    for expected_flit in expected_flit_list:
                        if expected_flit == result_flit_transaction:
                            self.sucess+=1
                            if source_to_destination in self.time_taken:
                                self.time_taken[source_to_destination].append(result_flit_transaction.time-expected_flit.time )
                            else:
                                self.time_taken[source_to_destination]=[result_flit_transaction.time-expected_flit.time]
                            info(f"Success--->{result_flit_transaction}")
                            expected_flit_list.remove(expected_flit)
                else:
                    info(f"cound't find the transaction in expected result transactions \nresult={str(result_flit_transaction)} ")
                    self.missed+=1



    def record_expected_transaction(self,transaction):
        source_to_destination=transaction.header_flit[6:]
        if source_to_destination in self.expected_transactions:
            self.expected_transactions[source_to_destination].append(transaction)
        else:
            self.expected_transactions[source_to_destination]=[transaction]
        
    def final_phase(self):
        coverage_score=0
        table_list=[["source --> destination","isCovered","No.Of Times"]]
        all_transactions=self.helper.all_transactions
        missed_list=[["source --> destination","isCovered","No.Of Times"]]
        for keys in all_transactions:
            source=self.helper.column*int(keys[0:4])+1*int(keys[4:8])
            destination=self.helper.column*int(keys[8:12])+1*int(keys[12:])
            if all_transactions[keys]>0:
                
                coverage_score+=1
            else:
                missed_list.append([str(source)+" --> "+str(destination),all_transactions[keys]>0,all_transactions[keys]])
        
            table_list.append([str(source)+" --> "+str(destination),all_transactions[keys]>0,all_transactions[keys]])
        
        
        unaccounted_transactions=self.helper.send_transactions-self.sucess-self.helper.incomplete_transactions-self.missed
        score_table=[
                        ["Total Sent",self.helper.send_transactions],
                        ["Total Success",self.sucess],
                        ["incomplete",self.helper.incomplete_transactions],
                        ["mis-match",self.missed],
                        ["",""],
                        ["Total Datapaths",self.helper.total_coverage],
                        ["coverage",str(coverage_score)+"/"+str(self.helper.total_coverage)]]
        info("Coverage Report")
        info(tabulate.tabulate(table_list,tablefmt="double_outline",headers="firstrow",showindex=True,numalign="centre",stralign="centre"))
        if len(missed_list)>0:
            info("Missed data paths")
            info(tabulate.tabulate(missed_list,tablefmt="double_outline",headers="firstrow",showindex=True,numalign="centre"))
        info("Summary")
        info(tabulate.tabulate(score_table,tablefmt="double_outline",showindex=False,numalign="centre"))
        info(f"the coverage percentage is {(coverage_score/self.helper.total_coverage)*100}%")
        
        #below is code for performance analysis and plotting the graph
        #x=[]
        #y=[]
        #z=[["Path","delay(ns)"]]
        #for keys in self.time_taken:
        #    x.append(keys)
        #    y.append(sum(self.time_taken[keys])//len(self.time_taken[keys]))
        #    z.append([keys,sum(self.time_taken[keys])//len(self.time_taken[keys])])
        #print("\033[95m"+"Timing analysis:"+"\033[0m")
        #print("\033[95m"+tabulate.tabulate(z,tablefmt="grid")+"\033[0m")
        #print("\033[95m"+f"total average time ={sum(y)/len(y)} ns ")
        #print(f"max time delay={max(y)}")
        #print(f"min time delay={min(y)}"+"\033[0m")

        
        
