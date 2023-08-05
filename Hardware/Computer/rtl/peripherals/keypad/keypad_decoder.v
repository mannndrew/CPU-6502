module keypad_decoder
(
	input [3:0] row,
	input [3:0] col,
	output reg [7:0] value,
	output reg valid
);
always @ (row, col)
begin
	// 1 2 3 A
	// 4 5 6 B
	// 7 8 9 C
	// E 0 F D
	case ({row, col})
		8'b0001_0001: begin value = 8'h00; 	valid = 0; 	end  	// 1
		8'b0001_0010: begin value = 8'h77; 	valid = 1; 	end  	// 2
		8'b0001_0100: begin value = 8'h00; 	valid = 0; 	end  	// 3
		8'b0001_1000: begin value = 8'h00; 	valid = 0; 	end  	// A
		8'b0010_0001: begin value = 8'h61; 	valid = 1; 	end  	// 4
		8'b0010_0010: begin value = 8'h00; 	valid = 0; 	end  	// 5
		8'b0010_0100: begin value = 8'h64; 	valid = 1; 	end  	// 6
		8'b0010_1000: begin value = 8'h00; 	valid = 0; 	end  	// B
		8'b0100_0001: begin value = 8'h00; 	valid = 0; 	end  	// 7
		8'b0100_0010: begin value = 8'h73; 	valid = 1; 	end  	// 8
		8'b0100_0100: begin value = 8'h00; 	valid = 0; 	end  	// 9
		8'b0100_1000: begin value = 8'h00; 	valid = 0; 	end  	// C
		8'b1000_0001: begin value = 8'h00; 	valid = 0; 	end  	// E
		8'b1000_0010: begin value = 8'h00; 	valid = 0; 	end  	// 0
		8'b1000_0100: begin value = 8'h00; 	valid = 0; 	end  	// F
		8'b1000_1000: begin value = 8'h00; 	valid = 0; 	end  	// D
		default: begin value = 8'h00; valid = 0; end
	endcase
end

endmodule
