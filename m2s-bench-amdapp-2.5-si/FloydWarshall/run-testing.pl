use File::Copy;


@fifo_list = (16, 32, 64, 128, 256, 512, 1024);
$dist = 0;

@fdist = (0, 0.1, 0.2, 0.3, 0.5, 0.6, 0.8, 1, 2, 3, 5, 10, 20, 50, 100);

foreach $length (@fifo_list)
{
	foreach $fd (@fdist){
		system("rm -rf *.rep");




		system("~/approximate_associative_mem/multi2sim-4.2/bin/m2s --si-sim detailed --si-fifo-length $length --si-profiling 0 --si-hamming-dist $dist --si-tcam-dist $fd --si-config conf FFT --load FFT_Kernels.bin -e > hit.rep");
	
		mkdir "./tested-data/"."$fd";

		$temp = "./tested-data/"."$fd/"."$length.rep";
		copy("hit.rep", "$temp");

	
		system("rm -rf *.rep");
	}
}

