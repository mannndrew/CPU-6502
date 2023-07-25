module address_mux
(
	input [2:0] address_select,
	input [7:0] pcl,
	input [7:0] pch,
	input [7:0] dirl,
	input [7:0] dirh,
	input [7:0] indirl,
	input [7:0] indirh,
	output reg [15:0] address
);

wire [7:0] indirl_plus;
assign indirl_plus = indirl + 1'b1;

always @(*) begin
	case (address_select)
		3'b000: address = {pch, pcl};
		3'b001: address = {8'h00, dirl};
		3'b010: address = {dirh, dirl};
		3'b011: address = {8'h00, indirl};
		3'b100: address = {8'h00, indirl_plus};
		default: address = 16'h0;
	endcase
end

endmodule
