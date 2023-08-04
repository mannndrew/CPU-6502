module display_driver
(
	input clk,
	input [7:0] color_data,
	output [15:0] color_address,
	output reg [3:0] red,
	output reg [3:0] green,
	output reg [3:0] blue,
	output hsync,
	output vsync
);

wire clk_slow;
wire video_active;
wire [2:0] color_index = color_data[2:0];
wire [9:0] pixel_x;
wire [9:0] pixel_y;

wire [31:0]sub_x;
wire [31:0]sub_y;

reg [3:0] count_x;
reg [4:0] chunk_x;
reg [3:0] count_y;
reg [4:0] chunk_y;

wire [31:0] color_address_tmp;


pll test
(
	.inclk0(clk),
	.c0(clk_slow)
);

vga_core core
(
	.clk(clk_slow),
	.hsync(hsync),
	.vsync(vsync),
	.video_active(video_active),
	.pixel_x(pixel_x),
	.pixel_y(pixel_y)
);

assign sub_x = (pixel_x - 80) / 15;
assign sub_y = (pixel_y) / 15;
assign color_address_tmp =  16'h0200 + (sub_y * 6'h20) + sub_x;
assign color_address = color_address_tmp[15:0];




always @(video_active, color_index, pixel_x, pixel_y) begin
//	if ((72 <= pixel_x && pixel_x < 80) || (560 <= pixel_x && pixel_x < 568))
//		{red, green, blue} = 12'hfff;
//		
//	else if (pixel_x == 10'd0 || pixel_x == 10'd639 || pixel_y == 10'd0 || pixel_y == 10'd479)
//		{red, green, blue} = 12'hfff;
		
	if ((pixel_x == 80 || pixel_x == 559) && (0 <= pixel_y && pixel_y < 480)) // LEFT and RIGHT
		{red, green, blue} = 12'hfff;
		
	else if ((pixel_y == 0 || pixel_y == 479) && (80 <= pixel_x && pixel_x < 560)) // TOP and BOTTOM
		{red, green, blue} = 12'hfff;
		
	else begin
		if (video_active == 0)
			{red, green, blue} = 12'h000;
	
		else begin
			case (color_index)
				3'b000: {red, green, blue} = 12'h000; // Black
				3'b001: {red, green, blue} = 12'hfff; // White
				3'b010: {red, green, blue} = 12'hf00; // Red
				3'b011: {red, green, blue} = 12'h0f0; // Green
				3'b100: {red, green, blue} = 12'h00f; // Blue
				3'b101: {red, green, blue} = 12'hff0; // Yellow
				3'b110: {red, green, blue} = 12'h0ff; // Cyan
				3'b111: {red, green, blue} = 12'hf0f; // Magenta
			endcase
		end
	end
end


endmodule
