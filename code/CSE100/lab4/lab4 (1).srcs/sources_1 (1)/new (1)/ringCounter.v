`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 02/05/2020 05:04:45 PM
// Design Name: 
// Module Name: ringCounter
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


module ringCounter(
    input adv,
    input clk,
    output [3:0] sel
    );
//    wire [3:0] D;
    wire [3:0] Q;

//    assign D[0] = (Q[0]&~adv) | (Q[3]&adv);
//    assign D[1] = (Q[1]&~adv) | (Q[0]&adv);
//    assign D[2] = (Q[2]&~adv) | (Q[1]&adv);
//    assign D[3] = (Q[3]&~adv) | (Q[2]&adv);
    
    FDRE #(.INIT(1'b1)) Q0_FF (.C(clk), .R(1'b0), .CE(adv), .D(Q[3]), .Q(Q[0]));
    FDRE #(.INIT(1'b0)) Q1_FF (.C(clk), .R(1'b0), .CE(adv), .D(Q[0]), .Q(Q[1]));
    FDRE #(.INIT(1'b0)) Q2_FF (.C(clk), .R(1'b0), .CE(adv), .D(Q[1]), .Q(Q[2]));
    FDRE #(.INIT(1'b0)) Q3_FF (.C(clk), .R(1'b0), .CE(adv), .D(Q[2]), .Q(Q[3]));
    
    assign sel[0] = Q[0];
    assign sel[1] = Q[1];
    assign sel[2] = Q[2];
    assign sel[3] = Q[3];
endmodule
