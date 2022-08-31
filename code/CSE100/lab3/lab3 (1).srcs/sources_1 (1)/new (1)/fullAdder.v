`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/24/2020 11:29:42 AM
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
    output s,
    output cout
    );
    
    m4_1 sum(.in({cin, ~cin, ~cin, cin}), .sel({a, b}), .o(s));
    m4_1 carry(.in({1'b1, cin, cin, 1'b0}), .sel({a, b}), .o(cout));
endmodule
