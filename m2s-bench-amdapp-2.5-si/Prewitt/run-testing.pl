use File::Copy;

@benchs = ("airplanes",
"brontosaurus",
"cougar_face",
"elephant",
"Faces_easy",
"grand_piano",
"laptop",
"nautilus",
"rhino",
"windsor_chair");

#@benchs = ("accordion","brain","cougar_body","electric_guitar","Faces","gramophone","lamp","Motorbikes","revolver","wild_cat");

@fifo_list = (512);
$dist = 0;
foreach $item (@benchs)
{
    foreach $length (@fifo_list)
    {
        system("rm -rf *.rep");

        $input_image = "../Caltech/".$item."/image_0001.jpg";
        print "$input_image\n";
        copy($input_image, "./images/0.jpg");
        system ("convert ./images/0.jpg -resize 256 ./images/0.bmp");
        system("m2s --si-sim detailed --si-fifo-length $length --si-profiling 0 --si-hamming-dist $dist --si-config conf SobelFilter --load SobelFilter_Kernels.bin > hit.rep");
        
        $temp = "./tested-data/"."$length"."_$item.rep";
        copy("hit.rep", "$temp");

        #$temp = "./tested-data/"."$length"."_$item.bmp";
        #copy("out0.bmp", "$temp");
        
        system("rm -rf *.rep");
    }
}
