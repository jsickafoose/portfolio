`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/16/2020 12:08:25 PM
// Design Name: 
// Module Name: fullAdder
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


module fullAdder(
    input a,
    input b,
    input cin,
    output cout,
    output s
    );
    
    wire w1, w2, w3;
    assign w1 = (a ^ b);
    assign w2 = (a & b);
    assign w3 = (w1 & cin);
    assign s = (w1 ^ cin);
    assign cout = (w3 | w2);
    
endmodule
