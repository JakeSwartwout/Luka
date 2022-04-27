// takes in a binary value 0-F and outputs the values needed to light up a 7-segment display
module valueToSevenSeg(input [3:0] number, output reg [6:0] display);

always @ *
    // use a case to match which value it is
    case (number[3:0])
        // 0 means the segment will be on
        4'h0: display[6:0] = 7'b100_0000;
        4'h1: display[6:0] = 7'b111_1001;
        4'h2: display[6:0] = 7'b010_0100;
        4'h3: display[6:0] = 7'b011_0000;
        4'h4: display[6:0] = 7'b001_1001;
        4'h5: display[6:0] = 7'b001_0010;
        4'h6: display[6:0] = 7'b000_0010;
        4'h7: display[6:0] = 7'b111_1000;
        4'h8: display[6:0] = 7'b000_0000;
        4'h9: display[6:0] = 7'b001_1000;
        4'hA: display[6:0] = 7'b000_1000;
        4'hb: display[6:0] = 7'b000_0011;
        4'hC: display[6:0] = 7'b100_0110;
        4'hd: display[6:0] = 7'b010_0001;
        4'hE: display[6:0] = 7'b000_0110;
        4'hF: display[6:0] = 7'b000_1110;
        default: display [6:0] = 7'b111_1111;
    endcase

endmodule