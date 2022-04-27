interface SDRAM_interface;
    logic        sdram_clk
    logic [12:0] addr,
    logic [1:0]  ba,
    logic        cas_n,
    logic        cke,
    logic        cs_n,
    wire  [31:0] dq,
    logic [3:0]  dqm,
    logic        ras_n,
    logic        we_n
	
// add directionality to the ports
modport source(
    output sdram_clk, addr, ba, cas_n, cke, cs_n, dqm, ras_n, we_n,
    inout dq
);
modport receiver(
    input sdram_clk, addr, ba, cas_n, cke, cs_n, dqm, ras_n, we_n,
    inout dq
);

endinterface