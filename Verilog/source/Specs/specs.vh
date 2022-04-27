`ifndef PARAMETERS

parameter VALUE_W = 16; // the width of a value
parameter INSTR_W = 19; // the length of an instruction
parameter NUM_REG = 16; // the number of registers
parameter REG_ADDR_W = 4; // the number of bits to address a register
parameter IMM_W = 5; // the length of an immediate
parameter UIMM_W = 11; // the length of an upper immediate
parameter NUM_INSTRS = 21; // how many instructions we have
parameter INSTR_ADDR_W = 5; // how many bits the address of the instruction is (pc length)

`define PARAMETERS
`endif
