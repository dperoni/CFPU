use File::Copy;

@benchs = (10000, 100000, 1000000);

@fifo_list = (180000);
$N_TOP = 2048;

system("rm -rf *.txt");
open FILE_W_ADD, ">", "add.txt" or die $!;
open FILE_W_MUL, ">", "mul.txt" or die $!;
open FILE_W_MULADD, ">", "muladd.txt" or die $!;
open FILE_W_SQRT, ">", "sqrt.txt" or die $!;
open FILE_W_MAD, ">", "mad.txt" or die $!;


foreach $length (@fifo_list)
{
    for($cut = 1; $cut <= $N_TOP; $cut = $cut + 1)
    {
        foreach $item (@benchs)
        {
            $temp_add = "./trained-data/add"."_$length"."_$item.txt";
            $temp_mul = "./trained-data/mul"."_$length"."_$item.txt";
            $temp_muladd = "./trained-data/muladd"."_$length"."_$item.txt";
            $temp_sqrt = "./trained-data/sqrt"."_$length"."_$item.txt";

            open my $info, $temp_add or die "Could not open $temp_add: $!";
            my $line;
            while ($line = <$info>)  {   
                last if $. == $cut;
            }
            print FILE_W_ADD $line;   
            close $info;

            open my $info, $temp_mul or die "Could not open $temp_mul: $!";
            while ($line = <$info>)  {   
                last if $. == $cut;
            }
            print FILE_W_MUL $line;   
            close $info;

            open my $info, $temp_muladd or die "Could not open $temp_muladd: $!";
            while ($line = <$info>)  {   
                last if $. == $cut;
            }
            print FILE_W_MULADD $line;   
            close $info;

            open my $info, $temp_sqrt or die "Could not open $temp_sqrt: $!";
            while ($line = <$info>)  {
                last if $. == $cut;
            }
            print FILE_W_SQRT $line;
            close $info;
        }
    }
}

close FILE_W_ADD;
close FILE_W_MUL;
close FILE_W_SQRT;
close FILE_W_MULADD;
close FILE_W_MAD;
