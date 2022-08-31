`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/09/2020 11:55:21 AM
// Design Name: 
// Module Name: myLab1
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


module myLab1(
    input BTNC,
    input SW0,
    input SW1,
    input SW2,
    
    output LD0,
    output LD1,
    output LD2,
    output LD3
    );
    // AND, | for OR, ~ for NOT and ^ for XOR
    assign LD0 = ~BTNC;
    assign LD1 = SW0 & SW1;
    assign LD2 = SW0 | SW1;
    assign LD3 = SW0 ^ SW1 ^ SW2;
    
endmodule
