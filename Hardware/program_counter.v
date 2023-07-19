module program_counter
(
	input clk,
	input increment,
	output carry,
	output [7:0] pc
);

reg [7:0] counter;

always @(posedge clk)
begin
	counter <= counter + increment;
end

assign pc = counter + increment;
assign carry = (counter == 8'hff && increment == 1'b1) ? 1'b1 : 1'b0;

endmodule

