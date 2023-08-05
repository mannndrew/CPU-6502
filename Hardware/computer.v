module computer
(
	input clk,
	input rst,
	input switch_on,
	// input w, a, s, d,		// Keyboard Switches		- Option 1
	input [3:0] row,			// Keypad Buttons			- Option 2
	output [3:0] col,			// Keypad Buttons			- Option 2
	output [3:0] red,
	output [3:0] green,
	output [3:0] blue,
	output hsync,
	output vsync
);


wire clk_slow;

// CPU
wire cpu_read_write;
wire [7:0] cpu_data;
wire [7:0] cpu_data_read;
wire [7:0] cpu_data_write;
wire [15:0] cpu_address;

// Display
wire [7:0] display_data;
wire [15:0] display_address;

// Peripheralsa
wire [7:0] random;
wire [7:0] key;

clock_div #(.WIDTH(32), .DIV(2500)) inst // Defaults to 20000 Hz
(
	.clk(clk), 
	.reset(~switch_on),
	.clk_out(clk_slow)
);

cpu inst1
(
	.clk(clk_slow),
	.rst(~rst),
	.data_read(cpu_data_read),
	.data_write(cpu_data_write),
	.read_write(cpu_read_write),
	.address(cpu_address)
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
	.q_a(cpu_data),
	.q_b(display_data)
);

random_gen inst3
(
    .clk(~clk_slow),
    .out(random)
);

//keyboard inst4
//(
//	.clk(~clk_slow),
//	.w(w),
//	.a(a),
//	.s(s),
//	.d(d),
//	.last_key(key)
//);

keypad inst4
(
	.clk(clk),
	.row(row),
	.col(col),
	.key(key)
);

cpu_mux inst5
(
	.address(cpu_address),
	.memory(cpu_data),
	.random(random),
	.key(key),
	.out(cpu_data_read)
);

display_driver inst6
(
	.clk(clk),
	.color_data(display_data),
	.color_address(display_address),
	.red(red),
	.green(green),
	.blue(blue),
	.hsync(hsync),
	.vsync(vsync)
);

endmodule
