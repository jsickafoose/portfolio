`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 02/25/2020 12:02:09 PM
// Design Name: 
// Module Name: top_lab7
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


module top_lab7(
    input clkin,
    input btnR,
    input btnL,
    input btnC,
    input [15:0] sw,
    output [3:0] vgaRed,
    output [3:0] vgaBlue,
    output [3:0] vgaGreen,
    output Hsync,
    output Vsync,
    output [15:0] led,
    output [3:0] an,
    output dp,
    output [6:0] seg
    );
    wire clk, digsel;
    wire [9:0] HQ, VQ;
    wire TwoSecs, Dead, init, CountDown, Run, Flash, reset, init1; // Wires for state machine
    
    lab7_clks lab7_clk(.clkin(clkin), .clk(clk), .greset(sw[0]),.digsel(digsel));
    counter10UDL Hcount (.Up(1'b1), .Reset(HQ>=10'd799), .clk(clk), .Q(HQ));
    counter10UDL Vcount (.Up(HQ>=10'd799), .Reset(VQ>=10'd524), .clk(clk), .Q(VQ));
    assign Hsync = ~((HQ >= 10'd655) && (HQ <= 10'd750));
    assign Vsync = ~((VQ >= 10'd489) && (VQ <= 10'd490));
    
    // Changes X when buttons L or R are pressed 
    wire [9:0] BPQX;
    counter10UDL BlockPosX(.Up(btnL & Run), .Dw(btnR & Run), .Reset(reset), .clk(VQ == 0 & HQ == 0), .Q(BPQX));

    edgeDetector EdgeDetector (.btn(init), .clk(clk), .btnOut(init1));
    // Tracks bottom Y of each block, reseting at the bottom
    wire [9:0] BPQ0, BPQ1, BPQ2, BPQ3, BPQ4, BPQ5, BPQ6, store0, store1, store2, store3, store4, store5, store6;
    counter10UDL BlockPos0(.Up(~Vsync&HQ == 10'd0&Run), .Reset(BPQ0>=10'd559), .clk(clk /*& Run*/), .init(10'd0), .LD(init1 | reset), .Q(BPQ0));
    counter10UDL BlockPos1(.Up(~Vsync&HQ == 10'd0&Run), .Reset(BPQ1>=10'd559), .clk(clk /*& Run*/), .init(10'd80), .LD(init1 | reset), .Q(BPQ1));
    counter10UDL BlockPos2(.Up(~Vsync&HQ == 10'd0&Run), .Reset(BPQ2>=10'd559), .clk(clk /*& Run*/), .init(10'd160), .LD(init1 | reset), .Q(BPQ2));
    counter10UDL BlockPos3(.Up(~Vsync&HQ == 10'd0&Run), .Reset(BPQ3>=10'd559), .clk(clk /*& Run*/), .init(10'd240), .LD(init1 | reset), .Q(BPQ3));
    counter10UDL BlockPos4(.Up(~Vsync&HQ == 10'd0&Run), .Reset(BPQ4>=10'd559), .clk(clk /*& Run*/), .init(10'd320), .LD(init1 | reset), .Q(BPQ4));
    counter10UDL BlockPos5(.Up(~Vsync&HQ == 10'd0&Run), .Reset(BPQ5>=10'd559), .clk(clk /*& Run*/), .init(10'd400), .LD(init1 | reset), .Q(BPQ5));
    counter10UDL BlockPos6(.Up(~Vsync&HQ == 10'd0&Run), .Reset(BPQ6>=10'd559), .clk(clk /*& Run*/), .init(10'd480), .LD(init1 | reset), .Q(BPQ6));
    
    // need to take 4 bits of LSFR, 16 possible numbers. Multiply the number by 8 and read in twosComp
    wire [7:0] lsfrOut;
    randomNum LSFR (.clk(clk), .Q(lsfrOut));
    storeNum storeNum0 (.Din((lsfrOut[6]) ? ((store1-lsfrOut[5:0]<=0) ? (store1+lsfrOut[5:0]) : (store1-lsfrOut[5:0])) : ((store1+lsfrOut[5:0]>=519) ? (store1-lsfrOut[5:0]) : (store1+lsfrOut[5:0]))), .LD(BPQ0 == 10'd0), .clk(clk), .Q(store0));
    storeNum storeNum1 (.Din((lsfrOut[6]) ? ((store2-lsfrOut[5:0]<=0) ? (store2+lsfrOut[5:0]) : (store2-lsfrOut[5:0])) : ((store2+lsfrOut[5:0]>=519) ? (store2-lsfrOut[5:0]) : (store2+lsfrOut[5:0]))), .LD(BPQ1 == 10'd0), .clk(clk), .Q(store1));
    storeNum storeNum2 (.Din((lsfrOut[6]) ? ((store3-lsfrOut[5:0]<=0) ? (store3+lsfrOut[5:0]) : (store3-lsfrOut[5:0])) : ((store3+lsfrOut[5:0]>=519) ? (store3-lsfrOut[5:0]) : (store3+lsfrOut[5:0]))), .LD(BPQ2 == 10'd0), .clk(clk), .Q(store2));
    storeNum storeNum3 (.Din((lsfrOut[6]) ? ((store4-lsfrOut[5:0]<=0) ? (store4+lsfrOut[5:0]) : (store4-lsfrOut[5:0])) : ((store4+lsfrOut[5:0]>=519) ? (store4-lsfrOut[5:0]) : (store4+lsfrOut[5:0]))), .LD(BPQ3 == 10'd0), .clk(clk), .Q(store3));
    storeNum storeNum4 (.Din((lsfrOut[6]) ? ((store5-lsfrOut[5:0]<=0) ? (store5+lsfrOut[5:0]) : (store5-lsfrOut[5:0])) : ((store5+lsfrOut[5:0]>=519) ? (store5-lsfrOut[5:0]) : (store5+lsfrOut[5:0]))), .LD(BPQ4 == 10'd0), .clk(clk), .Q(store4));
    storeNum storeNum5 (.Din((lsfrOut[6]) ? ((store6-lsfrOut[5:0]<=0) ? (store6+lsfrOut[5:0]) : (store6-lsfrOut[5:0])) : ((store6+lsfrOut[5:0]>=519) ? (store6-lsfrOut[5:0]) : (store6+lsfrOut[5:0]))), .LD(BPQ5 == 10'd0), .clk(clk), .Q(store5));
    storeNum storeNum6 (.Din((lsfrOut[6]) ? ((store0-lsfrOut[5:0]<=0) ? (store0+lsfrOut[5:0]) : (store0-lsfrOut[5:0])) : ((store0+lsfrOut[5:0]>=519) ? (store0-lsfrOut[5:0]) : (store0+lsfrOut[5:0]))), .LD(BPQ6 == 10'd0), .clk(clk), .Q(store6));
    
    // When given the X,Y coords of a corner, computes the coords of the block's opposite corner
    wire [9:0] outX0, outY0, outX1, outY1, outX2, outY2, outX3, outY3, outX4, outY4, outX5, outY5, outX6, outY6;
    wire [9:0] inX0, inX1, inX2, inX3, inX4, inX5, inX6;
    assign inX0 = /*reset ? (10'd320) : */(store0+BPQX);
    assign inX1 = /*reset ? (10'd320) : */(store1+BPQX);
    assign inX2 = /*reset ? (10'd320) : */(store2+BPQX);
    assign inX3 = /*reset ? (10'd320) : */(store3+BPQX);
    assign inX4 = /*reset ? (10'd320) : */(store4+BPQX);
    assign inX5 = /*reset ? (10'd320) : */(store5+BPQX);
    assign inX6 = /*reset ? (10'd320) : */(store6+BPQX);
    blockSize BlockSize0(.inX(inX0), .inY(BPQ0), .width(sw[6:4]), .outX(outX0), .outY(outY0));
    blockSize BlockSize1(.inX(inX1), .inY(BPQ1), .width(sw[6:4]), .outX(outX1), .outY(outY1));
    blockSize BlockSize2(.inX(inX2), .inY(BPQ2), .width(sw[6:4]), .outX(outX2), .outY(outY2));
    blockSize BlockSize3(.inX(inX3), .inY(BPQ3), .width(sw[6:4]), .outX(outX3), .outY(outY3));
    blockSize BlockSize4(.inX(inX4), .inY(BPQ4), .width(sw[6:4]), .outX(outX4), .outY(outY4));
    blockSize BlockSize5(.inX(inX5), .inY(BPQ5), .width(sw[6:4]), .outX(outX5), .outY(outY5));
    blockSize BlockSize6(.inX(inX6), .inY(BPQ6), .width(sw[6:4]), .outX(outX6), .outY(outY6));
    
    wire [9:0] frameQ, qsec;
    
    counter10UDL frame (.Up(1'b1), .Reset(frameQ > 10'd121), .clk(VQ == 0 & HQ == 0), .Q(frameQ));
    counter10UDL Qsec (.Up(1'b1), .Reset(qsec > 10'd15), .clk(VQ == 0 & HQ == 0), .Q(qsec));
    wire qsec1;
    edgeDetector EdgeDetector1 (.btn(qsec>=15), .clk(clk), .btnOut(qsec1));
    
    assign TwoSecs = (frameQ >= 10'd120);
    assign Dead = ~((10'd328>=inX0 & 10'd312<=outX0 & 10'd392<=BPQ0 & 10'd408>=outY0) | (10'd328>=inX1 & 10'd312<=outX1 & 10'd392<=BPQ1 & 10'd408>=outY1) | (10'd328>=inX2 & 10'd312<=outX2 & 10'd392<=BPQ2 & 10'd408>=outY2) | (10'd328>=inX3 & 10'd312<=outX3 & 10'd392<=BPQ3 & 10'd408>=outY3) | (10'd328>=inX4 & 10'd312<=outX4 & 10'd392<=BPQ4 & 10'd408>=outY4) | (10'd328>=inX5 & 10'd312<=outX5 & 10'd392<=BPQ5 & 10'd408>=outY5) | (10'd328>=inX6 & 10'd312<=outX6 & 10'd392<=BPQ6 & 10'd408>=outY6));
    stateMachine StateMachine (.clk(clk), .btnC(btnC), .TwoSecs(TwoSecs), .Dead(Dead), .init(init), .CountDown(CountDown), .Run(Run), .Flash(Flash), .reset(reset));
    wire [3:0] ringLed;
    RingCounterLed ringCounterLED0 (.adv(Run&qsec1), .clk(clk), .sel(ringLed), .reset(reset));

    assign led[15] = (frameQ >= 30)&CountDown | Run&ringLed[3];
    assign led[11] = (frameQ >= 60)&CountDown | Run&ringLed[3];
    assign led[7] = (frameQ >= 90)&CountDown | Run&ringLed[3];
    assign led[3] = (frameQ >= 120)&CountDown | Run&ringLed[3];
    
    assign led[14:12] = {3{Run}}&ringLed[2:0];
    assign led[10:8] = {3{Run}}&ringLed[2:0];
    assign led[6:4] = {3{Run}}&ringLed[2:0];
    assign led[2:0] = {3{Run}}&ringLed[2:0];
    
    assign vgaRed = ((4'h0&{4{HQ>10'd639 | VQ>10'd479}}) | (4'hf&{4{HQ>=10'd312 & HQ<=10'd328 & VQ>=10'd392 & VQ<=10'd408 & (~Flash | Flash&(frameQ<10'd30) | Flash&(frameQ<10'd90)&(frameQ>=10'd60))}}) | (4'hf&{4{HQ>=(inX0) & HQ<=outX0 & VQ<=BPQ0 & VQ>=outY0}}) | (4'hf&{4{HQ>=(inX1) & HQ<=outX1 & VQ<=BPQ1 & VQ>=outY1}}) | (4'hf&{4{HQ>=(inX2) & HQ<=outX2 & VQ<=BPQ2 & VQ>=outY2}}) | /*(4'h0&{4{HQ>=10'd280 & HQ<=outX3 & VQ<=BPQ3 & VQ>=outY3}}) | (4'h0&{4{HQ>=10'd280 & HQ<=outX4 & VQ<=BPQ4 & VQ>=outY4}}) |*/ (4'h2&{4{HQ>=(inX5) & HQ<=outX5 & VQ<=BPQ5 & VQ>=outY5}}) | (4'h8&{4{HQ>=(inX6) & HQ<=outX6 & VQ<=BPQ6 & VQ>=outY6}}));
    assign vgaBlue = ((4'h0&{4{HQ>10'd639 | VQ>10'd479}}) | (4'hf&{4{HQ>=10'd312 & HQ<=10'd328 & VQ>=10'd392 & VQ<=10'd408 & (~Flash | Flash&(frameQ<10'd30) | Flash&(frameQ<10'd90)&(frameQ>=10'd60))}}) | /*(4'h0&{4{HQ>=10'd280 & HQ<=outX0 & VQ<=BPQ0 & VQ>=outY0}}) |*/ (4'h7&{4{HQ>=(inX1) & HQ<=outX1 & VQ<=BPQ1 & VQ>=outY1}}) | (4'hf&{4{HQ>=(inX2) & HQ<=outX2 & VQ<=BPQ2 & VQ>=outY2}}) | (4'hf&{4{HQ>=(inX3) & HQ<=outX3 & VQ<=BPQ3 & VQ>=outY3}}) | /*(4'h0&{4{HQ>=10'd280 & HQ<=outX4 & VQ<=BPQ4 & VQ>=outY4}}) |*/ (4'h2&{4{HQ>=(inX5) & HQ<=outX5 & VQ<=BPQ5 & VQ>=outY5}}) /*| (4'h0&{4{HQ>=10'd280 & HQ<=outX6 & VQ<=BPQ6 & VQ>=outY6}})*/);
    assign vgaGreen = ((4'h0&{4{HQ>10'd639 | VQ>10'd479}}) | (4'hf&{4{HQ>=10'd312 & HQ<=10'd328 & VQ>=10'd392 & VQ<=10'd408 & (~Flash | Flash&(frameQ<10'd30) | Flash&(frameQ<10'd90)&(frameQ>=10'd60))}}) | /*(4'h0&{4{HQ>=10'd280 & HQ<=outX0 & VQ<=BPQ0 & VQ>=outY0}}) | (4'h0&{4{HQ>=10'd280 & HQ<=outX1 & VQ<=BPQ1 & VQ>=outY1}}) | (4'h0&{4{HQ>=10'd280 & HQ<=outX2 & VQ<=BPQ2 & VQ>=outY2}}) | (4'h0&{4{HQ>=10'd280 & HQ<=outX3 & VQ<=BPQ3 & VQ>=outY3}}) | */(4'hf&{4{HQ>=(inX4) & HQ<=outX4 & VQ<=BPQ4 & VQ>=outY4}}) | (4'h5&{4{HQ>=(inX5) & HQ<=outX5 & VQ<=BPQ5 & VQ>=outY5}}) | (4'hf&{4{HQ>=(inX6) & HQ<=outX6 & VQ<=BPQ6 & VQ>=outY6}}));
//    &(VQ == 0 & HQ == 0)
    
    wire [15:0] counterOut;
    counter10UDL gameCounter (.clk(clk), .Up(Run&qsec1), .Reset(reset), .Q(counterOut));
    wire [3:0] sel, H;
    ringCounter RingCounter (.adv(digsel), .clk(clk), .sel(sel));
    selector Selector (.sel(sel), .N(counterOut), .H(H));
    hex7seg hex7seg (.n(H), .seg(seg));
    assign an[3] = ~(sel[3] &(~Flash | Flash&(frameQ<10'd30) | Flash&(frameQ<10'd90)&(frameQ>=10'd60)));
    assign an[2] = ~(sel[2] &(~Flash | Flash&(frameQ<10'd30) | Flash&(frameQ<10'd90)&(frameQ>=10'd60)));
    assign an[1] = ~(sel[1] &(~Flash | Flash&(frameQ<10'd30) | Flash&(frameQ<10'd90)&(frameQ>=10'd60)));
    assign an[0] = ~(sel[0] &(~Flash | Flash&(frameQ<10'd30) | Flash&(frameQ<10'd90)&(frameQ>=10'd60)));
    assign dp = 1'b1;
endmodule

