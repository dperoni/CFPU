from scipy import misc
import re
import os
import numpy
import math

CFPU_dir = "/home/dperoni/CFPU/"
m2s_path = CFPU_dir + "multi2sim-4.2/bin/m2s"
output_directory = CFPU_dir + "data"
rodinia_dir = CFPU_dir + "rodinia_3.1"
amd_sdk_dir = CFPU_dir + "m2s-bench-amdapp-2.5-si"

max_error = [0,  0.015625, 0.03125, 0.0625, 0.125, 0.25, 1]

image_benchmarks = ["airplanes", "brontosaurus", "cougar_face", "elephant"]
#image_benchmarks = ["airplanes", "brontosaurus", "cougar_face", "elephant", "Faces_easy", "grand_piano", "laptop", "nautilus", "rhino", "windsor_chair"]
#image_benchmarks = ["elephant"]
#Lists of tests: Test name, test path, type, check script, kernel_name, commands
tests = [
["SobelFilter", amd_sdk_dir+"/SobelFilter", "image", "", "SobelFilter_Kernels.bin", ""],
#["Roberts", amd_sdk_dir + "/Roberts", "image", "", "Roberts_Kernel.bin", ""],
#["Blur", amd_sdk_dir + "/Blur", "image", "", "Blur_Kernel.bin"], "",
#["Sharpen", amd_sdk_dir + "/Sharpen", "image", "", "Sharpen_Kernel.bin", ""],
#["kmeans", rodinia_dir + "/opencl/kmeans", "rodinia", "kmeans_check.py", "kmeans.bin", "-i ../../data/kmeans/exp.txt -r -l 1 -m 4 -n 4"],
#["nn", rodinia_dir + "/opencl/nn", "rodinia", "nn_check.py", "nearestNeighbor_kernel.bin", "./inputs -p 0 -d 1"],
#["backprop", rodinia_dir + "/opencl/backprop", "rodinia", "back_check.py", "backprop_kernel.bin", "512"],
#["lud", rodinia_dir + "/opencl/lud/ocl", "rodinia", "lud_check.py", "lud_kernel.bin", "-v -i ../../../data/lud/64.dat"],
#["FFT", amd_sdk_dir + "/FFT", "rodinia",  "fft_check.py", "FFT_Kernels.bin", "-i 5 -e --load FFT_Kernels.bin"],
#["MersenneTwister", amd_sdk_dir + "/MersenneTwister", "rodinia", "twister_check.py", "MersenneTwister_Kernels.bin", "-e --load MersenneTwister_Kernels.bin"],
#["DwtHaar1D", amd_sdk_dir + "/DwtHaar1D", "rodinia", "dwt_check.py", "DwtHaar1D_Kernels.bin", "--load DwtHaar1D_Kernels.bin -x 20000 -e"],
#["BinomialOption", amd_sdk_dir + "/BinomialOption", "rodinia", "binom_check.py", "BiomialOption_Kernels.bin", "--load BinomialOption_Kernels.bin -x 20 -e"],
#["EigenValue", amd_sdk_dir + "/EigenValue", "rodinia", "eigen_check.py", "EigenValue_Kernels.bin", "--load EigenValue_Kernels.bin -x 2 -e"],
#["QuasiRandomSequence", amd_sdk_dir + "/QuasiRandomSequence", "rodinia", "quasi_check.py", "QuasiRandomSequence_Kernels.bin", "--load QuasiRandomSequence_Kernels.bin -e"],
#["SimpleConvolution", amd_sdk_dir + "/SimpleConvolution", "rodinia", "conv_test.py", "SimpleConvolution_Kernels.bin", "--load SimpleConvolution_Kernels.bin -e"],
#["RecursiveGaussian", amd_sdk_dir+ "/RecursiveGaussian", "image", "", "RecursiveGaussian_Kernels.bin"],
["BlackScholes", amd_sdk_dir + "/BlackScholes", "rodinia", "scholes_check.py", "BlackScholes_Kernels.bin", "--load BlackScholes_Kernels.bin -e"],


]

def main():
    print tests
    if os.path.isdir(output_directory) == False:
        os.mkdir(output_directory)

    for test in tests:
        testname = test[0]
        test_path = test[1]
        test_type = test[2]
        test_analysis = test[3]
        kernel = test[4]
        
        run_test(test)
        process_data(test)   






def run_test(test):
    #os.system()
    test_path = test[1]
    print test_path
    test_type = test[2]
    kernel = test[4]
    os.chdir(test_path)

    if os.path.isdir("tested-data") == False:
        os.mkdir("tested-data")
        

    if test_type == "image":
        run_image_test(test)
    elif test_type == "rodinia":
               run_rodinia_test(test)
        


def run_rodinia_test(test):
    test_name = test[0]
    kernel = test[4]
    test_path = test[1]
    os.environ["M2S_OPENCL_BINARY"] = test_path + "/" + kernel

    commands = test[5]
    if os.path.isdir("tested-data/Exact") == False:
            os.mkdir("tested-data/Exact")
    if os.path.isdir("tested-data/MantissaDrop") == False:
            os.mkdir("tested-data/MantissaDrop")
    if os.path.isdir("tested-data/Adaptive") == False:
            os.mkdir("tested-data/Adaptive")
    if os.path.isdir("tested-data/AdaptiveSimple") == False:
            os.mkdir("tested-data/AdaptiveSimple")
    if os.path.isdir("tested-data/Tuning") == False:
            os.mkdir("tested-data/Tuning")
    if os.path.isdir("tested-data/TuningAdaptiveSimple") == False:
            os.mkdir("tested-data/TuningAdaptiveSimple")

    if os.path.isdir("tested-data/ShiftAdd") == False:
            os.mkdir("tested-data/ShiftAdd")
    if os.path.isdir("tested-data/SATune") == False:
            os.mkdir("tested-data/SATune")
 
    benchmark = test_name
    base_command = m2s_path + " --si-sim detailed --si-fifo-length 0 --si-profiling 0 --si-config conf "  
    #run_m2s(command, test)

    #Exact case
    exact_command = base_command + "--si-cfpu_mode 0" + " ./"+ test_name  + " " + commands + " > hit.rep"
    os.system(exact_command)

    os.system("cp hit.rep tested-data/Exact/" +benchmark + ".rep")

    
    #Mantissa Drop
    mantissa_command = base_command + "--si-cfpu_mode 1" + " ./"+ test_name  + " " + commands + " > hit.rep"
    os.system(mantissa_command)

    os.system("cp hit.rep tested-data/MantissaDrop/" +benchmark + ".rep")

    #Adaptive
    adaptive_command = base_command + "--si-cfpu_mode 2" + " ./"+ test_name  + " " + commands + " > hit.rep"
    os.system(adaptive_command)

    os.system("cp hit.rep tested-data/Adaptive/" +benchmark + ".rep")

     #Adaptive Simple
    adaptive_command = base_command + "--si-cfpu_mode 6" + " ./"+ test_name  + " " + commands + " > hit.rep"
    os.system(adaptive_command)

    adaptive_file_path = "tested-data/AdaptiveSimple/"+benchmark+".bmp"
    os.system("cp hit.rep tested-data/AdaptiveSimple/" +benchmark + ".rep")
    os.system("cp out0.bmp " + adaptive_file_path)


    #Tuning
    for e in max_error:
        if os.path.isdir("tested-data/Tuning/" + str(e)) == False:
            os.mkdir("tested-data/Tuning/" + str(e))
        tuning_command = base_command + "--si-cfpu_mode 3 --si-cfpu_max_error " + str(e) + " ./"+ test_name + " " + commands + " > hit.rep"
        os.system(tuning_command)
        os.system("cp hit.rep tested-data/Tuning/" +str(e) + "/" + benchmark + ".rep")


    #TuningAdaptiveSimple
    for e in max_error:
        if os.path.isdir("tested-data/TuningAdaptiveSimple/" + str(e)) == False:
            os.mkdir("tested-data/TuningAdaptiveSimple/" + str(e))
        tuning_command = base_command + "--si-cfpu_mode 7 --si-cfpu_max_error " + str(e) + " ./"+ test_name + " " + commands + " > hit.rep"
        os.system(tuning_command)
        os.system("cp hit.rep tested-data/TuningAdaptiveSimple/" +str(e) + "/" + benchmark + ".rep")


    #ShiftAdd
    for e in max_error:
        if os.path.isdir("tested-data/ShiftAdd/" + str(e)) == False:
            os.mkdir("tested-data/ShiftAdd/" + str(e))
        tuning_command = base_command + "--si-cfpu_mode 4 --si-cfpu_max_error " + str(e) + " ./"+ test_name  + " " + commands + " > hit.rep"
        os.system(tuning_command)
        os.system("cp hit.rep tested-data/ShiftAdd/" +str(e) + "/" + benchmark + ".rep")

  #ShiftAddTune
    for e in max_error:
        if os.path.isdir("tested-data/SATune/" + str(e)) == False:
            os.mkdir("tested-data/SATune/" + str(e))
        tuning_command = base_command + "--si-cfpu_mode 5 --si-cfpu_max_error " + str(e) + " ./"+ test_name +" " + commands + " > hit.rep"
        os.system(tuning_command)
        os.system("cp hit.rep tested-data/SATune/" +str(e) + "/" + benchmark + ".rep")

    print tuning_command



def run_image_test(test):
    
    test_name = test[0]
    kernel = test[4]
    print os.getcwd()
    if os.path.isdir("tested-data/Exact") == False:
            os.mkdir("tested-data/Exact")
    if os.path.isdir("tested-data/MantissaDrop") == False:
            os.mkdir("tested-data/MantissaDrop")
    if os.path.isdir("tested-data/Adaptive") == False:
            os.mkdir("tested-data/Adaptive")
    if os.path.isdir("tested-data/AdaptiveSimple") == False:
            os.mkdir("tested-data/AdaptiveSimple")
    if os.path.isdir("tested-data/Tuning") == False:
            os.mkdir("tested-data/Tuning")
    if os.path.isdir("tested-data/ShiftAdd") == False:
            os.mkdir("tested-data/ShiftAdd")
    if os.path.isdir("tested-data/SATune") == False:
            os.mkdir("tested-data/SATune")
        
    if os.path.isdir("tested-data/TuningAdaptiveSimple") == False:
            os.mkdir("tested-data/TuningAdaptiveSimple")


    for benchmark in image_benchmarks:
        os.system("rm -rf *.rep")
        input_image = "../Caltech/"+benchmark + "/image_0001.jpg";
        os.system("cp "+ input_image+ " ./images/0.jpg");
        os.system("convert ./images/0.jpg -resize 256 ./images/0.bmp");
        base_command = m2s_path + " --si-sim detailed --si-fifo-length 0 --si-profiling 0 --si-config conf "  
        #run_m2s(command, test)

        #Exact case
        exact_command = base_command + "--si-cfpu_mode 0" + " ./"+ test_name +" "+ "--load ./" + kernel + " > hit.rep"
        os.system(exact_command)

        exact_file_path = "tested-data/Exact/"+benchmark+".bmp"
        os.system("cp hit.rep tested-data/Exact/" +benchmark + ".rep")
        os.system("cp out0.bmp " + exact_file_path)

        
        #Mantissa Drop
        mantissa_command = base_command + "--si-cfpu_mode 1" + " ./"+ test_name +" "+ "--load ./" + kernel + " > hit.rep"
        os.system(mantissa_command)

        mantissa_file_path = "tested-data/MantissaDrop/"+benchmark+".bmp"
        os.system("cp hit.rep tested-data/MantissaDrop/" +benchmark + ".rep")
        os.system("cp out0.bmp " + mantissa_file_path)

        #Adaptive
        adaptive_command = base_command + "--si-cfpu_mode 2" + " ./"+ test_name +" "+ "--load ./" + kernel + " > hit.rep"
        os.system(adaptive_command)

        adaptive_file_path = "tested-data/Adaptive/"+benchmark+".bmp"
        os.system("cp hit.rep tested-data/Adaptive/" +benchmark + ".rep")
        os.system("cp out0.bmp " + adaptive_file_path)

     #Adaptive Simple
        adaptive_command = base_command + "--si-cfpu_mode 6" + " ./"+ test_name +" "+ "--load ./" + kernel + " > hit.rep"
        os.system(adaptive_command)

        adaptive_file_path = "tested-data/AdaptiveSimple/"+benchmark+".bmp"
        os.system("cp hit.rep tested-data/AdaptiveSimple/" +benchmark + ".rep")
        os.system("cp out0.bmp " + adaptive_file_path)



        #Tuning
        for e in max_error:
            if os.path.isdir("tested-data/Tuning/" + str(e)) == False:
                os.mkdir("tested-data/Tuning/" + str(e))
            tuning_command = base_command + "--si-cfpu_mode 3 --si-cfpu_max_error " + str(e) + " ./"+ test_name +" "+ "--load ./" + kernel + " > hit.rep"
            os.system(tuning_command)
            tuning_file_path = "tested-data/Tuning/"+ str(e) +"/" + benchmark + ".bmp"
            os.system("cp hit.rep tested-data/Tuning/" +str(e) + "/" + benchmark + ".rep")
            os.system("cp out0.bmp " + tuning_file_path)

        #TuningiAdaptiveSimple
        for e in max_error:
            if os.path.isdir("tested-data/TuningAdaptiveSimple/" + str(e)) == False:
                os.mkdir("tested-data/TuningAdaptiveSimple/" + str(e))
            tuning_command = base_command + "--si-cfpu_mode 7 --si-cfpu_max_error " + str(e) + " ./"+ test_name +" "+ "--load ./" + kernel + " > hit.rep"
            os.system(tuning_command)
            tuning_file_path = "tested-data/TuningAdaptiveSimple/"+ str(e) +"/" + benchmark + ".bmp"
            os.system("cp hit.rep tested-data/TuningAdaptiveSimple/" +str(e) + "/" + benchmark + ".rep")
            os.system("cp out0.bmp " + tuning_file_path)


        #ShiftAdd
        for e in max_error:
            if os.path.isdir("tested-data/ShiftAdd/" + str(e)) == False:
                os.mkdir("tested-data/ShiftAdd/" + str(e))
            tuning_command = base_command + "--si-cfpu_mode 4 --si-cfpu_max_error " + str(e) + " ./"+ test_name +" "+ "--load ./" + kernel + " > hit.rep"
            os.system(tuning_command)
            tuning_file_path = "tested-data/ShiftAdd/"+ str(e) +"/" + benchmark + ".bmp"
            os.system("cp hit.rep tested-data/ShiftAdd/" +str(e) + "/" + benchmark + ".rep")
            os.system("cp out0.bmp " + tuning_file_path)
   
      #ShiftAddTune
        for e in max_error:
            if os.path.isdir("tested-data/SATune/" + str(e)) == False:
                os.mkdir("tested-data/SATune/" + str(e))
            tuning_command = base_command + "--si-cfpu_mode 5 --si-cfpu_max_error " + str(e) + " ./"+ test_name +" "+ "--load ./" + kernel + " > hit.rep"
            os.system(tuning_command)
            tuning_file_path = "tested-data/SATune/"+ str(e) + "/" + benchmark + ".bmp"
            os.system("cp hit.rep tested-data/SATune/" +str(e) + "/" + benchmark + ".rep")
            os.system("cp out0.bmp " + tuning_file_path)
   


def run_m2s(command, test):
    kernel = test[4]
    test_name = test[0]
    
    
    
    for e in max_error:
        call = command + " --si-cfpu_max_error " + str(e) + " ./"+ test_name +" "+ "--load ./" + kernel + " > hit.rep"
        print call
        os.system(call)


def process_data(test):
    test_name = test[0]
    test_path = test[1]
    test_type = test[2]
    os.chdir(test_path)

    #if os.path.isdir(output_directory + "/" + test_name) == False:
     #       os.mkdir(output_directory + "/" + test_name)

    output_file = open(output_directory + "/" + test_name + ".out", 'w')

    if os.path.isdir("tested-data") == False:
        raise Exception("No test data folder in " + test_path)
        

    if test_type == "image":
        process_images(test, output_file)
    if test_type == "rodinia" or test_type == "open_cl":
        process_others(test, output_file) 

    output_file.close()

def process_others(test, output_file):
    check_script = test[3]
    test_name = test[0]
    exact_hit_rate = 0

    exact_data_hitrate = 0

    mantissa_hitrate = 0
    mantissa_err = 0

    adaptive_hitrate = 0
    adaptive_err = 0

    adaptive_simple_hitrate = 0
    adaptive_simple_err = 0


    tuning_hitrate = {}
    tuning_err = {}
    tuningadaptivesimple_hitrate = {}
    tuningadaptivesimple_err = {}

    shiftadd_hitrate = {}
    shiftadd_hitrate2 = {}
    shiftadd_err = {}
    shiftadd_total_hitrate = {}

    satune_hitrate = {}
    satune_hitrate2 = {}
    satune_err = {}
    satune_total_hitrate = {}


    for e in max_error:
        tuning_hitrate[e] = 0
        tuning_err[e] = 0

        tuningadaptivesimple_hitrate[e] = 0
        tuningadaptivesimple_err[e] = 0

        shiftadd_hitrate[e] = 0
        shiftadd_hitrate2[e] = 0
        shiftadd_err[e] = 0
        shiftadd_total_hitrate[e] = 0

        satune_hitrate[e] = 0
        satune_hitrate2[e] = 0
        satune_err[e] = 0
        satune_total_hitrate[e] = 0




    benchmark = test_name
    exact_file_path ="tested-data/Exact/" +benchmark + ".rep"
    exact_rep = open(exact_file_path, 'r')
           #output_file.write(get_line(exact_rep))
    results = get_line(exact_rep)
    exact_data_hitrate += results["total_hit_rate"]


    #Mantissa Drop
    
    mantissa_rep = open("tested-data/MantissaDrop/" +benchmark + ".rep")
    results = get_line(mantissa_rep)
    mantissa_hitrate += results["first_hit_rate"]
    mantissa_err += compare_files(exact_file_path, "tested-data/MantissaDrop/" +benchmark + ".rep", check_script)


    #Adaptive
    adaptive_rep = open("tested-data/Adaptive/" +benchmark + ".rep")
    results = get_line(adaptive_rep)
    adaptive_hitrate += results["first_hit_rate"]
    adaptive_err += compare_files(exact_file_path, "tested-data/Adaptive/" +benchmark + ".rep", check_script)

 #AdaptiveSimple
    adaptive_simple_rep = open("tested-data/AdaptiveSimple/" +benchmark + ".rep")
    results = get_line(adaptive_simple_rep)
    adaptive_simple_hitrate += results["first_hit_rate"]
    adaptive_simple_err += compare_files(exact_file_path, "tested-data/AdaptiveSimple/" +benchmark + ".rep", check_script)



    #Tuning
    for e in max_error:
        tuning_rep = open("tested-data/Tuning/"+ str(e) + "/" + benchmark + ".rep")
        results = get_line(tuning_rep)
        tuning_hitrate[e] += results["first_hit_rate"]
        tuning_err[e] += compare_files(exact_file_path, "tested-data/Tuning/"+ str(e) + "/" + benchmark + ".rep", check_script)

    #TuningAdaptiveSimple
    for e in max_error:
        tuning_rep = open("tested-data/TuningAdaptiveSimple/"+ str(e) + "/" + benchmark + ".rep")
        results = get_line(tuning_rep)
        tuningadaptivesimple_hitrate[e] += results["first_hit_rate"]
        tuningadaptivesimple_err[e] += compare_files(exact_file_path, "tested-data/TuningAdaptiveSimple/"+ str(e) + "/" + benchmark + ".rep", check_script)


    #Shift and Add
    for e in max_error:
        tuning_rep = open("tested-data/ShiftAdd/"+ str(e) + "/" + benchmark + ".rep")
        results = get_line(tuning_rep)
        shiftadd_hitrate[e] += results["first_hit_rate"]
        shiftadd_hitrate2[e] += results["second_hit_rate"]
        shiftadd_total_hitrate[e] += results["total_hit_rate"]
        shiftadd_err[e] += compare_files(exact_file_path, "tested-data/ShiftAdd/"+ str(e) + "/" + benchmark + ".rep", check_script)

    #Tuning
    for e in max_error:
        tuning_rep = open("tested-data/SATune/"+ str(e) + "/" + benchmark + ".rep")
        results = get_line(tuning_rep)
        satune_hitrate[e] += results["first_hit_rate"]
        satune_hitrate2[e] += results["second_hit_rate"]
        satune_total_hitrate[e] += results["total_hit_rate"]
        satune_err[e] += compare_files(exact_file_path, "tested-data/SATune/"+ str(e) + "/" + benchmark + ".rep", check_script)


            



    output_file.write("Exact Results\n")
    output_file.write("Average Hitrate, " + str(exact_data_hitrate) + "\n")
    output_file.write("\n")

    output_file.write("Mantissa Drop Results\n")
    output_file.write("Average Error, " + str(mantissa_err) + "\n")
    output_file.write("Average hitrate, " + str(mantissa_hitrate) + "\n")
    output_file.write("\n")

    output_file.write("Adaptive Selection Results\n")
    output_file.write("Average Error, " + str(adaptive_err) + "\n")
    output_file.write("Average hitrate, " + str(adaptive_hitrate) + "\n")
    output_file.write("\n")

    output_file.write("Adaptive Simple Selection Results\n")
    output_file.write("Average Simple  Error, " + str(adaptive_simple_err) + "\n")
    output_file.write("Average Simple hitrate, " + str(adaptive_simple_hitrate) + "\n")
    output_file.write("\n")




    output_file.write("Tuning Results\n")
    output_file.write("Max Error, \t")
    for e in max_error:
        output_file.write(str(e) + ",\t")
    output_file.write("\n")
    output_file.write("Average Error, \t" + hitrate_string(tuning_err))
    output_file.write("Average hitrate, \t" + hitrate_string(tuning_hitrate))
    output_file.write("\n")

    output_file.write("TuningAdaptiveSimple Results\n")
    output_file.write("Max Error, \t")
    for e in max_error:
        output_file.write(str(e) + ",\t")
    output_file.write("\n")
    output_file.write("Average Error, \t" + hitrate_string(tuningadaptivesimple_err))
    output_file.write("Average hitrate, \t" + hitrate_string(tuningadaptivesimple_hitrate))
    output_file.write("\n")





    output_file.write("Shift and Add Results\n")
    output_file.write("Max Error, \t")
    for e in max_error:
        output_file.write(str(e) + ",\t")
    output_file.write("\n")

    output_file.write("Average Error, \t" + hitrate_string(shiftadd_err))
    output_file.write("Average first stage hitrate, \t" + hitrate_string(shiftadd_hitrate))
    output_file.write("Average second stage hitrate, \t" + hitrate_string(shiftadd_hitrate2))
    output_file.write("Average total hitrate, \t" + hitrate_string(shiftadd_total_hitrate))
    output_file.write("\n")

    output_file.write("Shift and Add w/ 2nd stage Tuning Results\n")
    output_file.write("Max Error, \t")
    for e in max_error:
        output_file.write(str(e) + ",\t")
    output_file.write("\n")

    output_file.write("Average Error, \t" + hitrate_string(satune_err))
    output_file.write("Average first stage hitrate, \t" + hitrate_string(satune_hitrate))
    output_file.write("Average second stage hitrate, \t" + hitrate_string(satune_hitrate2))
    output_file.write("Average total hitrate, \t" + hitrate_string(satune_total_hitrate))
    output_file.write("\n")


def compare_files(exact, comp, script):
    os.system("python " + script + " " + exact + " " + comp + " > tmp.out")
    data = open("tmp.out", "r")
    return float(data.readline())


def process_images(test, output_file):
    
    exact_hit_rate = 0
    total_benchmarks = len(image_benchmarks)
    print total_benchmarks

    exact_data_hitrate = 0

    mantissa_hitrate = 0
    mantissa_psnr = 0

    adaptive_hitrate = 0
    adaptive_psnr = 0

    adaptive_simple_hitrate = 0
    adaptive_simple_psnr = 0


    tuning_hitrate = {}
    tuning_psnr = {}

    tuningadaptivesimple_hitrate = {}
    tuningadaptivesimple_psnr = {}



    shiftadd_hitrate = {}
    shiftadd_hitrate2 = {}
    shiftadd_psnr = {}
    shiftadd_total_hitrate = {}

    satune_hitrate = {}
    satune_hitrate2 = {}
    satune_psnr = {}
    satune_total_hitrate = {}


    for e in max_error:
        tuningadaptivesimple_hitrate[e] = 0
        tuningadaptivesimple_psnr[e] = 0

        tuning_hitrate[e] = 0
        tuning_psnr[e] = 0

        shiftadd_hitrate[e] = 0
        shiftadd_hitrate2[e] = 0
        shiftadd_psnr[e] = 0
        shiftadd_total_hitrate[e] = 0

        satune_hitrate[e] = 0
        satune_hitrate2[e] = 0
        satune_psnr[e] = 0
        satune_total_hitrate[e] = 0





    for benchmark in image_benchmarks:
        exact_img = misc.imread("tested-data/Exact/"+benchmark+".bmp", flatten=0)
        exact_rep = open("tested-data/Exact/"+benchmark+".rep", 'r')
               #output_file.write(get_line(exact_rep))
        results = get_line(exact_rep)
        exact_data_hitrate += results["total_hit_rate"]/total_benchmarks


        #Mantissa Drop

        mantissa_img = misc.imread("tested-data/MantissaDrop/"+benchmark+".bmp", flatten=0)
        mantissa_rep = open("tested-data/MantissaDrop/" +benchmark + ".rep")
        results = get_line(mantissa_rep)
        mantissa_hitrate += results["first_hit_rate"]/total_benchmarks
        mantissa_psnr += compare_img(exact_img, mantissa_img)/total_benchmarks


        #Adaptive
        adaptive_img = misc.imread("tested-data/Adaptive/"+benchmark+".bmp", flatten=0)
        adaptive_rep = open("tested-data/Adaptive/" +benchmark + ".rep")
        results = get_line(adaptive_rep)
        adaptive_hitrate += results["first_hit_rate"]/total_benchmarks
        adaptive_psnr += compare_img(exact_img, adaptive_img)/total_benchmarks

     #AdaptiveSimple
        adaptive_simple_img = misc.imread("tested-data/AdaptiveSimple/"+benchmark+".bmp", flatten=0)
        adaptive_simple_rep = open("tested-data/AdaptiveSimple/" +benchmark + ".rep")
        results = get_line(adaptive_simple_rep)
        adaptive_simple_hitrate += results["first_hit_rate"]/total_benchmarks
        adaptive_simple_psnr += compare_img(exact_img, adaptive_img)/total_benchmarks



        #Tuning
        for e in max_error:
            tuning_img = misc.imread("tested-data/Tuning/"+ str(e) + "/" + benchmark + ".bmp", flatten=0)
            tuning_rep = open("tested-data/Tuning/"+ str(e) + "/" + benchmark + ".rep")
            results = get_line(tuning_rep)
            tuning_hitrate[e] += results["first_hit_rate"]/total_benchmarks
            tuning_psnr[e] += compare_img(exact_img, tuning_img)/total_benchmarks

    #TuningAdaptiveSimple
        for e in max_error:
            tuning_img = misc.imread("tested-data/TuningAdaptiveSimple/"+ str(e) + "/" + benchmark + ".bmp", flatten=0)
            tuning_rep = open("tested-data/TuningAdaptiveSimple/"+ str(e) + "/" + benchmark + ".rep")
            results = get_line(tuning_rep)
            tuningadaptivesimple_hitrate[e] +=  results["first_hit_rate"]/total_benchmarks
            tuningadaptivesimple_psnr[e] += compare_img(exact_img, tuning_img)/total_benchmarks



        #Shift and Add
        for e in max_error:
            tuning_img = misc.imread("tested-data/ShiftAdd/"+ str(e) + "/" + benchmark + ".bmp", flatten=0)
            tuning_rep = open("tested-data/ShiftAdd/"+ str(e) + "/" + benchmark + ".rep")
            results = get_line(tuning_rep)
            shiftadd_hitrate[e] += results["first_hit_rate"]/total_benchmarks
            shiftadd_hitrate2[e] += results["second_hit_rate"]/total_benchmarks
            shiftadd_total_hitrate[e] += results["total_hit_rate"]/total_benchmarks
            shiftadd_psnr[e] += compare_img(exact_img, tuning_img)/total_benchmarks

        #Tuning
        for e in max_error:
            tuning_img = misc.imread("tested-data/SATune/"+ str(e) + "/" + benchmark + ".bmp", flatten=0)
            tuning_rep = open("tested-data/SATune/"+ str(e) + "/" + benchmark + ".rep")
            results = get_line(tuning_rep)
            satune_hitrate[e] += results["first_hit_rate"]/total_benchmarks
            satune_hitrate2[e] += results["second_hit_rate"]/total_benchmarks
            satune_total_hitrate[e] += results["total_hit_rate"]/total_benchmarks
            satune_psnr[e] += compare_img(exact_img, tuning_img)/total_benchmarks


            



    output_file.write("Exact Results\n")
    output_file.write("Average Hitrate, " + str(exact_data_hitrate) + "\n")
    output_file.write("\n")

    output_file.write("Mantissa Drop Results\n")
    output_file.write("Average PSNR, " + str(mantissa_psnr) + "\n")
    output_file.write("Average hitrate, " + str(mantissa_hitrate) + "\n")
    output_file.write("\n")

    output_file.write("Adaptive Selection Results\n")
    output_file.write("Average PSNR, " + str(adaptive_psnr) + "\n")
    output_file.write("Average hitrate, " + str(adaptive_hitrate) + "\n")
    output_file.write("\n")

    output_file.write("Adaptive Simple Selection Results\n")
    output_file.write("Average Simple  PSNR, " + str(adaptive_simple_psnr) + "\n")
    output_file.write("Average Simple hitrate, " + str(adaptive_simple_hitrate) + "\n")
    output_file.write("\n")



    output_file.write("Tuning Results\n")
    output_file.write("Max Error, \t")
    for e in max_error:
        output_file.write(str(e) + ",\t")
    output_file.write("\n")
    output_file.write("Average PSNR, \t" + hitrate_string(tuning_psnr))
    output_file.write("Average hitrate, \t" + hitrate_string(tuning_hitrate))
    output_file.write("\n")

    output_file.write("TuningAdaptiveSimple Results\n")
    output_file.write("Max Error, \t")
    for e in max_error:
        output_file.write(str(e) + ",\t")
    output_file.write("\n")
    output_file.write("Average PSNR, \t" + hitrate_string(tuningadaptivesimple_psnr))
    output_file.write("Average hitrate, \t" + hitrate_string(tuningadaptivesimple_hitrate))
    output_file.write("\n")



    output_file.write("Shift and Add Results\n")
    output_file.write("Max Error, \t")
    for e in max_error:
        output_file.write(str(e) + ",\t")
    output_file.write("\n")

    output_file.write("Average PSNR, \t" + hitrate_string(shiftadd_psnr))
    output_file.write("Average first stage hitrate, \t" + hitrate_string(shiftadd_hitrate))
    output_file.write("Average second stage hitrate, \t" + hitrate_string(shiftadd_hitrate2))
    output_file.write("Average total hitrate, \t" + hitrate_string(shiftadd_total_hitrate))
    output_file.write("\n")

    output_file.write("Shift and Add w/ 2nd stage Tuning Results\n")
    output_file.write("Max Error, \t")
    for e in max_error:
        output_file.write(str(e) + ",\t")
    output_file.write("\n")

    output_file.write("Average PSNR, \t" + hitrate_string(satune_psnr))
    output_file.write("Average first stage hitrate, \t" + hitrate_string(satune_hitrate))
    output_file.write("Average second stage hitrate, \t" + hitrate_string(satune_hitrate2))
    output_file.write("Average total hitrate, \t" + hitrate_string(satune_total_hitrate))
    output_file.write("\n")

def hitrate_string(entry):
    string = ""
    for e in max_error:
        string += str(round(entry[e], 3)) + ",\t"
    string += "\n"
    return string
    

def get_line(rep_file):
        results = {}
        for line in rep_file:
            if "FPU_ID_MUL" in line:
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
        #print temp
        results["hits_first_stage"] = float(temp[0])
        results["hits_second_stage"] = float(temp[1])
        results["total_ops"] = float(temp[2])
        results["first_hit_rate"] = float(temp[3])
        results["second_hit_rate"] = float(temp[4])
        results["total_hit_rate"] = float(temp[5])
        #print results
        return results

                
        
def compare_img(img1, img2):
    diff = img1-img2
    #print diff.sum()
    image_size = diff.shape[0]*diff.shape[1]*diff.shape[2]
    #print image_size
    #print diff.sum()/image_size
    return psnr(img1, img2)

def psnr(img1, img2):
    mse = numpy.mean( (img1 - img2) ** 2 )
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0

    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

    










if __name__ == '__main__':
     main()
