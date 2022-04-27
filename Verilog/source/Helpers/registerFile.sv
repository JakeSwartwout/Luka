`ifndef REGISTER_FILE

`ifndef imports
    `include "../Specs/specs.vh"
`endif

module registerFile(
    input clock,
    input reset_n,
    input [REG_ADDR_W-1:0] rs1, rs2, rd,
    input [VALUE_W-1:0] writeData,
    input RegWrite,
    output reg [VALUE_W-1:0] read1, read2
);

logic [REG_ADDR_W-1:0][VALUE_W-1:0] registers;

// always reads
// only writes if RegWrite, and writes first so that read can get values
always_ff @ (posedge clock, negedge clock, negedge reset_n) begin
    if (~reset_n)
        registers = 0;
    else if (clock) begin // rising edge - read
        // reading
        read1 = registers[rs1];
        read2 = registers[rs2];
    end else if (~clock) // falling edge - write
        if (RegWrite & (rd != 0))
            registers[rd] = writeData;
end

// see digital logic HW week 12 for how to use the Max-10 Lite ROM
// probably can do a similar `ifdef Sim to do quartus vs simulation
// // Connect to our memory, putting displays directly onto HEX0
// ROM memory(	.address(counter),
// 				.clock(KEY[1]),
// 				.q(HEX0)
// );

endmodule

`define REGISTER_FILE
`endif