# Software Installation: 
- We have used Linux to build the bench, If you want to run this in Windows we suggest using `WSL(Windows Subsystem for Linux)` 
## Installation of Icarus(iverilog):
- Icarus is an open-source HDL simulator.
- Cocotb supports 11 or below versions.
- If you are using Ubuntu just run the command `sudo apt-get install iverilog`
- For redhat-based distribution you had to build the software from the source code.Folloe the instructions from the website
`https://steveicarus.github.io/iverilog/usage/installation.html`
## Python packages :
- To install cocotb 'pip install cocotb'
- To install PyUVM  'pip install PyUVM'
- To install tabulate `pip install tabulate`

# Executing the code
- To execute the command  `make` from the project folder,

# Automated Testbench for NOC module.
- Can scale to any size.
- The  inport ports should be named int the format `data_in_core_r{i}`.
- The output ports should be named in the format `data_out_core_r{i}`
- - Other inputs are clk and clr.
# Installation Requirements:
- I made this code using iverilog ,So for pyuvm need's iverilog verion 11 . Versions higher than 11 won't work as they don't produce vvp files.
- cocotb,pyuvm and cmake are the other requirements.
