module keypad_fsm
(
	input clk,
	input [3:0] row,
	output reg [3:0] col,
	output sense
);

wire trig = row[0] || row[1] || row[2] || row[3];
assign sense = (state == 10);

reg [3:0] state;

always @ (posedge clk)
begin
	case (state)
		0: begin col = 4'b1111; state = 1; end
		1: if (trig) begin state = 2; end
		2: begin col = 4'b0001; state = 3; end
		3: if (trig) begin state = 10; end else begin state = 4; end
		4: begin col = 4'b0010; state = 5; end
		5: if (trig) begin state = 10; end else begin state = 6; end
		6: begin col = 4'b0100; state = 7; end
		7: if (trig) begin state = 10; end else begin state = 8; end
		8: begin col = 4'b1000; state = 9; end
		9: if (trig) begin state = 10; end else begin state = 0; end
		10: begin state = 11; end
		11: if (~trig) begin state = 0; end
	endcase
end

endmodule
