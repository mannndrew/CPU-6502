module computer
(
	input clk,
	input rst,
	input switch,
	output [6:0] hex0,
	output [6:0] hex1,
	output [6:0] hex2,
	output [6:0] hex3,
	output [6:0] hex4,
	output [6:0] hex5,
	output [5:0] state,
	output [3:0] red,
	output [3:0] green,
	output [3:0] blue,
	output hsync,
	output vsync,
	output led
);

wire cpu_read_write;
wire [7:0] cpu_data_read;
wire [7:0] cpu_data_write;
wire [15:0] cpu_address;
wire clk_slow;

wire [7:0] display_data_read;
wire [15:0] display_address;

wire [7:0] tmp;

assign led = clk_slow;

clock_div #(.WIDTH(32), .DIV(5000000)) inst // Defaults to 10Hz
(
	.clk(clk), 
	.reset(~switch),
	.clk_out(clk_slow)
);

cpu inst1
(
	.clk(clk_slow),
	.rst(~rst),
	.data_read(cpu_data_read),
	.data_write(cpu_data_write),
	.read_write(cpu_read_write),
	.address(cpu_address),
	.state(state),
	.tmp(tmp)
);

ram inst2
(
	.address_a(cpu_address),
	.address_b(display_address),
	.clock_a(~clk_slow),
	.clock_b(~clk),
	.data_a(cpu_data_write),
	.data_b(8'b0),
	.wren_a(cpu_read_write),
	.wren_b(1'b0),
	.q_a(cpu_data_read),
	.q_b(display_data_read)
);

display_driver display
(
	.clk(clk),
	.color_data(display_data_read),
	.color_address(display_address),
	.red(red),
	.green(green),
	.blue(blue),
	.hsync(hsync),
	.vsync(vsync)
);

binary2seven inst3
(
	.bin(cpu_address[3:0]),
	.hex(hex0)
);

binary2seven inst4
(
	.bin(cpu_address[7:4]),
	.hex(hex1)
);

binary2seven inst5
(
	.bin(cpu_address[11:8]),
	.hex(hex2)
);

binary2seven inst6
(
	.bin(cpu_address[15:12]),
	.hex(hex3)
);

binary2seven inst7
(
	.bin(tmp[3:0]),
	.hex(hex4)
);

binary2seven inst8
(
	.bin(tmp[7:4]),
	.hex(hex5)
);

endmodule
