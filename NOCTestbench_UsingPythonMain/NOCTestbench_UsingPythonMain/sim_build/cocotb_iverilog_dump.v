module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/top_3x3_router.fst");
    $dumpvars(0, top_3x3_router);
end
endmodule
