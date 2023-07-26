module arithmetic_mux
(
	input [2:0] select,
	input [7:0] a,
	input [7:0] x,
	input [7:0] y,
	input [7:0] m,
	output reg [7:0] alu_a
);

always @(*)
begin
	case (select)
		3'b000: alu_a <= a;
		3'b001: alu_a <= x;
		3'b010: alu_a <= y;
		3'b011: alu_a <= m;
		default alu_a <= 8'b0;
	endcase
end

endmodule
