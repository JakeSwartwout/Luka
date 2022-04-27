`ifndef OPCODES

parameter OPTYPE_W = 3; // how many bits to describe the type of instruction
parameter OPCODE_add = 001;
parameter FN3_add = 100;
parameter OPCODE_sub = 001;
parameter FN3_sub = 101;
parameter OPCODE_addi = 010;
parameter FN3_addi = 000;
parameter OPCODE_subi = 010;
parameter FN3_subi = 001;
parameter OPCODE_prnt = 111;
parameter FN3_prnt = 0;
parameter OPCODE_prnti = 000;

`define OPCODES
`endif
