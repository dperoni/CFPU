/*
 *  Multi2Sim
 *  Copyright (C) 2012  Rafael Ubal (ubal@ece.neu.edu)
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */
#ifndef ARCH_SOUTHERN_ISLANDS_EMU_MACHINE_H
#define ARCH_SOUTHERN_ISLANDS_EMU_MACHINE_H
//#define _ABS_REUSE
//#define _ABS_DT
#define _ABS_APPROX
//#define HAMMING_THR 0
//#define _ABS_PRINTING_ISA
/*
typedef enum
{
    si_isa_V_SQRT_F32 = 0, //SI_INST_VOP1 all F32 except some CNVT
    si_isa_V_SIN_F32,
    si_isa_V_COS_F32,
    si_isa_V_CVT_F32_I32,
    si_isa_V_CVT_F32_U32,
    si_isa_V_CVT_U32_F32,
    si_isa_V_CVT_I32_F32,
    si_isa_V_RCP_F32,
    si_isa_V_ADD_F32,   //SI_INST_VOP2 all F32
    si_isa_V_SUB_F32,
    si_isa_V_SUBREV_F32,
    si_isa_V_MUL_LEGACY_F32,
    si_isa_V_MUL_F32,
    si_isa_V_MIN_F32,
    si_isa_V_MAX_F32,
    si_isa_V_MAC_F32,
    si_isa_V_MADMK_F32,
    si_isa_V_ADD_F32_VOP3a, //SI_INST_VOP3a all F32
    si_isa_V_SUBREV_F32_VOP3a,
    si_isa_V_MUL_F32_VOP3a,
    si_isa_V_MAX_F32_VOP3a,
    si_isa_V_MAD_F32,
    si_isa_V_FMA_F32,
    si_isa_V_FRACT_F32_VOP3a,
    si_isa_V_CMP_LT_F32_VOP3a,
    si_isa_V_CMP_EQ_F32_VOP3a,
    si_isa_V_CMP_GT_F32_VOP3a,
    si_isa_V_CMP_NEQ_F32_VOP3a,
    si_isa_V_CMP_NLT_F32_VOP3a,
    si_isa_V_CMP_LT_F32,    //SI_INST_VOPC for all F32
    si_isa_V_CMP_GT_F32,
    si_isa_V_CMP_NGT_F32,
    si_isa_V_CMP_NEQ_F32,
    si_isa_LAST

} _ABS_supported_si_isa_t;
*/

typedef union mytypes_t {
    float input;
    unsigned int output;
}f2int;

typedef enum
{
    si_isa_V_ADD_F32 = 0,
    si_isa_V_MUL_F32,
    si_isa_V_SQRT_F32,
    si_isa_V_MAC_F32,
    si_isa_V_RCP_F32,
    si_isa_V_SIN_F32,
    si_isa_V_COS_F32,
    si_isa_V_SUB_F32,
    si_isa_V_SUBREV_F32,
    si_isa_V_MUL_LEGACY_F32,
    si_isa_V_ADD_F32_VOP3a,
    si_isa_V_SUBREV_F32_VOP3a,
    si_isa_V_MUL_F32_VOP3a,
    si_isa_V_MAD_F32,
    si_isa_V_FMA_F32,
    si_isa_V_FRACT_F32_VOP3a,
    si_last_F32
} _ABS_Approximated_si_isa_t;

struct ADD_STRUCT {
    float op0;
    float op1;
    float q;
    unsigned long cnt;
};

struct MULADD_STRUCT {
    float op0;
    float op1;
    float op2;
    float q;
    unsigned long cnt;
};

struct SQRT_STRUCT {
    float op0;
    float q;
    unsigned long cnt;
};


struct FLP2INT_STRUCT {
    float op0;
    unsigned long cnt;
    int32_t q;
};



struct ADD_REC_STRUCT {
    float op0;
    float op1;
    float q;
    unsigned long cnt;
	int time;
};

struct MULADD_REC_STRUCT {
    float op0;
    float op1;
    float op2;
    float q;
    unsigned long cnt;
	int time;
};

struct SQRT_REC_STRUCT {
    float op0;
    float q;
    unsigned long cnt;
	int time;
};

#define N_Entr 500000

struct ADD_STRUCT add [N_Entr];
struct ADD_STRUCT mul [N_Entr];
struct MULADD_STRUCT muladd [N_Entr];
struct SQRT_STRUCT _sqrt [N_Entr];
struct SQRT_STRUCT recip [N_Entr];
struct FLP2INT_STRUCT flp2int [N_Entr];
struct MULADD_STRUCT mad [N_Entr];


struct ADD_REC_STRUCT add_rec [N_Entr];
struct ADD_REC_STRUCT mul_rec [N_Entr];
struct MULADD_REC_STRUCT muladd_rec [N_Entr];
struct SQRT_REC_STRUCT _sqrt_rec [N_Entr];

unsigned int add_index;
unsigned int mul_index;
unsigned int muladd_index;
unsigned int sqrt_index;
unsigned int recip_index;
unsigned int flp2int_index;
unsigned int mad_index;

#define MAX_REC_SIZE 16


unsigned int add_rec_index;
unsigned int mul_rec_index;
unsigned int muladd_rec_index;
unsigned int sqrt_rec_index;

unsigned long FPU_cnt [si_last_F32];
unsigned long FPU_hit_cnt [si_last_F32];
unsigned long FPU_rew_cnt [si_last_F32];
FILE *file_unmapped;


#endif
