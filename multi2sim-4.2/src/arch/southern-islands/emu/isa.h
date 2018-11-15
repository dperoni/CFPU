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

#ifndef ARCH_SOUTHERN_ISLANDS_EMU_ISA_H
#define ARCH_SOUTHERN_ISLANDS_EMU_ISA_H
#include <stdbool.h>
//_ABS_
//#define _ABS_SPATIAL
//#define _ABS_TEMPORAL
extern int si_gpu_simd_num_simd_lanes;
typedef enum {
	VREG = 0,
	SREG
} _ABS_si_isa_write_reg;


struct isa_context_t
{
	float op1;
	float op2;
	float op0;
	unsigned int q;
    unsigned long cnt; 
};


#define si_isa_LAST 20 
struct isa_context_t isa_context[1][4][16][si_isa_LAST][1];
unsigned int fifo_index[1][4][16][si_isa_LAST];
unsigned int fifo_unmapped[1][4][16][si_isa_LAST]; 
unsigned long gated_inst_cnt[si_isa_LAST];
unsigned long inst_cnt[si_isa_LAST];
unsigned long vreg_cnt;
unsigned long gated_vreg_cnt;
unsigned long check_cnt;
unsigned long clean_cnt;

//_ABS_

enum si_isa_write_task_kind_t
{
	SI_ISA_WRITE_TASK_NONE = 0,
	SI_ISA_WRITE_TASK_WRITE_LDS,
	SI_ISA_WRITE_TASK_WRITE_DEST,
	SI_ISA_WRITE_TASK_PUSH_BEFORE,
	SI_ISA_WRITE_TASK_SET_PRED
};


struct si_isa_write_task_t
{
	/* All */
	enum si_isa_write_task_kind_t kind;
	struct si_inst_t *inst;

	/* When 'kind' == SI_ISA_WRITE_TASK_WRITE_DEST */
	int gpr, rel, chan, index_mode, write_mask;
	unsigned int value;

	/* When 'kind' == SI_ISA_WRITE_TASK_WRITE_LDS */
	unsigned int lds_addr;
	unsigned int lds_value;
        size_t   lds_value_size;

	/* When 'kind' == GPU_ISA_WRITE_TASK_PRED_SET */
	int cond;
};

/* Functions to handle deferred tasks */
void si_isa_enqueue_write_lds(unsigned int addr, unsigned int value, size_t value_size);
void si_isa_enqueue_write_dest(unsigned int value);
void si_isa_enqueue_write_dest_float(float value);
void si_isa_enqueue_push_before(void);
void si_isa_enqueue_pred_set(int cond);
void si_isa_write_task_commit(void);

/* Macros for special registers */
#define SI_M0 124
#define SI_VCC 106
#define SI_VCCZ 251
#define SI_EXEC 126
#define SI_EXECZ 252
#define SI_SCC 253


/* Debugging */
#define si_isa_debug(...) debug(si_isa_debug_category, __VA_ARGS__)
extern int si_isa_debug_category;


/* Macros for unsupported parameters */
extern char *err_si_isa_note;

#define SI_ISA_ARG_NOT_SUPPORTED(p) \
	fatal("%s: %s: not supported for '" #p "' = 0x%x\n%s", \
	__FUNCTION__, si_isa_inst->info->name, (p), err_si_isa_note);
#define SI_ISA_ARG_NOT_SUPPORTED_NEQ(p, v) \
	{ if ((p) != (v)) fatal("%s: %s: not supported for '" #p "' != 0x%x\n%s", \
	__FUNCTION__, si_isa_inst->info->name, (v), err_si_isa_note); }
#define SI_ISA_ARG_NOT_SUPPORTED_RANGE(p, min, max) \
	{ if ((p) < (min) || (p) > (max)) fatal("%s: %s: not supported for '" #p "' out of range [%d:%d]\n%s", \
	__FUNCTION__, si_isa_inst->info->name, (min), (max), err_si_opencl_param_note); }


/* Macros for fast access of instruction words */
#define SI_INST_SMRD		inst->micro_inst.smrd
#define SI_INST_SOPP		inst->micro_inst.sopp
#define SI_INST_SOPK		inst->micro_inst.sopk
#define SI_INST_SOPC		inst->micro_inst.sopc
#define SI_INST_SOP1		inst->micro_inst.sop1
#define SI_INST_SOP2		inst->micro_inst.sop2
#define SI_INST_VOP1		inst->micro_inst.vop1
#define SI_INST_VOP2		inst->micro_inst.vop2
#define SI_INST_VOPC		inst->micro_inst.vopc
#define SI_INST_VOP3b		inst->micro_inst.vop3b
#define SI_INST_VOP3a		inst->micro_inst.vop3a
#define SI_INST_DS		inst->micro_inst.ds
#define SI_INST_MTBUF		inst->micro_inst.mtbuf
#define SI_INST_MUBUF		inst->micro_inst.mubuf


void si_isa_init();
void si_isa_done();

/* Forward declaration */
struct si_work_item_t;
union si_reg_t;

/* List of functions implementing GPU instructions 'amd_inst_XXX_impl' */
typedef void (*si_isa_inst_func_t)(struct si_work_item_t *work_item, struct si_inst_t *inst);
extern si_isa_inst_func_t *si_isa_inst_func;

/* FIXME
 * Some older compilers need the 'union' type to be not only declared but 
 * also defined to allow for the declaration below. This forces us to 
 * #include 'asm.h' from this file.  To avoid this extra dependence, 
 * 'union' types below could be replaced by 'unsigned int', and then all 
 * callers updated accordingly. */
unsigned int si_isa_read_sreg(struct si_work_item_t *work_item, int sreg);
void si_isa_write_sreg(struct si_work_item_t *work_item, int sreg, 
	unsigned int value);
unsigned int si_isa_read_vreg(struct si_work_item_t *work_item, int vreg);

//_ABS_
bool _ABS_si_isa_read_vreg_dirty(struct si_work_item_t *work_item, int vreg);
bool _ABS_si_isa_read_sreg_dirty(struct si_work_item_t *work_item, int sreg);
bool _ABS_si_isa_read_reg_dirty(struct si_work_item_t *work_item, int reg);
bool _ABS_check_dirtiness(bool op1, bool op2, bool op3);

//void _ABS_si_isa_check_v2ops (struct si_work_item_t *work_item, int vreg, unsigned int value,
//        float op1, float op2, _ABS_supported_si_isa_t si_isa_type, _ABS_si_isa_write_reg si_reg_type);

//void _ABS_si_isa_check_v3ops (struct si_work_item_t *work_item, int vreg, unsigned int value,
//        float op1, float op2, float op3, _ABS_supported_si_isa_t si_isa_type);

//_ABS_
void si_isa_write_vreg(struct si_work_item_t *work_item, int vreg, 
	unsigned int value);
unsigned int si_isa_read_reg(struct si_work_item_t *work_item, int reg);
void si_isa_bitmask_sreg(struct si_work_item_t *work_item, int sreg, 
	unsigned int value);
int si_isa_read_bitmask_sreg(struct si_work_item_t *work_item, int sreg);

struct si_buffer_desc_t;
struct si_mem_ptr_t;
void si_isa_read_buf_res(struct si_work_item_t *work_item, 
	struct si_buffer_desc_t *buf_desc, int sreg);
void si_isa_read_mem_ptr(struct si_work_item_t *work_item, 
	struct si_mem_ptr_t *mem_ptr, int sreg);

unsigned int si_isa_const_mem_allocate(unsigned int size);

int si_isa_get_num_elems(int data_format);
int si_isa_get_elem_size(int data_format);

#endif
