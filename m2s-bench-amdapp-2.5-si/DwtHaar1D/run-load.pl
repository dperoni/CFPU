use File::Copy;


#@folder_lst = (1000000, 1000010, 1000100, 1000200, 1000500, 1001000);
#@folder_lst = (1001000, 1002000, 1003000, 1005000, 1010000, 1015000);
@folder_lst = (1015000, 1020000, 1025000, 1030000, 1035000, 1040000, 1045000, 1050000);

@fifo_list = (64, 32);
@dist_lst = (0, 1);

foreach $dist (@dist_lst)
{
    foreach $item (@folder_lst)
    {
        $dir_hit = "./hit"."_$dist";
        system("mkdir -p $dir_hit");
        foreach $length (@fifo_list)
        {
            system("rm -rf *.rep");
            system("m2s --si-sim detailed --si-fifo-length $length --si-profiling 0 --si-hamming-dist $dist --si-config conf DwtHaar1D --load DwtHaar1D_Kernels.bin -x $item -e > hit.rep");
        
            $temp = "$dir_hit"."/$length"."_$item.rep";
            copy("hit.rep", "$temp");

            print "$temp\n";
            system("rm -rf *.rep");
        }
    }
}
