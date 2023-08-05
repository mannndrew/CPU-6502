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
wire press = valid & sense;

wire [7:0] value;

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
	.clk(clk),
	.ena(press),
	.d(value),
	.q(key)
);



endmodule
