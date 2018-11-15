use File::Copy;

#@benchs = ("airplanes", "brontosaurus", "cougar_face", "elephant", "Faces_easy", "grand_piano", "laptop", "nautilus", "rhino", "windsor_chair");

#@benchs = ("accordion","brain","cougar_body","electric_guitar","Faces","gramophone","lamp","Motorbikes","revolver","wild_cat");

@benchs = ("airplanes", "brontosaurus", "cougar_face", "elephant", "Faces_easy", "grand_piano", "laptop", "nautilus", "rhino", "windsor_chair", "accordion","brain","cougar_body","electric_guitar","Faces","gramophone","lamp","Motorbikes","revolver","wild_cat");

#@benchs = ("brain");

@fifo_list = (16);
$dist = 0;

@fdist = (0, 0.1, 0.2, 0.3, 0.5, 0.6, 0.8, 1, 2, 3, 5, 10, 20, 50, 100);
foreach $item (@benchs)
{
    foreach $length (@fifo_list)
    {
	foreach $fd (@fdist){
		system("rm -rf *.rep");

		$input_image = "../Caltech/".$item."/image_0001.jpg";
		print "$input_image\n";
		copy($input_image, "./images/0.jpg");
		system ("convert ./images/0.jpg -resize 256 ./images/0.bmp");
		system("~/approximate_associative_mem/multi2sim-4.2/bin/m2s --si-sim detailed --si-fifo-length $length --si-profiling 0 --si-hamming-dist $dist --si-tcam-dist $fd --si-config conf Roberts --load Roberts_Kernel.bin > hit.rep");
		
		mkdir "./tested-data/"."$fd";

		$temp = "./tested-data/"."$fd/"."$length"."_$item.rep";
		copy("hit.rep", "$temp");

		$temp = "./tested-data/"."$fd/"."180000"."_$item.bmp";
		copy("out0.bmp", "$temp");
		
		system("rm -rf *.rep");
	}
    }
}
