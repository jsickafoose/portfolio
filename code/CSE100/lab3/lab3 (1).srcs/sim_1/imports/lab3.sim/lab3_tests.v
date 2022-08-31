// CSE 100 Winter 2020
// This is a testbench for Lab 2.
// If the top level module in your Lab 2 project is named "top_lab2"
// and you used the suggested names for its inputs/outputs then
// then it will run without modification.  Otherwise follow the instructions
// in the comments marked "TODO" to modify it to conform to your project.
`timescale 1ns/1ps

module lab2_tests();
   
   reg [7:0] sw;
   wire [6:0] seg;
   reg btnR;
   reg btnL;
   reg btnC;
   reg clkin;
   wire dp;
   wire [3:0] an;
   
   
// TODO: replace "top_lab2" with the name of your top level Lab 2 module.

   lab3_top UUT (
        .sw(sw), .seg(seg), .btnR(btnR), .btnL(btnL), .btnC(btnC), .clkin(clkin), .dp(dp), .an(an)
        );
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
	 // add your (input) stimuli here
	 // to set signal foo to value 0 use
	 // foo = 1'b0;
	 // to set signal foo to value 1 use
	 // foo = 1'b1;
	 //always advance time my multiples of 100ns
	 // to advance time by 100ns use the following line
	 #100;
   end
   
    initial
    begin	

    sw = 8'b00000000;
    btnC = 1'b0;
    btnL = 1'b0;
    btnR = 1'b0;
        // sum is 10
        // -------------  Current Time:  1000ns
	#100;
	sw[0] = 1'b1;
	// complete this testbentch  so that all 
	// 16 hex values are generated
    end
endmodule	
