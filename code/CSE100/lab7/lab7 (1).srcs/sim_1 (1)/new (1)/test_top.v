`timescale 1ns / 1ps

module test_top();
   
   reg clkin;
   reg btnR;
   reg btnL;
   reg btnC;
   wire [3:0] vgaRed;
   wire [3:0] vgaBlue;
   wire [3:0] vgaGreen;
   wire Hsync;
   wire Vsync;
   
   top_lab7 UUT (.clkin(clkin), .btnR(btnR), .btnL(btnL), 
   .btnC(btnC), .vgaRed(vgaRed), .vgaBlue(vgaBlue), .vgaGreen(vgaGreen),
    .Hsync(Hsync), .Vsync(Vsync));
// TODO: In the three lines above, make sure the pin names match the names
// used for the inputs/outputs of your top level module.   For example, if you
// used "cin" rather than "sw0", then replace ".sw0(sw0)" with ".cin(sw0)" 
    parameter PERIOD = 10;
    parameter real DUTY_CYCLE = 0.5;
    parameter OFFSET = 2;

    initial    // Clock process for clkin
    begin
        #OFFSET
            clkin = 1'b1;
        forever
        begin
            #(PERIOD-(PERIOD*DUTY_CYCLE)) clkin = ~clkin;
        end
	end
	

   
    initial
    begin	

    btnR = 1'b0;
    btnL = 1'b0;
    btnC = 1'b0;    
        // sum is 10
        // -------------  Current Time:  100ns
	#1000;
	btnC=1'b0;
	#1000;
    btnC = 1'b0;
	#1000;
	#1000;
	#1000;
	#1000;
	#1000;

    end
endmodule