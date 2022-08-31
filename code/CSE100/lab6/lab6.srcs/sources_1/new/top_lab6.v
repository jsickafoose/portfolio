`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 02/18/2020 12:11:24 PM
// Design Name: 
// Module Name: top_lab6
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


module top_lab6(
    input clkin,
    input btnU,
    input btnR,
    input btnL,
    output [15:0] led,
    output [3:0] an,
    output dp,
    output [6:0] seg
    );
    /*Clk           */wire digsel, qsec, clk;
    /*StateMachine  */wire countUp, countDw, resetTimer/*, startTimer*/;
    /*Time_Counter  */wire [7:0] Q_timer;
    
    lab6_clks lab6_clk (.clkin(clkin), .greset(btnU), .clk(clk), .digsel(digsel), .qsec(qsec));
    stateMachine StateMachine (.clk(clk), .blockR(btnR), .blockL(btnL), .countUp(countUp),
        .countDw(countDw), .resetTimer(resetTimer)/*, .startTimer(startTimer)*/);
    // Have edge detector just in case, for the resetTimer because it stays high
    wire reset;
    edgeDetector EdgeDetector (.btn(resetTimer), .clk(clk), .btnOut(reset));
    counterUD8L Time_Counter (.clk(clk), .Din(8'b00000000), .Up(qsec & ~resetTimer & ~(&Q_timer)), .Dw(1'b0),.LD(reset), .Q(Q_timer));
    
    counterUD8L Turkey_Counter(); // need to modify for negatives I think
endmodule

module edgeDetector(
    input btn,
    input clk,
    output btnOut
    );
    wire [1:0] D;
    wire [1:0] Q;
    
    assign D[0] = btn;
    assign D[1] = Q[0];
    
    FDRE #(.INIT(1'b0)) Q0_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[0]), .Q(Q[0]));
    FDRE #(.INIT(1'b0)) Q1_FF (.C(clk), .R(1'b0), .CE(1'b1), .D(D[1]), .Q(Q[1]));
    
    assign btnOut = ~Q[1]&Q[0];
endmodule