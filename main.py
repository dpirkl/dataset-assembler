import argparse

from helper import compile_all, create_dataset_file, download, extract_c_files

if __name__ == "__main__":
    # add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--copy", action="store_true", help="Copys C files to specified folder.")
    args = parser.parse_args()

    download()
    if args.copy:
        extract_c_files()
    compile_all()
    create_dataset_file()
