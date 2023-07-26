module arithmetic_unit
(
	input clk,
	input [1:0] alu_opcode,
	input [7:0] alu_a,
	input [7:0] alu_b,
	input [7:0] flags_in,
	output reg [7:0] alu_out,
	output reg [7:0] flags_out,
	output reg [7:0] flags_ena
);

// Temp Carry Reg
reg carry_tmp;

// Flags In
wire carry_in = flags_in[0];

// ADC
wire [7:0] adc;
wire adc_n, adc_v, adc_z, adc_c;
assign {adc_c, adc} = alu_a + alu_b + carry_in;
assign adc_n = adc[7];
assign adc_v = (~alu_a[7] & ~alu_b[7] & adc[7]) || (alu_a[7] & alu_b[7] & ~adc[7]);
assign adc_z = ~(|adc);

// LDA, LDX, LDY
wire [7:0] ld;
wire ld_n, ld_z;
assign ld = alu_a;
assign ld_n = ld[7];
assign ld_z = !(|ld);

always @(posedge clk) begin
	carry_tmp <= flags_out[0]; 
end

always @(*)
begin
	case (alu_opcode)
		2'b00: begin // ADR0
			{flags_out[0], alu_out} <= alu_a + alu_b;
			flags_out[7:1] <= 7'b0; 
			flags_ena <= 8'b0; 
		end
		
		2'b01: begin // ADR1
			alu_out <= carry_tmp + alu_b;
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
		end
		
		2'b10: begin // ADC
			alu_out <= adc; 
			flags_out <= {adc_n, adc_v, 4'b0000, adc_z, adc_c}; 
			flags_ena <= 8'b11000011; 
		end
		
		2'b11: begin // LDA, LDX, LDY
			alu_out <= alu_b; 
			flags_out <= {ld_n, 5'b0000, ld_z, 1'b0}; 
			flags_ena <= 8'b01000010; 
		end
		
//		default: begin 
//			alu_out <= 8'b0; 
//			flags_out <= 8'b0; 
//			flags_ena <= 8'b0; 
//		end
	endcase
end

endmodule