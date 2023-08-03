module write_mux
(
	input [2:0] select,
	input [7:0] alu,
	input [7:0] result,
	input [7:0] pcl,
	input [7:0] pch,
	input [7:0] flags,
	output reg [7:0] data_write
);

always @(*) begin
	case (select)
		3'b000: data_write = alu;
		3'b001: data_write = result;
		3'b010: data_write = pcl;
		3'b011: data_write = pch;
		3'b100: data_write = flags;
		3'b101: data_write = 8'b0;
		default: data_write = 8'b0;
	endcase
end

endmodule
