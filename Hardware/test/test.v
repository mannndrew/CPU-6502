//module test
//(
//	input RWB,	// 0-Write 1-Read
//	inout Data_Bus,
//	inout D
//);
//
//assign D = (RWB) ? D : Data_Bus;
//assign Data_Bus = (RWB) ? D : Data_Bus;
//
//endmodule



//module test (
//  input   WRE,
//  input   [7:0] inp,
//  output  [7:0] outp,
//  inout   [7:0] D
//);
//
//reg [7:0] bidir_out; // Separate signal for bidir output
//
//always @(WRE or bidir) begin
//  if (WRE)
//    bidir_out <= bidir; // Assign inp to bidir_out when oe is asserted
//	else
//	bidir_out <= 8'd0;
//end
//
//assign bidir = (WRE) ? 8'bz : inp;
//assign outp = bidir_out;
//
//endmodule



//module Data_Bus_Buffer
//(
//	inout reg [7:0] D,
//	inout reg [7:0] Data_Bus,
//	input RWB,
//	input BE
//);
//
//always @ (D, Data_Bus, RWB, BE)
//begin
//	if (BE == 1'b1)
//		begin
//		D = (RWB) ? 8'bz : Data_Bus;
//		Data_Bus = (RWB) ? D : 8'bz;
//		end
//		
//	else
//		begin
//		D = 8'bz;
//		Data_Bus = 8'bz;
//		end
//end
//endmodule



module Data_Bus_Buffer
(
	inout [7:0] D,
	inout [7:0] Data_Bus,
	input RWB,
	input BE
);

assign D = 	(BE) ? (RWB) ? 8'bz : Data_Bus : 8'bz;
assign Data_Bus = (BE) ? (RWB) ? D : 8'bz : 8'bz;

endmodule
