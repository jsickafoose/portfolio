`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/08/2020 05:42:28 PM
// Design Name: 
// Module Name: counter16UDL
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


module counterUD16L(
    input clk,
    input Dw,
    input Up,
    input reset,
    output UTC,
    output DTC,
    output [15:0] Q
    );
    wire [3:0] utc;
    wire [3:0] dtc;
    
    countUD4L count0 (.Up(Up), .Dw(Dw), .reset(reset), .clk(clk), .UTC(utc[0]), .DTC(dtc[0]), .Q(Q[3:0]));
    countUD4L count1 (.Up(utc[0]&Up | Up&UTC), .Dw(dtc[0]&Dw | Dw&DTC), .reset(reset), .clk(clk), .UTC(utc[1]), .DTC(dtc[1]), .Q(Q[7:4]));
    countUD4L count2 (.Up(utc[1]&Up&utc[0] | Up&UTC), .Dw(dtc[0]&dtc[1]&Dw | Dw&DTC), .reset(reset), .clk(clk), .UTC(utc[2]), .DTC(dtc[2]), .Q(Q[11:8]));
    countUD4L count3 (.Up(utc[2]&Up&utc[0]&utc[1] | Up&UTC), .Dw(dtc[0]&dtc[1]&dtc[2]&Dw | Dw&DTC), .reset(reset), .clk(clk), .UTC(utc[3]), .DTC(dtc[3]), .Q(Q[15:12]));
    
    assign UTC = utc[0]&utc[1]&utc[2]&utc[3];
    assign DTC = dtc[0]&dtc[1]&dtc[2]&dtc[3];
    
endmodule

module countUD4L(
    input Up,
    input Dw,
    input clk,
    input reset,
    output UTC,
    output DTC,
    output [3:0] Q
    );
    wire [3:0] D;
    
    assign D[0] = (Q[0]^Up^Dw);
    assign D[1] = (Q[1]^(Q[0]&Up)^(~Q[0]&Dw));
    assign D[2] = (Q[2]^(Q[0]&Q[1]&Up)^(~Q[0]&~Q[1]&Dw));
    assign D[3] = (Q[3]^(Up&Q[2]&Q[1]&Q[0])^(Dw&~Q[2]&~Q[1]&~Q[0]));
    
    FDRE #(.INIT(1'b0)) Q0_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[0]), .Q(Q[0]));
    FDRE #(.INIT(1'b0)) Q1_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[1]), .Q(Q[1]));
    FDRE #(.INIT(1'b0)) Q2_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[2]), .Q(Q[2]));
    FDRE #(.INIT(1'b0)) Q3_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[3]), .Q(Q[3]));
    
    assign UTC = Q[0]&Q[1]&Q[2]&Q[3];
    assign DTC = ~Q[0]&~Q[1]&~Q[2]&~Q[3];
    
endmodule

