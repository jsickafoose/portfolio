`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/04/2020 10:42:27 PM
// Design Name: 
// Module Name: randomNum
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

module randomNum(
    input clk,
    input reset,
    output [7:0] Q
    );
    wire D;
    
    assign D = (Q[0]^Q[5]^Q[6]^Q[7]);
    
    FDRE #(.INIT(1'b1)) Q0_FF (.C(clk), .R(reset), .CE(1'b1), .D(D), .Q(Q[0]));
    FDRE #(.INIT(1'b0)) Q1_FF (.C(clk), .R(reset), .CE(1'b1), .D(Q[0]), .Q(Q[1]));
    FDRE #(.INIT(1'b0)) Q2_FF (.C(clk), .R(reset), .CE(1'b1), .D(Q[1]), .Q(Q[2]));
    FDRE #(.INIT(1'b0)) Q3_FF (.C(clk), .R(reset), .CE(1'b1), .D(Q[2]), .Q(Q[3]));
    FDRE #(.INIT(1'b0)) Q4_FF (.C(clk), .R(reset), .CE(1'b1), .D(Q[3]), .Q(Q[4]));
    FDRE #(.INIT(1'b0)) Q5_FF (.C(clk), .R(reset), .CE(1'b1), .D(Q[4]), .Q(Q[5]));
    FDRE #(.INIT(1'b0)) Q6_FF (.C(clk), .R(reset), .CE(1'b1), .D(Q[5]), .Q(Q[6]));
    FDRE #(.INIT(1'b0)) Q7_FF (.C(clk), .R(reset), .CE(1'b1), .D(Q[6]), .Q(Q[7]));
    
endmodule

module storeNum(
    input [9:0] Din,
    input LD,
    input reset,
    input clk,
    output [9:0] Q
    );
    wire [9:0] D;
    assign D = (~{10{LD}} & Q)&(~{10{reset}}) | ({10{LD}} & Din)&(~{10{reset}});
    
    FDRE #(.INIT(1'b0)) Q0_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[0]), .Q(Q[0]));
    FDRE #(.INIT(1'b0)) Q1_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[1]), .Q(Q[1]));
    FDRE #(.INIT(1'b0)) Q2_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[2]), .Q(Q[2]));
    FDRE #(.INIT(1'b0)) Q3_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[3]), .Q(Q[3]));
    FDRE #(.INIT(1'b0)) Q4_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[4]), .Q(Q[4]));
    FDRE #(.INIT(1'b0)) Q5_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[5]), .Q(Q[5]));
    FDRE #(.INIT(1'b1)) Q6_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[6]), .Q(Q[6]));
    FDRE #(.INIT(1'b0)) Q7_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[7]), .Q(Q[7]));
    FDRE #(.INIT(1'b1)) Q8_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[8]), .Q(Q[8]));
    FDRE #(.INIT(1'b0)) Q9_FF (.C(clk), .R(reset), .CE(1'b1), .D(D[9]), .Q(Q[9]));
    
endmodule