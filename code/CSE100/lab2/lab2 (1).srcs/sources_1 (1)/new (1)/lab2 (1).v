`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/14/2020 12:24:40 PM
// Design Name: 
// Module Name: lab2
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


module lab2(
    input sw0,
    input sw1,
    input sw2,
    input sw3,
    input sw4,
    input sw5,
    input sw6,
    output CA,
    output CB,
    output CC,
    output CD,
    output CE,
    output CF,
    output CG,
    output DP,
    output AN0,
    output AN1,
    output AN2,
    output AN3
    );
    
    wire t0, t1, t2, t3, u0, u1, u2, u3, u4, u5, u6;
    
    assign DP = 1'b1;
    assign AN0 = 1'b0;
    assign AN1 = 1'b1;
    assign AN2 = 1'b1;
    assign AN3 = 1'b1;
              // Inputs                                                                          // Outputs
    Adder add (.Cin(sw0), .a0(sw1), .a1(sw2), .a2(sw3), .b0(sw4), .b1(sw5), .b2(sw6), .S3(t3), .S2(t2), .S1(t1), .S0(t0));
    segConv segC (.n3(t3), .n2(t2), .n1(t1), .n0(t0), /*outputs:*/ .a(CA), .b(CB), .c(CC), .d(CD), .e(CE), .f(CF), .g(CG));
    assign CA = u0;
    assign CB = u1;
    assign CC = u2;
    assign CD = u3;
    assign CE = u4;
    assign CF = u5;
    assign CG = u6;
    
endmodule
