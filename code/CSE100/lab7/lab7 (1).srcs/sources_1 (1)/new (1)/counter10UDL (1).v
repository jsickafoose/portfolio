`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 02/25/2020 12:28:03 PM
// Design Name: 
// Module Name: counter10UDL
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


module counter10UDL(
    input Up,
    input Reset,
    input Dw,
    input clk,
    input [9:0] init,
    input LD,
    output [9:0] Q
    );
    wire [4:0] utc;
    wire [4:0] dtc;
//    countUD4L count1 (.Up(utc[0]&Up | Up&UTC), .Dw(dtc[0]&Dw | Dw&DTC), .LD(LD), .Din(Din[7:4]), .clk(clk), .UTC(utc[1]), .DTC(dtc[1]), .Q(Q[7:4]));
    count2UDL count0 (.Up(Up), .Reset(Reset), .Dw(Dw), .clk(clk), .init(init[1:0]), .LD(LD), .UTC(utc[0]), .Q(Q[1:0]), .DTC(dtc[0]));
    count2UDL count1 (.Up(Up&utc[0]), .Reset(Reset), .Dw(dtc[0]&Dw), .clk(clk), .init(init[3:2]), .LD(LD), .UTC(utc[1]), .Q(Q[3:2]), .DTC(dtc[1]));
    count2UDL count2 (.Up(Up&utc[1]&utc[0]), .Reset(Reset), .Dw(dtc[0]&dtc[1]&Dw), .clk(clk), .init(init[5:4]), .LD(LD), .UTC(utc[2]), .Q(Q[5:4]), .DTC(dtc[2]));
    count2UDL count3 (.Up(Up&utc[2]&utc[1]&utc[0]), .Reset(Reset), .Dw(dtc[0]&dtc[1]&dtc[2]&Dw), .clk(clk), .init(init[7:6]), .LD(LD), .UTC(utc[3]), .Q(Q[7:6]), .DTC(dtc[3]));
    count2UDL count4 (.Up(Up&utc[3]&utc[2]&utc[1]&utc[0]), .Reset(Reset), .Dw(dtc[0]&dtc[1]&dtc[2]&dtc[3]&Dw), .clk(clk), .init(init[9:8]), .LD(LD), .UTC(utc[4]), .Q(Q[9:8]), .DTC(dtc[4]));
    
endmodule

module count2UDL(
    input Up,
    input Reset,
    input Dw,
    input clk,
    input [1:0] init,
    input LD,
    output UTC,
    output DTC,
    output [1:0] Q
    );
    
    wire [1:0] D;
    assign D[0] = ~LD&(Up^Q[0]^Dw) | LD&init[0];
    assign D[1] = ~LD&(Q[1]^(Up&Q[0])^(Dw&~Q[0])) | LD&init[1];
    
    FDRE #(.INIT(1'b0)) Q0_FF (.C(clk), .R(Reset), .CE(1'b1), .D(D[0]), .Q(Q[0]));
    FDRE #(.INIT(1'b0)) Q1_FF (.C(clk), .R(Reset), .CE(1'b1), .D(D[1]), .Q(Q[1]));
    
    assign UTC = Q[0]&Q[1];
    assign DTC = ~Q[0]&~Q[1];
endmodule