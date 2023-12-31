module arithmetic_mux
(
	input [2:0] select,
	input [7:0] a,
	input [7:0] f,
	input [7:0] m,
	input [7:0] sp,
	input [7:0] x,
	input [7:0] y,
	output reg [7:0] alu_a
);

always @(*)
begin
	case (select)
		3'b000: alu_a <= a;
		3'b001: alu_a <= f;
		3'b010: alu_a <= m;
		3'b011: alu_a <= sp;
		3'b100: alu_a <= x;
		3'b101: alu_a <= y;
		3'b110: alu_a <= 8'b0;
		
		default alu_a <= 8'b0;
	endcase
end

endmodule
