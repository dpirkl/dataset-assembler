# Dataset Assembler

This is a code to assemble your own assembly dataset. I used it to finetune a language model on RISC-V assembly.

## Dependencies

- [GCC](https://gcc.gnu.org/) (or another compiler)
- Git
- Python

For RISC-V, you need:
- [RISC-V GNU Compiler Toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain)

## Usage

```bash
python main.py
```

If you want to first move/copy the files:

```bash
python main.py --copy
```

## Pipeline

- Clone repos with C-code.
- Copy and compile C files.
- Create one large text file.

The current default is RISC-V assembly, but it can be changed.

## Main problem

Out of ~50000 .c files, only ~2100 files finish compilation (when using compile_inplace). This is ~40%. Only ~2% when first copying the files.
