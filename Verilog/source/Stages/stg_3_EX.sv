`ifndef imports
    `include "../Specs/specs.vh"
    `include "../Specs/enums.vh"
`endif

module stg_3_EX(
    input sys_clock, reset_n, 
    input [ALU_OP_W-1:0] r_ex_aluop,
    input [VALUE_W-1:0] r_ex_read1,
    input [VALUE_W-1:0] r_ex_read2,
    input [REG_ADDR_W-1:0] r_ex_rd,
    input [VALUE_W-1:0] r_ex_imm,
    input r_ex_RegWrite,
    input r_ex_PrintValue,

    output reg [REG_ADDR_W-1:0] r_me_rd,
    output reg [VALUE_W-1:0] r_me_aluout,
    output reg r_me_aluzero,
    output reg r_me_RegWrite,
    output reg r_me_PrintValue
);

// --- ALU ---

wire [VALUE_W-1:0] s_ex_aluout;
assign s_ex_aluout = r_ex_read1 + r_ex_read2 + r_ex_imm;

wire s_ex_aluzero;
assign s_ex_aluzero = (s_ex_aluout == 0)? 1'b1 : 1'b0;


// ---  REGISTER CLOCKING ---

always_ff @ (posedge sys_clock, negedge reset_n) begin
    if (~reset_n) begin
        r_me_rd <= 0;
        r_me_aluout <= 0;
        r_me_aluzero <= 0;
        r_me_RegWrite <= 0;
        r_me_PrintValue <= 0;
    end else begin
        r_me_rd <= r_ex_rd;
        r_me_aluout <= s_ex_aluout;
        r_me_aluzero <= s_ex_aluzero;
        r_me_RegWrite <= r_ex_RegWrite;
        r_me_PrintValue <= r_ex_PrintValue;
    end 
end



endmodule