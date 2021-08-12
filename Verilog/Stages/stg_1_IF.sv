`ifndef imports
    `include "../Specs/specs.vh"
    `include "../inputs.vh"
`endif

module stg_1_IF(
    input clock, reset,

    output reg [INSTR_ADDR_W-1:0] r_if_pc,
    output reg [INSTR_W-1:0] r_id_instr,
    output [9:0] LEDR
);


logic [INSTR_W-1:0] s_if_instr;
logic [INSTR_ADDR_W-1:0] s_if_nextaddr;
logic [INSTR_ADDR_W-1:0] s_if_nextpc;



// Combinational Logic

parameter [INSTR_ADDR_W-1:0] tester = 0;

assign s_if_instr = instr_mem[r_if_pc];
// assign s_if_instr = instr_mem[tester];
// assign s_if_instr = 19'b0000000000010000111;


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