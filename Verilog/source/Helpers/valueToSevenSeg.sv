// takes in a binary value 0-F and outputs the values needed to light up a 7-segment display
module valueToSevenSeg(input [3:0] number, output reg [7:0] display);

always @ *
    // use a case to match which value it is
    case (number[3:0])
        // 0 means the segment will be on
        4'h0: display[7:0] = 8'b1100_0000;
        4'h1: display[7:0] = 8'b1111_1001;
        4'h2: display[7:0] = 8'b1010_0100;
        4'h3: display[7:0] = 8'b1011_0000;
        4'h4: display[7:0] = 8'b1001_1001;
        4'h5: display[7:0] = 8'b1001_0010;
        4'h6: display[7:0] = 8'b1000_0010;
        4'h7: display[7:0] = 8'b1111_1000;
        4'h8: display[7:0] = 8'b1000_0000;
        4'h9: display[7:0] = 8'b1001_1000;
        4'hA: display[7:0] = 8'b1000_1000;
        4'hb: display[7:0] = 8'b1000_0011;
        4'hC: display[7:0] = 8'b1100_0110;
        4'hd: display[7:0] = 8'b1010_0001;
        4'hE: display[7:0] = 8'b1000_0110;
        4'hF: display[7:0] = 8'b1000_1110;
        default: display [7:0] = 8'b1111_1111;
    endcase

endmodule