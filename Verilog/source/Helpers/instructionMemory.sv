`ifndef INSTRUCTION_MEMORY

// connects up to the SDRAM to read instructions from memory
`ifndef imports
    `include "../Specs/SDRAM_interface.sv"
`endif

module instructionMemory(
    input CLOCK_50,
    input reset_n,
    input read_addr,
    output instr_value,
    SDRAM_interface.source sdram
);


// figure out what to do with the read_addr???
// because the one out of the platform designer is generated by the SDRAM_controller
// so how do we feed ours in?


// ---  Connecting to the SDRAM controller ---

SDRAM_Connection sdram_controller (
    .clk_clk                         (CLOCK_50),                     //                   clk.clk
    .pll_sdram_clk_locked_export     (),                             //  pll_sdram_clk_locked.export
    .pll_sdram_clk_shifted_clk       (sdram.sdram_clk),              // pll_sdram_clk_shifted.clk
    .reset_reset_n                   (reset_n),                      //                 reset.reset_n
    .sdram_controller_wire_addr      (sdram.addr),                   // sdram_controller_wire.addr
    .sdram_controller_wire_ba        (sdram.ba),                     //                      .ba
    .sdram_controller_wire_cas_n     (sdram.cas_n),                  //                      .cas_n
    .sdram_controller_wire_cke       (sdram.cke),                    //                      .cke
    .sdram_controller_wire_cs_n      (sdram.cs_n),                   //                      .cs_n
    .sdram_controller_wire_dq        (sdram.dq),                     //                      .dq
    .sdram_controller_wire_dqm       (sdram.dqm),                    //                      .dqm
    .sdram_controller_wire_ras_n     (sdram.ras_n),                  //                      .ras_n
    .sdram_controller_wire_we_n      (sdram.we_n)                    //                      .we_n
);

endmodule

`define INSTRUCTION_MEMORY
`endif