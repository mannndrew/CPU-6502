module keyboard
(
	input clk,
	input w, a, s, d,
	output reg [7:0] last_key
);

always @(posedge clk) begin
	if (w == 1'b1)
		last_key <= 8'h77;
	else if (a == 1'b1)
		last_key <= 8'h61;
	else if (s == 1'b1)
		last_key <= 8'h73;
	else if (d == 1'b1)
		last_key <= 8'h64;
	else
		last_key <= 8'h0;
end

endmodule
