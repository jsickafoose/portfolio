`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/04/2020 11:21:46 PM
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
    input btnC,
    input TwoSecs,
    input Dead,
    output init,
    output CountDown,
    output Run,
    output Flash,
    output reset
    );
    wire [4:0] D;
    wire [4:0] Q;
    
    assign D[0] = (Q[0]&~btnC);
    assign D[1] = (Q[0]&btnC) | (Q[1]&~TwoSecs) | (Q[3]&btnC);
    assign D[2] = (Q[1]&TwoSecs) | (Q[2]&~Dead);
    assign D[3] = (Q[2]&Dead) | (Q[3]&~btnC);
    
    FDRE #(.INIT(1'b1)) Q0_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[0]), .Q(Q[0]));
    FDRE #(.INIT(1'b0)) Q1_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[1]), .Q(Q[1]));
    FDRE #(.INIT(1'b0)) Q2_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[2]), .Q(Q[2]));
    FDRE #(.INIT(1'b0)) Q3_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[3]), .Q(Q[3]));
    
    assign init = Q[0];
    assign CountDown = Q[1];
    assign Run = Q[2];
    assign Flash = Q[3] | Q[1];
    assign reset = Q[3] & btnC;
endmodule
