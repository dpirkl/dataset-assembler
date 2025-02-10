import argparse

from helper import compile_all, compile_inplace, create_dataset_file, download, extract_c_files

if __name__ == "__main__":
    # add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--copy", action="store_true")
    args = parser.parse_args()

    download()
    if args.copy:
        assembly_dir = "assembly"
        extract_c_files()
        compile_all()
    else:
        compile_inplace()
        assembly_dir = "assembly-inplace"
    create_dataset_file(source_dir=assembly_dir)
