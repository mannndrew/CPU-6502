module computer
(
	input clk,
	input rst,
	input switch,
	output [6:0] hex0,
	output [6:0] hex1,
	output [6:0] hex2,
	output [6:0] hex3,
	output [5:0] state,
	output led
);

wire read_write;
wire [7:0] data_read;
wire [7:0] data_write;
wire [15:0] address;
wire clk_slow;

assign led = clk_slow;

clock_div #(.WIDTH(32), .DIV(50000000)) inst // Defaults to 1MHz
(
	.clk(clk), 
	.reset(~switch),
	.clk_out(clk_slow)
);

cpu inst1
(
	.clk(clk_slow),
	.rst(~rst),
	.data_read(data_read),
	.data_write(data_write),
	.read_write(read_write),
	.address(address),
	.state(state)
);

ram inst2
(
	.address(address),
	.clock(~clk_slow),
	.data(data_write),
	.wren(read_write),
	.q(data_read)
);

binary2seven inst3
(
	.bin(address[3:0]),
	.hex(hex0)
);

binary2seven inst4
(
	.bin(address[7:4]),
	.hex(hex1)
);

binary2seven inst5
(
	.bin(address[11:8]),
	.hex(hex2)
);

binary2seven inst6
(
	.bin(address[15:12]),
	.hex(hex3)
);

endmodule
