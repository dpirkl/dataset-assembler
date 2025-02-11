import os
import shutil
import time

from tqdm import tqdm


def download(source_dir="sources", source_file="sources.txt", verbose=False):
    with open(os.path.join(source_dir, source_file), "r") as f:
        links = f.readlines()

    for link in tqdm(links, desc="Downloads"):
        link = link.strip()

        if link.startswith("wget"):
            file_name = link.split('/')[-1]
            if not os.path.exists(os.path.join(source_dir, file_name)):
                command = f"{link} -P ./sources"
                if not verbose:
                    command += " >/dev/null 2>/dev/null"
                os.system(command)
            else:
                if verbose:
                    print(f"A file with the name {file_name} already exists at {os.path.join('./sources', file_name)}. Continuing with the next link.")

        else:
            folder_name = os.path.join(source_dir, link.split('/')[-1][:-4])
            if not os.path.exists(folder_name):
                command = f"git clone {link} {folder_name}"
                if not verbose:
                    command += " >/dev/null 2>/dev/null"
                os.system(command)
            else:
                if verbose:
                    print(f"A folder with the name {link.split('/')[-1][:-4]} already exists at {folder_name} already exists. Continuing with the next link.")

def extract_c_files(source_dir="sources", dest_dir="extracted", verbose=False):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Walk through the source directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.7z'):
                command = f"7z x {os.path.join(root, file)} -o{source_dir} -aoa"
                if not verbose:
                    command += " >/dev/null 2>/dev/null"
                os.system(command)

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.c'):
                # Construct the full file path
                file_path = os.path.join(root, file)
                file_name = file_path[10:].replace("/", "_").replace(" ", "").replace("(", "_").replace(")", "_").lower()

                # Copy the file to the destination directory
                # shutil.copy2(file_path, destination_dir)
                dest = os.path.join(dest_dir, file_name)
                shutil.copy(file_path, dest)


def replace_tab(code:str, replace_with:str=" "):
    return code.replace("\t", replace_with)


def create_dataset_file(source_dir="assembly", dest_file:str="dataset.txt", eos:str="<|endoftext|>"):
    # create emtpy dataset.txt file. if it exists, delete it
    if os.path.exists(dest_file):
        os.remove(dest_file)

    for filename in tqdm(os.listdir(source_dir), desc="Creating dataset file"):
        if filename.lower().endswith(".s"):
            with open(f"{os.path.join(source_dir, filename)}", "r") as f:
                # lines = f.readlines()
                code = f.read()

            code = replace_tab(code)
            code += eos
            code = repr(code)[1:-1]

            with open(dest_file, "a") as f:
                f.write(code)

        else:
            raise RuntimeWarning(f"File in source folder with wrong extension. Should be .S, but is {filename.split('.')[-1]}")

def compile_all(source_dir="sources", dest_dir="assembly", assembler="gcc", riscv:bool=True, verbose:bool=False):
    if riscv:
        assembler = "riscv64-unknown-elf-" + assembler

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Walk through the source directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.7z'):
                command = f"7z x {os.path.join(root, file)} -o{source_dir} -aoa"
                if not verbose:
                    command += " >/dev/null 2>/dev/null"
                os.system(command)

    for file in tqdm([os.path.join(root, f) for root, _, files in os.walk('sources') for f in files], desc="Compiling"):
        for file in files:
            if file.endswith(".c"):
                c_file = os.path.join(source_dir, file)
                s_filename = file[:-2] + ".S"
                s_file = os.path.join(dest_dir, s_filename)

                command = f"{assembler} -O0 -S {c_file} -o {s_file}"
                if not verbose:
                        command += " >/dev/null 2>/dev/null"
                os.system(command)
            else:
                raise RuntimeError("Wrong file format in extracted directory.")
