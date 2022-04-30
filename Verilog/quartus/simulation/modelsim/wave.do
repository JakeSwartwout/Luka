onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -divider Inputs
add wave -noupdate -label base_clock /Simulator/base_clock
add wave -noupdate -label restart_n /Simulator/restart_n
add wave -noupdate -divider Internals
add wave -noupdate -label r_if_pc /Simulator/processor/r_if_pc
add wave -noupdate -label r_id_instr /Simulator/processor/r_id_instr
add wave -noupdate -label s_id_rs1 /Simulator/processor/s_id_rs1
add wave -noupdate -label s_id_rs2 /Simulator/processor/s_id_rs2
add wave -noupdate -label r_ex_read1 /Simulator/processor/r_ex_read1
add wave -noupdate -label r_ex_read2 /Simulator/processor/r_ex_read2
add wave -noupdate -label r_me_rd /Simulator/processor/r_me_rd
add wave -noupdate -label r_me_aluout /Simulator/processor/r_me_aluout
add wave -noupdate -divider Outputs
add wave -noupdate -childformat {{{/Simulator/dispValues[5]} -radix unsigned} {{/Simulator/dispValues[4]} -radix unsigned} {{/Simulator/dispValues[3]} -radix unsigned} {{/Simulator/dispValues[2]} -radix unsigned} {{/Simulator/dispValues[1]} -radix unsigned} {{/Simulator/dispValues[0]} -radix unsigned}} -expand -subitemconfig {{/Simulator/dispValues[5]} {-height 15 -radix unsigned} {/Simulator/dispValues[4]} {-height 15 -radix unsigned} {/Simulator/dispValues[3]} {-height 15 -radix unsigned} {/Simulator/dispValues[2]} {-height 15 -radix unsigned} {/Simulator/dispValues[1]} {-height 15 -radix unsigned} {/Simulator/dispValues[0]} {-height 15 -radix unsigned}} /Simulator/dispValues
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {2916 ps} 0}
quietly wave cursor active 1
configure wave -namecolwidth 150
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {0 ps} {84824 ps}
