use File::Copy;


@fifo_list = (16, 32, 64, 128, 256, 512, 1024);
$dist = 0;

@fdist = (1000);

system("mkdir tested-data");

foreach $length (@fifo_list)
{
	foreach $fd (@fdist){
		system("rm -rf *.rep");




		system("~/approximate_associative_mem/multi2sim-4.2/bin/m2s --si-sim detailed --si-fifo-length $length --si-profiling 0 --si-hamming-dist $dist --si-tcam-dist $fd QuasiRandomSequence --load QuasiRandomSequence_Kernels.bin -e > hit.rep");
	
		mkdir "./tested-data/"."$fd";

		$temp = "./tested-data/"."$fd/"."$length.rep";
		copy("hit.rep", "$temp");

	
		system("rm -rf *.rep");
	}
}

