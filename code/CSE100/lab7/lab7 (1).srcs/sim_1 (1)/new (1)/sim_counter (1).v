`timescale 1ns / 1ps

module sim_counter();
   
   reg Up;
   reg Reset;
   reg clk;
   wire [9:0] Q;
   
   counter10UDL UUT (.Up(Up), .Reset(Reset), .clk(clk), .Q(Q));
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
    Reset = 1'b0;
        
        // sum is 10
        // -------------  Current Time:  100ns
	#1000;
    Up = 1'b1;
	// Time: 2000ns
	#1000;
//	Go = 1'b0;
	#1000;
	Up = 1'b0;
	#1000;
    Reset = 1'b1;
	#1000;
	Reset = 1'b0;
	#1000;

    end
endmodule