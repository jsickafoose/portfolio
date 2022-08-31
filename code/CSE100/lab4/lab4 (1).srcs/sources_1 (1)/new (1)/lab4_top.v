`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 02/03/2020 02:17:08 PM
// Design Name: 
// Module Name: lab4_top
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


module lab4_top(
    input clkin,
    input btnR,
    input btnU,
    input btnD,
    input btnC,
    input btnL,
    input [15:0] sw,
    output [6:0] seg,
    output dp,
    output [3:0] an,
    output [15:0] led
    );

    wire dig_sel;
    wire Dw, OR1, OR2, OR3, UTC, DTC;
    wire [15:0] Q;
    wire [3:0] sel, H;
    wire clk;
    assign led = sw;
    
    questionMark question (.Q(Q), .btn(btnC), .out(OR1));
    lab4_clks clks (.clkin(clkin), .greset(btnR), .clk(clk), .digsel(dig_sel));
    edgeDetector edgeDetectorUp (.btn(btnU), .clk(clk), .btnOut(OR2));
    edgeDetector edgeDetectorDw (.btn(btnD), .clk(clk), .btnOut(Dw));
    assign OR3 = OR1 | OR2;
    counterUD16L Counter (.clk(clk), .Din(sw), .Dw(Dw), .Up(OR3), .LD(btnL), .UTC(UTC), .DTC(DTC), .Q(Q));
    ringCounter RingCounter (.adv(dig_sel), .clk(clk), .sel(sel));
    selector Selector (.sel(sel), .N(Q), .H(H));
    hex7seg hex7seg (.n(H), .seg(seg));
    
    assign an = ~sel;
    assign dp = ~(DTC & sel[1] | UTC & sel[2]);

    
endmodule

module questionMark(
    input [15:0] Q,
    input btn,
    output out
    );

    assign out = btn&~(&Q[15:2]);
endmodule