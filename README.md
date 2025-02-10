# DATASET ASSEMBLER

This is a code to assemble your own assembly dataset. I used it to finetune a language model on RISC-V assembly. It is only a rudimentary version and has many flaws.

## Pipeline

- Clone C repositiries
- Copy and compline C files
- Create one large text file.

The current default is RISC-V assembly, but it can be changed.

## Fruther Comments

Main problem: Out of ~50000 c files, only ~1200 files finish compilation. This is less than 2%.
