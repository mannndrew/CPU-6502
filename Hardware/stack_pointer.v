module stack_pointer
(
	input clk,
	input [1:0] sel,
	output reg [7:0] sp
);

reg [7:0] counter = 8'hff;

always @(posedge clk) begin
	case (sel)
		2'b00: counter <= counter;
		2'b01: counter <= (counter == 8'hff) ? counter : counter + 1'b1;
		2'b10: counter <= (counter == 8'h00) ? counter : counter - 1'b1;
	endcase
end

always @(counter, sel) begin
	if (sel == 2'b01)
		sp <= counter + 1'b1;
	else
		sp <= counter;
end

endmodule
