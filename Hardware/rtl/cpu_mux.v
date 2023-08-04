module cpu_mux
(
	input [15:0] address,
	input [7:0] memory,
	input [7:0] random,
	input [7:0] key,
	output reg [7:0] out
);

always @(*) begin
	if (address == 16'h00fe)
		out = random;
	else if (address == 16'h00ff)
		out = key;
	else
		out = memory;
end

endmodule
