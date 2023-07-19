module address_mux
(
	input address_select,
	input [7:0] pcl,
	input [7:0] pch,
	output [15:0] address
);

assign address = (address_select == 1'b1) ? {pch, pcl} : 16'b0;

endmodule
