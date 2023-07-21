module control_unit
(
	input clk,
	input rst,
	input [7:0] opcode,
	input [7:0] opcode_reg,
	output reg instruction_load,
	output reg increment_pc,
	output reg a_load,
	output reg x_load,
	output reg y_load,
	output reg read_write,
	output reg address_select,
	output reg [1:0] alu_select,
	output reg [1:0] alu_opcode
);

/* Read/Write */
parameter
	read				= 1'b0,
	write				= 1'b1;


/* Address Select */
parameter
	PC					= 1'b0;

/* ALU Select */
parameter
	A					= 2'b00,
	X					= 2'b01,
	Y					= 2'b10;
	
/* Opcodes */
parameter
	ADC				= 2'b00;

/* States */
parameter
	FETCH				= 6'd0,
	IM0				= 6'd1;
	ZP0				= 6'd2;
	ZP1				= 6'd3;
	
	
reg [5:0] state;
	
	
/* State Machine */
	
always @(posedge clk, negedge rst) begin
	if (rst == 1'b0)
		state <= FETCH;
	else begin
		case (state)
			FETCH:
				casex (opcode)
					8'bxxx0_1001: state <= IM0;
					8'b11x0_0000: state <= IM0;
					8'b1010_00x0: state <= IM0;
					8'bxxx0_01xx: state <= ZP0;
					8'bxxxx_0111: state <= ZP0;
					8'b000x_1000: state <= ZP0;
					default: state <= FETCH;
				endcase
			IM0: state <= FETCH;
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
		default: increment_pc <= 1'b0;
	endcase
end

/* A Load */

always @(state) begin
	case (state)
		FETCH: a_load <= 1'b0;
		IM0: a_load <= 1'b1;
		default: a_load <= 1'b0;
	endcase
end

/* X Load */

always @(state) begin
	case (state)
		FETCH: x_load <= 1'b0;
		IM0: x_load <= 1'b0;
		default: x_load <= 1'b0;
	endcase
end

/* Y Load */

always @(state) begin
	case (state)
		FETCH: y_load <= 1'b0;
		IM0: y_load <= 1'b0;
		default: y_load <= 1'b0;
	endcase
end

/* Read/Write */

always @(state) begin
	case (state)
		FETCH: read_write <= read;
		IM0: read_write <= read;
		default: read_write <= read;
	endcase
end

/* Address Select */

always @(state) begin
	case (state)
		FETCH: address_select <= PC;
		IM0: address_select <= PC;
		default: address_select <= PC;
	endcase
end

/* ALU Select */

always @(opcode_reg) begin
	casex (opcode_reg)
		8'b01110010: alu_select <= A;
		8'b011xxx01: alu_select <= A;
		default: alu_select <= X;
	endcase
end

/* ALU Opcode */

always @(opcode_reg) begin
	casex (opcode_reg)
		8'b01110010: alu_opcode <= ADC;
		8'b011xxx01: alu_opcode <= ADC;
		default: alu_opcode <= 2'b11;
	endcase
end



endmodule		

				
