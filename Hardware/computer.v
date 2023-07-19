module computer
(
	input clk
);

wire read_write;
wire [7:0] data_read;
wire [7:0] data_write;
wire [15:0] address;

cpu inst1
(
	.clk(clk),
	.data_read(data_read),
	.data_write(data_write),
	.read_write(read_write),
	.address(address)
);

ram inst2
(
	.address(address),
	.clock(clk),
	.data(data_write),
	.wren(read_write),
	.q(data_read)
);

endmodule
