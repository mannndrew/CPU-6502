module arithmetic_unit
(
	input [1:0] alu_opcode,
	input [7:0] alu_a,
	input [7:0] alu_b,
	input [7:0] flags_in,
	output reg [7:0] alu_out,
	output reg [7:0] flags_out,
	output reg [7:0] flags_ena
);

// Flags In
wire carry_in = flags_in[0];

// ADC
wire [7:0] adc;
wire adc_n, adc_v, adc_z, adc_c;
assign {adc_c, adc} = alu_a + alu_b + carry_in;
assign adc_n = adc[7];
assign adc_v = (~alu_a[7] & ~alu_b[7] & adc[7]) || (alu_a[7] & alu_b[7] & ~adc[7]);
assign adc_z = ~(|adc);

always @(*)
begin
	case (alu_opcode)
		2'b00: begin 
			alu_out <= adc; 
			flags_out <= {adc_n, adc_v, 4'b0000, adc_z, adc_c}; 
			flags_ena <= 8'b11000011; 
		end
		
		default: begin 
			alu_out <= 8'b0; 
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
		end
	endcase
end

endmodule