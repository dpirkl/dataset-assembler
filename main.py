import argparse

from helper import compile_all, copy_c_files, create_dataset_file, download

if __name__ == "__main__":
    # add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--copy", action="store_true", help="Copys C files to specified folder.")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--source_dir", default="sources")
    parser.add_argument("--sources_file", default="sources/sources.txt")
    parser.add_argument("--copy_dir", default="copy")
    parser.add_argument("--assembly_dir", default="assembly")
    args = parser.parse_args()

    source_dir = args.source_dir
    sources_file = args.sources_file
    copy_dir = args.copy_dir
    assembly_dir = args.assembly_dir

    verbose = args.verbose

    download(source_dir=source_dir, sources_file=sources_file, verbose=verbose)
    if args.copy:
        copy_c_files(source_dir=source_dir, dest_dir=copy_dir)
    compile_all(source_dir=source_dir, verbose=verbose)
    create_dataset_file(source_dir=source_dir, verbose=verbose)
