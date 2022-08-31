`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/22/2020 09:50:59 PM
// Design Name: 
// Module Name: lab3_top
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


module lab3_top(
    input [7:0] sw,
    input btnL,
    input btnC,
    input btnR,
    input clkin,
    output [6:0] seg,
    output dp,
    output [3:0] an
    );
    
    wire [7:0] s;
    wire [6:0] hex1;
    wire [6:0] hex2;
    wire dig_sel;
    wire [7:0] temp;
    
    lab3_digsel digsel(.clkin(clkin), .greset(btnR), .digsel(dig_sel));
    incrementer incrementer(.a(sw), .b({btnL, btnC}), /*outputs*/.s(s));
    
    hex7seg hex7seg1(.n(s[3:0]), /*outputs*/ .seg(hex1));
    hex7seg hex7seg2(.n(s[7:4]), /*outputs*/ .seg(hex2));
    
    m2_1x8 mux(.in0({1'b0, hex1} ), .in1({1'b0, hex2}), .sel(dig_sel), .o(temp));
    assign seg = temp[6:0];
    assign dp = 1'b1;
    assign an[0] = dig_sel/*1'b0*/;
    assign an[1] = ~dig_sel/*1'b1*/;
    assign an[2] = 1'b1;
    assign an[3] = 1'b1;
    
    
endmodule
