use File::Copy;

@folder_lst = (1);


@fifo_list = (16); #16, 32, 64, 128, 256, 512, 1024);
$dist = 0;

@fdist = (0, 0.25, 0.125, 0.0625, 0.03125, 0.015625);



foreach $length (@fifo_list)
{
	

  foreach $item (@folder_lst)
    {


	foreach $fd (@fdist){
		system("rm -rf *.rep");




		#system("~/approximate_associative_mem/multi2sim-4.2/bin/m2s --si-sim detailed --si-fifo-length $length --si-profiling 0 --si-tcam-dist $fdist --si-config conf DwtHaar1D --load DwtHaar1D_Kernels.bin -x $item -e ");
	        system("~/approximate_associative_mem/multi2sim-4.2/bin/m2s --si-sim detailed --si-fifo-length $length --si-profiling 0 --si-tcam-dist $fd --si-config conf BlackScholes --load BlackScholes_Kernels.bin -x 1 -i 1 -e > hit.rep");
		mkdir "./tested-data/"."$fd";

		$temp = "./tested-data/"."$fd/"."$length"."_$item.rep";
		copy("hit.rep", "$temp");

	
		system("rm -rf *.rep");
	}
}
}

