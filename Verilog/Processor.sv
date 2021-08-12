`ifndef imports
  `include "./Helpers/clockDivider.sv"      // for reducing our clock speed
  `include "./Specs/specs.vh"
  `include "./Specs/enums.vh"
  `include "./Stages/stg_1_IF.sv"
  `include "./Stages/stg_2_ID.sv"
  `include "./Stages/stg_3_EX.sv"
  `include "./Stages/stg_4_ME.sv"
  `include "./Stages/stg_5_WB.sv"
`endif


// ---  MODULE DECLARATION ---

module Processor(ADC_CLK_10, KEY, SW, HEX0, HEX1, HEX2, HEX3, HEX4, HEX5, LEDR);



// ---  INPUTS & OUTPUTS ---

parameter CLOCK_DIVISOR = 1_000_000;

// Specs are for the DE-10 Lite board
input ADC_CLK_10; // clock
input [1:0] KEY; // 2 buttons, KEY[0] is the reset button
input [9:0] SW; // 10 possible switches
output [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5; // 6 hex displays
output [9:0] LEDR; // 10 LEDs
// not all of these are needed, but they are available if they are


// ---  CLOCK SETUP ---

logic clock;
logic reset;
assign reset = KEY[0];

clockDivider #( .half_divide_by(CLOCK_DIVISOR) ) clockDivider 
              ( .clock_in( ADC_CLK_10 ),
                .reset_n( reset ),   // KEY and Reset are both active low
                .clock_out( clock )
              );



// ---  SIGNALS ---

// IF stage
logic [INSTR_ADDR_W-1:0] r_if_pc;
logic [INSTR_W-1:0] r_id_instr;

// ID stage
// logic [OPTYPE_W-1:0] r_ex_opc;
logic [ALU_OP_W-1:0] r_ex_aluop;
logic [REG_ADDR_W-1:0] s_id_rs1, s_id_rs2, r_ex_rd;
logic [VALUE_W-1:0] r_ex_imm;
logic [VALUE_W-1:0] r_ex_read1, r_ex_read2;
logic r_ex_RegWrite, r_ex_PrintValue;

// EX stage
logic [REG_ADDR_W-1:0] r_me_rd;
logic [VALUE_W-1:0] r_me_aluout;
logic r_me_aluzero;
logic r_me_RegWrite;
logic r_me_PrintValue;

// ME stage
logic [REG_ADDR_W-1:0] r_wb_rd;
logic [VALUE_W-1:0] r_wb_aluout;

// WB stage
logic [VALUE_W-1:0] s_wb_wbdat;



// --- Stage 1 - Instruction Fetch ---

stg_1_IF Stage1(
  .clock, .reset,

  .r_if_pc,
  .r_id_instr,
  .LEDR
  );



// --- Stage 2 - Instruction Decode ---

stg_2_ID Stage2(
  .clock, .reset,
  .r_id_instr,

  .r_ex_aluop,
  .s_id_rs1,
  .s_id_rs2,
  .r_ex_rd,
  .r_ex_imm,
  .r_ex_RegWrite,
  .r_ex_PrintValue
  );



// --- Stage 3 - Execute ---

stg_3_EX Stage3(
  .clock, .reset,
  .r_ex_aluop,
  .r_ex_read1,
  .r_ex_read2,
  .r_ex_rd,
  .r_ex_imm,
  .r_ex_RegWrite,
  .r_ex_PrintValue,

  .r_me_rd,
  .r_me_aluout,
  .r_me_aluzero,
  .r_me_RegWrite,
  .r_me_PrintValue
  );



// --- Stage 4 - Memory ---

stg_4_ME Stage4(
  .clock, .reset,
  .r_me_rd,
  .r_me_aluout,
  .r_me_aluzero,
  .r_me_RegWrite,
  .r_me_PrintValue,

  .r_wb_aluout,
  .r_wb_rd,
  .r_wb_RegWrite,
  .HEX0, .HEX1, .HEX2, .HEX3, .HEX4, .HEX5
  );



// --- Stage 5 - Writeback ---

stg_5_WB Stage5(
  .clock, .reset,
  .r_wb_aluout,
  .r_wb_rd,
  .r_wb_RegWrite,

  .s_wb_wbdat
  );



// --- Connect both ID and WB into the regsiter file

// register fetch
registerFile rf(
  .clock,
  .reset,
  .rs1(s_id_rs1),
  .rs2(s_id_rs2),
  .rd(r_wb_rd),
  .writeData(s_wb_wbdat),
  .RegWrite(r_wb_RegWrite),
  .read1(r_ex_read1),
  .read2(r_ex_read2)
);


endmodule