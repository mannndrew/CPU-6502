module arithmetic_unit
(
	input clk,
	input [2:0] alu_opcode,
	input [7:0] alu_a,
	input [7:0] alu_b,
	input [7:0] flags_in,
	output reg [7:0] alu_out,
	output reg [7:0] flags_out,
	output reg [7:0] flags_ena,
	output reg branch_valid
);


// Temp Reg
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


// ASL
wire [7:0] asl;
wire asl_n, asl_z, asl_c;
assign {asl_c, asl} = alu_a << 1'b1;
assign asl_n = asl[7];
assign asl_z = ~(|asl);


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
		3'b000: begin // ADR0
			{flags_out[0], alu_out} <= alu_a + alu_b;
			flags_out[7:1] <= 7'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		3'b001: begin // ADR1
			alu_out <= carry_tmp + alu_b;
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		3'b010: begin // ADC
			alu_out <= adc; 
			flags_out <= {adc_n, adc_v, 4'b0000, adc_z, adc_c}; 
			flags_ena <= 8'b11000011; 
			branch_valid <= 1'b0;
		end
		
		3'b011: begin // LDA, LDX, LDY
			alu_out <= alu_a; 
			flags_out <= {ld_n, 5'b0000, ld_z, 1'b0}; 
			flags_ena <= 8'b01000010; 
			branch_valid <= 1'b0;
		end
		
		3'b100: begin // ASL
			alu_out <= asl; 
			flags_out <= {asl_n, 5'b00000, asl_z, asl_c}; 
			flags_ena <= 8'b10000011; 
			branch_valid <= 1'b0;
		end
		
		3'b101: begin // BCC 
			alu_out <= 8'b0; 
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= ~carry_in;
		end
		
		default: begin 
			alu_out <= 8'b0; 
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
	endcase
end

endmodule
