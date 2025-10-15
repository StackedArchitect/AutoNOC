module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/Auto_Mesh      .fst");
    $dumpvars(0, Auto_Mesh      );
end
endmodule
