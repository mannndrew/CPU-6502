module keypad
(
	input clk,
	input [3:0] row,
	output [3:0] col,
	output [7:0] key
);

wire slow_clock;
wire sense;
wire valid;
wire valid_press;

wire [7:0] value;

assign valid_press = valid && sense;

keypad_div #(.DIV(100000)) L0 // 50MHz to 500Hz
(
	.clk(clk),
	.clk_out(slow_clock)
);

keypad_fsm L1
(
	.clk(slow_clock),
	.row(row),
	.col(col),
	.sense(sense)
);

keypad_decoder L2
(
	.row(row),
	.col(col),
	.value(value),
	.valid(valid)
);

keypad_reg L3
(
	.clk(valid_press),
	.d(value),
	.q(key)
);



endmodule
