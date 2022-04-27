// similar to a testbench, creates a clock signal and the start signals for the main processor

`timescale 1 ns / 100 ps

`ifndef imports
    `include "Processor.sv"
    `include "./Helpers/sevenSegToValue.sv"
`endif

module Simulator();

// set up our clock
logic base_clock;
initial base_clock = 1'b0;
always #1 base_clock = !base_clock;

// when to start/restart the program (active low)
logic restart;
// 6 hex displays
logic [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;

// connect up to the processor
Processor #( .CLOCK_DIVISOR(1) ) processor(
                    .ADC_CLK_10(base_clock),
                    .KEY({1'b0, restart}),
                    .SW(),
                    .HEX0, .HEX1, .HEX2, .HEX3, .HEX4, .HEX5,
                    .LEDR()
                    );

// convert our hex displays to actual values
logic [5:0][3:0] dispValues;
sevenSegToValue display5(.display(HEX5), .value(dispValues[5]));
sevenSegToValue display4(.display(HEX4), .value(dispValues[4]));
sevenSegToValue display3(.display(HEX3), .value(dispValues[3]));
sevenSegToValue display2(.display(HEX2), .value(dispValues[2]));
sevenSegToValue display1(.display(HEX1), .value(dispValues[1]));
sevenSegToValue display0(.display(HEX0), .value(dispValues[0]));

// Monitor our variables
// Use this for printing our values
initial
    $monitor($time, "  Display values: %h", dispValues);

initial
    begin
        $dumpfile("../output/simulation.vcd");
        $dumpvars;
        $display("Built by: Jake Swartwout");
            restart = 1;
        #1  restart = 0;
        #1  restart = 1;
        #80
        $display("Simulation ended");
        $finish;
    end

endmodule