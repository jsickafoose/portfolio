`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/08/2020 04:59:06 PM
// Design Name: 
// Module Name: RingCounterLed
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


module RingCounterLed(
    input adv,
    input clk,
    input tick,
    input reset,
    output [3:0] sel
    );

    wire [3:0] Q;

    FDRE #(.INIT(1'b1)) Q0_FF (.C(clk), .R(reset), .CE(adv), .D(Q[3] | ~Q[3]&tick), .Q(Q[0]));
    FDRE #(.INIT(1'b0)) Q1_FF (.C(clk), .R(reset), .CE(adv), .D(Q[0]), .Q(Q[1]));
    FDRE #(.INIT(1'b0)) Q2_FF (.C(clk), .R(reset), .CE(adv), .D(Q[1]), .Q(Q[2]));
    FDRE #(.INIT(1'b0)) Q3_FF (.C(clk), .R(reset), .CE(adv), .D(Q[2]), .Q(Q[3]));
    
    assign sel[0] = Q[3];
    assign sel[1] = Q[2];
    assign sel[2] = Q[1];
    assign sel[3] = Q[0];
endmodule
