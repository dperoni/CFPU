rm -rf *trilobite.rep
rm -rf A
grep -r -w "FPU_ID_0" ./2_* >> A
grep -r -w "FPU_ID_1" ./2_* >> A
grep -r -w "FPU_ID_2" ./2_* >> A
grep -r -w "FPU_ID_3" ./2_* >> A
grep -r -w "FPU_ID_13" ./2_* >> A

