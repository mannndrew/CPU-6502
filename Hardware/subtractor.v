module subtractor #(parameter N=8)
(
	input [N-1:0] a,
	input [N-1:0] b,
	input cin,
	output [N-1:0] result,
	output [7:0] flags
);

wire [N-1:0] sum;
wire [N-1:0] carry;
fulladder Sini 		(.a(a[0]), .b(~b[0]), .cin(cin), .sum(sum[0]), .cout(carry[0]));
fulladder S[N-1:1] 	(.a(a[N-1:1]), .b(~b[N-1:1]), .cin(carry[N-2:0]), .sum(sum[N-1:1]), .cout(carry[N-1:1]));
assign result = sum;
assign flags = {sum[7], (carry[7] ^ carry[6]), 4'b0000, ~(|sum), carry[7]};
endmodule





module fulladder
(
	input a,
	input b,
	input cin,
	output sum,
	output cout
);

assign sum = (a ^ b) ^ cin;
assign cout = ((a ^ b) & cin) | (a & b);
endmodule

