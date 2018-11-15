use File::Copy;


@fifo_list = (180000);

foreach $length (@fifo_list)
{
	system("rm -rf *.txt *.rep");

	system("~/approximate_associative_mem/multi2sim-4.2/bin/m2s --si-sim detailed --si-fifo-length $length --si-profiling $length  MatrixMultiplication --load MatrixMultiplication_Kernels.bin");

	$temp = "./trained-data/unmapped"."_$length.rep";
	copy("unmapped.rep", "$temp");

	$temp = "./trained-data/add"."_$length.txt";
	copy("add.txt", "$temp");

	$temp = "./trained-data/mul"."_$length.txt";
	copy("mul.txt", "$temp");

	$temp = "./trained-data/muladd"."_$length.txt";
	copy("muladd.txt", "$temp");

	$temp = "./trained-data/mad"."_$length.txt";
	copy("mad.txt", "$temp");


	$temp = "./trained-data/sqrt"."_$length.txt";
	copy("sqrt.txt", "$temp");

	system("rm -rf *.txt *.rep");
}

