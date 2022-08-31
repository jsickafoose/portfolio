`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/23/2020 11:11:05 AM
// Design Name: 
// Module Name: incrementer
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


module incrementer(
    input [7:0] a,
    input [1:0] b,
    output [7:0] s
    );
    wire c1, c2, c3, c4, c5, c6, c7, c8;
    fullAdder adder1(.a(a[0]), .b(b[0]), .cin(1'b0), .s(s[0]), .cout(c1));
    fullAdder adder2(.a(a[1]), .b(b[1]), .cin(c1), .s(s[1]), .cout(c2));
    fullAdder adder3(.a(a[2]), .b(1'b0), .cin(c2), .s(s[2]), .cout(c3));
    fullAdder adder4(.a(a[3]), .b(1'b0), .cin(c3), .s(s[3]), .cout(c4));
    fullAdder adder5(.a(a[4]), .b(1'b0), .cin(c4), .s(s[4]), .cout(c5));
    fullAdder adder6(.a(a[5]), .b(1'b0), .cin(c5), .s(s[5]), .cout(c6));
    fullAdder adder7(.a(a[6]), .b(1'b0), .cin(c6), .s(s[6]), .cout(c7));
    fullAdder adder8(.a(a[7]), .b(1'b0), .cin(c7), .s(s[7]), .cout(c8));
endmodule