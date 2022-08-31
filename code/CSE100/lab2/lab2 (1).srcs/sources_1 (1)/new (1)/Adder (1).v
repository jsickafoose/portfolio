`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/14/2020 12:43:31 PM
// Design Name: 
// Module Name: Adder
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


module Adder(
    input Cin,
    input a0,
    input a1,
    input a2,
    input b0,
    input b1,
    input b2,
    output S3,
    output S2,
    output S1,
    output S0
    );
    wire C1, C2;
     // segConv segC (.n3(t3), .n2(t2), .n1(t1), .n0(t0));
    fullAdder adder1 (.a(a0), .b(b0), .cin(Cin), .cout(C1), .s(S0));
    fullAdder adder2 (.a(a1), .b(b1), .cin(C1), .cout(C2), .s(S1));
    fullAdder adder3 (.a(a2), .b(b2), .cin(C2), .cout(S3), .s(S2));
    
endmodule
