`ifndef imports
    `include "../Specs/specs.vh"
    `include "../Helpers/instructionMemory.sv"
`endif

module stg_1_IF(
    input CLOCK_50, sys_clock, reset_n,

    output reg [INSTR_ADDR_W-1:0] r_if_pc,
    output reg [INSTR_W-1:0] r_id_instr,
    output [9:0] LEDR,
    SDRAM_interface.source sdram
);


logic [INSTR_W-1:0] s_if_instr;
logic [INSTR_ADDR_W-1:0] s_if_nextaddr;
logic [INSTR_ADDR_W-1:0] s_if_nextpc;



// Connect to the instruction memory
s_if_instr
instructionMemory instrMem(
    .CLOCK_50,
    .reset_n,
    .read_addr          (s_if_pc),
    .instr_value        (s_if_instr),
    .SDRAM_connection   (sdram.receiver)
);



// Combinational Logic



assign s_if_nextaddr = r_if_pc + 1;

assign s_if_nextpc = (s_if_nextaddr == NUM_INSTRS)? 0 : s_if_nextaddr;

assign LEDR = r_if_pc;


// ---  REGISTER CLOCKING ---

always_ff @ (posedge clock, negedge reset) begin
    if (!reset) begin
        r_if_pc <= 0;
        r_id_instr <= 0;
    end else begin
        r_if_pc <= s_if_nextpc;
        r_id_instr <= s_if_instr;
    end 
end



endmodule