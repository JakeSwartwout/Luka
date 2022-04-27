`ifndef imports
    `include "../Specs/specs.vh"
`endif

module stg_5_WB(
    input sys_clock, reset_n,
    input [VALUE_W-1:0] r_wb_aluout,
    input [REG_ADDR_W-1:0] r_wb_rd,
    input r_wb_RegWrite,

    output wire [VALUE_W-1:0] s_wb_wbdat
);


// choosing the writeback data

assign w_wb_wbdat = r_wb_aluout;

// No output registers to clock


endmodule