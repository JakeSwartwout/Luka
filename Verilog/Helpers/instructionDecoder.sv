// decodes an incoming exception into the necessary registers, signals, immediate, etc
`ifndef imports
    `include "../Specs/specs.vh"
    `include "../Specs/enums.vh"
    `include "../Specs/opcodes.vh"
`endif

module instructionDecoder(
    input [INSTR_W-1:0] instr,
    output reg [REG_ADDR_W-1:0] rs1, rs2, rd,
    output reg [ALU_OP_W-1:0] alu_op,
    output reg [VALUE_W-1:0] imm,
    output reg RegWrite, PrintValue
);

// defining some parameters
parameter RD_END = REG_ADDR_W + OPTYPE_W;
parameter RS1_END = REG_ADDR_W + RD_END;
parameter RS2_END = REG_ADDR_W + RS1_END;

// breaking off the optype

logic [OPTYPE_W-1:0] optype;
assign optype = instr[OPTYPE_W-1:0];

// break off all of the parts

logic [2:0] fn3;
logic fn1;
assign fn3 = instr[INSTR_W -1:INSTR_W -3];
assign fn1 = instr[INSTR_W -1];

logic [REG_ADDR_W -1:0] tempRd;
assign tempRd = instr[RD_END -1: OPTYPE_W];
logic [REG_ADDR_W -1:0] tempRs1;
assign tempRs1 = instr[RS1_END -1: RD_END];
logic [REG_ADDR_W -1:0] tempRs2;
assign tempRs2 = instr[RS2_END -1: RS1_END];

// breaking off the immediate

logic [IMM_W -1:0] Iimm; //, Simm, Bimm;
logic [UIMM_W -1:0] Aimm; // Uimm, JALimm, Aimm;
logic [VALUE_W -1:0] Pimm;

logic [VALUE_W -1:0] IimmFull;

assign Iimm = instr[INSTR_W -4:RS1_END];
// if fn3[2] is a 1, then it's unsigned, otherwise, sign extend
assign IimmFull = {(fn3[2] | ~Iimm[IMM_W-1])? 11'b0 : 11'h7ff, Iimm};
assign Aimm = {instr[VALUE_W -2: RS1_END], instr[RD_END -1: OPTYPE_W]};
assign Pimm = instr[INSTR_W -1: OPTYPE_W];

// set the control signals

assign PrintValue = (optype == 3'b000) | (optype == 3'b111);

always_comb begin
    case (optype)
        // R-type: Register
        3'b001: begin
            RegWrite = 1;
            rd = tempRd;
            rs1 = tempRs1;
            rs2 = tempRs2;
            imm = 0;
            alu_op = e_ALU_add;
        // I-type: Immediate
        end 3'b010: begin
            RegWrite = 1;
            rd = tempRd;
            rs1 = tempRs1;
            rs2 = 0;
            imm = IimmFull;
            alu_op = e_ALU_add;
        // S-type: Store
        end 3'b011: begin
            RegWrite = 0;
            rd = 0;
            rs1 = tempRs1;
            rs2 = tempRs2;
            imm = 0;
            alu_op = e_ALU_noop;
        // B-type: Branch
        end 3'b100: begin
            RegWrite = 0;
            rd = 0;
            rs1 = tempRs1;
            rs2 = tempRs2;
            imm = 0;
            alu_op = e_ALU_noop;
        // U-type: Upper imm
        end 3'b101: begin
            RegWrite = 1;
            rd = tempRd;
            rs1 = 0;
            rs2 = 0;
            imm = 0;
            alu_op = e_ALU_add;
        // J-type: Jump
        end 3'b110: begin
            RegWrite = 1;
            rd = tempRd;
            rs1 = 0;
            rs2 = 0;
            imm = 0;
            alu_op = e_ALU_noop;
        // A-type: Accept
        end 3'b111: begin
            RegWrite = 0;
            rd = 0;
            rs1 = tempRs1;
            rs2 = 0;
            imm = 0;
            alu_op = e_ALU_add;
        // P-type: Perform
        end 3'b000: begin
            RegWrite = 0;
            rd = 0;
            rs1 = 0;
            rs2 = 0;
            imm = Pimm;
            alu_op = e_ALU_add;
        // not implemented yet, or blank
        end default: begin
            RegWrite = 0;
            rd = 0;
            rs1 = 0;
            rs2 = 0;
            imm = 0;
        end
    endcase
end

endmodule