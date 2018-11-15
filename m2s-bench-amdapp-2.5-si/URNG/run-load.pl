use File::Copy;

my @folder_lst = ('/home/abbas/Approximate/m2s-bench-amdapp-2.5-si/Caltech', grep -d, glob '/home/abbas/Approximate/m2s-bench-amdapp-2.5-si/Caltech/*');

@fifo_list = (4);
@dist_lst = (0, 1, 2, 3);

foreach $dist (@dist_lst)
{
foreach $item (@folder_lst)
{
    $dir_hit = "./hit"."_$dist";
    system("mkdir -p $dir_hit");
    foreach $length (@fifo_list)
    {
        system("rm -rf *.rep");
        #$input_image = $item.".jpg";
        #copy("../Faces/$input_image", "./images/0.jpg");
        
        $folder_name = substr $item, 56;
        $input_image = $item."/image_0001.jpg";
        
        copy("$input_image", "./images/0.jpg");
        system("convert ./images/0.jpg -resize 256 ./images/0.bmp");
        system("m2s --si-sim detailed --si-fifo-length $length --si-profiling 0 --si-hamming-dist $dist --si-config conf URNG --load URNG_Kernels.bin > hit.rep");
        
        $temp = "$dir_hit"."/$length"."_$folder_name.rep";
        copy("hit.rep", "$temp");

        $temp = "$dir_hit"."/$length"."_$folder_name.bmp";
        copy("out0.bmp", "$temp");
        
        print "$temp\n";
        system("rm -rf *.rep");
    }
}
}
