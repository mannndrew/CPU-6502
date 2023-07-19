module flag_register
(
	input clk,
	input [7:0] ena,
	input [7:0] d,
	output reg [7:0] q 
);

always @(posedge clk)
begin
	if (ena[0] == 1'b1) q[0] <= d[0]; else q[0] <= q[0];
	if (ena[1] == 1'b1) q[1] <= d[1]; else q[1] <= q[1];
	if (ena[2] == 1'b1) q[2] <= d[2]; else q[2] <= q[2];
	if (ena[3] == 1'b1) q[3] <= d[3]; else q[3] <= q[3];
	if (ena[4] == 1'b1) q[4] <= d[4]; else q[4] <= q[4];
	if (ena[5] == 1'b1) q[5] <= d[5]; else q[5] <= q[5];
	if (ena[6] == 1'b1) q[6] <= d[6]; else q[6] <= q[6];
	if (ena[7] == 1'b1) q[7] <= d[7]; else q[7] <= q[7];
end

endmodule
