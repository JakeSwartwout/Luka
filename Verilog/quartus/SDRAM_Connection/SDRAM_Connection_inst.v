	SDRAM_Connection u0 (
		.clk_clk                     (<connected-to-clk_clk>),                     //                   clk.clk
		.pll_sdram_clk_locked_export (<connected-to-pll_sdram_clk_locked_export>), //  pll_sdram_clk_locked.export
		.pll_sdram_clk_shifted_clk   (<connected-to-pll_sdram_clk_shifted_clk>),   // pll_sdram_clk_shifted.clk
		.reset_reset_n               (<connected-to-reset_reset_n>),               //                 reset.reset_n
		.sdram_controller_wire_addr  (<connected-to-sdram_controller_wire_addr>),  // sdram_controller_wire.addr
		.sdram_controller_wire_ba    (<connected-to-sdram_controller_wire_ba>),    //                      .ba
		.sdram_controller_wire_cas_n (<connected-to-sdram_controller_wire_cas_n>), //                      .cas_n
		.sdram_controller_wire_cke   (<connected-to-sdram_controller_wire_cke>),   //                      .cke
		.sdram_controller_wire_cs_n  (<connected-to-sdram_controller_wire_cs_n>),  //                      .cs_n
		.sdram_controller_wire_dq    (<connected-to-sdram_controller_wire_dq>),    //                      .dq
		.sdram_controller_wire_dqm   (<connected-to-sdram_controller_wire_dqm>),   //                      .dqm
		.sdram_controller_wire_ras_n (<connected-to-sdram_controller_wire_ras_n>), //                      .ras_n
		.sdram_controller_wire_we_n  (<connected-to-sdram_controller_wire_we_n>)   //                      .we_n
	);

