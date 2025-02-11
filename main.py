import argparse

from helper import compile_all, copy_c_files, create_dataset_file, download

if __name__ == "__main__":
    # add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--copy", action="store_true", help="Copys C files to specified folder.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Prints extra information.")
    parser.add_argument("--source_dir", default="sources", help="Directory for downloads.")
    parser.add_argument("--sources_file", default="sources/sources.txt", help="File with list of sources (links).")
    parser.add_argument("--copy_dir", default="copy", help="Directory to copy C files to. Only used if -c/--copy is set.")
    parser.add_argument("--assembly_dir", default="assembly", help="Directory to store assembly files.")
    args = parser.parse_args()

    source_dir:str = args.source_dir
    sources_file:str = args.sources_file
    copy_dir:str = args.copy_dir
    assembly_dir:str = args.assembly_dir

    verbose:bool = True if args.verbose else False
    copy:bool = True if args.copy else False

    download(source_dir=source_dir, sources_file=sources_file, verbose=verbose)
    compile_all(source_dir=source_dir, copy=copy, copy_dir=copy_dir, verbose=verbose)
    create_dataset_file(source_dir=source_dir, verbose=verbose)
