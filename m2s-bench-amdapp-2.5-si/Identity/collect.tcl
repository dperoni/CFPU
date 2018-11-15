rm -rf A
rm -rf *_trilobite.*
grep -r -w "FPU_ID_0" ./8_* >> A
grep -r -w "FPU_ID_1" ./8_* >> A
grep -r -w "FPU_ID_2" ./8_* >> A
grep -r -w "FPU_ID_3" ./8_* >> A
grep -r -w "FPU_ID_13" ./8_* >> A



