module register
(
	input clk,
	input reset,
	input ena,
	input [7:0] d,
	output reg [7:0] q 
);

always @(posedge clk) begin
	if (reset == 1'b0)
		q <= 8'b0;
		
	else begin
		if (ena == 1'b1)
			q <= d;
		else
			q <= q;
	end
		
end

endmodule
