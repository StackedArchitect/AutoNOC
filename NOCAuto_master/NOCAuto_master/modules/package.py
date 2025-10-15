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
import os

from modules.helper import NOCHelper
from modules.transaction_objects import NOCTransaction_list,NOCTransaction
from modules.huristic_DE import *
from modules.huristic_PSO import *
from modules.huristic_GA import *
