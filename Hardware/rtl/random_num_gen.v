module random_num_gen
(
    input clk,     // System clock
    output [7:0] out
);

// Define an 8-bit LFSR with taps at positions 8 and 6
reg [7:0] lfsr_reg = 8'b00000001;

always @(posedge clk) begin 
	// Update the LFSR based on its taps
	lfsr_reg[0] <= lfsr_reg[7] ^ lfsr_reg[5]; // XOR feedback
	lfsr_reg[7:1] <= lfsr_reg[6:0];
end

// Assign the output to the LSB of the LFSR
assign out = lfsr_reg;

endmodule





