`ifndef VALUE_TO_DISPLAY

// takes in a value and outputs the result to an entire display of 6 x 7-segment displays

`ifndef imports
    `include "../Specs/specs.vh"
    `include "valueToSevenSeg.sv"
    `include "bin2bcd.sv"
`endif


module valueToDisplay(
    // we can represent a signed 16-bit value with a +/- and 5 digits
    input [VALUE_W -1:0] value,
    input print_it,
    output [6:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5
);


wire isNeg;
assign isNeg = value[VALUE_W -1];

// Make it negative with 2's complement
wire [VALUE_W -1:0] posValue;
assign posValue = isNeg? (~value + 1) : value;


// as a BCD, will have 5 digits that are 4-bits wide
wire [4:0][3:0] valueBCD;

bin2bcd converter(
    .binary_in(posValue),
    .bcd_out(valueBCD)
);


// store the hex inputs in temporary variables to zero-blank them
wire [4:0][7:0] value_decoded;

valueToSevenSeg display4(
    .number(valueBCD[4]),
    .display(value_decoded[4])
);
valueToSevenSeg display3(
    .number(valueBCD[3]),
    .display(value_decoded[3])
);
valueToSevenSeg display2(
    .number(valueBCD[2]),
    .display(value_decoded[2])
);
valueToSevenSeg display1(
    .number(valueBCD[1]),
    .display(value_decoded[1])
);
valueToSevenSeg display0(
    .number(valueBCD[0]),
    .display(value_decoded[0])
);


parameter HEX_OFF = 8'hFF;

// zero blanking
assign HEX4 = (valueBCD[4] == 0)? HEX_OFF : value_decoded[4];
assign HEX3 = (valueBCD[4:3] == 0)? HEX_OFF : value_decoded[3];
assign HEX2 = (valueBCD[4:2] == 0)? HEX_OFF : value_decoded[2];
assign HEX1 = (valueBCD[4:1] == 0)? HEX_OFF : value_decoded[1];
assign HEX0 = (valueBCD[4:0] == 0)? HEX_OFF : value_decoded[0];

// The negative sign
assign HEX5 = isNeg? 7'b011_1111 : HEX_OFF;


endmodule

`define VALUE_TO_DISPLAY
`endif