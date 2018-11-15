#use File::Find::Rule;
my @array = ('/home/abbas/Approximate/m2s-bench-amdapp-2.5-si/Caltech', grep -d, glob '/home/abbas/Approximate/m2s-bench-amdapp-2.5-si/Caltech/*');
#my @array = File::Find::Rule->directory->in('/home/abbas');
foreach $item (@array)
{
    print "$item\n";
}
