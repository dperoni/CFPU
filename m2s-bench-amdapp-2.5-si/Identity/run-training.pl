use File::Copy;

@benchs = ("accordion",
"brain",
"cougar_body",
"electric_guitar",
"Faces",
"gramophone",
"lamp",
"Motorbikes",
"revolver",
"wild_cat");

@fifo_list = (180000);

foreach $item (@benchs)
{
    foreach $length (@fifo_list)
    {
        system("rm -rf *.txt *.rep");

        copy("../Caltech/$item/image_0001.jpg", "./images/0.jpg");
        system ("convert ./images/0.jpg -resize 256 ./images/0.bmp");
        system("m2s --si-sim detailed --si-fifo-length $length --si-profiling $length --si-config conf Identity --load Identity_Kernel.bin");
        
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

        $temp = "./trained-data/"."$length"."_$item.bmp";
        copy("out0.bmp", "$temp");
        
        system("rm -rf *.txt *.rep");
    }
}
