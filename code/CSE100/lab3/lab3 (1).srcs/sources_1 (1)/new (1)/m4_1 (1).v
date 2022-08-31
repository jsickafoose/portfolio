`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/21/2020 01:04:28 PM
// Design Name: 
// Module Name: m4_1
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


module m4_1(
    input [3:0] in,
    input [1:0] sel,
    output o
    );
    
    assign o = ((~sel[1]&~sel[0]&in[0]) | (~sel[1]&sel[0]&in[1]) | (sel[1]&~sel[0]&in[2]) | (sel[1]&sel[0]&in[3]));
    //assign o = in[sel];
endmodule
