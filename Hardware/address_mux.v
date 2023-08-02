module address_mux
(
	input [3:0] address_select,
	input [7:0] pcl,
	input [7:0] pch,
	input [7:0] sp,
	input [7:0] dirl,
	input [7:0] dirh,
	input [7:0] indirl,
	input [7:0] indirh,
	output reg [15:0] address
);

wire [7:0] indirl_plus;
wire [15:0] indir_plus;
assign indirl_plus = indirl + 1'b1;
assign indir_plus = {indirh, indirl} + 1'b1;

always @(*) begin
	case (address_select)
		4'b0000: address = {pch, pcl};
		4'b0001: address = {8'h00, dirl};
		4'b0010: address = {dirh, dirl};
		4'b0011: address = {8'h00, indirl};
		4'b0100: address = {8'h00, indirl_plus};
		4'b0101: address = {indirh, indirl};
		4'b0110: address = {indir_plus};
		4'b0111: address = {8'h01, sp};
		4'b1000: address = {16'hfffe};
		4'b1001: address = {16'hffff};
		4'b1010: address = {16'hfffc};
		4'b1011: address = {16'hfffd};
		default: address = {pch, pcl};
	endcase
end

endmodule
