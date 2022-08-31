`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 02/18/2020 12:21:44 PM
// Design Name: 
// Module Name: stateMachine
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


module stateMachine(
    input clk,
    input blockR,
    input blockL,
    output countUp,
    output countDw,
    output resetTimer/*,
    output startTimer*/
    );
    wire [6:0] D;
    wire [6:0] Q;
    
    assign D[0] = (~blockR&~blockL);
    assign D[1] = (Q[0]&blockR&~blockL) | (Q[1]&blockR&~blockL) | (Q[3]&blockR&~blockL);
    assign D[2] = (Q[0]&~blockR&blockL) | (Q[2]&~blockR&blockL) | (Q[4]&~blockR&blockL);
    assign D[3] = (Q[1]&blockL&blockR) | (Q[3]&blockL&blockR) | (Q[5]&blockL&blockR);
    assign D[4] = (Q[2]&blockR&blockL) | (Q[4]&blockR&blockL) | (Q[6]&blockR&blockL);
    assign D[5] = (Q[3]&~blockR&blockL) | (Q[5]&~blockR&blockL);
    assign D[6] = (Q[4]&blockR&~blockL) | (Q[6]&blockR&~blockL);
    
    FDRE #(.INIT(1'b1)) Q0_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[0]), .Q(Q[0]));
    FDRE #(.INIT(1'b0)) Q1_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[1]), .Q(Q[1]));
    FDRE #(.INIT(1'b0)) Q2_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[2]), .Q(Q[2]));
    FDRE #(.INIT(1'b0)) Q3_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[3]), .Q(Q[3]));
    FDRE #(.INIT(1'b0)) Q4_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[4]), .Q(Q[4]));
    FDRE #(.INIT(1'b0)) Q5_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[5]), .Q(Q[5]));
    FDRE #(.INIT(1'b0)) Q6_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[6]), .Q(Q[6]));
    
    assign countUp = Q[5]&~blockL&~blockR;
    assign countDw = Q[6]&~blockL&~blockR;
    assign resetTimer = Q[0];
//    assign startTimer = (Q[0]&blockR) | (Q[0]&blockL);
endmodule
