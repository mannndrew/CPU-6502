module arithmetic_mux
(
	input [1:0] select,
	input [7:0] a,
	input [7:0] x,
	input [7:0] y,
	output reg [7:0] alu_a
);

always @(select, a, x, y)
begin
	case (select)
		2'b00: alu_a <= a;
		2'b01: alu_a <= x;
		2'b10: alu_a <= y;
		default alu_a <= 8'b0;
	endcase
end

endmodule
