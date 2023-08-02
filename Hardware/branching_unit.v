module branching_unit
(
	input clk,
	input [7:0] data_read,
	input [7:0] pcl,
	input [7:0] pch,
	output [7:0] pcl_branch,
	output [7:0] pch_branch
);

reg [7:0] offset;

always @(posedge clk) begin
	offset <= data_read;
end



wire [8:0] result = (pcl + offset);
wire carry = result[8] ^ offset[7];
assign pcl_branch = (pcl + offset);
assign pch_branch = (offset[7] == 1'b0) ? pch + carry : pch - carry; 



endmodule
