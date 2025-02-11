import os
import shutil

from tqdm import tqdm


def uncompress_files(directory:str="sources", verbose:bool=True):
    """Searches for compressed files/folder in `directory` and uncompresses them.

    Args:
        directory (str, optional): Directory to serach for compressed files. Also searches subdirectories. Defaults to "sources".
        verbose (bool, optional): Controlls verbosity. Defaults to True.
    """

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.7z'):
                os.system(f"7z x {os.path.join(root, file)} -o{directory} -aoa{" >/dev/null 2>/dev/null" if not verbose else ""}")

            # TODO: Add other compressed file types


def download(source_dir:str="sources", sources_file:str="sources/sources.txt", verbose=False):
    """Download files from links in `sources_file`. Assumes git repositories as default.
    For wget links, the line should start with "wget".

    Args:
        source_dir (str, optional): Directory for downloads. Defaults to "sources".
        sources_file (str, optional): File with list of sources. Defaults to "sources.txt".
        verbose (bool, optional): Controlls verbosity. Defaults to False.
    """
    with open(sources_file, "r") as f:
        links:list = f.readlines()

    for link in tqdm(links, desc="Downloads"):
        link:str = link.strip()  # noqa: PLW2901

        if link.startswith("wget"):
            file_name:str = link.split('/')[-1]
            if not os.path.exists(os.path.join(source_dir, file_name)):
                os.system(f"{link} -P {source_dir}{" >/dev/null 2>/dev/null" if not verbose else ""}")
            else:
                if verbose:
                    print(f"A file with the name {file_name} already exists at {os.path.join(source_dir, file_name)}. Continuing with the next link.")

        else:
            folder_name:str = os.path.join(source_dir, link.split('/')[-1][:-4])
            if not os.path.exists(folder_name):
                os.system(f"git clone {link} {folder_name}{" >/dev/null 2>/dev/null" if not verbose else ""}")
            else:
                if verbose:
                    print(f"A folder with the name {link.split('/')[-1][:-4]} already exists at {folder_name} already exists. Continuing with the next link.")

    uncompress_files(source_dir)


def copy_c_files(source_dir:str="sources", dest_dir="copy"):
    """Copy all `C` files from `source_dir` to `dest_dir`.

    Args:
        source_dir (str, optional): Directory to search for `C` files Subdirectories are also searched. Defaults to "sources".
        dest_dir (str, optional): Directory to copy `C` to. Defaults to "copy".
    """

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.c'):
                file_path:str = os.path.join(root, file)
                file_name:str = file_path[10:].replace("/", "_").replace(" ", "")
                dest:str = os.path.join(dest_dir, file_name)
                shutil.copy(file_path, dest)


def replace_tab(code:str, replace_with:str=" "):
    """Replace tabs with spaces in code."""
    return code.replace("\t", replace_with)


def create_dataset_file(source_dir:str="assembly", dest_file:str="dataset.txt", eos:str="<|endoftext|>"):
    """Creates a contiuos dataset file from all assembly files in `source_dir`.

    Args:
        source_dir (str, optional): The directory to serach for assembly files. Defaults to "assembly".
        dest_file (str, optional): The file to copy the code to. Defaults to "dataset.txt".
        eos (str, optional): Sperator between files. Defaults to "<|endoftext|>".
    """

    if os.path.exists(dest_file):
        os.remove(dest_file)

    for filename in tqdm(os.listdir(source_dir), desc="Creating dataset file"):
        if filename.lower().endswith(".s"):
            with open(f"{os.path.join(source_dir, filename)}", "r") as f:
                code:str = f.read()

            code = replace_tab(code)
            code += eos
            code = repr(code)[1:-1]

            with open(dest_file, "a") as f:
                f.write(code)


def compile_all(source_dir:str="sources", dest_dir:str="assembly", compiler:str="gcc", copy:bool=False, copy_dir:str="copy", riscv:bool=True, verbose:bool=False):
    """Compile all C files in `source_dir`.

    Args:
        source_dir (str, optional): Directory to serach for C files. Defaults to "sources".
        dest_dir (str, optional): Directory to save assembly files. Defaults to "assembly".
        compiler (str, optional): Name of compiler. Defaults to "gcc".
        riscv (bool, optional): Controlls use of RISC-V version of compiler. Defaults to True.
        verbose (bool, optional): Controlls verbosity. Defaults to False.
    """
    if riscv:
        compiler:str = "riscv64-unknown-elf-" + compiler

    for file in tqdm([os.path.join(root, f) for root, _, files in os.walk(source_dir) for f in files], desc="Compiling"):
        if file.endswith(".c") or file.endswith(".C"):
            c_file:str = file.replace(" ", "\ ")
            s_filename:str = c_file[len(source_dir)+1:-2].replace("/", "_").replace("\ ", "") + ".S"
            s_file:str = os.path.join(dest_dir, s_filename)

            os.system(f"{compiler} -O0 -S '{c_file}' -o '{s_file}'{" >/dev/null 2>/dev/null" if not verbose else ""}")

            if copy:
                dest:str = os.path.join(copy_dir, s_filename[:-2] + ".c")
                shutil.copy(file, dest)