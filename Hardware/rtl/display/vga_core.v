module vga_core
(
	input clk,
	output hsync,
	output vsync,
	output video_active,
	output [9:0] pixel_x,
	output [9:0] pixel_y
);

// Visible Width (640/1) --- Front Porch (16/1) --- Sync Pulse (96/0) --- Back Porch (48/1) >>> Total Line = 800
// Visible Height (480/1) --- Front Porch (10/1) --- Sync Pulse (2/0) --- Back Porch (33/1) >>> Total Frame = 525
// Refresh Rate 60 Hz @ 25.175MHz

localparam H_D 			= 640; 	//Horizontal Display
localparam H_FP			= 16;		//Horizontal Front Porch
localparam H_SP			= 96;		//Horizontal Sync Pulse
localparam H_BP			= 48;		//Horizontal Back Porch 
localparam H_Total		= H_D + H_FP + H_SP + H_BP;

localparam V_D 			= 480; 	//Vertical Display
localparam V_FP			= 10;		//Vertical Front Porch
localparam V_SP			= 2;		//Vertical Sync Pulse
localparam V_BP			= 33;		//Vertical Back Porch 
localparam V_Total		= V_D + V_FP + V_SP + V_BP;


reg [9:0] CounterX;
reg [9:0] CounterY;


wire CounterXmaxed = (CounterX == H_Total-1);
wire CounterYmaxed = (CounterY == V_Total-1);
	
	always @(posedge clk) begin
	
		if (CounterXmaxed) begin
			CounterX <= 10'd0;
			
			if(CounterYmaxed)
				CounterY <= 10'd0;
				
			else
				CounterY <= CounterY + 10'd1;
		end
		
		
		else
			CounterX <= CounterX + 10'd1;
		
	end
	
	
	assign hsync = (CounterX <= (H_D + H_FP) || ((H_D + H_FP + H_SP) <= CounterX));   // active for 640 clocks
	assign vsync = (CounterY <= (V_D + V_FP) || ((V_D + V_FP + V_SP) <= CounterY));   // active for 480 clocks
	assign video_active = (80 <= CounterX && CounterX < 560) && (CounterY < V_D);
	assign pixel_x = CounterX;
	assign pixel_y = CounterY;
	

endmodule
