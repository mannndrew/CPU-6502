module control_unit
(
	input clk,
	input rst,
	input [7:0] opcode,
	input [7:0] opcode_reg,
	input branch_valid,
	output reg instruction_load,
	output reg increment_pc,
	output reg indirl_load,
	output reg indirh_load,
	output reg dirl_load,
	output reg dirh_load,
	output reg a_load,
	output reg x_load,
	output reg y_load,
	output reg branch_load,
	output reg read_write,
	output reg [2:0] address_select,
	output reg [2:0] alu_select,
	output reg [2:0] alu_opcode
	,output [5:0] fsm
);

assign fsm = state;

/* Read/Write */
parameter
	read				= 1'b0,
	write				= 1'b1;


/* Address Select */
parameter
	PC					= 3'b000,
	ZERO				= 3'b001,
	ABS				= 3'b010,
	IND_ZERO_0		= 3'b011,
	IND_ZERO_1		= 3'b100,
	IND_ABS_0		= 3'b101,
	IND_ABS_1		= 3'b110;

/* ALU Select */
parameter
	A					= 3'b000,
	X					= 3'b001,
	Y					= 3'b010,
	M					= 3'b011,
	Z					= 3'b100;
	
/* Opcodes */
parameter
	ADR0				= 3'b000,
	ADR1				= 3'b001,
	ADC				= 3'b010,
	LD					= 3'b011,
	ASL				= 3'b100;

/* States */
parameter
	FETCH				= 6'd0,
	AC0				= 6'd1,
	IM0				= 6'd2,
	ZP0				= 6'd3,
	ZP1				= 6'd4,
	ABS0				= 6'd5,
	ABS1				= 6'd6,
	ABS2				= 6'd7,
	IND_ZP0			= 6'd8,
	IND_ZP1			= 6'd9,
	IND_ZP2			= 6'd10,
	IND_ZP3			= 6'd11,
	IND_ABS0			= 6'd12,
	IND_ABS1			= 6'd13,
	IND_ABS2			= 6'd14,
	IND_ABS3			= 6'd15,
	IND_ABS4			= 6'd16,
	ZP_STORE			= 6'd17,
	ABS_STORE		= 6'd18,
	BRANCH_CHECK	= 6'd19,
	BRANCH_GO		= 6'd20;
	
	
reg [5:0] state;
reg [2:0] alu_select_ad;
reg [2:0] alu_select_ex;
reg [2:0] alu_opcode_ex;
reg storing_instruction;
reg load;

/* Storing Instruction? */

always @(opcode_reg) begin
	casex (opcode_reg)
		8'b0xx0_xx10,
		8'b100x_0x01,
		8'b100x_0x10,
		8'b1001_xx01,
		8'b00xx_1x10,
		8'b100x_x10x,
		8'b01xx_01x0,
		8'bx1xx_x110,
		8'bx00x_x1x0,
		8'b0xxx_x110: storing_instruction <= 1'b1;
		default: storing_instruction <= 1'b0;
	endcase
end

	
/* State Machine */
	
always @(posedge clk, negedge rst) begin
	if (rst == 1'b0)
		state <= FETCH;
	else begin
		case (state)
			FETCH:
				casex (opcode)
					8'b0xx0_x01x,
					8'b00xx_101x: state <= AC0;
					8'b1x10_00x0,
					8'b11x0_00x0,
					8'bxxx0_1001: state <= IM0;
					8'bxxxx_01xx: state <= ZP0;
					8'bxx0x_11x0,
					8'b1xxx_11x0,
					8'bx0xx_11x0,
					8'b0010_00x0,
					8'bxxx1_1x01,
					8'bxxxx_1110,
					8'bxxxx_1101: state <= ABS0;
					8'bxxx1_001x,
					8'bxxxx_00x1: state <= IND_ZP0;
					8'b1001_0000: state <= BRANCH_CHECK;
					default: state <= FETCH;
				endcase
			AC0: state <= FETCH;
			
			
			IM0: state <= FETCH;
			
			
			ZP0: state <= ZP1;
			ZP1: 
				if (storing_instruction) state <= ZP_STORE;
				else state <= FETCH;
			
			
			
			ABS0: state <= ABS1;
			ABS1: state <= ABS2;
			ABS2:
				if (storing_instruction) state <= ABS_STORE;
				else state <= FETCH;
			
			
			IND_ZP0: state <= IND_ZP1;
			IND_ZP1: state <= IND_ZP2;
			IND_ZP2: state <= IND_ZP3;
			IND_ZP3:
				if (storing_instruction) state <= ABS_STORE;
				else state <= FETCH;
			
			
			IND_ABS0: state <= IND_ABS1;
			IND_ABS1: state <= IND_ABS2;
			IND_ABS2: state <= IND_ABS3;
			IND_ABS3: state <= IND_ABS4;
			IND_ABS4: state <= FETCH;
			
			ZP_STORE: state <= FETCH;
			
			BRANCH_CHECK:
				if (branch_valid) state <= BRANCH_GO;
				else state <= FETCH;
				
			BRANCH_GO: state <= FETCH;
			
		endcase
	end
end

/* Instruction Load */

always @(state) begin
	if (state == FETCH)
		instruction_load <= 1'b1;
	else
		instruction_load <= 1'b0;
end

/* Increment PC */

always @(state) begin
	case (state)
		FETCH: increment_pc <= 1'b1;
		IM0: increment_pc <= 1'b1;
		ZP0: increment_pc <= 1'b1;
		ABS0: increment_pc <= 1'b1;
		ABS1: increment_pc <= 1'b1;
		IND_ZP0: increment_pc <= 1'b1;
		IND_ABS0: increment_pc <= 1'b1;
		IND_ABS1: increment_pc <= 1'b1;
		BRANCH_CHECK: increment_pc <= 1'b1;
		default: increment_pc <= 1'b0;
	endcase
end

/* Indirect Low Load */

always @(state) begin
	case (state)
		IND_ZP0: indirl_load <= 1'b1;
		IND_ABS0: indirl_load <= 1'b1;
		default: indirl_load <= 1'b0;
	endcase
end

/* Indirect High Load */

always @(state) begin
	case (state)
		IND_ABS1: indirh_load <= 1'b1;
		default: indirh_load <= 1'b0;
	endcase
end

/* Direct Low Load */

always @(state) begin
	case (state)
		ZP0: dirl_load <= 1'b1;
		ABS0: dirl_load <= 1'b1;
		IND_ZP1: dirl_load <= 1'b1;
		IND_ABS2: dirl_load <= 1'b1;
		default: dirl_load <= 1'b0;
	endcase
end

/* Direct High Load */

always @(state) begin
	case (state)
		ABS1: dirh_load <= 1'b1;
		IND_ZP2: dirh_load <= 1'b1;
		IND_ABS3: dirh_load <= 1'b1;
		default: dirh_load <= 1'b0;
	endcase
end

/* Load */

always @(state) begin
	case (state)
		AC0: load <= 1'b1;
		IM0: load <= 1'b1;
		ZP1: load <= 1'b1;
		ABS2: load <= 1'b1;
		IND_ZP3: load <= 1'b1;
		IND_ABS4: load <= 1'b1;
		default: load <= 1'b0;
	endcase
end

/* A Load */

always @(opcode_reg, load) begin
	casex (opcode_reg)
		8'bx000_x01x,
		8'bxx11_001x,
		8'b0xxx_001x,
		8'b0xx0_x01x,
		8'b00xx_x01x,
		8'b1001_1000,
		8'bxx1x_xx01,
		8'b0xxx_xx01,
		8'b0110_10xx: a_load <= 1'b1 & load; 
		/* ADC, AND, ASL A, DEC A, EOR, INC A
		LDA, LSR A, ORA, PLA, ROL A, ROR A, SBC
		TXA, TYA */

		default: a_load <= 1'b0;
	endcase
end

/* X Load */

always @(opcode_reg, load) begin
	casex (opcode_reg)
		8'b1010_xx10,
		8'b1110_1000,
		8'b1100_x010,
		8'b101x_x110,
		8'b1x11_101x: x_load <= 1'b1 & load;
		/* DEX, INX, LDX, PLX, TAX, TSX */
		
		default: x_load <= 1'b0;
	endcase
end

/* Y Load */

always @(opcode_reg, load) begin
	casex (opcode_reg)
		8'b1x11_x100,
		8'b0111_101x,
		8'b1x00_1000,
		8'b1010_xx00: y_load <= 1'b1 & load;
		/* DEY, INY, LDY, PLY, TAY */
		
		default: y_load <= 1'b0;
	endcase
end

/* Branch Load */

always @(state) begin
	casex (state)
		BRANCH_GO: branch_load <= 1'b1;
		default: branch_load <= 1'b0;
	endcase
end

/* Read/Write */

always @(state) begin
	case (state)
		ZP_STORE: read_write <= write;
		ABS_STORE: read_write <= write;
		default: read_write <= read;
	endcase
end

/* Address Select */

always @(state) begin
	case (state)
		FETCH: address_select <= PC;
		AC0: address_select <= PC;
		IM0: address_select <= PC;
		ZP0: address_select <= PC;
		ZP1: address_select <= ZERO;
		ZP_STORE: address_select <= ZERO;
		ABS0: address_select <= PC;
		ABS1: address_select <= PC;
		ABS2: address_select <= ABS;
		ABS_STORE: address_select <= ABS;
		IND_ZP0: address_select <= PC;
		IND_ZP1: address_select <= IND_ZERO_0;
		IND_ZP2: address_select <= IND_ZERO_1;
		IND_ZP3: address_select <= ABS;
		IND_ABS0: address_select <= PC;
		IND_ABS1: address_select <= PC;
		IND_ABS2: address_select <= IND_ABS_0;
		IND_ABS3: address_select <= IND_ABS_1;
		IND_ABS4: address_select <= ABS;
		default: address_select <= PC;
	endcase
end



/* ALU Select */

always @(opcode_reg) begin
	casex (opcode_reg)
		8'bxxx0_00x1,
		8'bxx01_1110,
		8'bx1x1_x1x0,
		8'b0xx1_x110,
		8'bxx11_x10x,
		8'bxxx1_x101,
		8'b1xx1_010x: alu_select_ad <= X;
		8'b10x1_0110,
		8'b1011_x110,
		8'bxxx1_x001: alu_select_ad <= Y;
		default: alu_select_ad <= Z;
	endcase
end

always @(opcode_reg) begin
	casex (opcode_reg)
		8'b0111_0010,
		8'b011x_xx01: alu_select_ex <= A; 
		
		8'b0000_0110: alu_select_ex <= M;
		/* ------------------------------------------------------- Inputs -------------------------------------------------------- */
		/* A: ADC, AND, ASL A, BBR, BBS, BIT, CMP, DEC A, EOR, INC A, LSR A, ORA, PHA, ROL A, ROR A, SBC, STA, TAX, TAY, TRB, TSB	*/
		/* F: BCC, BCS, BEQ, BMI, BNE, BPL, BRA, BVC, BVS, CLC, CLD, CLI, CLV, PHP, SEC, SED, SEI 											*/
		/* M: ASL, DEC, INC, LDA, LDX, LDY, LSR, PLA, PLP, PLX, PLY, RMB, ROL, ROR, SMB															*/
		/* X: CPX, DEX, INX, PHX, STX, TXA, TXS    																											*/
		/* Y: CPY, DEY, INY, PHY, STY, TYA   																													*/
		/* Z: STZ 																																						*/
		/* SP: TSX 																																						*/
		
		/* ------------------------------------------------------- Outputs ------------------------------------------------------- */
		/* A: ADC, AND, ASL A, DEC A, EOR, INC A, LDA, LSR A, ORA, PLA, ROL A, ROR A, SBC, TXA, TYA 											*/
		/* F: CLC, CLD, CLI, CLV, PLP, SEC, SED, SEI 																										*/
		/* M: ASL, DEC, INC, LSR, PHA, PHP, PHX, PHY, RMB, ROL, ROR, SMB, STA, STX, STY, STZ, TRB, TSB   									*/
		/* X: DEX, INX, LDX, PLX, TAX, TSX,     																												*/
		/* Y: DEY, INY, LDY, PLY, TAY   																															*/
		/* SP: TXS  																																					*/
		/* PC: JMP, JSR 																																				*/
							
		
		default: alu_select_ex <= M;
	endcase
end

always @(state, alu_select_ad, alu_select_ex) begin
	case (state)
		AC0: alu_select <= A;
		IM0: alu_select <= alu_select_ex;
		ZP0: alu_select <= alu_select_ad;
		ZP1: alu_select <= alu_select_ex;
		ABS0: alu_select <= alu_select_ad;
		ABS2: alu_select <= alu_select_ex;
		
		IND_ZP0: if (alu_select_ad == X) alu_select <= alu_select_ad;
					else alu_select <= Z;
		IND_ZP1: if (alu_select_ad == Y) alu_select <= alu_select_ad;
					else alu_select <= Z;
		IND_ZP3: alu_select <= alu_select_ex;
		
		
		IND_ABS0: alu_select <= alu_select_ad;
		IND_ABS4: alu_select <= alu_select_ex;
		
		default: alu_select <= Z;
	endcase
end




/* ALU Opcode */

always @(opcode_reg) begin
	casex (opcode_reg)
		8'b011x_001x,
		8'b011x_xx01: alu_opcode_ex <= ADC;
		//8'b001x_001x,
		//8'b001x_xx01: alu_opcode_ex <= AND;
		//8'b0000_0110: alu_opcode_ex <= ASL;
		8'b1001_0000: alu_opcode_ex <= 3'b101;
		

		default: alu_opcode_ex <= 3'b011;
	endcase
end

always @(state, alu_opcode_ex) begin
	case (state)
		AC0: alu_opcode <= alu_opcode_ex;
		IM0: alu_opcode <= alu_opcode_ex;
		ZP0: alu_opcode <= ADR0;
		ZP1: alu_opcode <= alu_opcode_ex;
		ABS0: alu_opcode <= ADR0;
		ABS1: alu_opcode <= ADR1;
		ABS2: alu_opcode <= alu_opcode_ex;
		IND_ZP0: alu_opcode <= ADR0;
		IND_ZP1: alu_opcode <= ADR0;
		IND_ZP2: alu_opcode <= ADR1;
		IND_ZP3: alu_opcode <= alu_opcode_ex;
		IND_ABS0: alu_opcode <= ADR0;
		IND_ABS1: alu_opcode <= ADR1;
		IND_ABS2: alu_opcode <= ADR0;
		IND_ABS3: alu_opcode <= ADR0;
		IND_ABS4: alu_opcode <= alu_opcode_ex;
		BRANCH_CHECK: alu_opcode <= alu_opcode_ex;
		
		default: alu_opcode <= 3'b001;
	endcase
end



endmodule		

				
