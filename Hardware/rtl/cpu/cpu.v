module cpu
(
	input clk,
	input rst,
	input [7:0] data_read,
	output read_write,
	output [7:0] data_write,
	output [15:0] address
	
//	,output [7:0] register_a 
//	,output [7:0] register_x 
//	,output [7:0] register_y 
//	,output [7:0] register_f
	,output [5:0] state
);

//assign register_a = a_out;
//assign register_x = x_out;
//assign register_y = y_out;
//assign register_f = flags_out;


// FSM Wires
wire increment_pc;
wire [1:0] sp_op;
wire sp_load;
wire instruction_load;
wire indirl_load;
wire indirh_load;
wire dirl_load;
wire dirh_load;
wire a_load;
wire x_load;
wire y_load;
wire branch_valid;
wire branch_load;
wire pcl_load;
wire pch_load;
wire jmp_load;
wire jsr_load;
wire rst_load;
wire [2:0] write_select;
wire [3:0] address_select;
wire [2:0] alu_select;
wire [5:0] alu_opcode;


// Program Counter Wires
wire carry;
wire [7:0] pcl;
wire [7:0] pch;
wire [7:0] pcl_branch;
wire [7:0] pch_branch;

// Stack Pointer Wires
wire [7:0] sp;

// Instruction Reg Wires
wire [7:0] opcode;

// Indirect Reg Wires
wire [7:0] indirl_out;
wire [7:0] indirh_out;

// Direct Reg Wires
wire [7:0] dirl_out;
wire [7:0] dirh_out;

// A Reg Wires
wire [7:0] a_out;

// X Reg Wires
wire [7:0] x_out;

// Y Reg Wires
wire [7:0] y_out;

// Result Reg Wires
wire [7:0] result_out;

// ALU Wires
wire [7:0] alu_a;
wire [7:0] alu_out;
wire [7:0] flags_ena;
wire [7:0] flags_in;
wire [7:0] flags_out;



/*---------------------------------Registers---------------------------------*/


program_counter pc_low
(
	.clk(clk),
	.increment(increment_pc),
	.branch_load(branch_load),
	.pc_load(pcl_load),
	.jmp_load(jmp_load),
	.jsr_load(jsr_load),
	.branch(pcl_branch),
	.pc_addr(alu_out),
	.jmp_addr(dirl_out),
	.jsr_addr(dirl_out),
	.carry(carry),
	.pc(pcl)
);

program_counter pc_high
(
	.clk(clk),
	.increment(carry),
	.branch_load(branch_load),
	.pc_load(pch_load),
	.jmp_load(jmp_load),
	.jsr_load(jsr_load),
	.branch(pch_branch),
	.pc_addr(alu_out),
	.jmp_addr(alu_out),
	.jsr_addr(dirh_out),
	.pc(pch)
);

stack_pointer sp_reg
(
	.clk(clk),
	.reset(rst_load),
	.sp_load(sp_load),
	.sel(sp_op),
	.d(alu_out),
	.sp(sp)
);

register instruction_reg
(
	.clk(clk),
	.reset(1'b1),
	.ena(instruction_load),
	.d(data_read),
	.q(opcode)
);

register indirl_reg
(
	.clk(clk),
	.reset(1'b1),
	.ena(indirl_load),
	.d(alu_out),
	.q(indirl_out)
);

register indirh_reg
(
	.clk(clk),
	.reset(1'b1),
	.ena(indirh_load),
	.d(alu_out),
	.q(indirh_out)
);

register dirl_reg
(
	.clk(clk),
	.reset(1'b1),
	.ena(dirl_load),
	.d(alu_out),
	.q(dirl_out)
);

register dirh_reg
(
	.clk(clk),
	.reset(1'b1),
	.ena(dirh_load),
	.d(alu_out),
	.q(dirh_out)
);

register a_reg
(
	.clk(clk),
	.reset(rst_load),
	.ena(a_load),
	.d(alu_out),
	.q(a_out)
);

register x_reg
(
	.clk(clk),
	.reset(rst_load),
	.ena(x_load),
	.d(alu_out),
	.q(x_out)
);

register y_reg
(
	.clk(clk),
	.reset(rst_load),
	.ena(y_load),
	.d(alu_out),
	.q(y_out)
);

flag_register f_reg
(
	.clk(clk),
	.reset(rst_load),
	.ena(flags_ena),
	.d(flags_in),
	.q(flags_out)
);

register result
(
	.clk(clk),
	.reset(1'b1),
	.ena(1'b1),
	.d(alu_out),
	.q(result_out)
);

/*---------------------------------MUXs--------------------------------------*/


arithmetic_mux mux1
(
	.select(alu_select),
	.a(a_out),
	.f(flags_out),
	.m(data_read),
	.sp(sp),
	.x(x_out),
	.y(y_out),
	.alu_a(alu_a)
);

address_mux mux2
(
	.address_select(address_select),
	.pcl(pcl),
	.pch(pch),
	.sp(sp),
	.dirl(dirl_out),
	.dirh(dirh_out),
	.indirl(indirl_out),
	.indirh(indirh_out),
	.address(address)
);

write_mux mux3
(
	.select(write_select),
	.alu(alu_out),
	.result(result_out),
	.pcl(pcl),
	.pch(pch),
	.flags(flags_out),
	.data_write(data_write)
);


/*---------------------------------Units-------------------------------------*/


control_unit clu
(
	.clk(clk),
	.rst(rst),
	.opcode(data_read),
	.opcode_reg(opcode),
	.instruction_load(instruction_load),
	.increment_pc(increment_pc),
	.sp_op(sp_op),
	.sp_load(sp_load),
	.indirl_load(indirl_load),
	.indirh_load(indirh_load),
	.dirl_load(dirl_load),
	.dirh_load(dirh_load),
	.a_load(a_load),
	.x_load(x_load),
	.y_load(y_load),
	.branch_valid(branch_valid),
	.branch_load(branch_load),
	.pcl_load(pcl_load),
	.pch_load(pch_load),
	.jmp_load(jmp_load),
	.jsr_load(jsr_load),
	.rst_load(rst_load),
	.read_write(read_write),
	.write_select(write_select),
	.address_select(address_select),
	.alu_select(alu_select),
	.alu_opcode(alu_opcode)
	,.fsm(state)
);

arithmetic_unit alu
(
	.clk(clk),
	.alu_opcode(alu_opcode),
	.alu_a(alu_a),
	.alu_b(data_read),
	.flags_in(flags_out),
	.alu_out(alu_out),
	.flags_out(flags_in),
	.flags_ena(flags_ena),
	.branch_valid(branch_valid)
);

branching_unit bru
(
	.clk(clk),
	.data_read(data_read),
	.pcl(pcl),
	.pch(pch),
	.pcl_branch(pcl_branch),
	.pch_branch(pch_branch)
);


endmodule
