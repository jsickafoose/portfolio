// CSE 100 Winter 2020
// This is a testbench for Lab 4.
// If the top level module in your Lab 4 project is named "top_lab4"
// and you used the suggested names for its inputs/outputs then
// then it will run without modification.  Otherwise follow the instructions
// in the comments marked "TODO" to modify it to conform to your project.
`timescale 1ns/1ps

module count4_test();
   
   reg Up;
   reg Dw;
   reg LD;
   reg [3:0] Din;
   reg clk;
   wire UTC;
   wire DTC;
   wire [3:0] Q;
   
// TODO: replace "top_lab2" with the name of your top level Lab 2 module.

   countUD4L UUT (
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
	 #100;
   end
   
    initial
    begin	
    
    Up = 1'b0;
    Dw = 1'b0;
    Din = 4'b0010;
    LD = 1'b1;
    
        // sum is 10
        // -------------  Current Time:  100ns
	#1000;
	LD = 1'b0;
	Up = 1'b1;
	// Time: 200ns
	#1000;
	Up = 1'b0;
	// Time: 300ns
	#100;
	Up = 1'b1;
	// Time: 400ns
	#100;
	Up = 1'b0;
	// Time: 500ns
	#100;
	Up = 1'b1;
	// Time: 600ns

    end
endmodule