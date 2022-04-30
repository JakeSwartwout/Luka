// similar to a testbench, creates a clock signal and the start signals for the main processor

`timescale 1 ns / 100 ps

`ifndef imports
    `include "Processor.sv"
    `include "./Helpers/sevenSegToValue.sv"
`endif

`define SIMULATION

module Simulator();

// set up our clock
logic base_clock;
initial base_clock = 1'b0;
always #1 base_clock = !base_clock;

// when to start/restart the program (active low)
logic restart_n;
// 6 hex displays
logic [6:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;


// connect up to the processor
Processor processor(
        .CLOCK_50   (base_clock),
        .KEY        ({1'b0, restart_n}),
        .HEX0, .HEX1, .HEX2, .HEX3, .HEX4, .HEX5,
        // don't bother to hook these things up
        .LEDR       (),
        .DRAM_ADDR  (),
        .DRAM_BA    (),
        .DRAM_CAS_N (),
        .DRAM_CKE   (),
        .DRAM_CLK   (),
        .DRAM_CS_N  (),
        .DRAM_DQ    (),
        .DRAM_LDQM  (),
        .DRAM_RAS_N (),
        .DRAM_UDQM  (),
        .DRAM_WE_N  ()
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
        $display("Built by: Jake Swartwout");
            restart_n = 1;
        #1  restart_n = 0;
        #1  restart_n = 1;
        #80
        $display("Simulation ended");
        $stop;
    end

endmodule