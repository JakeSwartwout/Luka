transcript on
if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vlog -vlog01compat -work work +incdir+C:/Users/Jake/Documents/CU\ Junior\ Year/Luka/Verilog/quartus {C:/Users/Jake/Documents/CU Junior Year/Luka/Verilog/quartus/RegisterRam.v}
vlib SDRAM_Connection
vmap SDRAM_Connection SDRAM_Connection
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/sdram_connection.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/sdram_connection_jtag_master.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/sdram_connection_mm_interconnect_0.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/sdram_connection_pll_sdram_clk.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/sdram_connection_sdram_controller.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_avalon_packets_to_master.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_avalon_sc_fifo.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_avalon_st_bytes_to_packets.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_avalon_st_clock_crosser.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_avalon_st_idle_inserter.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_avalon_st_idle_remover.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_avalon_st_jtag_interface.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_avalon_st_packets_to_bytes.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_avalon_st_pipeline_base.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_jtag_dc_streaming.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_jtag_sld_node.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_jtag_streaming.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_reset_controller.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_reset_synchronizer.v}
vlog -vlog01compat -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_std_synchronizer_nocut.v}
vlog -sv -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/sdram_connection_jtag_master_b2p_adapter.sv}
vlog -sv -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/sdram_connection_jtag_master_p2b_adapter.sv}
vlog -sv -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/sdram_connection_jtag_master_timing_adt.sv}
vlog -sv -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_merlin_master_translator.sv}
vlog -sv -work SDRAM_Connection +incdir+c:/users/jake/documents/cu\ junior\ year/luka/verilog/quartus/db/ip/sdram_connection/submodules {c:/users/jake/documents/cu junior year/luka/verilog/quartus/db/ip/sdram_connection/submodules/altera_merlin_slave_translator.sv}
vlog -sv -work work +incdir+C:/Users/Jake/Documents/CU\ Junior\ Year/Luka/Verilog/source {C:/Users/Jake/Documents/CU Junior Year/Luka/Verilog/source/Processor.sv}

vlog -sv -work work +incdir+C:/Users/Jake/Documents/CU\ Junior\ Year/Luka/Verilog/quartus/../source {C:/Users/Jake/Documents/CU Junior Year/Luka/Verilog/quartus/../source/Simulator.sv}

vsim -t 1ps -L altera_ver -L lpm_ver -L sgate_ver -L altera_mf_ver -L altera_lnsim_ver -L cyclonev_ver -L cyclonev_hssi_ver -L cyclonev_pcie_hip_ver -L rtl_work -L work -L SDRAM_Connection -voptargs="+acc"  Simulator

do wave.do
view structure
view signals
run -all
