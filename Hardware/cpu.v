module cpu
(
	input [8:0] sw,
	input button,
	output [7:0] led
);

ram ram_inst
(
	.address(16'h0000),
	.clock(button),
	.data(sw[7:0]),
	.wren(sw[8]),
	.q(led)
);

endmodule
