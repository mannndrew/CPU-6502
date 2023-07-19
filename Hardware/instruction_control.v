module instruction_control
(
	input clk,
	input [7:0] opcode,
	output reg instruction_load,
	output reg alu_load,
	output reg alu_mux,
	output reg alu_data
);

reg [5:0] state;

parameter
	ADC				= 8'd0;

parameter
	ADC_I				= 8'h69,
	ADC_ZP			= 8'h65,
	ADC_ZP_X			= 8'h75,
	ADC_ZPI			= 8'h72,
	ADC_ZPI_X		= 8'h61,
	ADC_ZPI_Y		= 8'h71,
	ADC_A				= 8'h6d,
	ADC_A_X			= 8'h7d,
	ADC_A_Y			= 8'h79;
	
parameter
	FETCH				= 6'd0,
	EXECUTE			= 6'd1;
	
	
	
always @(posedge clk, negedge reset) 
begin
	if (reset == 1'b0)
		state <= FETCH
		
	else begin
		case (state)
			DECODE:
				case (opcode)
					ADC_I: state <= FETCH;
					
	end
end



always @(state) begin
	if (state == FETCH)
		instruction_load = 1'b1;
	else
		instruction_load = 1'b0;
end



always @(state) begin
	case (state)
		DECODE:
end












endmodule		

				
