	component SDRAM_Connection is
		port (
			clk_clk                     : in    std_logic                     := 'X';             -- clk
			pll_sdram_clk_locked_export : out   std_logic;                                        -- export
			pll_sdram_clk_shifted_clk   : out   std_logic;                                        -- clk
			reset_reset_n               : in    std_logic                     := 'X';             -- reset_n
			sdram_controller_wire_addr  : out   std_logic_vector(12 downto 0);                    -- addr
			sdram_controller_wire_ba    : out   std_logic_vector(1 downto 0);                     -- ba
			sdram_controller_wire_cas_n : out   std_logic;                                        -- cas_n
			sdram_controller_wire_cke   : out   std_logic;                                        -- cke
			sdram_controller_wire_cs_n  : out   std_logic;                                        -- cs_n
			sdram_controller_wire_dq    : inout std_logic_vector(31 downto 0) := (others => 'X'); -- dq
			sdram_controller_wire_dqm   : out   std_logic_vector(3 downto 0);                     -- dqm
			sdram_controller_wire_ras_n : out   std_logic;                                        -- ras_n
			sdram_controller_wire_we_n  : out   std_logic                                         -- we_n
		);
	end component SDRAM_Connection;

	u0 : component SDRAM_Connection
		port map (
			clk_clk                     => CONNECTED_TO_clk_clk,                     --                   clk.clk
			pll_sdram_clk_locked_export => CONNECTED_TO_pll_sdram_clk_locked_export, --  pll_sdram_clk_locked.export
			pll_sdram_clk_shifted_clk   => CONNECTED_TO_pll_sdram_clk_shifted_clk,   -- pll_sdram_clk_shifted.clk
			reset_reset_n               => CONNECTED_TO_reset_reset_n,               --                 reset.reset_n
			sdram_controller_wire_addr  => CONNECTED_TO_sdram_controller_wire_addr,  -- sdram_controller_wire.addr
			sdram_controller_wire_ba    => CONNECTED_TO_sdram_controller_wire_ba,    --                      .ba
			sdram_controller_wire_cas_n => CONNECTED_TO_sdram_controller_wire_cas_n, --                      .cas_n
			sdram_controller_wire_cke   => CONNECTED_TO_sdram_controller_wire_cke,   --                      .cke
			sdram_controller_wire_cs_n  => CONNECTED_TO_sdram_controller_wire_cs_n,  --                      .cs_n
			sdram_controller_wire_dq    => CONNECTED_TO_sdram_controller_wire_dq,    --                      .dq
			sdram_controller_wire_dqm   => CONNECTED_TO_sdram_controller_wire_dqm,   --                      .dqm
			sdram_controller_wire_ras_n => CONNECTED_TO_sdram_controller_wire_ras_n, --                      .ras_n
			sdram_controller_wire_we_n  => CONNECTED_TO_sdram_controller_wire_we_n   --                      .we_n
		);

