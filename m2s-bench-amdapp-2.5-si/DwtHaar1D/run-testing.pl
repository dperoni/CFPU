use File::Copy;

@folder_lst = (20000);
#@folder_lst = (1000000, 1000010, 1000100, 1000200, 1000500, 1001000);
#@folder_lst = (1001000, 1002000, 1003000, 1005000, 1010000, 1015000);
#@folder_lst = (1015000, 1020000, 1025000, 1030000, 1035000, 1040000, 1045000, 1050000);

@fifo_list = (16, 32, 64, 128, 256, 512, 1024);
$dist = 0;

@fdist = (1000);



foreach $length (@fifo_list)
{
	

  foreach $item (@folder_lst)
    {


	foreach $fd (@fdist){
		system("rm -rf *.rep");




		#system("~/approximate_associative_mem/multi2sim-4.2/bin/m2s --si-sim detailed --si-fifo-length $length --si-profiling 0 --si-tcam-dist $fdist --si-config conf DwtHaar1D --load DwtHaar1D_Kernels.bin -x $item -e ");
	        system("~/approximate_associative_mem/multi2sim-4.2/bin/m2s --si-sim detailed --si-fifo-length $length --si-profiling 0 --si-tcam-dist $fd --si-config conf DwtHaar1D --load DwtHaar1D_Kernels.bin -x $item -e > hit.rep");
		mkdir "./tested-data/"."$fd";

		$temp = "./tested-data/"."$fd/"."$length"."_$item.rep";
		copy("hit.rep", "$temp");

	
		system("rm -rf *.rep");
	}
}
}

