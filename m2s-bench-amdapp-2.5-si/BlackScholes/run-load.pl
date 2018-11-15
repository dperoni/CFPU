use File::Copy;



@folder_lst = (1500, 2000, 5000, 5100);
@fifo_list = (32, 64);
@dist_lst = (0, 1, 2);

foreach $dist (@dist_lst)
{
    foreach $item (@folder_lst)
    {
        $dir_hit = "./hit"."_$dist";
        system("mkdir -p $dir_hit");
        foreach $length (@fifo_list)
        {
            system("rm -rf *.rep");
            system("m2s --si-sim detailed --si-fifo-length $length --si-profiling 0 --si-hamming-dist $dist --si-config conf BlackScholes --load BlackScholes_Kernels.bin -x $item -e > hit.rep");
        
            $temp = "$dir_hit"."/$length"."_$item.rep";
            copy("hit.rep", "$temp");

            print "$temp\n";
            system("rm -rf *.rep");
        }
    }
}
