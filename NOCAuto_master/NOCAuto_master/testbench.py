import cocotb
from cocotb.triggers import Timer,ClockCycles,FallingEdge,RisingEdge
import pyuvm
from pyuvm import *
import random

from cocotb.clock import Clock

from logging import warning,error,fatal
import random

# Figure 6: Setting up logging using the logger variable
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class NOCHelper():
    """
    This class is to contain all the common functions regarding the NOC .Like Sequence generator
    and sending commands.
    """
    def __init__(self,row=2,column=2):
        """
        In this class we have
        self.Data_In_Ports=[f"data_in_core_r{i+1}" for i in range(0,4)]
        self.Data_Out_Ports=[f"data_in_core_r{i+1}" for i in range(0,4)]
        self.sequence=[]
        self.Input_sequence=[]-->these  is the sequence of the command
        self.data[i]--This tells the data that is sent to the noc for each core
        self.result[i]-->this tells the        warning(f"data in ports={self.Data_In_Ports}")
 data that is recieved by the each core
        self.size----->this defines the size of the noc
        self.routerId--->represents the Id of each router(ROW+COlUM) in binary 8bit format
        """
        self.Input_sequence=[]
        self.sequence=[]
        self.data={}
        self.result={}
        self.routerId=[]
        self.row=row
        self.column=column
        self.Data_In_Ports=[f"data_in_core_r{i+1}" for i in range(0,self.row*self.column)]
        self.Data_Out_Ports=[f"data_out_core_r{i+1}" for i in range(0,self.row*self.column)]
        warning(f"data in ports={self.Data_In_Ports}")
        warning(f"data in ports={self.Data_Out_Ports}")

        #this for loop will create router ids
        for rows in range(0,self.row):
            for colums in range(0,self.column):
                routerRow=bin(rows)[2:].zfill(4)
                routerColumn=bin(colums)[2:].zfill(4)
                tempId=routerRow+routerColumn
                self.routerId.append(tempId)
        warning(f"all the routerId={self.routerId}")
        self.state=[1 for i in self.routerId]

    def headerSequenceGenerator(self)->None:
        """
             generate the header sequences for  header from source
        """
        header = "0" + "01" + "11" + "000" + "0000" + "0000"#we asssumed vsID is equal 11 for all the data tranmisions
        for source in self.routerId:
            for destination in self.routerId:
                if source==destination:continue
                flit=header+source+destination
                assert len(flit)==32,f"The flit size is not 32"
                self.sequence.append(header+source+destination)
        
   
    def paylodGenerator(self):
        """
        creates random payloads
        
        """
        self.initial = ["00011100", "00011011"]
        payload=[0,0]
        data = random.randrange(0, 16777215)
        data = bin(data)[2:]
        data1 = random.randrange(0, 16777215)
        data1 = bin(data1)[2:]
        if len(data) < 24:data = "0" * (24 - len(data)) + data  
        if len(data1) < 24:data1 = "0" * (24 - len(data1)) + data1  
        assert len(data) == 24, f"payload data value is not 16 its length is {len(data)}"
        payload[0] = self.initial[0] + data
        payload[1] = self.initial[1] + data1
        return payload
    
    def sequeceGenerator(self):
        """ created a list of complete sequences.In this stage we also storing the  sent data for comapring
        the score board.
        """
        self.headerSequenceGenerator()
        header = self.sequence
        for i in header:
            #decoded destination
            #generating the payload
            payload = self.paylodGenerator()
            self.data[hex(int(i[15:],2))[2:].zfill(4)]=[hex(int(str(payload[0]),2)),hex(int(str(payload[1]),2))]
            #storing the payload value in the
            #generating the list of 4 flits and storing them in input_sequence
            self.Input_sequence.append([hex(int(i,2)), hex(int(payload[0],2)),hex(int(payload[1],2)), hex(int("01011000000000000000000000000000",2))])
        
        return self.Input_sequence
    
    async def clrAndReset(self,dut):
        """
            This fucntion will clear and reset the 2x2driver module
            expects dut as input value
        """
        #clearing all the values
        dut.clr.value=1
        await ClockCycles(dut.clk,2)
        dut.clr.value=0
        #resetting all the cores
        for i in self.Data_In_Ports:setattr(getattr(dut,i),"value",0x7fffffff)
        await ClockCycles(dut.clk,1)

    async def clockClockGenearation(self,dut):
        """
            Clock generation, requires dut to pass
        """
        clk= Clock(dut.clk,10,units="us")
        cocotb.start_soon(clk.start())
        warning("clock is created")

    async def driver(self,dut):
        """
        This block will drive the inputs to the noc
        """
        sequnce=self.sequeceGenerator()
        for i in sequnce:
            source_row_column=str(i[0][6:8])
            destination_row_column=str(i[0][8:])
            source=self.column*int(source_row_column[0])+1*int(source_row_column[1])
            destination=3*int(destination_row_column[0])+1*int(destination_row_column[1])
            for cmd in i:
                port=getattr(dut,self.Data_In_Ports[source])
                setattr(port,"value",int(cmd,16))
                await ClockCycles(dut.clk,2,rising=False)

            setattr(port,"value",0x7fffffff)
            await ClockCycles(dut.clk,3,rising=False)
        await ClockCycles(dut.clk,30,rising=False)
        await ClockCycles(dut.clk,100)

    async def monitor(self,dut):
        """
            This module capture the output value and stores in a structure.
        """
        key={}
        current={}
        for i in self.Data_Out_Ports:
            current[i] = []
        

        while True:
            await FallingEdge(dut.clk)
            for i in self.Data_Out_Ports:
                try:
                    current[i]=hex(int(str(getattr(getattr(dut,i),"value")),2))
                    if current[i] == "0x60000000":
                        continue
                    elif current[i][:6] == "0x2000":
                        # self.result[i]+=[current[i]], we don't require this value
                        key[i]=current[i][6:]
                        
                    elif current[i] == "0x40000000":
                        # self.result[i]+=[current[i]], we don't need this value
                        continue
                    elif current[i] not in self.result[key[i]]:
                        # print(f"we are decieveing data key[{i}]={key[i]} current[{i}]={current[i]}")
                        self.result[key[i]]+=[current[i]]
                except KeyError:
                    self.result[key[i]]=[current[i]]
                
                    

@cocotb.test()
async def test(dut):
    noc=NOCHelper(2,2)
    #generating the clock
    await noc.clockClockGenearation(dut)
    #resetting the module
    await noc.clrAndReset(dut)
    #start the monitor
    cocotb.start_soon(noc.monitor(dut))
    #applying the sequence
    await noc.driver(dut)
    warning(f"\ndata send:")
    [warning(f"data[{i}]={noc.data[i]}") for i in noc.data]    
    warning(f"\ndata recieved:")
    [warning(f"result[{i}]={noc.result[i]}") for i in noc.result]
    