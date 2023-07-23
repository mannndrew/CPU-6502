module address_mux
(
	input [1:0] address_select,
	input [7:0] pcl,
	input [7:0] pch,
	input [7:0] dirl,
	input [7:0] dirh,
	output reg [15:0] address
);

always @(*) begin
	case (address_select)
		2'b00: address = {pch, pcl};
		2'b01: address = {8'h00, dirl};
		2'b10: address = {dirh, dirl};
		default: address = 16'h0;
	endcase
end

endmodule
