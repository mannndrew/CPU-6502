module address_mux
(
	input address_select,
	input [7:0] pcl,
	input [7:0] pch,
	input [7:0] zero,
	output [15:0] address
);

assign address = (address_select == 1'b0) ? {pch, pcl} : {8'h00, zero};

endmodule
