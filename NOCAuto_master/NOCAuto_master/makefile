CWD=$(shell pwd)
COCOTB_REDUCED_LOG_FMT = True
SIM ?= xcelium
EXTRA_ARGS +=  -coverage all -covfile coverage.txt -covoverwrite
EXTRA_ARGS += +access+rwc
EXTRA_ARGS += -input signal.tcl
WAVES=1


VERILOG_INCLUDE_DIRS=$(CWD)/RTL
VERILOG_SOURCES=$(CWD)/RTL/Auto_Mesh.sv\
                $(CWD)/RTL/top_module.v \
                $(CWD)/RTL/op_link1.v \
                $(CWD)/RTL/op_link2.v \
                $(CWD)/RTL/op_link3.v \
                $(CWD)/RTL/op_link4.v \
                $(CWD)/RTL/op_core.v \
                $(CWD)/RTL/op_data_path.v\
                $(CWD)/RTL/allot_vc.v \
                $(CWD)/RTL/demux_16.v\
                $(CWD)/RTL/dff_asynch_clr.v \
                $(CWD)/RTL/dff_synch_clr.v \
                $(CWD)/RTL/dff_synch_reset.v\
                $(CWD)/RTL/dff_synch_set.v\
                $(CWD)/RTL/encoder.v\
                $(CWD)/RTL/falling_edge_pulse_generator.v\
                $(CWD)/RTL/fop.v\
                $(CWD)/RTL/gray_mod6.v\
                $(CWD)/RTL/gray_mod8.v\
                $(CWD)/RTL/ip_chnl.v\
                $(CWD)/RTL/ip_link.v\
                $(CWD)/RTL/IRS.v\
                $(CWD)/RTL/jk_ff.v\
                $(CWD)/RTL/memory.v\
                $(CWD)/RTL/mux.v\
                $(CWD)/RTL/priority_encoder.v\
                $(CWD)/RTL/register_1bit.v\
                $(CWD)/RTL/register_32bit.v\
                $(CWD)/RTL/register_4bit.v\
                $(CWD)/RTL/round_robin_req.v\
                $(CWD)/RTL/router_fifo.v\
                $(CWD)/RTL/routing_algo_mesh.v\
                $(CWD)/RTL/rr_arbiter.v\
                $(CWD)/RTL/rr_comb_new.v\
                $(CWD)/RTL/asynch_comparator.v

MODULE := testbenchUvm
TOPLEVEL := Auto_Mesh     
TOPLEVEL_LANG := verilog
COCOTB_HDL_TIMEUNIT=1us
COCOTB_HDL_TIMEPRECISION=1ns

include $(shell cocotb-config --makefiles)/Makefile.sim
# include ../cleanall.mk
