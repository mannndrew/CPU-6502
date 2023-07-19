module register
(
	input clk,
	input ena,
	input [7:0] d,
	output reg [7:0] q 
);

always @(posedge clk)
begin
	if (ena == 1'b1)
		q <= d;
	else
		q <= q;
end

endmodule
