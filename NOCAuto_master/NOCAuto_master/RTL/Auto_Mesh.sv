
`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/22/2024 11:34:17 PM
// Design Name: 
// Module Name: Auto_Mesh
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

module Auto_Mesh #(parameter M=2,N=2,T=0)(
    input clk, clr,
    input [31:0] data_in_core [0:M-1][0:N-1],
    output [31:0] data_out_core [0:M-1][0:N-1] 
);
 
//parameter M = 3; // Number of rows
//parameter N = 3; // Number of columns
//parameter T = Topology = 0 for Mesh and 1 for Torus 
 
// Define data_out_link as an array of arrays
wire [31:0] data_out_link[4:1][0:M-1][0:N-1];
wire [31:0] full_out_vc1_link[4:1][0:M-1][0:N-1];
wire [31:0] full_out_vc2_link[4:1][0:M-1][0:N-1];
wire [31:0] full_out_vc3_link[4:1][0:M-1][0:N-1];
wire [31:0] full_out_vc4_link[4:1][0:M-1][0:N-1];
wire [31:0] full_out_core_vc[4:1][0:M-1][0:N-1];
 
 
// Parameterized constants
parameter DEFAULT_DATA = 32'h60000000;
 
wire gnd = 0;
wire vdd = 1;
// Instances of routers
genvar i, j;
generate
    for (i = 0; i < M; i = i + 1) begin : gen_rows
        for (j = 0; j < N; j = j + 1) begin : gen_columns
            top_module inst (
                .data_in_link1((i < M-1) ? data_out_link[2][i+1][j] :((T == 0)? DEFAULT_DATA :data_out_link[2][0][j])), // Link 2 of router below. done
                .data_in_link2((i > 0) ? data_out_link[1][i-1][j] : ((T==0)? DEFAULT_DATA : data_out_link[1][M-1][j])), // Link 1 of router to the right. done
                .data_in_link3((j < N-1) ? data_out_link[4][i][j+1] : ((T==0) ? DEFAULT_DATA : data_out_link[4][i][j+1])),  // Link 4 of router to the right. done
                .data_in_link4((j > 0) ? data_out_link[3][i][j-1] : ((T==0) ? DEFAULT_DATA : data_out_link[3][i][N-1])), // Link 3 of router to left
                .data_in_core(data_in_core[i][j]),
                .clk(clk),
                .clr(clr),
                .current_address(((16*i)+j)&8'hff),
                .full_in_link1_vc1((i < M-1)?full_out_vc1_link[2][i+1][j]:((T==0)? gnd : full_out_vc1_link[2][0][j])),
                .full_in_link1_vc2((i < M-1)?full_out_vc2_link[2][i+1][j]:((T==0)? gnd : full_out_vc2_link[2][0][j])),
                .full_in_link1_vc3((i < M-1)?full_out_vc3_link[2][i+1][j]:((T==0)? gnd : full_out_vc3_link[2][0][j])),
                .full_in_link1_vc4((i < M-1)?full_out_vc4_link[2][i+1][j]:((T==0)? gnd : full_out_vc4_link[2][0][j])),
                .full_in_link2_vc1((i > 0 )?full_out_vc1_link[1][i-1][j]:((T==0)? gnd : full_out_vc1_link[1][M-1][j])),
                .full_in_link2_vc2((i > 0 )?full_out_vc2_link[1][i-1][j]:((T==0)? gnd : full_out_vc2_link[1][M-1][j])),
                .full_in_link2_vc3((i > 0 )?full_out_vc3_link[1][i-1][j]:((T==0)? gnd : full_out_vc3_link[4][i][j+1])),
                .full_in_link2_vc4((i > 0 )?full_out_vc4_link[1][i-1][j]:((T==0)? gnd : full_out_vc4_link[1][M-1][j])),
                .full_in_link3_vc1((j < N-1)?full_out_vc1_link[4][i][j+1]:((T==0)? gnd : full_out_vc1_link[4][i][j+1])),
                .full_in_link3_vc2((j < N-1)?full_out_vc2_link[4][i][j+1]:((T==0)? gnd : full_out_vc2_link[4][i][j+1])),
                .full_in_link3_vc3((j < N-1)?full_out_vc3_link[4][i][j+1]:((T==0)? gnd : full_out_vc3_link[4][i][j+1])),
                .full_in_link3_vc4((j < N-1)?full_out_vc4_link[4][i][j+1]:((T==0)? gnd : full_out_vc4_link[4][i][j+1])),
                .full_in_link4_vc1((j>0)? full_out_vc1_link[3][i][j-1]:((T==0)? gnd : full_out_vc1_link[3][i][N-1])),
                .full_in_link4_vc2((j>0)? full_out_vc2_link[3][i][j-1]:((T==0)? gnd : full_out_vc2_link[3][i][N-1])),
                .full_in_link4_vc3((j>0)? full_out_vc3_link[3][i][j-1]:((T==0)? gnd : full_out_vc3_link[3][i][N-1])),
                .full_in_link4_vc4((j>0)? full_out_vc4_link[3][i][j-1]:((T==0)? gnd : full_out_vc4_link[3][i][N-1])),
                .full_in_core_vc1(0),//done
                .full_in_core_vc2(0),//done
                .full_in_core_vc3(0),//done
                .full_in_core_vc4(0),//done
                .data_out_link1(data_out_link[1][i][j]),  // done
                .data_out_link2(data_out_link[2][i][j]), // done
                .data_out_link3(data_out_link[3][i][j]),  // done
                .data_out_link4(data_out_link[4][i][j]), // done
                .data_out_core(data_out_core[i][j]),  //done
                .full_out_link1_vc1(full_out_vc1_link[1][i][j]),
                .full_out_link1_vc2(full_out_vc2_link[1][i][j]),
                .full_out_link1_vc3(full_out_vc3_link[1][i][j]),
                .full_out_link1_vc4(full_out_vc4_link[1][i][j]),
                .full_out_link2_vc1(full_out_vc1_link[2][i][j]),
                .full_out_link2_vc2(full_out_vc2_link[2][i][j]),
                .full_out_link2_vc3(full_out_vc3_link[2][i][j]),
                .full_out_link2_vc4(full_out_vc4_link[2][i][j]),
                .full_out_link3_vc1(full_out_vc1_link[3][i][j]),
                .full_out_link3_vc2(full_out_vc2_link[3][i][j]),
                .full_out_link3_vc3(full_out_vc3_link[3][i][j]),
                .full_out_link3_vc4(full_out_vc4_link[3][i][j]),
                .full_out_link4_vc1(full_out_vc1_link[4][i][j]),
                .full_out_link4_vc2(full_out_vc2_link[4][i][j]),
                .full_out_link4_vc3(full_out_vc3_link[4][i][j]),
                .full_out_link4_vc4(full_out_vc4_link[4][i][j]),
                .full_out_core_vc1(full_out_core_vc[1][i][j]),
                .full_out_core_vc2(full_out_core_vc[2][i][j]),
                .full_out_core_vc3(full_out_core_vc[3][i][j]),
                .full_out_core_vc4(full_out_core_vc[4][i][j])
            );
//            new1 (rd_clk,wr_clk,data_in_risc[i][j],reset,wr_en,destination[i][j],((16*i)+j)&8'hff,empty,full_int,data_in_core[i][j],wr_o); 
        end
    end
    
endgenerate
endmodule

