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

// Connect up to a RAM memory
// quartus doesn't have a 3 port one, so need one for (RD in, RS1 out) and one for (RD in, RS2 out)
// this way, both get the same new data on the falling edge, then both can clock out their own selection for reading on rising edge
RegisterRam ram_for_rs1(
	.data       (writeData),
	.rdaddress  (rs1),
	.rdclock    (clock), // read on the rising edge
	.wraddress  (rd),
	.wrclock    (~clock), // write on the falling edge
	.wren       (RegWrite),
	.q          (read1)
);

RegisterRam ram_for_rs2(
	.data       (writeData),
	.rdaddress  (rs2),
	.rdclock    (clock), // read on the rising edge
	.wraddress  (rd),
	.wrclock    (~clock), // write on the falling edge
	.wren       (RegWrite),
	.q          (read2)
);

endmodule

`define REGISTER_FILE
`endif