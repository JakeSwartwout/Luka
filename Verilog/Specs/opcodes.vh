`ifndef opcodes
`define opcodes

parameter OPTYPE_W = 3; // how many bits to describe the type of instruction
parameter OPCODE_add = 001;
parameter FN3_add = 100;
parameter OPCODE_sub = 001;
parameter FN3_sub = 101;
parameter OPCODE_slt = 001;
parameter FN3_slt = 010;
parameter OPCODE_xor = 001;
parameter FN3_xor = 011;
parameter OPCODE_addi = 010;
parameter FN3_addi = 101;
parameter OPCODE_subi = 010;
parameter FN3_subi = 110;
parameter OPCODE_xori = 010;
parameter FN3_xori = 010;
parameter OPCODE_slti = 010;
parameter FN3_slti = 100;
parameter OPCODE_sltiu = 010;
parameter FN3_sltiu = 001;
parameter OPCODE_prnt = 111;
parameter FN3_prnt = 0;
parameter OPCODE_prnti = 000;

`endif
