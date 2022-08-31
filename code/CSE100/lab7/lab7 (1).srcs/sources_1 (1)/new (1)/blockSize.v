`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/02/2020 12:07:26 PM
// Design Name: 
// Module Name: blockSize
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


module blockSize(
    input [9:0] inX,
    input [9:0] inY,
    input [2:0] width,
    output [9:0] outX,
    output [9:0] outY
    );
    
//    assign outX = inX+120;
    assign outX = inX+8+(16*width);
    assign outY = inY<80 ? 10'd0 : inY-80;
endmodule
