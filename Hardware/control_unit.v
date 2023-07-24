module control_unit
(
	input clk,
	input rst,
	input [7:0] opcode,
	input [7:0] opcode_reg,
	output reg instruction_load,
	output reg increment_pc,
	output reg indirl_load,
	output reg indirh_load,
	output reg dirl_load,
	output reg dirh_load,
	output reg a_load,
	output reg x_load,
	output reg y_load,
	output reg read_write,
	output reg [1:0] address_select,
	output reg [1:0] alu_select,
	output reg [1:0] alu_opcode
);

/* Read/Write */
parameter
	read				= 1'b0,
	write				= 1'b1;


/* Address Select */
parameter
	PC					= 2'b00,
	ZERO				= 2'b01,
	ABS				= 2'b10;

/* ALU Select */
parameter
	A					= 2'b00,
	X					= 2'b01,
	Y					= 2'b10,
	Z					= 2'b11;
	
/* Opcodes */
parameter
	ADR0				= 2'b00,
	ADR1				= 2'b01,
	ADC				= 2'b10,
	LDX				= 2'b11;

/* States */
parameter
	FETCH				= 6'd0,
	IM0				= 6'd1,
	ZP0				= 6'd2,
	ZP1				= 6'd3,
	ABS0				= 6'd4,
	ABS1				= 6'd5,
	ABS2				= 6'd6;
	
	
reg [5:0] state;
reg [1:0] alu_select_ad;
reg [1:0] alu_select_ex;
reg [1:0] alu_opcode_ex;
	
	
/* State Machine */
	
always @(posedge clk, negedge rst) begin
	if (rst == 1'b0)
		state <= FETCH;
	else begin
		case (state)
			FETCH:
				casex (opcode)
					8'bxxx0_1001,
					8'b11x0_0000,
					8'b1010_00x0: state <= IM0;
					8'bxxx0_01xx,
					8'bxxxx_0x11,
					8'bxxxx_01xx: state <= ZP0;
					8'bxxx0_1101,
					8'bxxx0_1110,
					8'bxx0x_1100,
					8'bx0x0_11x0,
					8'b1xx0_11x0: state <= ABS0;
					default: state <= FETCH;
				endcase
			IM0: state <= FETCH;
			ZP0: state <= ZP1;
			ZP1: state <= FETCH;
			ABS0: state <= ABS1;
			ABS1: state <= ABS2;
			ABS2: state <= FETCH;
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
		ZP1: increment_pc <= 1'b0;
		ABS0: increment_pc <= 1'b1;
		ABS1: increment_pc <= 1'b1;
		ABS2: increment_pc <= 1'b0;
		default: increment_pc <= 1'b0;
	endcase
end

/* Indirect Low Load */

always @(state) begin
	case (state)
		FETCH: indirl_load <= 1'b0;
		IM0: indirl_load <= 1'b0;
		ZP0: indirl_load <= 1'b0;
		ZP1: indirl_load <= 1'b0;
		ABS0: indirl_load <= 1'b0;
		ABS1: indirl_load <= 1'b0;
		ABS2: indirl_load <= 1'b0;
		default: indirl_load <= 1'b0;
	endcase
end

/* Indirect High Load */

always @(state) begin
	case (state)
		FETCH: indirh_load <= 1'b0;
		IM0: indirh_load <= 1'b0;
		ZP0: indirh_load <= 1'b0;
		ZP1: indirh_load <= 1'b0;
		ABS0: indirh_load <= 1'b0;
		ABS1: indirh_load <= 1'b0;
		ABS2: indirh_load <= 1'b0;
		default: indirh_load <= 1'b0;
	endcase
end

/* Direct Low Load */

always @(state) begin
	case (state)
		FETCH: dirl_load <= 1'b0;
		IM0: dirl_load <= 1'b0;
		ZP0: dirl_load <= 1'b1;
		ZP1: dirl_load <= 1'b0;
		ABS0: dirl_load <= 1'b1;
		ABS1: dirl_load <= 1'b0;
		ABS2: dirl_load <= 1'b0;
		default: dirl_load <= 1'b0;
	endcase
end

/* Direct High Load */

always @(state) begin
	case (state)
		FETCH: dirh_load <= 1'b0;
		IM0: dirh_load <= 1'b0;
		ZP0: dirh_load <= 1'b0;
		ZP1: dirh_load <= 1'b0;
		ABS0: dirh_load <= 1'b0;
		ABS1: dirh_load <= 1'b1;
		ABS2: dirh_load <= 1'b0;
		default: dirh_load <= 1'b0;
	endcase
end

/* A Load */

always @(state) begin
	case (state)
		FETCH: a_load <= 1'b0;
		IM0: a_load <= 1'b1;
		ZP0: a_load <= 1'b0;
		ZP1: a_load <= 1'b1;
		ABS0: a_load <= 1'b0;
		ABS1: a_load <= 1'b0;
		ABS2: a_load <= 1'b1;
		default: a_load <= 1'b0;
	endcase
end

/* X Load */

always @(state) begin
	case (state)
		FETCH: x_load <= 1'b0;
		IM0: x_load <= 1'b0;
		ZP0: x_load <= 1'b0;
		ZP1: x_load <= 1'b0;
		ABS0: x_load <= 1'b0;
		ABS1: x_load <= 1'b0;
		ABS2: x_load <= 1'b0;
		default: x_load <= 1'b0;
	endcase
end

/* Y Load */

always @(state) begin
	case (state)
		FETCH: y_load <= 1'b0;
		IM0: y_load <= 1'b0;
		ZP0: y_load <= 1'b0;
		ZP1: y_load <= 1'b0;
		ABS0: y_load <= 1'b0;
		ABS1: y_load <= 1'b0;
		ABS2: y_load <= 1'b0;
		default: y_load <= 1'b0;
	endcase
end

/* Read/Write */

always @(state) begin
	case (state)
		FETCH: read_write <= read;
		IM0: read_write <= read;
		ZP0: read_write <= read;
		ZP1: read_write <= read;
		ABS0: read_write <= read;
		ABS1: read_write <= read;
		ABS2: read_write <= read;
		default: read_write <= read;
	endcase
end

/* Address Select */

always @(state) begin
	case (state)
		FETCH: address_select <= PC;
		IM0: address_select <= PC;
		ZP0: address_select <= PC;
		ZP1: address_select <= ZERO;
		ABS0: address_select <= PC;
		ABS1: address_select <= PC;
		ABS2: address_select <= ABS;
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
		8'b011x_xx01: alu_select_ex <= A; //ADC
		default: alu_select_ex <= Z;
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
		default: alu_select <= Z;
	endcase
end




/* ALU Opcode */

always @(opcode_reg) begin
	casex (opcode_reg)
		8'b01110010,
		8'b011xxx01: alu_opcode_ex <= ADC; // ADC
		default: alu_opcode_ex <= 2'b01;
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
		default: alu_opcode <= 2'b01;
	endcase
end



endmodule		

				
