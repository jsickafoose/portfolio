`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/30/2020 01:21:12 PM
// Design Name: 
// Module Name: counterUD16L
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


module counterUD8L(
    input clk,
    input [7:0] Din,
    input Dw,
    input Up,
    input LD,
    output UTC,
    output DTC,
    output [7:0] Q
    );
    wire [1:0] utc;
    wire [1:0] dtc;
    
    countUD4L count0 (.Up(Up), .Dw(Dw), .LD(LD), .Din(Din[3:0]), .clk(clk), .UTC(utc[0]), .DTC(dtc[0]), .Q(Q[3:0]));
    countUD4L count1 (.Up(utc[0]&Up | Up&UTC), .Dw(dtc[0]&Dw | Dw&DTC), .LD(LD), .Din(Din[7:4]), .clk(clk), .UTC(utc[1]), .DTC(dtc[1]), .Q(Q[7:4]));
    
    assign UTC = utc[0]&utc[1];
    assign DTC = dtc[0]&dtc[1];
endmodule
