use File::Copy;

@benchs = ("image_0022", "image_0042", "image_0052", "image_0072", "image_0092", "image_0122", "image_0142", "image_0162", "image_0168", "image_0182", "image_0199", "image_0227", "image_0257", "image_0274", "image_0288", "image_0320", "image_0339", "image_0365", "image_0384", "image_0395", "image_0417", "image_0425");

#@benchs = ("image_0042");

@fifo_list = (180000);
$prof = 180000;

foreach $item (@benchs)
{
    foreach $length (@fifo_list)
    {
        system("rm -rf *.txt *.rep");

        $input_image = $item.".jpg";
        copy("../Faces/$input_image", "./images/0.jpg");
        system ("convert ./images/0.jpg -resize 256 ./images/0.bmp");
        system("m2s --si-sim detailed --si-fifo-length $length --si-profiling $prof --si-config conf SobelFilter --load SobelFilter_Kernels.bin");
        $temp = "./result/unmapped_$prof"."_$length"."_$item.rep";
        copy("unmapped.rep", "$temp");

        $temp = "./result/add_$prof"."_$length"."_$item.txt";
        copy("add.txt", "$temp");
        
        $temp = "./result/mul_$prof"."_$length"."_$item.txt";
        copy("mul.txt", "$temp");

        $temp = "./result/muladd_$prof"."_$length"."_$item.txt";
        copy("muladd.txt", "$temp");

        $temp = "./result/sqrt_$prof"."_$length"."_$item.txt";
        copy("sqrt.txt", "$temp");

        #$temp = "./result/recip_$prof"."_$length"."_$item.txt";
        #copy("recip.txt", "$temp");

        #$temp = "./result/flp2int_$prof"."_$length"."_$item.txt";
        #copy("flp2int.txt", "$temp");
    }
}
