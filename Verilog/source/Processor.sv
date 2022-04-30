`ifndef imports
    `include "./Helpers/clockDivider.sv"      // for reducing our clock speed
    `include "./Helpers/registerFile.sv"
    `include "./Specs/specs.vh"
    `include "./Specs/SDRAM_interface.sv"
    `include "./Specs/enums.vh"
    `include "./Stages/stg_1_IF.sv"
    `include "./Stages/stg_2_ID.sv"
    `include "./Stages/stg_3_EX.sv"
    `include "./Stages/stg_4_ME.sv"
    `include "./Stages/stg_5_WB.sv"
`endif


// ---  MODULE DECLARATION ---

module Processor(
    input 		          		CLOCK_50,
    input 		     [3:0]		KEY,
    output		     [9:0]		LEDR,
    // 7 segment display
    output		     [6:0]		HEX0,
    output		     [6:0]		HEX1,
    output		     [6:0]		HEX2,
    output		     [6:0]		HEX3,
    output		     [6:0]		HEX4,
    output		     [6:0]		HEX5,
    // SDRAM access
    output		    [12:0]		DRAM_ADDR,
    output		     [1:0]		DRAM_BA,
    output		          		DRAM_CAS_N,
    output		          		DRAM_CKE,
    output		          		DRAM_CLK,
    output		          		DRAM_CS_N,
    inout 		    [15:0]		DRAM_DQ,
    output		          		DRAM_LDQM,
    output		          		DRAM_RAS_N,
    output		          		DRAM_UDQM,
    output		          		DRAM_WE_N
);



// ---  Reset setup ---

logic reset_n;
assign reset_n = KEY[0];



// ---  Clock setup ---

logic sys_clock;

`ifdef SIMULATION
    clockDivider #( .half_divide_by (1) ) clk_div(
        .clock_in       (CLOCK_50),
        .reset_n,
        .clock_out      (sys_clock)
);
`else
    // 50 MHz = 50000000 Hz
    // half divisor of 50000000 = 1/2 Hz output, cycle once every 2 seconds
    clockDivider #( .half_divide_by (50_000_000) ) clk_div(
        .clock_in       (CLOCK_50),
        .reset_n,
        .clock_out      (sys_clock)
);
`endif



// ---  Bundling the SDRAM signals ---
SDRAM_interface sdram();
    assign DRAM_CLK                 = sdram.sdram_clk;
    assign DRAM_ADDR                = sdram.addr;
    assign DRAM_BA                  = sdram.ba;
    assign DRAM_CAS_N               = sdram.cas_n;
    assign DRAM_CKE                 = sdram.cke;
    assign DRAM_CS_N                = sdram.cs_n;
    assign DRAM_DQ                  = sdram.dq;
    assign {DRAM_UDQM, DRAM_LDQM}   = sdram.dqm;
    assign DRAM_RAS_N               = sdram.ras_n;
    assign DRAM_WE_N                = sdram.we_n;



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
logic r_wb_RegWrite;

// WB stage
logic [VALUE_W-1:0] s_wb_wbdat;



// --- Stage 1 - Instruction Fetch ---

stg_1_IF Stage1(
    .CLOCK_50, .sys_clock, .reset_n,

    .r_if_pc,
    .r_id_instr,
    .LEDR,
    .sdram
);



// --- Stage 2 - Instruction Decode ---

stg_2_ID Stage2(
    .sys_clock, .reset_n,
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
    .sys_clock, .reset_n,
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
    .sys_clock, .reset_n,
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
    .sys_clock, .reset_n,
    .r_wb_aluout,
    .r_wb_rd,
    .r_wb_RegWrite,

    .s_wb_wbdat
);


// --- Connect both ID and WB into the regsiter file

// register fetch
registerFile rf(
    .clock(sys_clock), .reset_n,
    .rs1(s_id_rs1),
    .rs2(s_id_rs2),
    .rd(r_wb_rd),
    .writeData(s_wb_wbdat),
    .RegWrite(r_wb_RegWrite),
    .read1(r_ex_read1),
    .read2(r_ex_read2)
);

endmodule