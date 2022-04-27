`ifndef imports
    `include "../Specs/specs.vh"
    `include "../Specs/enums.vh"
    `include "../Helpers/registerFile.sv"      // for storing our register values
    `include "../Helpers/instructionDecoder.sv"// for decoding our instruction into registers, imm, and control signals
`endif

module stg_2_ID(
    input clock, reset,
    input [INSTR_W-1:0] r_id_instr,

    // output [OPTYPE_W-1:0] r_ex_opc,
    output reg [ALU_OP_W-1:0] r_ex_aluop,
    output reg [REG_ADDR_W-1:0] s_id_rs1, s_id_rs2, r_ex_rd,
    output reg [VALUE_W-1:0] r_ex_imm,
    output reg [INSTR_W-1:0] r_ex_instr,
    output reg r_ex_RegWrite, r_ex_PrintValue
);


wire [REG_ADDR_W-1:0] s_id_rd;
wire s_id_RegWrite, s_id_PrintValue;
wire [VALUE_W-1:0] s_id_imm;


// --- INSTRUCTION DECODE ---

instructionDecoder instrDecode(
    .instr(r_id_instr),
    .rs1(s_id_rs1),
    .rs2(s_id_rs2),
    .rd(s_id_rd),
    .alu_op(s_id_aluop),
    .imm(s_id_imm),
    .RegWrite(s_id_RegWrite),
    .PrintValue(s_id_PrintValue)
);


// ---  REGISTER CLOCKING ---

// don't clock the rs1 or rs2, since those need to go to the register file still

always_ff @ (posedge clock, negedge reset) begin
    if (!reset) begin
        r_ex_aluop <= 0;
        r_ex_rd <= 0;
        r_ex_imm <= 0;
        r_ex_RegWrite <= 0;
        r_ex_PrintValue <= 0;
    end else begin
        r_ex_aluop <= s_id_aluop;
        r_ex_rd <= s_id_rd;
        r_ex_imm <= s_id_imm;
        r_ex_RegWrite <= s_id_RegWrite;
        r_ex_PrintValue <= s_id_PrintValue;
    end
end


endmodule