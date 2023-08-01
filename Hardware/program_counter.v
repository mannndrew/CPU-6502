module program_counter
(
	input clk,
	input increment,
	input branch_load,
	input pc_load,
	input jmp_load,
	input jsr_load,
	input [7:0] branch,
	input [7:0] pc_addr,
	input [7:0] jmp_addr,
	input [7:0] jsr_addr,
	output carry,
	output [7:0] pc
);

reg [7:0] counter;

always @(posedge clk) begin

	if (pc_load == 1'b1) counter <= pc_addr;
	else if (jmp_load == 1'b1) counter <= jmp_addr;
	else if (jsr_load == 1'b1) counter <= jsr_addr;
	else if (branch_load == 1'b1) counter <= branch;
	else counter <= counter + increment;
	
end

assign pc = counter + increment;
assign carry = (counter == 8'hff && increment == 1'b1) ? 1'b1 : 1'b0;

endmodule

