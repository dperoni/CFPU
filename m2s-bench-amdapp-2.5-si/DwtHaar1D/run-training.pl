use File::Copy;

#@benchs = (10, 100, 500, 1000, 5000);
@benchs = (10000, 100000, 1000000);
@fifo_list = (180000);

system("mkdir trained-data");

foreach $item (@benchs)
{
    foreach $length (@fifo_list)
    {
        system("rm -rf *.txt *.rep");

        #copy("../Caltech/$item/image_0001.jpg", "./images/0.jpg");
        #system ("convert ./images/0.jpg -resize 256 ./images/0.bmp");
        system("~/approximate_associative_mem/multi2sim-4.2/bin/m2s --si-sim detailed --si-fifo-length $length --si-profiling $length --si-config conf DwtHaar1D --load DwtHaar1D_Kernels.bin -x $item");
        
        $temp = "./trained-data/unmapped"."_$length"."_$item.rep";
        copy("unmapped.rep", "$temp");

        $temp = "./trained-data/add"."_$length"."_$item.txt";
        copy("add.txt", "$temp");
        
        $temp = "./trained-data/mul"."_$length"."_$item.txt";
        copy("mul.txt", "$temp");

        $temp = "./trained-data/muladd"."_$length"."_$item.txt";
        copy("muladd.txt", "$temp");

        $temp = "./trained-data/sqrt"."_$length"."_$item.txt";
        copy("sqrt.txt", "$temp");

        #$temp = "./trained-data/"."$length"."_$item.bmp";
        #copy("out0.bmp", "$temp");
        
        system("rm -rf *.txt *.rep");
    }
}
