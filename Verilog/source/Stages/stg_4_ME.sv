`ifndef imports
    `include "../Specs/specs.vh"
    `include "../Helpers/valueToDisplay.sv"    // for displaying our values
`endif

module stg_4_ME(
    input sys_clock, reset_n,
    input [REG_ADDR_W-1:0] r_me_rd,
    input [VALUE_W-1:0] r_me_aluout,
    input r_me_aluzero,
    input r_me_RegWrite,
    input r_me_PrintValue,

    output reg [VALUE_W-1:0] r_wb_aluout,
    output reg [REG_ADDR_W-1:0] r_wb_rd,
    output reg r_wb_RegWrite,
    output wire [6:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5
);


// Branching logic

//


// ---  PRINTING ---

// sending it to the hex display
valueToDisplay printer( .value(r_me_aluout),
                        .print_it(r_me_PrintValue),
                        .HEX0, .HEX1, .HEX2, .HEX3, .HEX4, .HEX5
                        );



// ---  REGISTER CLOCKING ---

always_ff @ (posedge sys_clock, negedge reset_n) begin
    if (~reset_n) begin
        r_wb_aluout <= 0;
        r_wb_rd <= 0;
        r_wb_RegWrite <= 0;
    end else begin
        r_wb_aluout <= r_me_aluout;
        r_wb_rd <= r_me_rd;
        r_wb_RegWrite <= r_me_RegWrite;
    end 
end

endmodule