module clock_div #(parameter WIDTH = 32, parameter DIV = 50) // Defaults to 1MHz
(
	input clk, reset,
	output clk_out
);

reg [WIDTH-1:0] r_reg;
wire [WIDTH-1:0] r_nxt;
reg clk_track;

always @(posedge clk or posedge reset)
begin
	if (reset)
	begin
		r_reg <= 0;
		clk_track <= 1'b0;
	end
	
	else if (r_nxt == DIV)
	begin
		r_reg <= 0;
		clk_track <= ~clk_track;
	end
	
	else 
		r_reg <= r_nxt;
end

assign r_nxt = r_reg+1;   
assign clk_out = clk_track;

endmodule
