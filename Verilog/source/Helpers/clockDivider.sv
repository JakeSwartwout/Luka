// takes an input clock signal and divides it by some parameter value (slows it down)
module clockDivider(input clock_in, reset_n, output reg clock_out);
parameter half_divide_by = 0;

logic [22:0] clock_divider;

always_ff @ (posedge clock_in, negedge reset_n)
    // if we should reset it (synchronous reset only)
    if (!reset_n)
        begin
            clock_out <= 0;
            clock_divider <= 0;
        end
    else
        // able to continue counting up
        if (clock_divider != half_divide_by - 1)
            clock_divider <= clock_divider + 1;
        // should rollover
        else
            begin
                clock_divider <= 0;
                clock_out <= !clock_out;
            end

endmodule
