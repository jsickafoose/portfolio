`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 02/05/2020 04:43:08 PM
// Design Name: 
// Module Name: selector
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


module selector(
    input [3:0] sel,
    input [15:0] N,
    output [3:0] H
    );
    
    assign H[0] = (~sel[3]&~sel[2]&~sel[1]&sel[0]&N[0]) | (~sel[3]&~sel[2]&sel[1]&~sel[0]&N[4]) | (~sel[3]&sel[2]&~sel[1]&~sel[0]&N[8]) | (sel[3]&~sel[2]&~sel[1]&~sel[0]&N[12]);
    assign H[1] = (~sel[3]&~sel[2]&~sel[1]&sel[0]&N[1]) | (~sel[3]&~sel[2]&sel[1]&~sel[0]&N[5]) | (~sel[3]&sel[2]&~sel[1]&~sel[0]&N[9]) | (sel[3]&~sel[2]&~sel[1]&~sel[0]&N[13]);
    assign H[2] = (~sel[3]&~sel[2]&~sel[1]&sel[0]&N[2]) | (~sel[3]&~sel[2]&sel[1]&~sel[0]&N[6]) | (~sel[3]&sel[2]&~sel[1]&~sel[0]&N[10]) | (sel[3]&~sel[2]&~sel[1]&~sel[0]&N[14]);
    assign H[3] = (~sel[3]&~sel[2]&~sel[1]&sel[0]&N[3]) | (~sel[3]&~sel[2]&sel[1]&~sel[0]&N[7]) | (~sel[3]&sel[2]&~sel[1]&~sel[0]&N[11]) | (sel[3]&~sel[2]&~sel[1]&~sel[0]&N[15]);

endmodule
