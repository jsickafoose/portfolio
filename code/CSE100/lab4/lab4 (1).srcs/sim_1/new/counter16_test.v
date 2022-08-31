// CSE 100 Winter 2020
// This is a testbench for Lab 4.
// If the top level module in your Lab 4 project is named "top_lab4"
// and you used the suggested names for its inputs/outputs then
// then it will run without modification.  Otherwise follow the instructions
// in the comments marked "TODO" to modify it to conform to your project.
`timescale 1ns/1ps

module counter16_test();
   
   reg Up;
   reg Dw;
   reg LD;
   reg [15:0] Din;
   reg clk;
   wire UTC;
   wire DTC;
   wire [15:0] Q;
   
// TODO: replace "top_lab2" with the name of your top level Lab 2 module.

   counterUD16L UUT (
        .Up(Up), .Dw(Dw), .LD(LD), .Din(Din), .clk(clk), .UTC(UTC), .DTC(DTC), .Q(Q)
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
            clk = 1'b1;
        forever
        begin
            #(PERIOD-(PERIOD*DUTY_CYCLE)) clk = ~clk;
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
	 #1000;
   end
   
    initial
    begin	
    
    Up = 1'b0;
    Dw = 1'b0;
    Din = 16'b1111111100000000;
    LD = 1'b1;
    
        // sum is 10
        // -------------  Current Time:  100ns
	#1000;
	LD = 1'b0;
	Up = 1'b1;
	// Time: 2000ns
	#1000;
	Up = 1'b1;
	Dw = 1'b0;
	// Time: 4000ns
	#6000;
	Up = 1'b1;
	// Time: 5000ns
//	#1000;
//	Up = 1'b0;
//	Dw = 1'b0;
	// Time: 6000ns
	#1000;
	Up = 1'b1;
	// Time: 7000ns

    end
endmodule