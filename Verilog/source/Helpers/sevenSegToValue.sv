`ifndef SEVEN_SEG_TO_VALUE

// takes in an 8-bit value meant to be displayed on a 7-segment display and converts it back into a binary value
// Returns 0xE if the value is not recognized
// This is purely for testing purposes
module sevenSegToValue(input [6:0] display, output reg [3:0] value);

always @ *
    // use a case to match which value it is
    // only match on the lower 6 to ignore the decimal
    case (display[6:0])
        // 0 means the segment will be on
        6'b100_0000: value[3:0] = 4'h0;
        6'b111_1001: value[3:0] = 4'h1;
        6'b010_0100: value[3:0] = 4'h2;
        6'b011_0000: value[3:0] = 4'h3;
        6'b001_1001: value[3:0] = 4'h4;
        6'b001_0010: value[3:0] = 4'h5;
        6'b000_0010: value[3:0] = 4'h6;
        6'b111_1000: value[3:0] = 4'h7;
        6'b000_0000: value[3:0] = 4'h8;
        6'b001_1000: value[3:0] = 4'h9;
        6'b000_1000: value[3:0] = 4'hA;
        6'b000_0011: value[3:0] = 4'hb;
        6'b100_0110: value[3:0] = 4'hC;
        6'b010_0001: value[3:0] = 4'hd;
        6'b000_0110: value[3:0] = 4'hE;
        6'b000_1110: value[3:0] = 4'hF;
        // special characters
        6'b011_1111: value[3:0] = 4'hD; // a Dash
        6'b111_1111: value[3:0] = 4'hE; // Empty
        // if we don't recognize the setup, display an F for fail
        default: value[3:0] = 4'hF;
    endcase

endmodule

`define SEVEN_SEG_TO_VALUE
`endif