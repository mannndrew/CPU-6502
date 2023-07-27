module arithmetic_unit
(
	input clk,
	input [5:0] alu_opcode,
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
wire [7:0] adc_out;
wire adc_n, adc_v, adc_z, adc_c;
assign {adc_c, adc_out} = alu_a + alu_b + carry_in;
assign adc_n = adc_out[7];
assign adc_v = (~alu_a[7] & ~alu_b[7] & adc_out[7]) || (alu_a[7] & alu_b[7] & ~adc_out[7]);
assign adc_z = ~(|adc_out);

// AND
wire [7:0] and_out;
wire and_n, and_z;
assign and_out = alu_a & alu_b;
assign and_n = and_out[7];
assign and_z = ~(|and_out);

// ASL
wire [7:0] asl_out;
wire asl_n, asl_z, asl_c;
assign {asl_c, asl_out} = alu_a << 1'b1;
assign asl_n = asl_out[7];
assign asl_z = ~(|asl_out);

// BIT
wire [7:0] bit_out;
wire bit_n, bit_v, bit_z;
assign bit_out = alu_a & alu_b;
assign bit_n = bit_out[7];
assign bit_v = bit_out[6];
assign bit_z = ~(|bit_out);

// BBR0, BCC
wire bbr0_branch = ~alu_a[0];

// BBR1, BNE
wire bbr1_branch = ~alu_a[1];

// BBR2
wire bbr2_branch = ~alu_a[2];

// BBR3
wire bbr3_branch = ~alu_a[3];

// BBR4
wire bbr4_branch = ~alu_a[4];

// BBR5
wire bbr5_branch = ~alu_a[5];

// BBR6, BVC
wire bbr6_branch = ~alu_a[6];

// BBR7, BPL
wire bbr7_branch = ~alu_a[7];

// BBS0, BCS
wire bbs0_branch = alu_a[0];

// BBS1, BEQ
wire bbs1_branch = alu_a[1];

// BBS2
wire bbs2_branch = alu_a[2];

// BBS3
wire bbs3_branch = alu_a[3];

// BBS4
wire bbs4_branch = alu_a[4];

// BBS5
wire bbs5_branch = alu_a[5];

// BBS6, BVS
wire bbs6_branch = alu_a[6];

// BBS7, BMI
wire bbs7_branch = alu_a[7];

// BRA
wire bra_branch = 1'b1;

// CLC, CLD, CLI, CLV

// CMP, CPX, CPY
wire [7:0] cmp_out;
wire cmp_n, cmp_z, cmp_c;
assign {cmp_c, cmp_out} = alu_a + ~alu_b + 1'b1;
assign cmp_n = cmp_out[7];
assign cmp_z = ~(|cmp_out);

// DEC, DEX, DEY
wire [7:0] dec_out;
wire dec_n, dec_z;
assign dec_out = alu_a + 8'b11111111;
assign dec_n = dec_out[7];
assign dec_z = ~(|dec_out);

// EOR
wire [7:0] eor_out;
wire eor_n, eor_z;
assign eor_out = alu_a ^ alu_b;
assign eor_n = eor_out[7];
assign eor_z = ~(|eor_out);

// INC, INX, INY
wire [7:0] inc_out;
wire inc_n, inc_z;
assign inc_out = alu_a + 8'b00000001;
assign inc_n = inc_out[7];
assign inc_z = ~(|inc_out);

// LDA, LDX, LDY, PLA, PLP, PLX, PLY
wire [7:0] load_out;
wire load_n, load_z;
assign load_out = alu_a;
assign load_n = load_out[7];
assign load_z = !(|load_out);

// PHA, PHP, PHX, PHY, STA, STX, STY, STZ, TAX, TAY, TSX, TXA, TXS, TYA
wire [7:0] store_out;
assign store_out = alu_a;

// LSR
wire [7:0] lsr_out;
wire lsr_n, lsr_z, lsr_c;
assign lsr_out = (alu_a[0] << 7) | (alu_a >> 1);
assign lsr_n = lsr_out[7];
assign lsr_z = !(|lsr_out);
assign lsr_c = alu_a[0];

// ORA
wire [7:0] ora_out;
wire ora_n, ora_z;
assign ora_out = alu_a | alu_b;
assign ora_n = ora_out[7];
assign ora_z = !(|ora_out);

// RMB0
wire [7:0] rmb0_out = alu_a & 8'b11111110;

// RMB1
wire [7:0] rmb1_out = alu_a & 8'b11111101;

// RMB2
wire [7:0] rmb2_out = alu_a & 8'b11111011;

// RMB3
wire [7:0] rmb3_out = alu_a & 8'b11110111;

// RMB4
wire [7:0] rmb4_out = alu_a & 8'b11101111;

// RMB5
wire [7:0] rmb5_out = alu_a & 8'b11011111;

// RMB6
wire [7:0] rmb6_out = alu_a & 8'b10111111;

// RMB7
wire [7:0] rmb7_out = alu_a & 8'b01111111;


// ROL
wire [7:0] rol_out;
wire rol_n, rol_z, rol_c;
assign rol_out = alu_a << 1 | flags_in[0];
assign rol_n = rol_out[7];
assign rol_z = !(|rol_out);
assign rol_c = alu_a[7];


// ROR
wire [7:0] ror_out;
wire ror_n, ror_z, ror_c;
assign ror_out = (flags_in[0] << 7) | (alu_a >> 1);
assign ror_n = ror_out[7];
assign ror_z = !(|ror_out);
assign ror_c = alu_a[0];



// SBC
wire [7:0] sbc_out;
wire sbc_n, sbc_v, sbc_z, sbc_c;
assign {sbc_c, sbc_out} = alu_a + (~alu_b) + carry_in;
assign sbc_n = sbc_out[7];
assign sbc_v = (~alu_a[7] & ~alu_b[7] & sbc_out[7]) || (alu_a[7] & alu_b[7] & ~sbc_out[7]);
assign sbc_z = ~(|sbc_out);

// SEC, SED, SEI

// SMB0
wire [7:0] smb0_out = alu_a | 8'b00000001;

// SMB1
wire [7:0] smb1_out = alu_a | 8'b00000010;

// SMB2
wire [7:0] smb2_out = alu_a | 8'b00000100;

// SMB3
wire [7:0] smb3_out = alu_a | 8'b00001000;

// SMB4
wire [7:0] smb4_out = alu_a | 8'b00010000;

// SMB5
wire [7:0] smb5_out = alu_a | 8'b00100000;

// SMB6
wire [7:0] smb6_out = alu_a | 8'b01000000;

// SMB7
wire [7:0] smb7_out = alu_a | 8'b10000000;



// TRB
wire [7:0] trb_out;
wire trb_z;
assign trb_out = alu_a & (~alu_b);
assign trb_z = ~(|(alu_a & alu_b));

// TSB
wire [7:0] tsb_out;
wire tsb_z;
assign tsb_out = alu_a | alu_b;
assign tsb_z = ~(|(alu_a & alu_b));




always @(posedge clk) begin
	carry_tmp <= flags_out[0]; 
end



always @(*)
begin
	case (alu_opcode)
		6'b000000: begin // ADR0
			{flags_out[0], alu_out} <= alu_a + alu_b;
			flags_out[7:1] <= 7'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b000001: begin // ADR1
			alu_out <= carry_tmp + alu_b;
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b000010: begin // ADC
			alu_out <= adc_out; 
			flags_out <= {adc_n, adc_v, 4'b0000, adc_z, adc_c}; 
			flags_ena <= 8'b11000011; 
			branch_valid <= 1'b0;
		end
		
		6'b000011: begin // AND
			alu_out <= and_out; 
			flags_out <= {and_n, 5'b00000, and_z, 1'b0}; 
			flags_ena <= 8'b10000010; 
			branch_valid <= 1'b0;
		end
		
		6'b000100: begin // ASL
			alu_out <= asl_out; 
			flags_out <= {asl_n, 5'b00000, asl_z, asl_c}; 
			flags_ena <= 8'b10000011; 
			branch_valid <= 1'b0;
		end
		
		6'b000101: begin // BIT
			alu_out <= bit_out; 
			flags_out <= {bit_n, bit_v, 4'b0000, bit_z, 1'b0}; 
			flags_ena <= 8'b11000010; 
			branch_valid <= 1'b0;
		end
		
		6'b000110: begin // BBR0, BCC
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbr0_branch;
		end
		
		6'b000111: begin // BBR1, BNE
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbr1_branch;
		end
		
		6'b001000: begin // BBR2
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbr2_branch;
		end
		
		6'b001001: begin // BBR3
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbr3_branch;
		end
		
		6'b001010: begin // BBR4
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbr4_branch;
		end
		
		6'b001011: begin // BBR5
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbr5_branch;
		end
		
		6'b001100: begin // BBR6, BVC
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbr6_branch;
		end
		
		6'b001101: begin // BBR7, BPL
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbr7_branch;
		end
		
		6'b001110: begin // BBS0, BCS
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbs0_branch;
		end
		
		6'b001111: begin // BBS1, BEQ
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbs1_branch;
		end
		
		6'b010000: begin // BBS2
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbs2_branch;
		end
		
		6'b010001: begin // BBS3
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbs3_branch;
		end
		
		6'b010010: begin // BBS4
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbs4_branch;
		end
		
		6'b010011: begin // BBS5
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbs5_branch;
		end
		
		6'b010100: begin // BBS6, BVS
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbs6_branch;
		end
		
		6'b010101: begin // BBS7, BMI
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bbs7_branch;
		end
		
		6'b010110: begin // BRA
			alu_out <= 8'b0;
			flags_out <= 8'b0;
			flags_ena <= 8'b0;
			branch_valid <= bra_branch;
		end
		
		6'b010111: begin // CLC
			alu_out <= 8'b0;
			flags_out <= 8'b0; 
			flags_ena <= 8'b00000001; 
			branch_valid <= 1'b0;
		end
		
		
		6'b011000: begin // CLI
			alu_out <= 8'b0;
			flags_out <= 8'b0; 
			flags_ena <= 8'b00000100; 
			branch_valid <= 1'b0;
		end
		
		6'b011001: begin // CLD
			alu_out <= 8'b0;
			flags_out <= 8'b0; 
			flags_ena <= 8'b00001000; 
			branch_valid <= 1'b0;
		end
		
		6'b011010: begin // CLV
			alu_out <= 8'b0;
			flags_out <= 8'b0; 
			flags_ena <= 8'b01000000; 
			branch_valid <= 1'b0;
		end
		
		6'b011011: begin // CMP, CPX, CPY
			alu_out <= cmp_out;
			flags_out <= {cmp_n, 5'b00000, cmp_z, cmp_c}; 
			flags_ena <= 8'b10000011; 
			branch_valid <= 1'b0;
		end
		
		6'b011100: begin // DEC, DEX, DEY
			alu_out <= dec_out;
			flags_out <= {dec_n, 5'b00000, dec_z, 1'b0}; 
			flags_ena <= 8'b10000010; 
			branch_valid <= 1'b0;
		end
		
		6'b011101: begin // EOR
			alu_out <= eor_out;
			flags_out <= {eor_n, 5'b00000, eor_z, 1'b0}; 
			flags_ena <= 8'b10000010; 
			branch_valid <= 1'b0;
		end
		
		6'b011110: begin // INC, INX, INY
			alu_out <= inc_out;
			flags_out <= {inc_n, 5'b00000, inc_z, 1'b0}; 
			flags_ena <= 8'b10000010; 
			branch_valid <= 1'b0;
		end
		
		6'b011111: begin // LDA, LDX, LDY, PLA, PLP, PLX, PLY
			alu_out <= load_out;
			flags_out <= {load_n, 5'b00000, load_z, 1'b0}; 
			flags_ena <= 8'b10000010; 
			branch_valid <= 1'b0;
		end
		
		6'b100000: begin // PHA, PHP, PHX, PHY, STA, STX, STY, STZ, TAX, TAY, TSX, TXA, TXS, TYA
			alu_out <= store_out;
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b100001: begin // LSR
			alu_out <= lsr_out;
			flags_out <= {lsr_n, 5'b00000, lsr_z, lsr_c}; 
			flags_ena <= 8'b10000011; 
			branch_valid <= 1'b0;
		end
		
		6'b100010: begin // ORA
			alu_out <= ora_out;
			flags_out <= {ora_n, 5'b00000, ora_z, 1'b0}; 
			flags_ena <= 8'b10000010; 
			branch_valid <= 1'b0;
		end
		
		6'b100011: begin // RMB0
			alu_out <= rmb0_out;
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b100100: begin // RMB1
			alu_out <= rmb1_out;
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b100101: begin // RMB2
			alu_out <= rmb2_out;
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b100110: begin // RMB3
			alu_out <= rmb3_out;
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b100111: begin // RMB4
			alu_out <= rmb4_out;
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b101000: begin // RMB5
			alu_out <= rmb5_out;
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b101001: begin // RMB6
			alu_out <= rmb6_out;
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b101010: begin // RMB7
			alu_out <= rmb7_out;
			flags_out <= 8'b0; 
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b101011: begin // ROL
			alu_out <= rol_out;
			flags_out <= {rol_n, 5'b00000, rol_z, rol_c}; 
			flags_ena <= 8'b10000011; 
			branch_valid <= 1'b0;
		end
		
		6'b101100: begin // ROR
			alu_out <= ror_out;
			flags_out <= {ror_n, 5'b00000, ror_z, ror_c}; 
			flags_ena <= 8'b10000011; 
			branch_valid <= 1'b0;
		end
		
		6'b101101: begin // SBC
			alu_out <= sbc_out;
			flags_out <= {sbc_n, sbc_v, 4'b0000, sbc_z, sbc_c}; 
			flags_ena <= 8'b11000011; 
			branch_valid <= 1'b0;
		end
		
		6'b101110: begin // SEC
			alu_out <= 8'b0;
			flags_out <= 8'b11111111;
			flags_ena <= 8'b00000001; 
			branch_valid <= 1'b0;
		end
		
		6'b101111: begin // SEI
			alu_out <= 8'b0;
			flags_out <= 8'b11111111;
			flags_ena <= 8'b00000100; 
			branch_valid <= 1'b0;
		end
		
		6'b110000: begin // SED
			alu_out <= 8'b0;
			flags_out <= 8'b11111111;
			flags_ena <= 8'b00001000; 
			branch_valid <= 1'b0;
		end
		
		6'b110001: begin // SMB0
			alu_out <= smb0_out;
			flags_out <= 8'b0;
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b110010: begin // SMB1
			alu_out <= smb1_out;
			flags_out <= 8'b0;
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b110011: begin // SMB2
			alu_out <= smb2_out;
			flags_out <= 8'b0;
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b110100: begin // SMB3
			alu_out <= smb3_out;
			flags_out <= 8'b0;
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b110101: begin // SMB4
			alu_out <= smb4_out;
			flags_out <= 8'b0;
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b110110: begin // SMB5
			alu_out <= smb5_out;
			flags_out <= 8'b0;
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b110111: begin // SMB6
			alu_out <= smb6_out;
			flags_out <= 8'b0;
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b111000: begin // SMB7
			alu_out <= smb7_out;
			flags_out <= 8'b0;
			flags_ena <= 8'b0; 
			branch_valid <= 1'b0;
		end
		
		6'b111001: begin // TRB
			alu_out <= trb_out;
			flags_out <= {6'b000000, trb_z, 1'b0}; 
			flags_ena <= 8'b00000010; 
			branch_valid <= 1'b0;
		end
		
		6'b111010: begin // TSB
			alu_out <= tsb_out;
			flags_out <= {6'b000000, tsb_z, 1'b0}; 
			flags_ena <= 8'b00000010; 
			branch_valid <= 1'b0;
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
