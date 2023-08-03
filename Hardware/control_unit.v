module control_unit
(
	input clk,
	input rst,
	input [7:0] opcode,
	input [7:0] opcode_reg,
	input branch_valid,
	output reg instruction_load,
	output reg increment_pc,
	output reg [1:0] sp_op,
	output reg sp_load,
	output reg indirl_load,
	output reg indirh_load,
	output reg dirl_load,
	output reg dirh_load,
	output reg a_load,
	output reg x_load,
	output reg y_load,
	output reg branch_load,
	output reg pcl_load,
	output reg pch_load,
	output reg jmp_load,
	output reg jsr_load,
	output reg rst_load,
	output reg read_write,
	output reg [2:0] write_select,
	output reg [3:0] address_select,
	output reg [2:0] alu_select,
	output reg [5:0] alu_opcode
	,output [5:0] fsm
);

assign fsm = state;

/* Read/Write */
parameter
	read				= 1'b0,
	write				= 1'b1;


/* Address Select */
parameter
	PC					= 4'b0000,
	ZERO				= 4'b0001,
	ABS				= 4'b0010,
	IND_ZERO_0		= 4'b0011,
	IND_ZERO_1		= 4'b0100,
	IND_ABS_0		= 4'b0101,
	IND_ABS_1		= 4'b0110,
	STACK				= 4'b0111,
	IVL				= 4'b1000,
	IVH				= 4'b1001,
	RVL				= 4'b1010,
	RVH				= 4'b1011;

/* ALU Select */
parameter
	A					= 3'b000,
	F					= 3'b001,
	M					= 3'b010,
	SP					= 3'b011,
	X					= 3'b100,
	Y					= 3'b101,
	Z					= 3'b110;

	
/* Opcodes */
parameter
	ADR0				= 6'b000000,
	ADR1				= 6'b000001;

/* States */
parameter
	FETCH				= 6'd0,
	IM0				= 6'd1,
	ZP0				= 6'd2,
	ZP1				= 6'd3,
	ABS0				= 6'd4,
	ABS1				= 6'd5,
	ABS2				= 6'd6,
	IND_ZP0			= 6'd7,
	IND_ZP1			= 6'd8,
	IND_ZP2			= 6'd9,
	IND_ZP3			= 6'd10,
	IND_ABS0			= 6'd11,
	IND_ABS1			= 6'd12,
	IND_ABS2			= 6'd13,
	ZP_WRITE			= 6'd14,
	ABS_WRITE		= 6'd15,
	ZP_STORE			= 6'd16,
	ABS_STORE		= 6'd17,
	IND_ZP_STORE	= 6'd18,
	BRANCH_CHECK	= 6'd19,
	BRANCH_GO		= 6'd20,
	PUSH				= 6'd21,
	PULL				= 6'd22,
	ABS_JMP			= 6'd23,
	IND_ABS_JMP		= 6'd24,
	JSR0				= 6'd25,
	JSR1				= 6'd26,
	JSR2				= 6'd27,
	BRK0				= 6'd28,
	BRK1				= 6'd29,
	BRK2				= 6'd30,
	BRK3				= 6'd31,
	BRK4				= 6'd32,
	BRK5				= 6'd33,
	RTI0				= 6'd34,
	RTI1				= 6'd35,
	RTI2				= 6'd36,
	RTS0				= 6'd37,
	RTS1				= 6'd38,
	STP				= 6'd39,
	WAI				= 6'd40,
	RST0				= 6'd41,
	RST1				= 6'd42,
	RST2				= 6'd43;
	
	
	
reg [5:0] state;
reg [2:0] alu_select_ad;
reg [2:0] alu_select_ex;
reg [5:0] alu_opcode_ex;
reg jumping_nosave_instruction;
reg jumping_save_instruction;
reg writing_instruction;
reg storing_instruction;
reg load;

/* Jumping No Save Instruction? */

always @(opcode_reg) begin
	casex (opcode_reg)
		8'b01x0_1100,
		8'b011x_1100: jumping_nosave_instruction <= 1'b1;
		/* JMP */
		default: jumping_nosave_instruction <= 1'b0;
	endcase
end

/* Jumping Save Instruction? */

always @(opcode_reg) begin
	casex (opcode_reg)
		8'b0010_0000: jumping_save_instruction <= 1'b1;
		/* JSR */
		default: jumping_save_instruction <= 1'b0;
	endcase
end

/* Writing Instruction? */

always @(opcode_reg) begin
	casex (opcode_reg)
		8'b000x_x1x0,
		8'b00xx_1x10,
		8'bx1xx_x110,
		8'b0xx0_1x10,
		8'b0xxx_x110: writing_instruction <= 1'b1;
		/* ASL, DEC, INC, LSR, RMB, ROL, ROR, SMB, TRB, TSB */
		default: writing_instruction <= 1'b0;
	endcase
end

/* Storing Instruction? */

always @(opcode_reg) begin
	casex (opcode_reg)
		8'b011x_0100,
		8'b1001_0x10,
		8'b1001_xx01,
		8'b100x_0x01,
		8'b100x_x1x0,
		8'b100x_x10x: storing_instruction <= 1'b1;
		/* STA, STX, STY, STZ */
		default: storing_instruction <= 1'b0;
	endcase
end

	
/* State Machine */
	
always @(posedge clk) begin
	if (rst == 1'b0)
		state <= RST0;
	else begin
		case (state)
			FETCH:
				casex (opcode)
					8'b1xx0_10x0,
					8'bx0xx_1010,
					8'b1010_x0x0,
					8'b11x0_x000,
					8'bxxx0_1001,
					8'bxxx1_1000,
					8'bxxx0_1010: state <= IM0;
					8'b1xx0_01xx,
					8'b0x1x_01xx,
					8'bx0xx_01xx,
					8'bxxxx_011x,
					8'bxxxx_01x1: state <= ZP0;
					8'b1xx0_11x0,
					8'bxx00_11x0,
					8'bx0xx_11x0,
					8'b0010_0000,
					8'bxxx1_1x01,
					8'bxxxx_1110,
					8'bxxxx_1101: state <= ABS0;
					8'bxxx1_0010,
					8'bxxxx_0001: state <= IND_ZP0;
					8'b011x_1100: state <= IND_ABS0;
					8'b100x_0000,
					8'bxxx1_0000,
					8'bxxxx_1111: state <= BRANCH_CHECK;
					8'b0x00_1000,
					8'bx101_1010: state <= PUSH;
					8'b0x10_1000,
					8'bx111_1010: state <= PULL;
					8'b0000_0000: state <= BRK0;
					8'b0100_0000: state <= RTI0;
					8'b0110_0000: state <= RTS0;
					8'b1101_1011: state <= STP;
					8'b1100_1011: state <= WAI;


					default: state <= FETCH;
					
				endcase
			
			IM0: state <= FETCH;
			
			
			ZP0:
				if (storing_instruction) state <= ZP_STORE;
				else state <= ZP1;
			ZP1: 
				if (writing_instruction) state <= ZP_WRITE;
				else state <= FETCH;
			
			
			
			ABS0:
				if (jumping_nosave_instruction) state <= ABS_JMP;
				else state <= ABS1;
			ABS1:
				if (storing_instruction) state <= ABS_STORE;
				else if (jumping_save_instruction) state <= JSR0;
				else state <= ABS2;
			ABS2:
				if (writing_instruction) state <= ABS_WRITE;
				else state <= FETCH;
			
			
			IND_ZP0: state <= IND_ZP1;
			IND_ZP1: state <= IND_ZP2;
			IND_ZP2: 
				if (storing_instruction) state <= IND_ZP_STORE;
				else state <= IND_ZP3;
			IND_ZP3: state <= FETCH;
				
			
			
			IND_ABS0: state <= IND_ABS1;
			IND_ABS1: state <= IND_ABS2;
			IND_ABS2: state <= IND_ABS_JMP;
			
			
			ZP_STORE: state <= FETCH;
			ABS_STORE: state <= FETCH;
			IND_ZP_STORE: state <= FETCH;
			
			ZP_WRITE: state <= FETCH;
			ABS_WRITE: state <= FETCH;
			
			BRANCH_CHECK:
				if (branch_valid) state <= BRANCH_GO;
				else state <= FETCH;
				
			BRANCH_GO: state <= FETCH;
			
			PUSH: state <= FETCH;
			PULL: state <= FETCH;
			
			ABS_JMP: state <= FETCH;
			IND_ABS_JMP: state <= FETCH;
			
			JSR0: state <= JSR1;
			JSR1: state <= JSR2;
			JSR2: state <= FETCH;
			
			BRK0: state <= BRK1;
			BRK1: state <= BRK2;
			BRK2: state <= BRK3;
			BRK3: state <= BRK4;
			BRK4: state <= BRK5;
			BRK5: state <= FETCH;
			
			RTI0: state <= RTI1;
			RTI1: state <= RTI2;
			RTI2: state <= FETCH;
			
			RTS0: state <= RTS1;
			RTS1: state <= FETCH;
			
			STP: state <= STP;
			WAI: state <= WAI;
			
			RST0: state <= RST1;
			RST1: state <= RST2;
			RST2: state <= FETCH;
			
			
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

/* Stack Pointer Operation */

always @(state) begin
	case (state)
		PUSH: sp_op <= 2'b10;		// Decrement SP
		JSR0: sp_op <= 2'b10;		// Decrement SP
		JSR1: sp_op <= 2'b10;		// Decrement SP
		BRK0: sp_op <= 2'b10;		// Decrement SP
		BRK1: sp_op <= 2'b10;		// Decrement SP
		BRK2: sp_op <= 2'b10;		// Decrement SP
		PULL: sp_op <= 2'b01;		// Increment SP
		RTI0: sp_op <= 2'b01;		// Increment SP
		RTI1: sp_op <= 2'b01;		// Increment SP
		RTI2: sp_op <= 2'b01;		// Increment SP
		RTS0: sp_op <= 2'b01;		// Increment SP
		RTS1: sp_op <= 2'b01;		// Increment SP
		
		default: sp_op <= 2'b00;	// Leave SP as is
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
		default: dirh_load <= 1'b0;
	endcase
end						
		

/* Load */

always @(state) begin
	case (state)
		IM0: load <= 1'b1;
		ZP1: load <= 1'b1;
		ABS2: load <= 1'b1;
		IND_ZP3: load <= 1'b1;
		PULL: load <= 1'b1;
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

/* SP Load */

always @(opcode_reg, load) begin
	casex (opcode_reg)
		8'b1001_1010: sp_load <= 1'b1 & load;
		/* TXS */
		
		default: sp_load <= 1'b0;
	endcase
end

/* Branch Load */

always @(state) begin
	casex (state)
		BRANCH_GO: branch_load <= 1'b1;
		default: branch_load <= 1'b0;
	endcase
end

/* PCL Load */

always @(state) begin
	casex (state)
		BRK4: pcl_load <= 1'b1;
		RTI1: pcl_load <= 1'b1;
		RTS0: pcl_load <= 1'b1;
		RST1: pcl_load <= 1'b1;
		default: pcl_load <= 1'b0;
	endcase
end

/* PCH Load */

always @(state) begin
	casex (state)
		BRK5: pch_load <= 1'b1;
		RTI2: pch_load <= 1'b1;
		RTS1: pch_load <= 1'b1;
		RST2: pch_load <= 1'b1;
		default: pch_load <= 1'b0;
	endcase
end

/* JMP Load */

always @(state) begin
	casex (state)
		ABS_JMP,
		IND_ABS_JMP: jmp_load <= 1'b1;
		default: jmp_load <= 1'b0;
	endcase
end

/* JSR Load */

always @(state) begin
	casex (state)
		JSR2: jsr_load <= 1'b1;
		default: jsr_load <= 1'b0;
	endcase
end

/* RST Load */

always @(state) begin
	casex (state)
		RST0: rst_load <= 1'b1;
		default: rst_load <= 1'b1;
	endcase
end

/* Read/Write */

always @(state) begin
	case (state)
		ZP_STORE: read_write <= write;
		ZP_WRITE: read_write <= write;
		ABS_STORE: read_write <= write;
		ABS_WRITE: read_write <= write;
		IND_ZP_STORE: read_write <= write;
		PUSH: read_write <= write;
		JSR0: read_write <= write;
		JSR1: read_write <= write;
		BRK0: read_write <= write;
		BRK1: read_write <= write;
		BRK2: read_write <= write;
		default: read_write <= read;
	endcase
end

/* Write Select */

always @(state) begin
	case (state)
		ZP_WRITE,
		ABS_WRITE: write_select <= 3'b001; // Result
		JSR0: write_select <= 3'b011; // PCH
		JSR1: write_select <= 3'b010; // PCL
		BRK0: write_select <= 3'b011; // PCH
		BRK1: write_select <= 3'b010; // PCL
		BRK2: write_select <= 3'b100; // Flags
		default: write_select <= 3'b000; // ALU
	endcase
end

/* Address Select */

always @(state) begin
	case (state)
		FETCH: address_select <= PC;
		IM0: address_select <= PC;
		ZP0: address_select <= PC;
		ZP1: address_select <= ZERO;
		ZP_STORE: address_select <= ZERO;
		ABS0: address_select <= PC;
		ABS1: address_select <= PC;
		ABS2: address_select <= ABS;
		ABS_STORE: address_select <= ABS;
		ABS_JMP: address_select <= PC;
		IND_ZP0: address_select <= PC;
		IND_ZP1: address_select <= IND_ZERO_0;
		IND_ZP2: address_select <= IND_ZERO_1;
		IND_ZP3: address_select <= ABS;
		IND_ZP_STORE: address_select <= ABS;
		IND_ABS0: address_select <= PC;
		IND_ABS1: address_select <= PC;
		IND_ABS2: address_select <= IND_ABS_0;
		IND_ABS_JMP: address_select <= IND_ABS_1;
		PUSH: address_select <= STACK;
		PULL: address_select <= STACK;
		JSR0: address_select <= STACK;
		JSR1: address_select <= STACK;
		BRK0: address_select <= STACK;
		BRK1: address_select <= STACK;
		BRK2: address_select <= STACK;
		BRK4: address_select <= IVL;
		BRK5: address_select <= IVH;
		RTI0: address_select <= STACK;
		RTI1: address_select <= STACK;
		RTI2: address_select <= STACK;
		RTS0: address_select <= STACK;
		RTS1: address_select <= STACK;
		RST1: address_select <= RVL;
		RST2: address_select <= RVH;
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
		8'b0100_10x0,
		8'b00x1_x010,
		8'bx1x1_0010,
		8'bxx01_0010,
		8'b0xx0_1010,
		8'b1010_10x0,
		8'b00xx_x10x,
		8'bx1xx_xx01,
		8'bxx0x_xx01,
		8'b0xxx_xx01: alu_select_ex <= A;
		/* ADC, AND, ASL A, BBR, BBS,
		BIT, CMP, DEC A, EOR, INC A, 
		LSR A, ORA, PHA, ROL A, ROR A, 
		SBC, STA, TAX, TAY, TRB, TSB */
		
		8'bxxx1_0000,
		8'b100x_0000,
		8'b000x_1000,
		8'bx1x1_x000,
		8'bxx11_x000: alu_select_ex <= F;
		/* BCC, BCS, BEQ, BMI, BNE, 
		BPL, BRA, BVC, BVS, CLC, CLD, 
		CLI, CLV, PHP, SEC, SED, SEI */
		
		8'b1010_0xx0,
		8'b101x_x1x0,
		8'b101x_xx01,
		8'b0x10_1000,
		8'bx111_1x10,
		8'b0xxx_x110,
		8'bx1xx_x110,
		8'b101x_0x10: alu_select_ex <= M;
		/* ASL, DEC, INC, LDA, LDX, 
		LDY, LSR, PLA, PLP, PLX, PLY, 
		RMB, ROL, ROR, SMB */
		
		8'b1000_x110,
		8'b1110_xx00,
		8'b100x_0110,
		8'b1x0x_1010: alu_select_ex <= X;
		/* CPX, DEX, INX, PHX, STX, TXA, TXS */
		
		8'b1x00_x100,
		8'b0101_1010,
		8'b100x_0100,
		8'b100x_1000,
		8'b1100_xx00: alu_select_ex <= Y;
		/* CPY, DEY, INY, PHY, STY, TYA */
		
		8'b011x_0100,
		8'b1001_11x0: alu_select_ex <= Z;
		/* STZ */
		
		8'b1011_1010: alu_select_ex <= SP;
		/* TSX */
		
		default: alu_select_ex <= M;
	endcase
end
		
		
		
		
		


always @(state, alu_select_ad, alu_select_ex) begin
	case (state)
		IM0: alu_select <= alu_select_ex;
		ZP0: alu_select <= alu_select_ad;
		ZP1: alu_select <= alu_select_ex;
		ABS0: alu_select <= alu_select_ad;
		ABS1: alu_select <= Z;
		ABS2: alu_select <= alu_select_ex;
		
		IND_ZP0: if (alu_select_ad == X) alu_select <= alu_select_ad;
					else alu_select <= Z;
		IND_ZP1: if (alu_select_ad == Y) alu_select <= alu_select_ad;
					else alu_select <= Z;
		IND_ZP2: alu_select <= Z;

		IND_ZP3: alu_select <= alu_select_ex;
		
		IND_ABS0: alu_select <= alu_select_ad;
		IND_ABS1: alu_select <= Z;
		IND_ABS2: alu_select <= Z;
		
		default: alu_select <= alu_select_ex;
	endcase
end




/* ALU Opcode */

always @(opcode_reg) begin
	casex (opcode_reg)
		8'b0111_0010,
		8'b011x_xx01: alu_opcode_ex <= 6'b000010; // ADC
		
		8'b0011_0010,
		8'b001x_xx01: alu_opcode_ex <= 6'b000011; // AND
		
		8'b0000_1x10,
		8'b000x_x110: alu_opcode_ex <= 6'b000100; // ASL
		
		8'b1000_1001,
		8'b001x_x100: alu_opcode_ex <= 6'b000101; // BIT
		
		8'b1001_0000,
		8'b0000_1111: alu_opcode_ex <= 6'b000110; // BBR0, BCC
		
		8'b1101_0000,
		8'b0001_1111: alu_opcode_ex <= 6'b000111; // BBR1, BNE
		
		8'b0010_1111: alu_opcode_ex <= 6'b001000; // BBR2
		
		8'b0011_1111: alu_opcode_ex <= 6'b001001; // BBR3
		
		8'b0100_1111: alu_opcode_ex <= 6'b001010; // BBR4
		
		8'b0101_1111: alu_opcode_ex <= 6'b001011; // BBR5
		
		8'b0101_0000,
		8'b0110_1111: alu_opcode_ex <= 6'b001100; // BBR6, BVC
		
		8'b0001_0000,
		8'b0111_1111: alu_opcode_ex <= 6'b001101; // BBR7, BPL

		8'b1011_0000,
		8'b1000_1111: alu_opcode_ex <= 6'b001110; // BBS0, BCS
		
		8'b1111_0000,
		8'b1001_1111: alu_opcode_ex <= 6'b001111; // BBS1, BEQ
		
		8'b1010_1111: alu_opcode_ex <= 6'b010000; // BBS2
		
		8'b1011_1111: alu_opcode_ex <= 6'b010001; // BBS3
		
		8'b1100_1111: alu_opcode_ex <= 6'b010010; // BBS4
		
		8'b1101_1111: alu_opcode_ex <= 6'b010011; // BBS5
		
		8'b0111_0000,
		8'b1110_1111: alu_opcode_ex <= 6'b010100; // BBS6, BVS
		
		8'b0011_0000,
		8'b1111_1111: alu_opcode_ex <= 6'b010101; // BBS7, BMI
		
		8'b1000_0000: alu_opcode_ex <= 6'b010110; // BRA
		
		8'b0001_1000: alu_opcode_ex <= 6'b010111; // CLC
		
		8'b0101_1000: alu_opcode_ex <= 6'b011000; // CLI
		
		8'b1101_1000: alu_opcode_ex <= 6'b011001; // CLD
		
		8'b1011_1000: alu_opcode_ex <= 6'b011010; // CLV
		
		8'b1101_0010,
		8'b11x0_x100,
		8'b11x0_0x00,
		8'b110x_xx01: alu_opcode_ex <= 6'b011011; // CMP, CPX, CPY
		
		8'b0011_1010,
		8'b1000_1000,
		8'b110x_x110,
		8'b1100_1x10: alu_opcode_ex <= 6'b011100; // DEC, DEX, DEY
		
		8'b0101_0010,
		8'b010x_xx01: alu_opcode_ex <= 6'b011101; // EOR
		
		8'b0001_1010,
		8'b11x0_1000,
		8'b111x_x110: alu_opcode_ex <= 6'b011110; // INC, INX, INY
		
		8'b1010_0xx0,
		8'bx111_1010,
		8'b0x10_1000,
		8'b101x_0x10,
		8'b101x_xx01,
		8'b101x_x1x0: alu_opcode_ex <= 6'b011111; // LDA, LDX, LDY, PLA, PLP, PLX, PLY
		
		8'bx101_1010,
		8'b100x_0x01,
		8'b1001_1x0x,
		8'b100x_xx10,
		8'b01xx_0100,
		8'b0x00_1000,
		8'b10xx_101x,
		8'b1010_10x0,
		8'b100x_x10x: alu_opcode_ex <= 6'b100000; // PHA, PHP, PHX, PHY, STA, STX, STY, STZ, TAX, TAY, TSX, TXA, TXS, TYA
		
		8'b0100_1x10,
		8'b010x_x110: alu_opcode_ex <= 6'b100001; // LSR
		
		8'b0001_0010,
		8'b000x_xx01: alu_opcode_ex <= 6'b100010; // ORA
		
		8'b0000_0111: alu_opcode_ex <= 6'b100011; // RMB0
		
		8'b0001_0111: alu_opcode_ex <= 6'b100100; // RMB1
		
		8'b0010_0111: alu_opcode_ex <= 6'b100101; // RMB2
		
		8'b0011_0111: alu_opcode_ex <= 6'b100110; // RMB3
		
		8'b0100_0111: alu_opcode_ex <= 6'b100111; // RMB4
		
		8'b0101_0111: alu_opcode_ex <= 6'b101000; // RMB5
		
		8'b0110_0111: alu_opcode_ex <= 6'b101001; // RMB6
		
		8'b0111_0111: alu_opcode_ex <= 6'b101010; // RMB7
		
		8'b0010_1x10,
		8'b001x_x110: alu_opcode_ex <= 6'b101011; // ROL
		
		8'b0110_1x10,
		8'b011x_x110: alu_opcode_ex <= 6'b101100; // ROR
		
		8'b1111_0010,
		8'b111x_xx01: alu_opcode_ex <= 6'b101101; // SBC
		
		8'b0011_1000: alu_opcode_ex <= 6'b101110; // SEC
		
		8'b0111_1000: alu_opcode_ex <= 6'b101111; // SEI
		
		8'b1111_1000: alu_opcode_ex <= 6'b110000; // SED
		
		8'b1000_0111: alu_opcode_ex <= 6'b110001; // SMB0
		
		8'b1001_0111: alu_opcode_ex <= 6'b110010; // SMB1
		
		8'b1010_0111: alu_opcode_ex <= 6'b110011; // SMB2
		
		8'b1011_0111: alu_opcode_ex <= 6'b110100; // SMB3
		
		8'b1100_0111: alu_opcode_ex <= 6'b110101; // SMB4
		
		8'b1101_0111: alu_opcode_ex <= 6'b110110; // SMB5
		
		8'b1110_0111: alu_opcode_ex <= 6'b110111; // SMB6
		
		8'b1111_0111: alu_opcode_ex <= 6'b111000; // SMB7
		
		8'b0001_x100: alu_opcode_ex <= 6'b111001; // TRB
		
		8'b0000_x100: alu_opcode_ex <= 6'b111010; // TSB
		
		8'b0000_0000: alu_opcode_ex <= 6'b111011; // BRK
		
		8'b0100_0000: alu_opcode_ex <= 6'b111110; // RTI
		
		default: alu_opcode_ex <= 6'b100000;
		
	endcase
end

always @(state, alu_opcode_ex) begin
	case (state)
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
		IND_ABS_JMP: alu_opcode <= ADR1;
		BRANCH_CHECK: alu_opcode <= alu_opcode_ex;
		BRK3: alu_opcode <= alu_opcode_ex;
		RTI0: alu_opcode <= alu_opcode_ex;
		
		default: alu_opcode <= 6'b100000;
	endcase
end



endmodule		

				
