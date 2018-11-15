use File::Copy;

#@benchs = ("airplanes", "brontosaurus", "cougar_face", "elephant", "Faces_easy", "grand_piano", "laptop", "nautilus", "rhino", "windsor_chair");

#@benchs = ("accordion","brain","cougar_body","electric_guitar","Faces","gramophone","lamp","Motorbikes","revolver","wild_cat", "airplanes", "brontosaurus", "cougar_face", "elephant", "Faces_easy", "grand_piano", "laptop", "nautilus", "rhino", "windsor_chair");
@benchs = ("accordion");
@fifo_list = (32);
$dist = 0;
@fdist = (0.0625);
@buffsize = (0, 8, 16, 32);

foreach $item (@benchs)
{
    foreach $length (@fifo_list)
    {
	foreach $fd (@fdist){
		mkdir "./tested-data/"."$fd/";
		foreach $bf (@buffsize){
		system("rm -rf *.rep");

		$input_image = "../Caltech/".$item."/image_0001.jpg";
		print "$input_image\n";
		copy($input_image, "./images/0.jpg");
		system ("convert ./images/0.jpg -resize 256 ./images/0.bmp");
		system("~/approximate_associative_mem_gpu/multi2sim-4.2/bin/m2s --si-sim detailed --si-fifo-length $length --si-profiling 0 --si-hamming-dist $dist --si-tcam-dist $fd --si-abuff-size $bf --si-config conf Sharpen --load Sharpen_Kernel.bin > hit.rep");
		
		mkdir "./tested-data/"."$fd/"."$length-$bf";

		$temp = "./tested-data/"."$fd/$length-$bf/"."_$item.rep";
		copy("hit.rep", "$temp");

		$temp = "./tested-data/"."$fd/$length-$bf/"."_$item.bmp";
		copy("out0.bmp", "$temp");

		system("rm -rf *.rep");
		}		
	}
    }
}